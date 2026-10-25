"""Transporte HTTP sólo loopback para laboratorio ficticio; no servidor de producción."""
import argparse
import json
import os
import re
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from socketserver import ThreadingMixIn

from .security_lab import AccessError, SecurityLab, seed_demo


class LabServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    request_queue_size = 8

    def __init__(self, address, lab):
        if address[0] != "127.0.0.1":
            raise ValueError("Este laboratorio sólo admite 127.0.0.1.")
        self.lab = lab
        self._workers = threading.BoundedSemaphore(4)
        super().__init__(address, LabHandler)

    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(3)
        return connection, address

    def process_request(self, request, client_address):
        if not self._workers.acquire(blocking=False):
            # Límite anterior a crear hilos y analizar solicitudes de clientes sin identidad.
            try:
                request.sendall(b"HTTP/1.0 429 Too Many Requests\r\nContent-Length: 0\r\nCache-Control: no-store\r\n\r\n")
            except OSError:
                pass
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self._workers.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._workers.release()


class LabHandler(BaseHTTPRequestHandler):
    server_version = "ForestRAG-Lab"
    sys_version = ""

    def log_message(self, *_args):
        pass  # Evita registrar cabeceras, consultas o credenciales por accidente.

    def send_error(self, code, message=None, explain=None):
        self._reply(code, {"error": "Solicitud no disponible."})

    def _reply(self, status, payload):
        raw = payload if isinstance(payload, bytes) else json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8" if isinstance(payload, bytes) else "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        if isinstance(payload, bytes):
            self.send_header("Content-Disposition", 'attachment; filename="documento-sintetico.txt"')
        self.end_headers()
        self.wfile.write(raw)

    def _handle(self):
        # Sin cookies/CORS. Host fijo previene DNS rebinding; no se aceptan peticiones de páginas web.
        if (self.headers.get("Host") != f"127.0.0.1:{self.server.server_port}"
                or self.headers.get("Origin") is not None
                or self.headers.get("Transfer-Encoding") is not None):
            raise AccessError(403, "Origen o transporte no permitido.")
        authorizations = self.headers.get_all("Authorization", [])
        token = None
        if len(authorizations) == 1 and authorizations[0].startswith("Bearer "):
            token = authorizations[0][7:]
        if self.command == "POST" and self.path == "/query":
            lengths = self.headers.get_all("Content-Length", [])
            if (len(lengths) != 1 or not lengths[0].isdecimal() or not 0 < int(lengths[0]) <= 8192
                    or self.headers.get_content_type() != "application/json"):
                raise AccessError(400, "Cuerpo de solicitud inválido.")
            data = json.loads(self.rfile.read(int(lengths[0])))
            # No se aceptan org/rol/usuario en el cuerpo: identidad exclusivamente del token.
            if not isinstance(data, dict) or set(data) != {"question"}:
                raise AccessError(400, "Sólo se admite question.")
            return self.server.lab.query(token, data["question"])
        if self.command == "GET" and self.path == "/history":
            return self.server.lab.history(token)
        match = re.fullmatch(r"/documents/([a-zA-Z0-9_-]{1,80})", self.path)
        if self.command == "GET" and match:
            return self.server.lab.download(token, match[1])
        raise AccessError(404, "Recurso no disponible.")

    def _dispatch(self):
        try:
            self._reply(200, self._handle())
        except AccessError as exc:
            self._reply(exc.status, {"error": str(exc)})
        except (ValueError, UnicodeError):
            self._reply(400, {"error": "Entrada o artefacto inválido."})
        except (OSError, socket.timeout):
            self.close_connection = True
        except Exception:
            # No se publican excepciones SQL, rutas o detalles de documentos.
            self._reply(503, {"error": "Servicio no disponible."})

    do_GET = _dispatch
    do_POST = _dispatch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["init", "serve"])
    parser.add_argument("--directory", type=Path, default=Path("data/security-lab"))
    parser.add_argument("--port", type=int, default=8510)
    args = parser.parse_args()
    db = args.directory / "lab.sqlite"
    if args.command == "init":
        # Preflight evita crear una DB si ya existe un archivo de credenciales.
        credentials = args.directory / "credentials.json"
        if db.exists() or credentials.exists():
            parser.error("El laboratorio ya existe; no se sobrescribe.")
        _, tokens = seed_demo(db)
        fd = os.open(credentials, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w") as stream:
            json.dump(tokens, stream)
        print("Laboratorio ficticio creado. Credenciales efímeras en archivo local protegido; no compartir.")
    else:
        lab = SecurityLab(db)
        with LabServer(("127.0.0.1", args.port), lab) as server:
            print(f"Laboratorio sintético: http://127.0.0.1:{server.server_port}; detener con Ctrl+C.")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
