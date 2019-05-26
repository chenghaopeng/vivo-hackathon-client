#!/usr/bin/python3

import webbrowser
import sys
from http.server import HTTPServer,BaseHTTPRequestHandler
import io,shutil,urllib

import game

class MyHttpHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # do nothing to avoid output
        pass

    def __readHtml(self, htmlname):
        file = open(htmlname, 'r')
        html = "\n".join(file.readlines())
        file.close()
        return html.encode("UTF-8")

    def do_GET(self):
        html = self.__readHtml('index.html')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(html)
    
    def do_POST(self):
        global httpd
        html = '<p class="title">Success!</p><p class="title">Please check in command line window.</p>'.encode("UTF-8")
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.send_header('Content-length', len(html))
        self.end_headers()
        self.wfile.write(html)
        data = urllib.parse.parse_qs(urllib.parse.unquote(str(self.rfile.readline(), 'UTF-8')))
        # print(data)
        # game.cfg = {'url': data['url'][0], 'token': data['token'][0], 'path': data['path'][0].replace("file://", "")}
        game.cfg = {'url': data['url'][0], 'path': data['path'][0].replace("file://", "")}
        game.main()
        sys.exit(0)
        httpd.shutdown()
        httpd.server_close()

httpd = HTTPServer(('', 8080), MyHttpHandler)
webbrowser.open('http://localhost:8080')
httpd.serve_forever()