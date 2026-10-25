"""Demostración HTTP local sintética; nunca imprime credenciales."""
import http.client
import json
from pathlib import Path

tokens = json.loads(Path("data/security-lab/credentials.json").read_text())
expected = {"ops": {"public", "ops", "injection"}, "hr": {"public", "hr"},
            "admin": {"public"}, "other": {"public", "other"}, "app": {"public", "ops", "injection"}}
for pid, token in tokens.items():
    conn = http.client.HTTPConnection("127.0.0.1", 8510, timeout=5)
    conn.request("POST", "/query", body=json.dumps({"question": "inventario"}),
                 headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
    response = conn.getresponse()
    assert response.status == 200
    result = json.loads(response.read())
    documents = {p["url"].split("/")[-1] for p in result["passages"]}
    assert documents == expected[pid]
    print(pid, sorted(documents), "PASS")
    conn.close()
conn = http.client.HTTPConnection("127.0.0.1", 8510, timeout=5)
conn.request("GET", "/documents/hr", headers={"Authorization": "Bearer " + tokens["ops"]})
response = conn.getresponse()
assert response.status == 404 and b"NOMINA" not in response.read()
conn.close()
print("Descarga no autorizada:", response.status, "PASS")
