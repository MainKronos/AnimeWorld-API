import httpx
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie

# sudo ./main.py 80 http://jenkins.example.com:8080/

# ssh -R 80:localhost:8080 localhost.run

URL = "https://www.animeworld.so/api"

class Redirect(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Credentials','true')
        self.send_header('Access-Control-Allow-Origin', self.headers.get('Origin'))
        self.send_header('Access-Control-Allow-Headers','Cookie, Csrf-Token, Origin, Content-Type, Accept, Authorization, X-Request-With, Set-Cookie, Cookie, Bearer');
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_POST(self):
        self.do_REQUEST()

    def do_GET(self):

        self.do_REQUEST()


    def do_REQUEST(self):

        content_len = self.headers.get('Content-Length')

        req_cookies = {k: v.value for k, v in SimpleCookie(self.headers.get('Cookie')).items()}
        req_headers = dict()
        req_data = self.rfile.read(int(content_len)) if content_len is not None else None



        if self.headers.get('Csrf-Token'): 
            req_headers['Csrf-Token'] = self.headers.get('Csrf-Token')
        
        res_data = None
        res_headers = {
            'Access-Control-Allow-Origin': self.headers.get('Origin'),
            'Access-Control-Allow-Credentials': 'true'
        }
        res = None
        try:
            with httpx.Client(http2=True) as client:
                res = client.request(method=self.command, url="https://www.animeworld.so" + self.path, headers=req_headers, cookies=req_cookies, content=req_data)
                res_data = res.content
                
                self.send_response(res.status_code)
                for h in res.headers:
                    if h == "content-encoding": continue
                    res_headers[h] = res.headers[h]
                    # self.send_header(h, res.headers[h])
                    
                # self.send_header('Content-Type', res.headers['Content-Type'])
        except httpx.ReadTimeout:
            self.send_response(403)
        finally:
            for h in res_headers:
                self.send_header(h, res_headers[h])
            self.end_headers()

            if res_data: self.wfile.write(res_data)
            

if __name__ == "__main__":
    sock = ThreadingHTTPServer(("", int(8000)), Redirect)

    try:
        sock.serve_forever()
    except KeyboardInterrupt:
        sock.socket.close()