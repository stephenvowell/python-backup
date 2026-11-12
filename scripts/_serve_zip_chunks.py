"""Start local HTTP server for zip b64 chunks (background helper)."""
import http.server
import socketserver
from pathlib import Path

PORT = 8765
ROOT = Path(__file__).resolve().parent


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)


if __name__ == "__main__":
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Serving {ROOT} at http://127.0.0.1:{PORT}/", flush=True)
        httpd.serve_forever()
