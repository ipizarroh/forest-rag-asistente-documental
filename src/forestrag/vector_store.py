"""Índice SQLite local; búsqueda exacta por coseno para corpus pequeños."""
import json
import os
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

import numpy as np

from .embeddings import normalize_vectors
from .models import Chunk, Hit


def write_index(path: Path, chunks: list[Chunk], vectors, embedder_id: str) -> None:
    vectors = normalize_vectors(vectors)
    if not chunks or len(chunks) != len(vectors) or len(chunks) > 10_000:
        raise ValueError("Cantidad de fragmentos inválida.")
    if len({c.id for c in chunks}) != len(chunks):
        raise ValueError("Hay fragmentos duplicados.")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".db")
    os.close(fd)
    try:
        with closing(sqlite3.connect(temporary)) as con:
            con.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            con.execute("CREATE TABLE chunks (id TEXT PRIMARY KEY, payload TEXT NOT NULL, vector BLOB NOT NULL)")
            con.executemany("INSERT INTO metadata VALUES (?, ?)", [
                ("schema_version", "1"), ("embedder", embedder_id),
                ("dimension", str(vectors.shape[1])),
            ])
            con.executemany("INSERT INTO chunks VALUES (?, ?, ?)", [
                (c.id, json.dumps(c.to_dict(), ensure_ascii=False), v.astype("<f4").tobytes())
                for c, v in zip(chunks, vectors)
            ])
            con.commit()
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def index_metadata(path: Path) -> dict:
    if not path.is_file() or path.stat().st_size > 200_000_000:
        raise ValueError("Índice inexistente o demasiado grande.")
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as con:
        metadata = dict(con.execute("SELECT key, value FROM metadata"))
    if metadata.get("schema_version") != "1":
        raise ValueError("Versión de índice incompatible.")
    return metadata


def search_index(path: Path, vector, embedder_id: str, k: int = 3,
                 threshold: float = 0.5, source_id: str | None = None) -> list[Hit]:
    if not 1 <= k <= 20 or not 0 <= threshold <= 1:
        raise ValueError("Parámetros de recuperación inválidos.")
    metadata = index_metadata(path)
    if metadata["embedder"] != embedder_id:
        raise ValueError("El índice y la consulta usan modelos diferentes. Reindexe.")
    query = normalize_vectors([vector])[0]
    if len(query) != int(metadata["dimension"]):
        raise ValueError("Dimensión incompatible.")
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as con:
        rows = con.execute("SELECT payload, vector FROM chunks ORDER BY id").fetchall()
    hits = []
    for payload, blob in rows:
        chunk = Chunk(**json.loads(payload))
        if source_id is not None and chunk.source_id != source_id:
            continue
        stored = np.frombuffer(blob, dtype="<f4")
        if len(stored) != len(query) or not np.isfinite(stored).all():
            raise ValueError("Índice corrupto.")
        score = float(np.dot(query, stored))
        if score >= threshold:
            hits.append(Hit(chunk, score))
    return sorted(hits, key=lambda h: (-h.score, h.chunk.id))[:k]

