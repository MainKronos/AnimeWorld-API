import sys
import httpx
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie

# sudo ./main.py 80 http://jenkins.example.com:8080/

# ssh -R 80:localhost:8080 localhost.run

URL = "https://www.animeworld.so/api"

class Redirect(BaseHTTPRequestHandler):


    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Headers", "csrf-token")
        self.send_header("Access-Control-Request-Method", "*")

        self.end_headers()

    def do_POST(self):
        self.do_REQUEST()

    def do_GET(self):

        self.do_REQUEST()

    def do_REQUEST(self):
        cookies = dict(SimpleCookie(self.headers.get('Cookie')))
        headers = {}
        if self.headers.get('csrf-token'): 
            headers['csrf-token'] = self.headers.get('csrf-token')
        
        data = None
        content_len = self.headers.get('Content-Length')
        if content_len:
            data = self.rfile.read(int(content_len))

        content = None
        try:
            with httpx.Client(http2=True) as client:
                res = client.request(method=self.command, url="https://www.animeworld.so/api" + self.path, headers=headers, cookies=cookies, content=data)
                content = res.content
                
                self.send_response(res.status_code)
                self.send_header('Content-Type', res.headers['Content-Type'])
        except httpx.ReadTimeout:
            self.send_response('403')
        finally:
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            if content: self.wfile.write(content)
            

if __name__ == "__main__":
    sock = HTTPServer(("", int(8000)), Redirect)

    try:
        sock.serve_forever()
    except KeyboardInterrupt:
        sock.socket.close()