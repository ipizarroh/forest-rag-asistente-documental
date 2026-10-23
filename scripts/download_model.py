"""Descarga explícita de pesos públicos; no ejecuta código remoto del modelo."""
from pathlib import Path
from huggingface_hub import snapshot_download
from forestrag.embeddings import MODEL_FILES, MODEL_REPO, MODEL_REVISION, SemanticEmbedder

snapshot_download(repo_id=MODEL_REPO, revision=MODEL_REVISION,
                  allow_patterns=list(MODEL_FILES), cache_dir="data/models")
SemanticEmbedder(Path("data/models"))
print("Modelo descargado y hashes verificados; inferencia local preparada.")

