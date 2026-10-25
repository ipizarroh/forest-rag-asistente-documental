from dataclasses import replace

import numpy as np
import pytest

from forestrag.models import Page
from forestrag.preprocessing import chunk_pages, normalize
from forestrag.retrieval import retrieve
from forestrag.vector_store import search_index, write_index, index_metadata


def test_normalization():
    assert normalize("conser-\nvación \n  forestal\x00") == "conservación forestal"


def test_chunks_stay_on_page_and_stable(source):
    pages = [Page(source, n, str(n), " ".join(f"palabra{i}" for i in range(20))) for n in [1, 2]]
    chunks = chunk_pages(pages, max_words=8, overlap=2)
    assert {c.page for c in chunks} == {1, 2}
    assert len({c.id for c in chunks}) == len(chunks)
    assert chunks == chunk_pages(pages, max_words=8, overlap=2)
    assert chunks[0].id != chunk_pages([replace(pages[0], source=replace(source, sha256="1"*64))], 8, 2)[0].id


def test_token_budget_and_coverage(source):
    text = " ".join(f"p{i}" for i in range(50))
    chunks = chunk_pages([Page(source, 1, "1", text)], max_words=20, overlap=3,
                        token_count=lambda s: len(s.split()) * 3, max_tokens=21)
    assert all(len(c.text.split()) <= 7 for c in chunks)
    assert set(" ".join(c.text for c in chunks).split()) == set(text.split())
    with pytest.raises(ValueError):
        chunk_pages([Page(source, 1, "1", "imposible")], token_count=lambda s: 999)


@pytest.mark.parametrize("max_words,overlap", [(0, 0), (4, 4), (4, -1)])
def test_invalid_chunk_parameters(max_words, overlap):
    with pytest.raises(ValueError):
        chunk_pages([], max_words, overlap)


def test_retrieval_roundtrip_and_page(index):
    path, embedder = index
    hits = retrieve("orden mantenimiento equipo", path, embedder, threshold=0.3)
    assert hits[0].chunk.page == 1
    assert hits[0].chunk.document_sha256 == "0" * 64
    assert index_metadata(path)["embedder"] == embedder.id
    assert not retrieve("astronomía galaxia júpiter", path, embedder, threshold=0.8)
    assert not retrieve("mantenimiento", path, embedder, source_id="otra-fuente")


def test_embedding_mismatch_and_dimensions(index):
    path, embedder = index
    vector = embedder.encode(["equipo"])[0]
    with pytest.raises(ValueError, match="modelos diferentes"):
        search_index(path, vector, "modelo-distinto")
    with pytest.raises(ValueError, match="Dimensión"):
        search_index(path, vector[:3], embedder.id)


def test_atomic_index_preserved_on_invalid_write(index, sample):
    path, embedder = index
    before = path.read_bytes()
    with pytest.raises(ValueError):
        write_index(path, sample, [[float("nan")]], embedder.id)
    assert path.read_bytes() == before


@pytest.mark.parametrize("question", ["", "   ", "a" * 1001, None])
def test_bad_queries(index, question):
    path, embedder = index
    with pytest.raises(ValueError):
        retrieve(question, path, embedder)


def test_retrieval_limits(index):
    path, embedder = index
    with pytest.raises(ValueError):
        retrieve("equipo", path, embedder, k=0)

