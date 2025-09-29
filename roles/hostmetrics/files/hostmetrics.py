#!/usr/bin/env python3
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

import os, shutil, subprocess

def _in_container():
    try:
        if os.path.exists("/.dockerenv"):
            return True
        with open("/proc/1/cgroup","rb") as f:
            data = f.read()
            if b"docker" in data or b"kubepods" in data or b"container" in data or b"libpod" in data:
                return True
    except Exception:
        pass
    return False

def detect_host_type():
    try:
        if _in_container():
            return "container"
        sdv = shutil.which("systemd-detect-virt")
        if sdv:
            if subprocess.run([sdv,"--container"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                return "container"
            if subprocess.run([sdv,"--vm"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                return "vm"
        return "bare-metal"
    except Exception:
        return "unknown"


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
