"""test_server

Usage:
    test_server.py [--port=<int>]

Options:
    --port=<int>  Port used [default=8000]
"""
import os
import logging
import json
import threading
from typing import Text
from docopt import docopt
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify

app = Flask(__name__)
text_input = ''

def server():
    app.run(host='localhost', port=ARGS['--port'])

def input():
    while(True):
        text_input = input('> ')


@app.route('/p2p_get', methods=['GET'])
def p2p_get():
    data = {'text': text_input}
    json_data = json.dumps(data)
    return Response(json_data)
    # return Response(status=200)

@app.route('/p2p_post', methods=['POST']) 
def p2p_post():
    data = request.get_json()
    text = data.get('text', '')
    user = data.get('username', '')
    ip = data.get('ip', '')
    print('< ' + user + ': ' + text)
    return data


thread1 = threading.Thread(target=server)
thread2 = threading.Thread(target=input)

if __name__ == '__main__':
    ARGS = docopt(__doc__)
    print(ARGS['--port'])
    if ARGS['--port']:
        text = input()
        text.start()
        thread1.start()
        # thread2.start()
    else:
        logging.error("Wrong command line arguments")
    