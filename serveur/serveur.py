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
   # if request.method == 'POST':
    payload=request.json
    print("payload:",payload)
    # name = request.form['name']
    # ip = request.form['ip']
    # db = "data.db"
    
    # name =payload['name']
    error = None
    code=None
    if not payload['name']:
        code="455"
        error = 'name is required.'
        print("|!| Error: ",code,error)
        # return code
        return Response(status=code)
    elif not payload['ip']:
        code="456"
        error = 'ip is required.'
        print("|!| Error: ",code,error)
        # return code
        return Response(status=code)
    elif cur.execute(
        'SELECT id FROM bdd WHERE name = ?', (payload['name'],)
    ).fetchone() is not None:
        code="457"
        error = 'User {} is already registered.'.format(name)
        print("Error",code,error)
        # return code
        return Response(status=code)

    if error is None:
        cur.execute(
            'INSERT INTO bdd (name, ip) VALUES (?, ?)',
            (payload['name'], payload['ip'])
        )
        conn.commit()
    return payload

if __name__ == '__main__':
    ARGS = docopt(__doc__)
    if ARGS['--port']:
        APP.run(host='0.0.0.0', port=ARGS['--port'])
    else:
        logging.error("Wrong command line arguments")

    cur.close()
    conn.close()
