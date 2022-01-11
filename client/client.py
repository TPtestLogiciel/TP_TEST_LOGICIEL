"""test_p2p_client

Usage:
    test_p2p_client.py --ip=<ip> --port=<int> --buddy=<buddy>

Options:
    -h --help  Show this screen.
    --ip=<ip>  ip used [default=0.0.0.0]
    --port=<int>  port used
    --buddy=<buddy>  username of the person we want to talk with
"""

import os
import logging
from docopt import docopt
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
import http.client
import json


def send_message(ip, port, message):
    print("in send_message")
    conn = http.client.HTTPConnection(ip, port)

    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(message)

    conn.request('POST', '/post_json', json_data, headers)

    response = conn.getresponse()
    data_send = response.read().decode()
    server_status = response.status
    server_reason = response.reason
    print("Data", data_send)
    print("status", server_status)
    print("reason", server_reason)
    return data_send, server_status, server_reason


# def receive_message(ip, port):
#   print("in receive_message")
#   conn = http.client.HTTPConnection(ip, port)

#   headers = {'Content-Type': 'application/json'}

#   # foo = {'name': 'Hello HTTP #1 cool, and #1!'}
#   json_data = json.dumps(message)

#   print(headers)
#   print('json_data:' + json_data)

#   conn.request('POST', '/post_json', json_data, headers)

#   response = conn.getresponse()
#   print(response.read().decode())
#   print("Status: {} and reason: {}".format(response.status, response.reason))


def main(ARGS):
    print(ARGS['--port'])
    print(ARGS['--buddy'])
    print(ARGS['--ip'])
    choice_user = input("Send message : 0; receive message: 1; Quit chat: quit\n")
    while (choice_user != "quit"):
        print("in while")
        if (choice_user == "0"):
            print("in if 0")
            username = ARGS.get('--buddy', '')
            print(username)
            msg_to_send = input("Enter message to send to {}: ".format(username))
            msg_json = {'username': username, 'message': msg_to_send}
            send_message(ARGS['--ip'], ARGS['--port'], msg_json)
            choice_user = input("Send message : 0; receive message: 1; Quit chat: quit\n")
        else:
            break


if __name__ == '__main__':
    ARGS = docopt(__doc__)

    if ARGS['--port'] and ARGS['--ip']:
        main(ARGS)
    else:
        logging.error("Wrong command line arguments")
