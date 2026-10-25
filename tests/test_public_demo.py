import copy
import hashlib
import json
from pathlib import Path
import numpy as np
import pytest
from public_demo.build import ROOT, build, read_corpus
from forestrag.embeddings import LexicalEmbedder, terms

def test_public_build_only_contains_allowlisted_assets(tmp_path):
    manifest = build(tmp_path)
    assert set(p.name for p in tmp_path.iterdir()) == set(manifest["files"]) | {"release.json"}
    assert manifest["runtime_dependencies"] == []
    assert manifest["generative_model"] is None
    for name, spec in manifest["files"].items():
        raw = (tmp_path/name).read_bytes()
        assert len(raw) == spec["bytes"] and hashlib.sha256(raw).hexdigest() == spec["sha256"]
    data = json.loads((tmp_path/"corpus.json").read_text(encoding="utf-8"))
    assert len(data["documents"]) == 3 and len(data["chunks"]) == 6
    for chunk in data["chunks"]:
        vector = np.zeros(512, dtype=np.float32)
        for i,v in chunk["vector"]: vector[i] = v
        assert np.array_equal(vector, LexicalEmbedder().encode([chunk["text"]])[0])

@pytest.mark.parametrize("key,value", [
    ("classification","confidential"), ("synthetic",False), ("approved_for_public_demo",False),
    ("status","retired"), ("version",True), ("id","../../private"),
    ("unexpected_host_path","private.db"),
])
def test_build_rejects_unapproved_or_ambiguous_corpus(tmp_path,key,value):
    corpus=json.loads((ROOT/"public_demo/corpus.json").read_text(encoding="utf-8"))
    corpus["documents"][0][key]=value
    path=tmp_path/"input.json";path.write_text(json.dumps(corpus),encoding="utf-8")
    with pytest.raises(ValueError): read_corpus(path)

def test_unknown_schema_and_duplicate_documents_are_rejected(tmp_path):
    original=json.loads((ROOT/"public_demo/corpus.json").read_text(encoding="utf-8"))
    for variant in ("schema","duplicate"):
        corpus=copy.deepcopy(original)
        if variant=="schema": corpus["schema_version"]=2
        else: corpus["documents"].append(copy.deepcopy(corpus["documents"][0]))
        path=tmp_path/"input.json";path.write_text(json.dumps(corpus),encoding="utf-8")
        with pytest.raises(ValueError): read_corpus(path)

def test_retirement_rebuild_excludes_old_source_and_chunks(tmp_path):
    original=read_corpus(ROOT/"public_demo/corpus.json")
    before=build(tmp_path/"site")
    removed=original["documents"].pop(0)["id"]
    custom=tmp_path/"input.json";custom.write_text(json.dumps(original),encoding="utf-8")
    after=build(tmp_path/"site",custom)
    payload=(tmp_path/"site/corpus.json").read_text(encoding="utf-8")
    assert removed not in payload
    assert before["files"]["corpus.json"]["sha256"] != after["files"]["corpus.json"]["sha256"]

def test_repeat_build_is_byte_reproducible_and_refuses_mixed_destination(tmp_path):
    build(tmp_path/"one");build(tmp_path/"two")
    assert {p.name:p.read_bytes() for p in (tmp_path/"one").iterdir()} == {
        p.name:p.read_bytes() for p in (tmp_path/"two").iterdir()}
    (tmp_path/"one/private.db").write_text("not a public file")
    with pytest.raises(ValueError):build(tmp_path/"one")

def test_web_templates_do_not_have_executable_html_sinks_or_tracking():
    combined="\n".join((ROOT/"public_demo/web"/f).read_text(encoding="utf-8")
                       for f in ("index.html","engine.mjs","app.mjs"))
    for forbidden in ("innerHTML", "insertAdjacentHTML", "eval(", "localStorage", "sessionStorage",
                      "document.cookie", "sendBeacon", "file_uploader", "localhost:11434"):
        assert forbidden not in combined

def test_export_cross_runtime_reference(tmp_path):
    # Node reads this exported reference; test fixture never enters the public artifact.
    samples=["campos observación terreno", "MONITOREO imágenes resolución", "huella SHA-256",
             "áéíóú ñ Ñ ü", "abc_foo 123 12 a", "abc東京 abc", "precisión versión nubes",
             "¿Cómo se retira un documento?", "a"*300]
    target=ROOT/"reports/public_arch001/lexical-reference.json"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps([{"query":s,"terms":terms(s),
        "vector":LexicalEmbedder().encode([s])[0].tolist()} for s in samples],
        ensure_ascii=False),encoding="utf-8")
