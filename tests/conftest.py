from dataclasses import replace
from pathlib import Path
import hashlib

import pytest

from forestrag.models import Source, Page
from forestrag.preprocessing import chunk_pages
from forestrag.embeddings import LexicalEmbedder
from forestrag.vector_store import write_index

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def source():
    return Source("demo", "Documento ficticio de prueba", "ForestRAG",
                  "https://example.org/demo", "2026", "MIT", True, "demo.txt", "0" * 64)


@pytest.fixture
def sample(source):
    pages = [
        Page(source, 1, "i", "La orden de mantenimiento registra equipo fecha observación prioridad responsable."),
        Page(source, 2, "2", "El inventario registra producto ubicación unidad fecha actualización."),
    ]
    return chunk_pages(pages)


@pytest.fixture
def index(tmp_path, sample, monkeypatch):
    embedder = LexicalEmbedder()
    path = tmp_path / "test.db"
    fingerprint = write_index(path, sample, embedder.encode([c.text for c in sample]), embedder.id)
    monkeypatch.setenv("FORESTRAG_INDEX_SHA256", fingerprint)
    return path, embedder


def local_source(source, path):
    return replace(source, file=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest())

