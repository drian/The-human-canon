from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, sqlite3, os

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get("DATA_DIR", "/data"))
DATA.mkdir(parents=True, exist_ok=True)
BOOKS = json.loads((ROOT / "books.json").read_text())
IDS = {b["id"] for b in BOOKS}
DB = DATA / "canon.db"
with sqlite3.connect(DB) as db:
    db.execute("CREATE TABLE IF NOT EXISTS progress (id INTEGER PRIMARY KEY, status TEXT NOT NULL)")

class Handler(BaseHTTPRequestHandler):
    def send_data(self, data, kind="application/json", status=200):
        body = data if isinstance(data, bytes) else json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_data((ROOT / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/books":
            with sqlite3.connect(DB) as db:
                states = dict(db.execute("SELECT id,status FROM progress"))
            self.send_data([{**b, "status": states.get(b["id"], "unread")} for b in BOOKS])
        else:
            self.send_data({"error":"Not found"}, status=404)

    def do_POST(self):
        if self.path != "/api/progress":
            return self.send_data({"error":"Not found"}, status=404)
        try:
            if self.headers.get_content_type() != "application/json":
                raise ValueError()
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError()
            payload = json.loads(self.rfile.read(length))
            bid, status = payload["id"], payload["status"]
            if type(bid) is not int or bid not in IDS or status not in ("unread","reading","read"):
                raise ValueError()
        except (ValueError, TypeError, KeyError):
            return self.send_data({"error":"Invalid input"}, status=400)
        with sqlite3.connect(DB) as db:
            db.execute("INSERT INTO progress VALUES (?,?) ON CONFLICT(id) DO UPDATE SET status=excluded.status",(bid,status))
        self.send_data({"ok":True})

if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
