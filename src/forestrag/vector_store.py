"""SQLite público: huella externa confiable y snapshot verificado antes de leer SQL."""
import hashlib
import json
import os
import re
import sqlite3
import tempfile
from contextlib import closing, contextmanager
from pathlib import Path

import numpy as np

from .embeddings import normalize_vectors
from .models import Chunk, Hit
from .preprocessing import chunk_identity


def row_digest(identifier: str, payload: str, blob: bytes) -> str:
    return hashlib.sha256(identifier.encode() + b"\0" + payload.encode() + b"\0" + blob).hexdigest()


def checked_chunk(identifier: str, payload: str, blob: bytes, checksum: str, dimension: int):
    """Valida asociación, procedencia estructural y norma antes de puntuar."""
    try:
        if row_digest(identifier, payload, blob) != checksum:
            raise ValueError("checksum")
        chunk = Chunk(**json.loads(payload))
        if (chunk.id != identifier or type(chunk.page) is not int or chunk.page < 1
                or type(chunk.start_word) is not int or chunk.start_word < 0
                or not isinstance(chunk.text, str) or not chunk.text.strip()
                or not re.fullmatch(r"[a-f0-9]{64}", chunk.document_sha256)
                or chunk.id != chunk_identity(chunk.source_id, chunk.document_sha256,
                                               chunk.page, chunk.start_word, chunk.text)):
            raise ValueError("procedencia")
        stored = np.frombuffer(blob, dtype="<f4")
        norm = float(np.linalg.norm(stored))
        if (len(stored) != dimension or not np.isfinite(stored).all()
                or not (norm == 0 or abs(norm - 1) < 1e-5)):
            raise ValueError("vector")
        return chunk, stored
    except (TypeError, KeyError, ValueError) as exc:
        raise ValueError("Índice corrupto o procedencia inconsistente. Reindexe.") from exc


def write_index(path: Path, chunks: list[Chunk], vectors, embedder_id: str) -> str:
    vectors = normalize_vectors(vectors)
    if not chunks or len(chunks) != len(vectors) or len(chunks) > 10_000:
        raise ValueError("Cantidad de fragmentos inválida.")
    if len({c.id for c in chunks}) != len(chunks):
        raise ValueError("Hay fragmentos duplicados.")
    rows = []
    for c, v in zip(chunks, vectors):
        payload, blob = json.dumps(c.to_dict(), ensure_ascii=False), v.astype("<f4").tobytes()
        checksum = row_digest(c.id, payload, blob)
        checked_chunk(c.id, payload, blob, checksum, vectors.shape[1])
        rows.append((c.id, payload, blob, checksum))
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".db")
    os.close(fd)
    try:
        with closing(sqlite3.connect(temporary)) as con:
            con.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            con.execute("CREATE TABLE chunks (id TEXT PRIMARY KEY, payload TEXT NOT NULL, vector BLOB NOT NULL, checksum TEXT NOT NULL)")
            con.executemany("INSERT INTO metadata VALUES (?, ?)", [
                ("schema_version", "2"), ("embedder", embedder_id),
                ("dimension", str(vectors.shape[1])), ("count", str(len(rows))),
                ("manifest", hashlib.sha256("".join(r[3] for r in sorted(rows)).encode()).hexdigest()),
            ])
            con.executemany("INSERT INTO chunks VALUES (?, ?, ?, ?)", rows)
            con.commit()
        fingerprint = hashlib.sha256(Path(temporary).read_bytes()).hexdigest()
        os.replace(temporary, path)
        return fingerprint
    finally:
        Path(temporary).unlink(missing_ok=True)


@contextmanager
def verified_index(path: Path, trusted_sha256: str | None = None):
    # El operador configura esta referencia fuera del ámbito escribible del índice.
    expected = trusted_sha256 if trusted_sha256 is not None else os.environ.get("FORESTRAG_INDEX_SHA256")
    if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
        raise ValueError("Falta huella confiable FORESTRAG_INDEX_SHA256 del operador.")
    if not path.is_file() or path.stat().st_size > 200_000_000:
        raise ValueError("Índice inexistente o demasiado grande.")
    with path.open("rb") as stream:
        snapshot = stream.read(200_000_001)
    if len(snapshot) > 200_000_000 or hashlib.sha256(snapshot).hexdigest() != expected:
        raise ValueError("Índice corrupto o sustituido: no coincide con la huella confiable.")
    # Parsear exactamente los bytes verificados evita reabrir una ruta sustituible (TOCTOU).
    with closing(sqlite3.connect(":memory:")) as con:
        con.deserialize(snapshot)
        con.execute("PRAGMA query_only=ON")
        con.execute("PRAGMA trusted_schema=OFF")
        yield con


def _metadata(con) -> dict:
    try:
        metadata = dict(con.execute("SELECT key, value FROM metadata"))
        if metadata.get("schema_version") != "2":
            raise ValueError("Versión de índice incompatible. Reindexe desde las fuentes autorizadas.")
        if (not metadata.get("embedder") or not 1 <= int(metadata["dimension"]) <= 65536
                or not 1 <= int(metadata["count"]) <= 10000
                or not re.fullmatch(r"[a-f0-9]{64}", metadata["manifest"])):
            raise ValueError("Metadatos de índice inválidos.")
        return metadata
    except (sqlite3.Error, KeyError, TypeError) as exc:
        raise ValueError("Metadatos de índice inválidos. Reindexe.") from exc


def index_metadata(path: Path, *, trusted_sha256: str | None = None) -> dict:
    try:
        with verified_index(path, trusted_sha256) as con:
            return _metadata(con)
    except sqlite3.Error as exc:
        raise ValueError("Índice corrupto o metadatos inválidos. Reindexe.") from exc


def search_index(path: Path, vector, embedder_id: str, k: int = 3,
                 threshold: float = 0.5, source_id: str | None = None,
                 *, trusted_sha256: str | None = None) -> list[Hit]:
    if not 1 <= k <= 20 or not 0 <= threshold <= 1:
        raise ValueError("Parámetros de recuperación inválidos.")
    try:
        with verified_index(path, trusted_sha256) as con:
            metadata = _metadata(con)
            rows = con.execute("SELECT id, payload, vector, checksum FROM chunks ORDER BY id LIMIT 10001").fetchall()
    except sqlite3.Error as exc:
        raise ValueError("Índice corrupto. Reindexe.") from exc
    if metadata["embedder"] != embedder_id:
        raise ValueError("El índice y la consulta usan modelos diferentes. Reindexe.")
    query = normalize_vectors([vector])[0]
    if len(query) != int(metadata["dimension"]):
        raise ValueError("Dimensión incompatible.")
    if (len(rows) != int(metadata["count"]) or
            hashlib.sha256("".join(r[3] for r in rows).encode()).hexdigest() != metadata["manifest"]):
        raise ValueError("Índice corrupto: inventario inconsistente.")
    hits = []
    for identifier, payload, blob, checksum in rows:
        chunk, stored = checked_chunk(identifier, payload, blob, checksum, len(query))
        if source_id is not None and chunk.source_id != source_id:
            continue
        score = float(np.clip(np.dot(query, stored), -1, 1))
        if score >= threshold:
            hits.append(Hit(chunk, score))
    return sorted(hits, key=lambda h: (-h.score, h.chunk.id))[:k]
