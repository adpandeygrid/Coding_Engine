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
import urllib.request
import json

PORT = 8000
BASE_DIR = Path(__file__).parent.parent

# Railway API URL - can be overridden with RAILWAY_API_URL env var
RAILWAY_API_URL = os.getenv('RAILWAY_API_URL', 'https://codingengine-production.up.railway.app')

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR / 'frontend'), **kwargs)
    
    def do_GET(self):
        # Handle API proxy requests
        if self.path.startswith('/api/proxy/'):
            self.handle_api_proxy('GET')
            return
        
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
    
    def do_POST(self):
        # Handle API proxy requests
        if self.path.startswith('/api/proxy/'):
            self.handle_api_proxy('POST')
            return
        
        # Default: 404
        self.send_response(404)
        self.end_headers()
    
    def do_OPTIONS(self):
        # Handle CORS preflight for API proxy
        if self.path.startswith('/api/proxy/'):
            self.send_response(200)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
    
    def handle_api_proxy(self, method):
        """Proxy API requests to Railway to avoid CORS issues"""
        try:
            # Extract the API path (everything after /api/proxy/)
            api_path = self.path.replace('/api/proxy', '')
            if not api_path.startswith('/'):
                api_path = '/' + api_path
            
            # Build the full Railway API URL
            railway_url = f"{RAILWAY_API_URL.rstrip('/')}{api_path}"
            
            print(f"\n{'='*60}")
            print(f"PROXY REQUEST: {method} {self.path}")
            print(f"Forwarding to: {railway_url}")
            print(f"{'='*60}\n")
            
            if method == 'GET':
                # GET request
                req = urllib.request.Request(railway_url)
                req.add_header('User-Agent', 'Python-Proxy/1.0')
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    self.send_response(response.getcode())
                    self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response.read())
            
            elif method == 'POST':
                # POST request - read body
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                req = urllib.request.Request(railway_url, data=post_data)
                req.add_header('Content-Type', 'application/json')
                req.add_header('User-Agent', 'Python-Proxy/1.0')
                
                with urllib.request.urlopen(req, timeout=60) as response:
                    self.send_response(response.getcode())
                    self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(response.read())
        
        except urllib.error.HTTPError as e:
            # Read error body once
            error_body_bytes = b''
            try:
                error_body_bytes = e.read()
                error_body_str = error_body_bytes.decode('utf-8') if error_body_bytes else ''
            except:
                error_body_str = ''
            
            print(f"\n{'='*60}")
            print(f"HTTP Error from Railway: {e.code} - {e.reason}")
            print(f"URL: {railway_url}")
            if error_body_str:
                print(f"Error body: {error_body_str}")
            else:
                print(f"No error body received")
            print(f"{'='*60}\n")
            
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            if error_body_bytes:
                self.wfile.write(error_body_bytes)
            else:
                self.wfile.write(json.dumps({'error': f'HTTP {e.code}: {e.reason}'}).encode())
        
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"\n{'='*60}")
            print(f"Proxy error: {e}")
            print(f"Traceback:\n{error_trace}")
            print(f"{'='*60}\n")
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e), 'traceback': error_trace}).encode())
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

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

