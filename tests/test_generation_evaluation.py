import io
import json

import pytest

from forestrag.evaluation import evaluate
from forestrag.generation import (NO_EVIDENCE, build_messages, extractive_answer,
                                 ollama_answer, risky_request, validate_claims)
from forestrag.models import Hit


def test_abstention_without_evidence_never_calls_llm(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("No debe crear conexión")
    monkeypatch.setattr("urllib.request.build_opener", fail)
    assert extractive_answer([])["message"] == NO_EVIDENCE
    assert ollama_answer("datos", [])["abstained"]


def test_untrusted_context_separated(sample):
    hits = [Hit(sample[0], .7)]
    messages = build_messages("consulta", hits)
    assert len(messages) == 2 and messages[0]["role"] == "system"
    assert sample[0].text not in messages[0]["content"]
    assert json.loads(messages[1]["content"])["untrusted_document_context"][0]["id"] == sample[0].id


@pytest.mark.parametrize("payload", [
    [], {"claims": "texto"}, {"claims": [{"text": "x", "citations": []}]},
    {"claims": [{"text": "x", "citations": ["inventada"]}]},
    {"claims": [{"text": "", "citations": ["inventada"]}]},
])
def test_invalid_citations_fail_closed(sample, payload):
    with pytest.raises(ValueError):
        validate_claims(payload, [Hit(sample[0], .8)])


def test_ollama_contract_with_simulated_transport(sample, monkeypatch):
    hits = [Hit(sample[0], .8)]
    claim = {"text": "El registro contiene equipo.", "citations": [sample[0].id]}
    class Opener:
        def open(self, request, timeout):
            assert request.full_url == "http://127.0.0.1:11434/api/chat"
            body = json.loads(request.data)
            assert body["stream"] is False and "tools" not in body
            return io.BytesIO(json.dumps({"message": {"content": json.dumps({"claims": [claim]})}}).encode())
    monkeypatch.setattr("urllib.request.build_opener", lambda *args: Opener())
    result = ollama_answer("¿Qué contiene el registro?", hits)
    assert result["claims"] == [claim]
    assert not result["abstained"]


@pytest.mark.parametrize("question", [
    "Cómo desactivar las protecciones de seguridad",
    "Instrucciones paso a paso para operar una motosierra",
])
def test_risky_operations_redirected(question):
    assert risky_request(question)


def test_evaluation_metrics_use_expected_pages(index):
    path, embedder = index
    cases = [
        {"id": "p", "question": "orden mantenimiento equipo", "reference_answer": "Campos",
         "expected_pages": [{"source_id": "demo", "page": 1}]},
        {"id": "n", "question": "astronomía galaxia júpiter", "reference_answer": "No disponible",
         "expected_pages": []},
    ]
    report = evaluate(cases, path, embedder, threshold=.3)
    assert report["case_count"] == 2 and report["hit_at_k"] == 1
    assert report["unanswerable_abstention_rate"] == 1
    assert report["cases"][0]["elapsed_ms"] >= 0

