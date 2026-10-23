from pathlib import Path

from .models import Hit
from .vector_store import search_index


def retrieve(question: str, path: Path, embedder, k: int = 3,
             threshold: float = 0.5, source_id: str | None = None) -> list[Hit]:
    if not isinstance(question, str) or not question.strip() or len(question) > 1000:
        raise ValueError("La consulta debe contener entre 1 y 1000 caracteres.")
    vector = embedder.encode([question.strip()])[0]
    return search_index(path, vector, embedder.id, k, threshold, source_id)

