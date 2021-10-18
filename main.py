import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request

STORAGE_PATH = os.getenv("STORAGE_PATH")

class LFSFileServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            url = "https://raw.githubusercontent.com" + self.path
            resp = urllib.request.urlopen(url)
        except urllib.error.HTTPError as ex:
            traceback.print_exc()
            self.send_response(ex.code)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(ex.msg.encode())
            return
        try:
            sha_line = resp.readlines()[1]
            sha256 = sha_line.decode().lstrip("oid sha256:").rstrip('\n')
        except:
            msg = f"File content under {url} is not a valid LFS description file!"
            print(msg, file=sys.stderr)
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(msg.encode())
            return

        try:
            repo_user, repo_name = self.path.split("/")[1:3]
            # not sure about this part below
            with open(f'{STORAGE_PATH}/{repo_user}/{repo_name}.git/{sha256}', 'rb') as file:
                self.wfile.write(file.read())
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(self.path)}"')
            self.end_headers()
        except:
            traceback.print_exc()
            msg = f"Unable to read a file content for SHA265: {sha256} and path: {self.path}"
            print(msg, file=sys.stderr)
            self.send_response(500, msg)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(msg.encode())


myServer = HTTPServer(('0.0.0.0', 8080), LFSFileServer)
myServer.serve_forever()
myServer.server_close()