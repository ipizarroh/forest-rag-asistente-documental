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
        import onnxruntime as ort
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
        # Sólo este tokenizer/modelo fijado por hash; no autodetección ni código remoto.
        self.tokenizer.enable_padding(pad_id=self.tokenizer.token_to_id("<pad>"), pad_token="<pad>")
        options = ort.SessionOptions()
        options.intra_op_num_threads = 2
        options.inter_op_num_threads = 2
        self.model = ort.InferenceSession(str(path / "model_optimized.onnx"),
                                         sess_options=options, providers=["CPUExecutionProvider"])

    def token_count(self, text: str) -> int:
        return len(self.tokenizer.encode(text).ids)

    def encode(self, texts: list[str]):
        if not isinstance(texts, list) or any(not isinstance(text, str) for text in texts):
            raise ValueError("Se requiere una lista de textos.")
        if any(self.token_count(text) > 128 for text in texts):
            raise ValueError("Texto excede 128 tokens; fragmente el documento o acorte la consulta.")
        pooled = []
        for start in range(0, len(texts), 32):
            batch = self.tokenizer.encode_batch(texts[start:start + 32])
            ids = np.asarray([item.ids for item in batch], dtype=np.int64)
            mask = np.asarray([item.attention_mask for item in batch], dtype=np.int64)
            hidden = self.model.run(["last_hidden_state"], {
                "input_ids": ids, "attention_mask": mask, "token_type_ids": np.zeros_like(ids),
            })[0]
            # Media sólo de tokens reales; acumular en float64 conserva el contrato previo.
            total = np.sum(hidden, axis=1, where=mask[:, :, None].astype(bool), dtype=np.float64)
            pooled.extend((total / mask.sum(axis=1, keepdims=True)).astype(np.float32))
        return normalize_vectors(pooled) if pooled else np.empty((0, 384), dtype=np.float32)


def make_embedder(backend: str):
    if backend == "lexical":
        return LexicalEmbedder()
    if backend == "semantic":
        return SemanticEmbedder()
    raise ValueError("Backend desconocido.")

