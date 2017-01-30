import click
import http.server
import os
import pathlib
import socketserver


class MagicHTMLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.rewrite_endpoint()
        return super().do_GET()

    def rewrite_endpoint(self):
        path = self.translate_path(self.path)
        new_path = self.path
        if os.path.exists(path + ".html"):
            new_path += ".html"
        elif os.path.exists(path + "/index.html"):
            new_path += "/index.html"
        else:
            return
        print("REWROTE {} => {}".format(self.path, new_path))
        # noinspection PyAttributeOutsideInit
        self.path = new_path


@click.command("serve")
@click.option("--root", required=True, help="Directory to serve")
@click.option("--port", default=8020, type=int, help="Port to serve on")
def main(root: str, port: str):
    root = pathlib.Path(root).expanduser().resolve()
    os.chdir(str(root))
    handler = MagicHTMLHandler
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("", port), handler)
    print("Serving CONSOLE on {}".format(port))
    httpd.serve_forever()
