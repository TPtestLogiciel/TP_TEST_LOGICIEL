"""test_server

Usage:
    p2p_client.py [options]

Options:
    --ip=<ip>
    --port_dest=<int>
    --port_source=<int>
    --buddy=<buddy>
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

buddy = ""
user = ""
target_ip = ""
# thread_continue = True

app = Flask(__name__)

def handle_message(user, message):
    logging.info('[MESSAGE]' + user + " : " + message)

def send_message(message):
    # string1 = "http://"+target_ip+"/p2p_post"
    # print(string1)
    # req = requests.post('http://'+target_ip+'/p2p_post', json={"username": user, "message": message})
    print("-- post function called --")
    headers = {'Content-Type': 'application/json'}
    data = {'username': user, 'text': message}
    json_data = json.dumps(data)
    print(json_data)
    conn.request('POST', '/p2p_post', json_data, headers)

def compose_message():
    while(True):
        text_input = input('> ')
        send_message(text_input)

    # send_message("test")

    # for line in sys.stdin:
    #     logging.debug("message to send :" + line)
    #     print("message to send " + line)
    #     send_message(buddy, line)
    #     if not thread_continue:
    #         break

def server(ipaddress, local_port):
    app.run(host=ipaddress, port=local_port)

@app.route('/p2p_post', methods=['POST']) 
def p2p_post():
    # handle_message(flask_request.json['user'].request.json['message'])
    # return Response(status=404)
    data = request.get_json()
    text = data.get('text', '')
    user = data.get('username', '')
    ip = data.get('ip', '')
    print('< ' + user + ': ' + text)
    return data

if __name__ == '__main__':
    ARGS = docopt(__doc__)
    if ARGS['--ip'] and ARGS['--port_dest'] and ARGS['--port_source'] and ARGS['--buddy']:
        user = ARGS['--buddy']
        target_ip = ARGS['--ip']
        target_port = ARGS['--port_dest']
        local_ip = '0.0.0.0'
        local_port = ARGS['--port_source']
        conn = http.client.HTTPConnection(target_ip, target_port)
        thread1 = threading.Thread(target=compose_message)
        thread2 = threading.Thread(target=server, args=(local_ip,local_port,))
        thread1.start()
        thread2.start()
        
    else:
        logging.error("Wrong command line arguments")

    # thread_continue = False
    # thread1.join()