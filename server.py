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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT, PATCH, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Headers", "csrf-token")
        self.send_header("Access-Control-Request-Method", "*")

        self.end_headers()

    def do_POST(self):
        self.do_REQUEST()

    def do_GET(self):

        self.do_REQUEST()

    def do_REQUEST(self):

        content_len = self.headers.get('Content-Length')

        req_cookies = dict(SimpleCookie(self.headers.get('Cookie')))
        req_headers = dict()
        req_data = self.rfile.read(int(content_len)) if content_len else None

        # req_headers.pop()


        # if self.headers.get('csrf-token'): 
        #     headers['csrf-token'] = self.headers.get('csrf-token')
        
        res_data = None
        res_headers = {'Access-Control-Allow-Origin': '*'}
        res_code = 200

        try:
            with httpx.Client(http2=True) as client:
                res = client.request(method=self.command, url="https://www.animeworld.so/api" + self.path, headers=req_headers, cookies=req_cookies, content=req_data)
                res_data = res.content
                
                self.send_response(res.status_code)
                for h in res.headers:
                    if h == "content-encoding": continue
                    res_headers[h] = res.headers[h]
                    # self.send_header(h, res.headers[h])
                    
                # self.send_header('Content-Type', res.headers['Content-Type'])
        except httpx.ReadTimeout:
            self.send_response('403')
        finally:
            for h in res_headers:
                self.send_header(h, res_headers[h])
            self.end_headers()

            if res_data: self.wfile.write(res_data)
            

if __name__ == "__main__":
    sock = HTTPServer(("", int(8000)), Redirect)

    try:
        sock.serve_forever()
    except KeyboardInterrupt:
        sock.socket.close()