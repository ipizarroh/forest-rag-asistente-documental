"""Local review only: serves exactly the built artifact on loopback, never the repo."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] not in ("/","/index.html","/style.css","/app.mjs","/engine.mjs","/corpus.json","/release.json","/.nojekyll"):
            self.send_error(404);return
        return super().do_GET()
    def end_headers(self):
        self.send_header("Cache-Control","no-store")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("Referrer-Policy","no-referrer")
        super().end_headers()
    def log_message(self,*args): pass

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--port",type=int,default=8768);args=p.parse_args()
    root=ROOT/"dist/public-demo"
    if not (root/"release.json").is_file():raise SystemExit("Build the public demo first.")
    ThreadingHTTPServer(("127.0.0.1",args.port),partial(Handler,directory=str(root))).serve_forever()
