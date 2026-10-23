"""Regresión del banco congelado anterior. No es un nuevo conjunto reservado."""
import hashlib
import json
import statistics
import zipfile
from pathlib import Path
from time import perf_counter

from forestrag.embeddings import SemanticEmbedder
from forestrag.ingestion import load_sources, read_source
from forestrag.preprocessing import chunk_pages, normalize
from forestrag.retrieval import retrieve
from forestrag.vector_store import write_index

archive = Path("docs/history/EVIDENCIAS_AUDITORIA_FORESTRAG.zip")
with zipfile.ZipFile(archive) as package:
    manifest = json.loads(package.read("MANIFEST_SHA256.json"))
    raw = package.read("evidence/cases_frozen.json")
    assert hashlib.sha256(raw).hexdigest() == manifest["evidence/cases_frozen.json"]
    # El archivo original conserva su propio manifiesto; no se modifica ni recalifica.
    cases = json.loads(raw)
pages = [p for s in load_sources(Path("examples/sources.json")) for p in read_source(s, Path("data/raw"))]
by_page = {(p.source.id, p.number): normalize(p.text) for p in pages}
embedder = SemanticEmbedder()
chunks = chunk_pages(pages, token_count=embedder.token_count)
index = Path("data/regression-freg001.db")
write_index(index, chunks, embedder.encode([c.text for c in chunks]), embedder.id)
rows, reconciliation = [], []
for case in cases:
    if case["page"]:
        text = by_page[(case["source_id"], case["page"])]
        # pypdf actualizado puede cambiar espacios. Alinear ANTES de consultar, sin
        # modificar el banco congelado ni aceptar diferencias de letras/puntuación.
        positions = [i for i, ch in enumerate(text) if not ch.isspace()]
        compact = "".join(text[i] for i in positions)
        needle = "".join(case["gold_text"].split())
        start = compact.find(needle)
        assert start >= 0 and compact.count(needle) == 1, case["id"]
        first, last = positions[start], positions[start + len(needle) - 1] + 1
        before = [case["gold_word_start"], case["gold_word_end"]]
        case["gold_word_start"], case["gold_word_end"] = len(text[:first].split()), len(text[:last].split())
        after = [case["gold_word_start"], case["gold_word_end"]]
        if before != after or case["gold_text"] != text[first:last]:
            reconciliation.append({"id": case["id"], "old_words": before, "new_words": after,
                                   "reason": "Sólo espacios de extracción; texto sin espacios idéntico."})
    started = perf_counter()
    hits = retrieve(case["question"], index, embedder, k=3, threshold=.5)
    latency = (perf_counter() - started) * 1000
    covered, relevant = set(), False
    for hit in hits:
        assert hit.chunk.text in by_page[(hit.chunk.source_id, hit.chunk.page)]
        if case["page"] and hit.chunk.source_id == case["source_id"] and hit.chunk.page == case["page"]:
            interval = set(range(hit.chunk.start_word, hit.chunk.start_word + len(hit.chunk.text.split())))
            gold = set(range(case["gold_word_start"], case["gold_word_end"]))
            covered.update(interval & gold)
            relevant |= len(interval & gold) / len(gold) >= .35
    coverage = len(covered) / (case["gold_word_end"] - case["gold_word_start"]) if case["page"] else None
    passed = coverage >= .9 if case["page"] else not hits
    rows.append({"id": case["id"], "requirement": "F01 recuperación/completitud/abstención",
                 "split_historico": case["split"], "answerable": bool(case["page"]),
                 "expected": case["expected"], "observed": {"relevant": relevant, "coverage": coverage,
                 "abstained": not hits, "latency_ms": round(latency, 3)},
                 "status": "PASS" if passed else "FAIL",
                 "hit_ids": [h.chunk.id for h in hits]})
def summarize(items):
    positives = [r for r in items if r["answerable"]]
    negatives = [r for r in items if not r["answerable"]]
    return {"cases": len(items), "pass": sum(r["status"] == "PASS" for r in items),
            "fail": sum(r["status"] == "FAIL" for r in items),
            "relevant": [sum(r["observed"]["relevant"] for r in positives), len(positives)],
            "complete": [sum(r["observed"]["coverage"] >= .9 for r in positives), len(positives)],
            "abstention": [sum(r["observed"]["abstained"] for r in negatives), len(negatives)],
            "latency_median_ms": statistics.median(r["observed"]["latency_ms"] for r in items)}
output = {"version": "FREG-CRITICAL-001", "base_commit": "eee8da5035340abef011357e5f85ad7b2fc34bc3",
          "method": "Regresión de 30 preguntas conocidas; reglas y parámetros históricos, no nueva validación ciega.",
          "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
          "cases_sha256": hashlib.sha256(raw).hexdigest(), "chunk_count": len(chunks),
          "reference_reconciliation": reconciliation,
          "summary": {"all": summarize(rows), "historical_final": summarize([r for r in rows if r["split_historico"] == "final"])},
          "rows": rows}
destination = Path("reports/freg001/retrieval-regression.json")
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(json.dumps(output, ensure_ascii=False, indent=2))
print(json.dumps(output["summary"], ensure_ascii=False))
