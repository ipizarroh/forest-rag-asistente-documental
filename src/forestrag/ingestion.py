"""Ingesta explícita de un corpus autorizado; nunca recorre carpetas ajenas."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from .models import Page, Source

MAX_FILE_BYTES = 20 * 1024 * 1024
MAX_PAGES = 250
MAX_TEXT_CHARS = 2_000_000


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load_sources(manifest: Path) -> list[Source]:
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    sources = [Source(**row) for row in payload["sources"]]
    if not sources or len({s.id for s in sources}) != len(sources):
        raise ValueError("El manifiesto debe contener fuentes con identificadores únicos.")
    for s in sources:
        if s.reuse_authorized is not True or not s.license.strip():
            raise ValueError("Fuente sin autorización de reutilización registrada.")
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", s.id):
            raise ValueError("Identificador de fuente inválido.")
        if not re.fullmatch(r"[a-f0-9]{64}", s.sha256):
            raise ValueError("SHA-256 documental inválido.")
        url = urlsplit(s.url)
        if url.scheme != "https" or not url.netloc or url.username or url.password:
            raise ValueError("La fuente debe tener un enlace HTTPS público, sin credenciales.")
    return sources


def read_source(source: Source, raw_dir: Path) -> list[Page]:
    if source.reuse_authorized is not True:
        raise ValueError("Fuente no autorizada.")
    if source.pages is not None and (not isinstance(source.pages, list) or not source.pages):
        raise ValueError("Selección de páginas inválida: use null explícito para todas.")
    base = raw_dir.resolve()
    path = (base / source.file).resolve()
    if not path.is_relative_to(base) or not path.is_file():
        raise ValueError("Archivo inexistente o fuera del directorio autorizado.")
    if not 0 < path.stat().st_size <= MAX_FILE_BYTES:
        raise ValueError("El archivo debe medir entre 1 byte y 20 MiB.")
    if digest(path) != source.sha256:
        raise ValueError("El archivo no coincide con el SHA-256 del manifiesto.")
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        if path.read_bytes()[:5] != b"%PDF-":
            raise ValueError("La firma del archivo no corresponde a un PDF.")
        from pypdf import PdfReader
        from pypdf.errors import PdfReadError
        try:
            reader = PdfReader(path)
        except PdfReadError as exc:
            raise ValueError("PDF inválido o incompleto.") from exc
        if reader.is_encrypted:
            raise ValueError("No se aceptan PDF cifrados.")
        if len(reader.pages) > MAX_PAGES:
            raise ValueError("PDF demasiado extenso para este prototipo.")
        selected = source.pages if source.pages is not None else list(range(1, len(reader.pages) + 1))
        if any(type(n) is not int or n < 1 or n > len(reader.pages) for n in selected):
            raise ValueError("Selección de páginas inválida.")
        labels = reader.page_labels
        pages = []
        total = 0
        for number in sorted(set(selected)):
            page = reader.pages[number - 1]
            # Es un límite posterior a descompresión, no un sandbox de PDF hostiles.
            contents = page.get_contents()
            if contents is not None and len(contents.get_data()) > 5_000_000:
                raise ValueError("Flujo de página demasiado grande.")
            text = page.extract_text() or ""
            total += len(text)
            if total > MAX_TEXT_CHARS:
                raise ValueError("Texto extraído demasiado extenso.")
            if text.strip():
                pages.append(Page(source, number, labels[number - 1], text))
    elif suffix in {".txt", ".md"}:
        text = path.read_text(encoding="utf-8")
        if len(text) > MAX_TEXT_CHARS:
            raise ValueError("Texto demasiado extenso.")
        pages = [Page(source, 1, "1", text)] if text.strip() else []
    else:
        raise ValueError("Sólo se aceptan PDF con texto, TXT y Markdown.")
    if not pages:
        raise ValueError("No se encontró texto extraíble; OCR no implementado.")
    return pages

