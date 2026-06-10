import http.server
import os

# Pterodactyl/MonkeyBytes sets different port variables — try all of them
PORT = int(
    os.environ.get("PORT") or
    os.environ.get("SERVER_PORT") or
    os.environ.get("APP_PORT") or
    8080
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

print(f"mycord docs running on port {PORT}")
print(f"Open: http://localhost:{PORT}")

with http.server.HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()
