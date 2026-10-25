import io
import hashlib
import json
import sqlite3
from dataclasses import replace

import numpy as np
import pytest

from forestrag.generation import ollama_answer, risky_request
from forestrag.ingestion import read_source
from forestrag.models import Hit
from forestrag.retrieval import retrieve
from forestrag.vector_store import index_metadata, row_digest
from conftest import local_source


@pytest.mark.parametrize("mutation", ["payload", "swap", "scale", "delete"])
def test_f02_tampered_index_fails_closed(index, mutation):
    path, embedder = index
    with sqlite3.connect(path) as con:
        rows = con.execute("SELECT id,payload,vector FROM chunks ORDER BY id").fetchall()
        identifier, payload, vector = rows[0]
        if mutation == "payload":
            obj = json.loads(payload)
            obj.update(text="EVIDENCIA INVENTADA", page=999, url="https://evil.invalid")
            con.execute("UPDATE chunks SET payload=? WHERE id=?", (json.dumps(obj), identifier))
        elif mutation == "swap":
            con.execute("UPDATE chunks SET vector=? WHERE id=?", (rows[1][2], identifier))
        elif mutation == "scale":
            blob = (np.frombuffer(vector, dtype="<f4") * 100).astype("<f4").tobytes()
            # Incluso con checksum actualizado, inventario/norma impiden puntuaciones >1.
            con.execute("UPDATE chunks SET vector=?,checksum=? WHERE id=?", (blob, row_digest(identifier,payload,blob), identifier))
        else:
            con.execute("DELETE FROM chunks WHERE id=?", (identifier,))
    with pytest.raises(ValueError, match="corrupto"):
        retrieve("mantenimiento", path, embedder)


def test_f06_missing_metadata_is_domain_error(index, monkeypatch):
    path, _ = index
    with sqlite3.connect(path) as con:
        con.execute("DELETE FROM metadata WHERE key='dimension'")
    monkeypatch.setenv("FORESTRAG_INDEX_SHA256", hashlib.sha256(path.read_bytes()).hexdigest())
    with pytest.raises(ValueError, match="Metadatos"):
        index_metadata(path)


def test_old_schema_requires_explicit_rebuild(index, monkeypatch):
    path, _ = index
    with sqlite3.connect(path) as con:
        con.execute("UPDATE metadata SET value='1' WHERE key='schema_version'")
    monkeypatch.setenv("FORESTRAG_INDEX_SHA256", hashlib.sha256(path.read_bytes()).hexdigest())
    with pytest.raises(ValueError, match="Reindexe"):
        index_metadata(path)


def test_f04_empty_page_selection_is_not_whole_document(tmp_path, source):
    path = tmp_path / "test.txt"
    path.write_text("texto autorizado")
    with pytest.raises(ValueError, match="Selección"):
        read_source(replace(local_source(source, path), pages=[]), tmp_path)


def test_f06_malformed_pdf_translated(tmp_path, source):
    path = tmp_path / "bad.pdf"
    path.write_bytes(b"%PDF-1.4\narchivo incompleto")
    with pytest.raises(ValueError, match="PDF inválido"):
        read_source(local_source(source, path), tmp_path)


def test_f07_newline_does_not_bypass_conservative_filter():
    assert risky_request("desactivar\nprotecciones de seguridad")


def test_f09_cloud_tag_rejected_without_connection(sample, monkeypatch):
    monkeypatch.setenv("FORESTRAG_OLLAMA_MODEL", "qwen:cloud")
    monkeypatch.setattr("urllib.request.build_opener", lambda *a: pytest.fail("No debe conectar"))
    with pytest.raises(ValueError, match="modelo local"):
        ollama_answer("registro", [Hit(sample[0], .8)])


def test_f06_ollama_envelope_array_is_controlled_error(sample, monkeypatch):
    class Opener:
        def open(self, *_args, **_kwargs):
            return io.BytesIO(b"[]")
    monkeypatch.setattr("urllib.request.build_opener", lambda *a: Opener())
    with pytest.raises(RuntimeError, match="formato inválido"):
        ollama_answer("registro", [Hit(sample[0], .8)])
