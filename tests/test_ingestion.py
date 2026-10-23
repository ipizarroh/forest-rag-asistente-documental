from dataclasses import asdict, replace
import hashlib
import json

import pytest
from pypdf import PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject

from forestrag.ingestion import load_sources, read_source
from conftest import local_source


def test_registered_text_and_hash(tmp_path, source):
    path = tmp_path / "demo.txt"
    path.write_text("Documentación forestal española.", encoding="utf-8")
    source = local_source(source, path)
    pages = read_source(source, tmp_path)
    assert pages[0].text == "Documentación forestal española."
    assert pages[0].source.sha256 == source.sha256
    with pytest.raises(ValueError, match="SHA-256"):
        read_source(replace(source, sha256="0" * 64), tmp_path)


@pytest.mark.parametrize("changes", [
    {"reuse_authorized": False}, {"id": "../otro"}, {"sha256": "no"},
    {"url": "http://example.org"}, {"url": "https://u:p@example.org/"},
])
def test_manifest_rejects_unapproved_source(tmp_path, source, changes):
    file = tmp_path / "manifest.json"
    file.write_text(json.dumps({"sources": [asdict(replace(source, **changes))]}), encoding="utf-8")
    with pytest.raises(ValueError):
        load_sources(file)


def test_manifest_rejects_duplicate_sources(tmp_path, source):
    file = tmp_path / "sources.json"
    file.write_text(json.dumps({"sources": [asdict(source), asdict(source)]}))
    with pytest.raises(ValueError, match="únicos"):
        load_sources(file)


def test_directory_escape_blocked(tmp_path, source):
    raw = tmp_path / "raw"
    raw.mkdir()
    secret = tmp_path / "elsewhere.txt"
    secret.write_text("No debe leerse")
    with pytest.raises(ValueError, match="directorio"):
        read_source(replace(local_source(source, secret), file="../elsewhere.txt"), raw)


def test_file_limits_and_signature(tmp_path, source, monkeypatch):
    path = tmp_path / "demo.pdf"
    path.write_text("No es PDF")
    source = local_source(source, path)
    with pytest.raises(ValueError, match="firma"):
        read_source(source, tmp_path)
    monkeypatch.setattr("forestrag.ingestion.MAX_FILE_BYTES", 3)
    with pytest.raises(ValueError, match="20 MiB"):
        read_source(source, tmp_path)


def test_scanned_empty_pdf_fails_explicitly(tmp_path, source):
    path = tmp_path / "scanned.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)
    writer.write(path)
    with pytest.raises(ValueError, match="OCR"):
        read_source(local_source(source, path), tmp_path)


def test_real_pdf_extraction_preserves_page(tmp_path, source):
    path = tmp_path / "document.pdf"
    writer = PdfWriter()
    for text in [b"Registro de mantenimiento", b"Inventario de productos"]:
        page = writer.add_blank_page(width=300, height=300)
        font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                                 NameObject("/Subtype"): NameObject("/Type1"),
                                 NameObject("/BaseFont"): NameObject("/Helvetica")})
        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)})})
        content = DecodedStreamObject()
        content.set_data(b"BT /F1 12 Tf 10 270 Td (" + text + b") Tj ET")
        page[NameObject("/Contents")] = writer._add_object(content)
    writer.write(path)
    pages = read_source(replace(local_source(source, path), pages=[2]), tmp_path)
    assert len(pages) == 1 and pages[0].number == 2
    assert "Inventario" in pages[0].text
    with pytest.raises(ValueError, match="páginas"):
        read_source(replace(local_source(source, path), pages=[3]), tmp_path)


def test_no_unapproved_direct_ingestion(tmp_path, source):
    with pytest.raises(ValueError, match="autorizada"):
        read_source(replace(source, reuse_authorized=False), tmp_path)

