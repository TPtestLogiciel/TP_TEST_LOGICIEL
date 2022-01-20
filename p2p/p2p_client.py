"""test_server

Usage:
    p2p_client.py [--ip=<ip>] [--port_dest=<int>] [--port_source=<int>] --buddy=<buddy>

Options:
    -h --help  Show this screen for help
    --ip=<ip>  ip used [default: 0.0.0.0]
    --port_dest=<int>  port destinataire [default: 8080]
    --port_source=<int>  port source [default: 8000]
    --buddy=<buddy>  buddy username
"""

import sys
import logging
import threading
from docopt import docopt
from flask import Flask
from flask import Response
from flask import request
import http.client
import json


app = Flask(__name__)
# app.debug = True


def handle_message(user, message):
    logging.info('[MESSAGE]' + user + " : " + message)


def send_message(message, target_ip, target_port, user):
    print("-- post function called --")
    conn = http.client.HTTPConnection(target_ip, target_port)    
    headers = {'Content-Type': 'application/json'}
    data = {'username': user, 'text': message}
    json_data = json.dumps(data)
    print(json_data)
    
    conn.request('POST', '/p2p_post', json_data, headers)
    response = conn.getresponse()
    data_send = response.read().decode()
    server_status = response.status
    server_reason = response.reason
    return data_send, server_status, server_reason


def compose_message(target_ip, target_port, user):
    print("In compose_message (thread1)")
    while(True):
        text_input = input('>> ')
        print("text ", text_input)
        if text_input == 'quit':
            break
        data_send, server_status,server_reason = send_message(text_input, target_ip, target_port, user)


def server(ipaddress, local_port, user):
    app.run(host=ipaddress, port=local_port)


@app.route('/p2p_post', methods=['POST']) 
def p2p_post():
    data = request.get_json()
    text = data.get('text', '')
    ip = data.get('ip', '')
    print("<< {} : {}".format(user, text))
    return data


if __name__ == '__main__':
    ARGS = docopt(__doc__)

    user = ARGS['--buddy']
    target_ip = ARGS['--ip']
    target_port = ARGS['--port_dest']
    ip = ARGS['--ip']
    source_port = ARGS['--port_source']

    thread1 = threading.Thread(target=compose_message, args=(target_ip, target_port, user))
    thread2 = threading.Thread(target=server, args=(ip, source_port, user))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

