"""Embeddings densos locales y baseline léxico explícitamente identificado."""
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import numpy as np

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_REPO = "Qdrant/paraphrase-multilingual-MiniLM-L12-v2-onnx-Q"
MODEL_REVISION = "faf4aa4225822f3bc6376869cb1164e8e3feedd0"
MODEL_FILES = {
    "config.json": "c8ec081fdad2df991bf5abbf18418fec7a5cdaa421f60ffb060a30040b8c376f",
    "model_optimized.onnx": "634d0f66c29dc934c8fa72b8a4fe91dd4d420a22f1d82a241058d4316e659a99",
    "special_tokens_map.json": "8c785abebea9ae3257b61681b4e6fd8365ceafde980c21970d001e834cf10835",
    "tokenizer.json": "fa685fc160bbdbab64058d4fc91b60e62d207e8dc60b9af5c002c5ab946ded00",
    "tokenizer_config.json": "0666eebf692422757e1dddf3c9fb1ded73ba3dc726c5828671fc89e45bf3609f",
}


def normalize_vectors(values):
    array = np.asarray(values, dtype=np.float32)
    if array.ndim != 2 or not np.isfinite(array).all():
        raise ValueError("Vectores inválidos.")
    norms = np.linalg.norm(array, axis=1, keepdims=True)
    return array / np.maximum(norms, 1e-12)


def terms(text: str) -> list[str]:
    text = "".join(c for c in unicodedata.normalize("NFD", text.lower())
                   if unicodedata.category(c) != "Mn")
    return re.findall(r"\b[a-z0-9]{3,}\b", text)


class LexicalEmbedder:
    """Hashing de palabras. Baseline sin descarga; NO es un modelo semántico."""
    id = "lexical-sha256-512-v1"
    token_count = None

    def encode(self, texts: list[str]):
        values = np.zeros((len(texts), 512), dtype=np.float32)
        for i, text in enumerate(texts):
            for term in terms(text):
                bucket = int.from_bytes(hashlib.sha256(term.encode()).digest()[:4], "big") % 512
                values[i, bucket] += 1
        return normalize_vectors(values)


class SemanticEmbedder:
    id = f"{MODEL_NAME}@{MODEL_REVISION}"

    def __init__(self, cache_dir: Path = Path("data/models")):
        from fastembed import TextEmbedding
        from tokenizers import Tokenizer
        path = cache_dir / ("models--" + MODEL_REPO.replace("/", "--")) / "snapshots" / MODEL_REVISION
        for name, expected in MODEL_FILES.items():
            file = path / name
            if not file.is_file():
                raise ValueError("Modelo no descargado. Ejecute python scripts/download_model.py")
            with file.open("rb") as stream:
                actual = hashlib.file_digest(stream, "sha256").hexdigest()
            if actual != expected:
                raise ValueError(f"El modelo no supera la verificación de integridad: {name}")
        self.tokenizer = Tokenizer.from_file(str(path / "tokenizer.json"))
        self.tokenizer.no_truncation()
        self.tokenizer.no_padding()
        self.model = TextEmbedding(
            model_name=MODEL_NAME, specific_model_path=str(path),
            local_files_only=True, threads=2, providers=["CPUExecutionProvider"],
        )

    def token_count(self, text: str) -> int:
        return len(self.tokenizer.encode(text).ids)

    def encode(self, texts: list[str]):
        if any(self.token_count(text) > 128 for text in texts):
            raise ValueError("Texto excede 128 tokens; fragmente el documento o acorte la consulta.")
        return normalize_vectors(list(self.model.embed(texts, batch_size=32)))


def make_embedder(backend: str):
    if backend == "lexical":
        return LexicalEmbedder()
    if backend == "semantic":
        return SemanticEmbedder()
    raise ValueError("Backend desconocido.")

