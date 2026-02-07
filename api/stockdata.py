# api/stockdata.py - Vercel官方Python示例
from http.server import BaseHTTPRequestHandler
from datetime import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        message = {
            'message': 'Hello from Vercel Python!',
            'time': str(datetime.now())
        }
        import json
        self.wfile.write(json.dumps(message).encode('utf-8'))

# 这是Vercel要求的确切入点
def main(request, response):
    handler = Handler(request, response)
    handler.handle_request()
    return response
