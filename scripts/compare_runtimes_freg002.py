"""Comparación reproducible en entorno HISTÓRICO aislado con FastEmbed0.9.0.

No instalar FastEmbed en el entorno final FREG-002. Sólo corpus público/ficticio.
"""
import json
from pathlib import Path

import numpy as np

from forestrag.embeddings import MODEL_NAME, MODEL_REPO, MODEL_REVISION, SemanticEmbedder, normalize_vectors
from forestrag.ingestion import load_sources, read_source
from forestrag.preprocessing import chunk_pages

try:
    from fastembed import TextEmbedding
except ImportError as exc:
    raise SystemExit("Ejecutar sólo en el entorno histórico aislado con FastEmbed0.9.0.") from exc

current = SemanticEmbedder()
pages = [p for source in load_sources(Path("examples/sources.json"))
         for p in read_source(source, Path("data/raw"))]
chunks = chunk_pages(pages, token_count=current.token_count)
questions = json.loads(Path("examples/evaluation_fao.json").read_text())
texts = [c.text for c in chunks] + [r["question"] for r in questions] + [
    "Inventario forestal ficticio.", "Árboles, conservación y teledetección.", ""]
path = Path("data/models") / ("models--" + MODEL_REPO.replace("/", "--")) / "snapshots" / MODEL_REVISION
previous = TextEmbedding(model_name=MODEL_NAME, specific_model_path=str(path),
                         local_files_only=True, threads=2, providers=["CPUExecutionProvider"])
old = normalize_vectors(list(previous.embed(texts, batch_size=32)))
new = current.encode(texts)
report = {"cases": len(texts), "dimensions": new.shape[1], "atol": 1e-6, "rtol": 1e-6,
          "max_abs_error": float(np.max(np.abs(old - new))),
          "allclose": bool(np.allclose(old, new, atol=1e-6, rtol=1e-6)),
          "same_token_counts": all(sum(previous.model.tokenizer.encode(t).attention_mask)
                                   == current.token_count(t) for t in texts)}
print(json.dumps(report))
assert report["allclose"] and report["same_token_counts"]
