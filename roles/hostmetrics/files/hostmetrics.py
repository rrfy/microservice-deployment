#!/usr/bin/env python3
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

def detect_host_type():
    c = subprocess.run(["systemd-detect-virt", "--container"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    if c.returncode == 0:
        return "container"
    v = subprocess.run(["systemd-detect-virt", "--vm"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    if v.returncode == 0:
        return "vm"
    return "bare-metal"

def render_metrics():
    host_type = detect_host_type()
    lines = []
    lines.append("# HELP host_type_info Host environment type as an info metric")
    lines.append("# TYPE host_type_info gauge")
    lines.append(f'host_type_info{{type="{host_type}"}} 1')
    lines.append("# HELP app_up Application liveness")
    lines.append("# TYPE app_up gauge")
    lines.append("app_up 1")
    return "\n".join(lines) + "\n"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/metrics", "/"):
            body = render_metrics().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

def main():
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
