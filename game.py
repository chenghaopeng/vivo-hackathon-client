import json
import sys
import json
import subprocess
import os
import websocket
import time

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
    sys.exit(0)

def on_close(ws):
    print("Connection Closed.")
    sys.exit(0)

def on_open(ws):
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
    print("Connect successful.")
    ws.run_forever()