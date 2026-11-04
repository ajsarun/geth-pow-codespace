from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen

RPC_URL = "http://localhost:8545"


class Handler(SimpleHTTPRequestHandler):

    def do_POST(self):

        if self.path != "/rpc":
            self.send_error(404)
            return

        length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(length)

        request = Request(
            RPC_URL,
            data=body,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:

            response = urlopen(request)

            data = response.read()

            self.send_response(response.status)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.end_headers()

            self.wfile.write(data)

        except Exception as error:

            self.send_response(500)

            self.send_header(
                "Content-Type",
                "text/plain"
            )

            self.end_headers()

            self.wfile.write(
                str(error).encode()
            )


print("Web3 Client")

HTTPServer(
    ("0.0.0.0", 8000),
    Handler
).serve_forever()