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
from docopt import docopt
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify

APP = Flask(__name__)


conn = sqlite3.connect('data.db',check_same_thread=False)
cur = conn.cursor()
sql = "DROP TABLE IF EXISTS bdd"
cur.execute(sql)
conn.commit()

sql = '''CREATE TABLE bdd (
              id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              ip TEXT NOT NULL
       );'''
    
cur.execute(sql)
conn.commit()


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

@APP.route('/nameIp',methods=['POST'])
def nameIp():


if __name__ == '__main__':
    ARGS = docopt(__doc__)
    if ARGS['--port']:
        APP.run(host='0.0.0.0', port=ARGS['--port'])
    else:
        logging.error("Wrong command line arguments")

    cur.close()
    conn.close()
