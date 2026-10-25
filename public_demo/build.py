"""Build an allowlisted public artifact; no private paths or runtime secrets."""
import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from forestrag.embeddings import LexicalEmbedder
from forestrag.models import Page, Source
from forestrag.preprocessing import chunk_pages

ASSETS = ("index.html", "style.css", "engine.mjs", "app.mjs")
ID = re.compile(r"[a-z][a-z0-9-]{1,40}")

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_corpus(path):
    raw = path.read_bytes()
    if len(raw) > 1_000_000:
        raise ValueError("Corpus demasiado grande")
    data = json.loads(raw)
    if set(data) != {"schema_version", "corpus_version", "documents"} or data["schema_version"] != 1:
        raise ValueError("Esquema de corpus incompatible")
    docs = data["documents"]
    if not isinstance(docs, list) or not 1 <= len(docs) <= 12:
        raise ValueError("Número de documentos inválido")
    ids = set()
    for doc in docs:
        if set(doc) != {"id", "title", "version", "classification", "synthetic",
                        "approved_for_public_demo", "status", "license", "sections"}:
            raise ValueError("Campos documentales no autorizados")
        if (not isinstance(doc["id"], str) or not ID.fullmatch(doc["id"]) or doc["id"] in ids
            or doc["classification"] != "public" or doc["synthetic"] is not True
            or doc["approved_for_public_demo"] is not True or doc["status"] != "active"
            or type(doc["version"]) is not int or doc["version"] < 1 or doc["license"] != "CC0-1.0"):
            raise ValueError("Sólo material sintético público aprobado y activo")
        ids.add(doc["id"])
        if not isinstance(doc["title"], str) or not 1 <= len(doc["title"]) <= 120:
            raise ValueError("Título inválido")
        if not isinstance(doc["sections"], list) or not 1 <= len(doc["sections"]) <= 8:
            raise ValueError("Secciones inválidas")
        for section in doc["sections"]:
            if (set(section) != {"title", "text"} or
                any(not isinstance(section[k], str) or not section[k].strip() for k in section) or
                len(section["title"]) > 120 or len(section["text"]) > 4000):
                raise ValueError("Sección inválida")
    return data

def build(output, corpus_path=ROOT / "public_demo/corpus.json"):
    output = Path(output)
    if output.is_symlink():
        raise ValueError("Destino simbólico no permitido")
    allowed = set(ASSETS) | {"corpus.json", "release.json", ".nojekyll"}
    if output.exists() and any(p.name not in allowed or not p.is_file() or p.is_symlink() for p in output.iterdir()):
        raise ValueError("El destino contiene archivos ajenos; use un directorio aislado")
    corpus = read_corpus(corpus_path)
    spec = json.loads((ROOT / "public_demo/release-spec.json").read_text(encoding="utf-8"))
    docs, chunks = [], []
    for doc in corpus["documents"]:
        doc_hash = digest(json.dumps(doc, ensure_ascii=False, sort_keys=True).encode())
        source = Source(doc["id"], doc["title"], "ForestRAG - ejemplo ficticio",
                        "#" + doc["id"], "2026-10-24", doc["license"], True,
                        doc["id"] + ".json", doc_hash)
        pages = [Page(source, i, section["title"], section["text"])
                 for i, section in enumerate(doc["sections"], 1)]
        for chunk in chunk_pages(pages, **spec["chunking"]):
            vector = LexicalEmbedder().encode([chunk.text])[0]
            chunks.append({"id": chunk.id, "document_id": doc["id"], "section": chunk.page,
                           "section_title": chunk.page_label, "text": chunk.text,
                           "vector": [[int(i), float(v)] for i, v in enumerate(vector) if v]})
        docs.append({**doc, "sha256": doc_hash})
    if len(chunks) > spec["limits"]["chunks"]:
        raise ValueError("Demasiados fragmentos")
    payload = json.dumps({"schema_version": 1, "engine": spec["engine"],
                          "corpus_version": corpus["corpus_version"],
                          "documents": docs, "chunks": chunks},
                         ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    if len(payload) > spec["limits"]["payload_bytes"]:
        raise ValueError("Paquete demasiado grande")
    generated = {"corpus.json": payload, ".nojekyll": b""}
    generated.update({name: (ROOT / "public_demo/web" / name).read_bytes() for name in ASSETS})
    source_paths = [ROOT / "public_demo/build.py", ROOT / "public_demo/release-spec.json", corpus_path,
                    ROOT / "src/forestrag/embeddings.py", ROOT / "src/forestrag/preprocessing.py",
                    ROOT / "src/forestrag/models.py", ROOT / "requirements-lab-linux-py312.lock"]
    source_paths += [ROOT / "public_demo/web" / name for name in ASSETS]
    # No environment variables or machine identifiers enter this artifact.
    source_inputs = {str(p.relative_to(ROOT)).replace("\\", "/"): digest(p.read_bytes())
                     for p in source_paths if p.is_relative_to(ROOT)}
    import numpy
    commit = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    dirty = bool(subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain"], text=True).strip())
    manifest = {**spec, "source_commit": commit, "source_dirty": dirty,
                "corpus_version": corpus["corpus_version"], "source_inputs": source_inputs,
                "build_runtime": {"python": platform.python_version(), "numpy": numpy.__version__},
                "runtime_dependencies": [], "generative_model": None,
                "files": {name: {"sha256": digest(data), "bytes": len(data)}
                          for name, data in sorted(generated.items())}}
    output.mkdir(parents=True, exist_ok=True)
    for name, data in generated.items():
        (output / name).write_bytes(data)
    (output / "release.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n",
                                       encoding="utf-8", newline="\n")
    return manifest

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "dist/public-demo")
    args = parser.parse_args()
    result = build(args.out)
    print(json.dumps({"version": result["candidate_version"], "files": len(result["files"])+1,
                      "bytes": sum(p.stat().st_size for p in args.out.iterdir())}))
