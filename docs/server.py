import http.server
import os

print("=== ENV VARS ===")
for k, v in os.environ.items():
    print(f"  {k} = {v}")
print("================")

PORT = int(
    os.environ.get("PORT") or
    os.environ.get("SERVER_PORT") or
    os.environ.get("APP_PORT") or
    os.environ.get("HTTP_PORT") or
    8080
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[req] {args}")

print(f">>> Starting on port {PORT}")

with http.server.HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()
