"""Empaqueta resultados existentes y ejecuta demo HTTP sintética sin guardar secretos."""
import ast
import hashlib
import importlib.metadata as metadata
import json
import platform
import subprocess
import tempfile
import threading
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from forestrag.embeddings import MODEL_FILES, MODEL_REPO, MODEL_REVISION
from forestrag.ingestion import digest, load_sources
from forestrag.security_http import LabServer
from forestrag.security_lab import seed_demo

root = Path(__file__).resolve().parents[1]
reports = root / "reports/freg001"
reports.mkdir(parents=True, exist_ok=True)
def save(name, payload):
    (reports / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

cases, suites = [], {}
for filename in ("full-suite.xml", "lab-clean-suite.xml"):
    xml = ET.parse(reports / filename)
    nodes = list(xml.iter("testcase"))
    suites[filename] = {"cases": len(nodes), "failed": sum(n.find("failure") is not None or n.find("error") is not None for n in nodes),
                        "skipped": sum(n.find("skipped") is not None for n in nodes), "sha256": digest(reports / filename)}
    if filename != "full-suite.xml":
        continue
    for i, node in enumerate(nodes, 1):
        name = node.attrib["name"]
        module = node.attrib["classname"].replace(".", "/") + ".py"
        tree = ast.parse((root / module).read_text())
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name.split("[")[0])
        expected = [ast.unparse(n.test) for n in ast.walk(function) if isinstance(n, ast.Assert)]
        if "security_lab" in module:
            requirement = "FORESTRAG SECURITY; " + name.split("_")[1].upper()
        elif "audit_regressions" in module:
            requirement = name.split("_")[1].upper()
        else:
            requirement = "Regresión funcional original: " + module
        status = "FAIL" if node.find("failure") is not None or node.find("error") is not None else "NOT RUN" if node.find("skipped") is not None else "PASS"
        cases.append({"id": f"PY-{i:03}", "requirement": requirement, "scenario": name,
                      "expected": expected or ["El escenario completa sus aserciones/raises sin fallo."],
                      "observed": "Pytest ejecutó el caso sin fallo." if status == "PASS" else status,
                      "status": status, "evidence": f"{module}::{name}; reports/freg001/full-suite.xml",
                      "elapsed_seconds": float(node.attrib.get("time", 0))})
save("test-cases.json", cases)

with tempfile.TemporaryDirectory() as directory:
    lab, tokens = seed_demo(Path(directory) / "lab.sqlite")
    with LabServer(("127.0.0.1", 0), lab) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        import http.client
        demo = []
        try:
            for pid, token in tokens.items():
                conn = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
                conn.request("POST", "/query", body=json.dumps({"question": "inventario"}),
                             headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
                response = conn.getresponse()
                result = json.loads(response.read())
                assert response.status == 200
                demo.append({"identity_ficticia": pid, "status": response.status,
                             "documents": sorted(p["url"].split("/")[-1] for p in result["passages"])})
                conn.close()
            conn = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
            conn.request("GET", "/documents/hr", headers={"Authorization": "Bearer " + tokens["ops"]})
            response = conn.getresponse()
            raw = response.read()
            assert response.status == 404 and b"NOMINA" not in raw
            demo.append({"scenario": "descarga hr como ops", "status": response.status,
                         "contains_confidential_canary": False})
            conn.close()
        finally:
            server.shutdown()
            thread.join(5)
save("http-demo.json", {"transport": "HTTP/socket real en loopback, servidor y cliente en una ejecución", "results": demo})

archive = root / "docs/history/EVIDENCIAS_AUDITORIA_FORESTRAG.zip"
with zipfile.ZipFile(archive) as z:
    manifest = json.loads(z.read("MANIFEST_SHA256.json"))
    assert all(hashlib.sha256(z.read(p)).hexdigest() == value for p, value in manifest.items())
    historical_integrity = {"entries": len(z.namelist()), "verified_hashes": len(manifest), "crc_error": z.testzip()}
model_path = root / "data/models" / ("models--" + MODEL_REPO.replace("/", "--")) / "snapshots" / MODEL_REVISION
models = [{"file": name, "sha256": digest(model_path / name), "bytes": (model_path / name).stat().st_size}
          for name in MODEL_FILES]
assert all(row["sha256"] == MODEL_FILES[row["file"]] for row in models)
corpus = [{"source": s.id, "sha256": digest(root / "data/raw" / s.file), "pages": s.pages,
           "bytes": (root / "data/raw" / s.file).stat().st_size,
           "license": s.license, "original_acquisition_date": "NO VERIFICADO"}
          for s in load_sources(root / "examples/sources.json")]
def git(*args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
def audit_summary(name):
    data = json.loads((reports / name).read_text())
    return {"packages_reported": len(data["dependencies"]),
            "advisories": sum(len(p.get("vulns", [])) for p in data["dependencies"]),
            "affected": [{"name": p["name"], "version": p["version"], "count": len(p["vulns"])}
                         for p in data["dependencies"] if p.get("vulns")]}
save("execution-receipt.json", {
    "version": "FREG-CRITICAL-001", "created_at_utc": datetime.now(timezone.utc).isoformat(),
    "branch": git("branch", "--show-current"), "code_commit": git("rev-parse", "HEAD"),
    "base_commit": "eee8da5035340abef011357e5f85ad7b2fc34bc3", "published": False,
    "runtime": {"python": platform.python_version(), "platform": platform.platform()},
    "suites": suites, "new_cases": sum("security_lab" in c["evidence"] or "audit_regressions" in c["evidence"] for c in cases),
    "scanner_version": metadata.version("pip-audit"),
    "dependency_scan_full": audit_summary("dependency-audit-full.json"),
    "dependency_scan_lab": audit_summary("dependency-audit-lab.json"),
    "pip_check": {"full": "exit0: No broken requirements found.", "lab": "exit0: No broken requirements found."},
    "historical_archive": {"sha256": digest(archive), **historical_integrity},
    "historical_plan_sha256": digest(root / "docs/history/PLAN_PRESENTACION_FORESTRAG_ARAUCO.md"),
    "corpus_reacquired_this_session": corpus, "model_revision": MODEL_REVISION, "model_files": models,
    "limitations": ["No push/merge/CI nuevo", "Sin inferencia LLM real, SSO/MFA, TLS remoto o cifrado en reposo",
                    "Scanner full incluye herramientas de auditoría/preparación; entorno mínimo distinto",
                    "Pruebas locales sintéticas, mismo agente; no pentest externo ni certificación",
                    "Integridad coeditable no protege contra escritura completa del host",
                    "No se guardan credenciales de laboratorio en las evidencias"]})
print(json.dumps({"suites": suites, "cases": len(cases), "historical_hashes": len(manifest)}, ensure_ascii=False))
