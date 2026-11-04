from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen

RPC_URL = "http://localhost:8545"


class Handler(SimpleHTTPRequestHandler):

    # ใช้ HTTP/1.0 เพื่อไม่ให้ connection ค้าง
    protocol_version = "HTTP/1.0"

    def do_POST(self):

        if self.path != "/rpc":
            self.send_error(404)
            return

        length = int(
            self.headers.get("Content-Length", "0")
        )

        body = self.rfile.read(length)

        print("RPC request:", body.decode())

        try:
            req = Request(
                RPC_URL,
                data=body,
                headers={
                    "Content-Type": "application/json"
                },
                method="POST"
            )

            with urlopen(req, timeout=5) as response:
                result = response.read()

            print("RPC response:", result.decode())

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.send_header(
                "Content-Length",
                str(len(result))
            )
            self.end_headers()

            self.wfile.write(result)

        except Exception as e:

            print("RPC ERROR:", e)

            result = (
                '{"jsonrpc":"2.0",'
                '"id":null,'
                '"error":{'
                '"code":-32000,'
                '"message":"' + str(e) + '"'
                '}}'
            ).encode()

            self.send_response(500)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.send_header(
                "Content-Length",
                str(len(result))
            )
            self.end_headers()

            self.wfile.write(result)


print("Web server started")
print("Open port 8000 in Codespaces")

server = ThreadingHTTPServer(
    ("0.0.0.0", 8000),
    Handler
)

server.serve_forever()