#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend and test cases
Run with: python server.py
"""

import http.server
import socketserver
import os
from pathlib import Path
import urllib.parse

PORT = 8000
BASE_DIR = Path(__file__).parent.parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR / 'frontend'), **kwargs)
    
    def do_GET(self):
        # Handle test cases requests
        if self.path.startswith('/test_cases/'):
            file_path = BASE_DIR / 'test_cases' / self.path.replace('/test_cases/', '')
            if file_path.exists() and file_path.is_file():
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.end_headers()
                return
        
        # Handle CORS for all requests
        if self.path.endswith('.js') or self.path.endswith('.css') or self.path.endswith('.html'):
            super().do_GET()
            return
        
        # Default behavior
        super().do_GET()
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    os.chdir(BASE_DIR / 'frontend')
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Frontend server running at http://localhost:{PORT}")
        print(f"📁 Serving from: {BASE_DIR / 'frontend'}")
        print(f"📝 Test cases available at: http://localhost:{PORT}/test_cases/")
        print("\nPress Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == "__main__":
    main()

