"""Amenaza: escritor del índice/sidecar sin control de la referencia del operador."""
import hashlib
from dataclasses import replace

import pytest

from forestrag.preprocessing import chunk_identity
from forestrag.retrieval import retrieve
from forestrag.vector_store import index_metadata, write_index


def replacement(sample):
    chunk = replace(sample[0], text="Inventario FICTICIO de reemplazo: canario NUEVO-INDICE.")
    return [replace(chunk, id=chunk_identity(chunk.source_id, chunk.document_sha256,
                                            chunk.page, chunk.start_word, chunk.text))]


def test_missing_anchor_denies_before_sqlite(index, monkeypatch):
    path, _ = index
    monkeypatch.delenv("FORESTRAG_INDEX_SHA256")
    monkeypatch.setattr("forestrag.vector_store.sqlite3.connect", lambda *a: pytest.fail("No debe parsear"))
    with pytest.raises(ValueError, match="huella confiable"):
        index_metadata(path)


def test_modified_bytes_denied_before_sqlite(index, monkeypatch):
    path, _ = index
    path.write_bytes(b"No es un SQLite autorizado")
    monkeypatch.setattr("forestrag.vector_store.sqlite3.connect", lambda *a: pytest.fail("No debe parsear"))
    with pytest.raises(ValueError, match="huella confiable"):
        index_metadata(path)


def test_replaced_index_and_coedited_sidecar_cannot_change_trust(index, sample):
    path, embedder = index
    old_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    chunks = replacement(sample)
    new_sha = write_index(path, chunks, embedder.encode([c.text for c in chunks]), embedder.id)
    path.with_suffix(".sha256").write_text(new_sha)
    assert old_sha != new_sha
    # El reemplazo es estructuralmente válido si el operador lo autorizara explícitamente.
    assert index_metadata(path, trusted_sha256=new_sha)["count"] == "1"
    with pytest.raises(ValueError, match="sustituido"):
        retrieve("inventario", path, embedder)


def test_verified_snapshot_survives_path_swap_without_using_new_bytes(index, monkeypatch):
    import forestrag.vector_store as module
    path, embedder = index
    original_connect = module.sqlite3.connect
    def switch_path(*args, **kwargs):
        path.write_bytes(b"SUSTITUIDO DESPUES DE VERIFICAR")
        return original_connect(*args, **kwargs)
    monkeypatch.setattr(module.sqlite3, "connect", switch_path)
    hits = retrieve("orden mantenimiento equipo", path, embedder, threshold=.3)
    assert hits and "mantenimiento" in hits[0].chunk.text
    assert "SUSTITUIDO" not in hits[0].chunk.text
    with pytest.raises(ValueError, match="sustituido"):
        retrieve("orden mantenimiento", path, embedder)


def test_authorized_new_version_rejects_rollback_and_retirement(index, sample, monkeypatch):
    path, embedder = index
    old_bytes = path.read_bytes()
    chunks = replacement(sample)
    new_sha = write_index(path, chunks, embedder.encode([c.text for c in chunks]), embedder.id)
    monkeypatch.setenv("FORESTRAG_INDEX_SHA256", new_sha)
    assert "NUEVO-INDICE" in retrieve("inventario", path, embedder, threshold=.1)[0].chunk.text
    path.write_bytes(old_bytes)
    with pytest.raises(ValueError, match="sustituido"):
        retrieve("mantenimiento", path, embedder)
    path.unlink()
    with pytest.raises(ValueError, match="inexistente"):
        index_metadata(path)


def test_trusted_but_invalid_sqlite_is_controlled(tmp_path):
    path = tmp_path / "invalid.db"
    path.write_bytes(b"no SQLite")
    with pytest.raises(ValueError, match="inválidos"):
        index_metadata(path, trusted_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
