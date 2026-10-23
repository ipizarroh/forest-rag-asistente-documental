import hashlib
import re
import unicodedata
from collections.abc import Callable

from .models import Chunk, Page


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\x00", "")
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", text)
    return re.sub(r"\s+", " ", text).strip()


def chunk_pages(pages: list[Page], max_words: int = 55, overlap: int = 10,
                token_count: Callable[[str], int] | None = None,
                max_tokens: int = 120) -> list[Chunk]:
    if max_words <= 0 or overlap < 0 or overlap >= max_words or max_tokens < 4:
        raise ValueError("Parámetros de fragmentación inválidos.")
    chunks = []
    for page in pages:
        words = normalize(page.text).split()
        start = 0
        while start < len(words):
            end = min(start + max_words, len(words))
            if token_count is not None:
                while end > start and token_count(" ".join(words[start:end])) > max_tokens:
                    end -= 1
                if end == start:
                    raise ValueError("Una palabra excede el límite de tokens del modelo.")
            text = " ".join(words[start:end])
            identity = f"{page.source.id}:{page.source.sha256}:{page.number}:{start}:{text}"
            chunks.append(Chunk(
                id=hashlib.sha256(identity.encode()).hexdigest()[:24],
                source_id=page.source.id, title=page.source.title,
                url=page.source.url, license=page.source.license,
                document_sha256=page.source.sha256, page=page.number,
                page_label=page.label, start_word=start, text=text,
            ))
            if end == len(words):
                break
            start = max(start + 1, end - overlap)
    return chunks

