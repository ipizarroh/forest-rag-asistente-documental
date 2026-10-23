"""Descarga única del corpus aprobado; sin URLs configurables ni credenciales."""
import hashlib
import json
import os
import tempfile
import urllib.request
from pathlib import Path

from forestrag.ingestion import MAX_FILE_BYTES, load_sources

sources = load_sources(Path("examples/sources.json"))
for source in sources:
    destination = Path("data/raw") / source.file
    destination.parent.mkdir(parents=True, exist_ok=True)
    url = "https://bibliotecadigital.ciren.cl/server/api/core/bitstreams/fb3ee874-e6bd-408c-8c99-b9d1a0e55864/content"
    fd, temp = tempfile.mkstemp(dir=destination.parent)
    os.close(fd)
    try:
        with urllib.request.urlopen(url, timeout=60) as response, open(temp, "wb") as stream:
            if response.headers.get_content_type() != "application/pdf":
                raise ValueError("La fuente no devolvió un PDF.")
            total = 0
            while data := response.read(65536):
                total += len(data)
                if total > MAX_FILE_BYTES:
                    raise ValueError("Descarga excede 20 MiB.")
                stream.write(data)
        file = Path(temp)
        if file.read_bytes()[:5] != b"%PDF-":
            raise ValueError("Firma PDF inválida.")
        with file.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != source.sha256:
                raise ValueError("El PDF cambió; revisar procedencia antes de actualizar el manifiesto.")
        os.replace(temp, destination)
        print(f"Verificado: {source.id} ({total} bytes)")
    finally:
        Path(temp).unlink(missing_ok=True)

