import os
from pathlib import Path

import pytest

from forestrag.cli import build_index
from forestrag.embeddings import SemanticEmbedder
from forestrag.retrieval import retrieve

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.environ.get("FORESTRAG_RUN_INTEGRATION") != "1",
                       reason="Activa FORESTRAG_RUN_INTEGRATION=1 tras descargar modelo y PDF"),
]


def test_real_pdf_and_pinned_multilingual_model(tmp_path):
    embedder = SemanticEmbedder()
    path = tmp_path / "real.db"
    built = build_index("examples/sources.json", "data/raw", path, embedder)
    assert built["dimensions"] == 384 and built["pages"] == 2
    hits = retrieve("¿Cómo ayuda la visión artificial a detectar defectos en madera?", path, embedder)
    assert hits and hits[0].chunk.page == 47
    assert any("defectos" in hit.chunk.text for hit in hits)
    assert len(hits[0].chunk.document_sha256) == 64

