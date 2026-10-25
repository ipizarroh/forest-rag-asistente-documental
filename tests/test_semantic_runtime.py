import json
import os
from pathlib import Path

import numpy as np
import pytest

from forestrag.embeddings import SemanticEmbedder

pytestmark = [pytest.mark.integration,
              pytest.mark.skipif(os.environ.get("FORESTRAG_RUN_INTEGRATION") != "1",
                                 reason="Requiere pesos fijados y dependencias semánticas locales")]


@pytest.fixture(scope="module")
def encoder():
    return SemanticEmbedder()


def test_direct_runtime_matches_frozen_fastembed_reference(encoder):
    reference = json.loads((Path(__file__).parent / "fixtures/semantic_reference_freg001.json").read_text())
    values = encoder.encode(reference["texts"])
    assert values.shape == (3, 384)
    assert np.allclose(values, reference["vectors"], atol=1e-6, rtol=1e-6)
    assert np.allclose(np.linalg.norm(values, axis=1), 1, atol=1e-6)


def test_direct_runtime_empty_batch_and_input_budget(encoder):
    assert encoder.encode([]).shape == (0, 384)
    with pytest.raises(ValueError, match="128 tokens"):
        encoder.encode(["inventario " * 200])
    with pytest.raises(ValueError, match="lista de textos"):
        encoder.encode([None])


def test_direct_runtime_token_count_not_affected_by_batch_padding(encoder):
    before = encoder.token_count("inventario")
    values = encoder.encode(["inventario", "inventario forestal " * 10])
    assert values.shape == (2, 384) and np.isfinite(values).all()
    assert encoder.token_count("inventario") == before
