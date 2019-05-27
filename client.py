#!/usr/bin/python3

import webbrowser
import sys
from http.server import HTTPServer,BaseHTTPRequestHandler
import io,shutil,urllib
import json
import subprocess
import os
import websocket

cfg = {}

def is_json(str):
    try:
        json.loads(str)
    except ValueError:
        return False
    return True

def ws_send(ws, op, data):
    global cfg
    ws.send(json.dumps({'op': op, 'data': data}))

def on_message(ws, message):
    print("Got new message from server.")
    global cfg
    res = json.loads(message)
    if res['status'] == "win" or res['status'] == "lose" or res['status'] == "draw":
        print("The result is " + res['status'] + ".")
        sys.exit(0)
    elif res['status'] == "error":
        print("Your token is invalid.")
        sys.exit(0)
    elif res['status'] == "wrong":
        print("Your AI application output a invaild result!")
        print("You may have to edit your AI application.")
        os.system("pause")
    print("It's your turn.")
    while True:
        print("Running your AI application.")
        sp = subprocess.Popen([cfg['path'], res['data']], stdout=subprocess.PIPE)
        dat = sp.stdout.readline()
        if is_json(dat):
            break
        print("Your AI application output a wrong JSON string. Please check your application.")
        os.system("pause")
    print("Send your solution to server.")
    ws_send(ws, 'operation', dat)
    print("Waiting for others' turn.")

def on_error(ws, error):
    print("Something Wrong Happened: ", end='.')
    print(error)
    print("Please check your configuraion or network.")
    sys.exit(0)

def on_close(ws):
    print("Connection Closed.")
    sys.exit(0)

def on_open(ws):
    print("Connect successful.")
    print("Send prepare message to server.")
    ws_send(ws, "prepare", {})
    print("Waiting for server response.")

def main():

    global cfg
    URL = cfg['url']
    PTH = cfg['path']

    if not os.path.exists(PTH):
        print("AI application not exists.")
        sys.exit(0)

    print("Connecting to server " + URL + ".")
    ws = websocket.WebSocketApp(URL, on_message = on_message, on_error = on_error, on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

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
        global cfg
        html = '<p class="title">Success!</p><p class="title">Please check in command line window,</p><p class="title">and watch the game in the webbrowser.</p>'.encode("UTF-8")
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.send_header('Content-length', len(html))
        self.end_headers()
        self.wfile.write(html)
        data = urllib.parse.parse_qs(urllib.parse.unquote(str(self.rfile.readline(), 'UTF-8')))
        cfg = {'url': data['url'][0], 'path': data['path'][0].replace("file://", "")}
        main()
        sys.exit(0)
        httpd.shutdown()
        httpd.server_close()

httpd = HTTPServer(('', 8080), MyHttpHandler)
webbrowser.open('http://localhost:8080')
httpd.serve_forever()