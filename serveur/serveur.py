"""test_server

Usage:
    dtb_user.py [--port=<int>]

Options:
    --port=<int>  Port used [default=8000]
"""

import os
import sqlite3
import logging
import json
import bdd
from docopt import docopt
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify

APP = Flask(__name__)


@APP.route('/isalive', methods=['GET'])
def is_alive():
    return Response(status=200)

# message received in json format
@APP.route('/post_json', methods=['POST']) 
def post_json():
    data = request.get_json()
    name = data.get('name', '')
    ip = data.get('ip', '')
    return data

@APP.route('/register',methods=['POST'])
def register():

    payload=request.json
    print("payload:",payload)

    error = None

    code=bdd.bdd_add(payload['name'],payload['pwd'],payload['ip'],payload['key'])
    if code==455:
        error = 'name is empty or incorrect.'
        print("|!| Error ",code,":",error)
        return Response(status=code)

    elif code==456:
        error = 'ip is empty or incorrect.'
        print("|!| Error ",code,":",error)
        return Response(status=code)
    elif code==457:
        error = 'password is empty or incorrect.'
        print("|!| Error ",code,":",error)
        return Response(status=code)

    elif code==458:
        error = 'key is empty or incorrect.'
        print("|!| Error ",code,":",error)
        return Response(status=code)
    elif code==459:
        error = 'Username already used. Choose another.'
        print("|!| Error ",code,":",error)
        return Response(status=code)

    return payload

if __name__ == '__main__':
    ARGS = docopt(__doc__)
    if ARGS['--port']:
        APP.run(host='0.0.0.0', port=ARGS['--port'])
    else:
        logging.error("Wrong command line arguments")
