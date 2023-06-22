import sys
import httpx
from http.server import HTTPServer, BaseHTTPRequestHandler

# sudo ./main.py 80 http://jenkins.example.com:8080/

# ssh -R 80:localhost:8080 localhost.run

URL = "https://www.animeworld.so/api"

class Redirect(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Headers", "csrf-token")
        self.send_header("Access-Control-Request-Method", "*")

        self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        data = self.rfile.read(content_len)

        with httpx.Client(http2=True) as client:
            try:
                res = client.post("https://www.animeworld.so/api" + self.path, data=data.decode(), headers=dict(self.headers))

                self.send_response(res.status_code)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', res.headers['Content-Type'])
                self.end_headers()
                self.wfile.write(res.content)
            except httpx.ReadTimeout:
                self.send_response(403)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

    def do_GET(self):

        with httpx.Client(http2=True) as client:
            res = client.get("https://www.animeworld.so/api" + self.path, headers=self.headers)

            self.send_response(res.status_code)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', res.headers['Content-Type'])
            # for h in res.headers:
            #     self.send_header(h, res.headers[h])
            self.end_headers()
            self.wfile.write(res.content)


if __name__ == "__main__":
    sock = HTTPServer(("", int(8000)), Redirect)

    try:
        sock.serve_forever()
    except KeyboardInterrupt:
        sock.socket.close()