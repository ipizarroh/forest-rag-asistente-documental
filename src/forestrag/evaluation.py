"""Evaluación pequeña y reproducible de páginas recuperadas y abstención."""
from datetime import datetime, timezone
from time import perf_counter

from .retrieval import retrieve
from .embeddings import terms


def evaluate(cases: list[dict], path, embedder, k=3, threshold=0.5) -> dict:
    if not cases:
        raise ValueError("No hay casos de evaluación.")
    rows = []
    for case in cases:
        started = perf_counter()
        hits = retrieve(case["question"], path, embedder, k, threshold)
        expected = {(p["source_id"], p["page"]) for p in case.get("expected_pages", [])}
        retrieved = {(h.chunk.source_id, h.chunk.page) for h in hits}
        found = expected & retrieved
        anchors = case.get("reference_terms", [])
        evidence = " " + " ".join(terms(" ".join(h.chunk.text for h in hits))) + " "
        covered = [a for a in anchors if " " + " ".join(terms(a)) + " " in evidence]
        rows.append({
            "id": case["id"], "question": case["question"],
            "reference_answer": case["reference_answer"],
            "answerable": bool(expected), "expected_pages": sorted(expected),
            "retrieved_pages": sorted(retrieved),
            "hit_at_k": bool(found) if expected else None,
            "page_recall_at_k": len(found) / len(expected) if expected else None,
            "abstained": not hits,
            "reference_terms": anchors,
            "reference_terms_found": covered,
            "reference_term_coverage": len(covered) / len(anchors) if anchors else None,
            "all_reference_terms_found": len(covered) == len(anchors) if anchors else None,
            "elapsed_ms": round((perf_counter() - started) * 1000, 2),
            "hits": [{"id": h.chunk.id, "page": h.chunk.page,
                      "source_id": h.chunk.source_id, "score": round(h.score, 6),
                      "text": h.chunk.text} for h in hits],
        })
    positive = [r for r in rows if r["answerable"]]
    negative = [r for r in rows if not r["answerable"]]
    anchored = [r for r in positive if r["reference_terms"]]
    return {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "embedder": embedder.id, "k": k, "threshold": threshold,
        "case_count": len(rows),
        "hit_at_k": sum(r["hit_at_k"] for r in positive) / len(positive) if positive else None,
        "mean_page_recall_at_k": sum(r["page_recall_at_k"] for r in positive) / len(positive) if positive else None,
        "unanswerable_abstention_rate": sum(r["abstained"] for r in negative) / len(negative) if negative else None,
        "full_reference_term_coverage_rate": sum(r["all_reference_terms_found"] for r in anchored) / len(anchored) if anchored else None,
        "note": "Muestra de desarrollo, sin validación industrial ni evaluación de un LLM.",
        "cases": rows,
    }

