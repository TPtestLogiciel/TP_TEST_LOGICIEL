"""test_server

Usage:
    test_server.py [--port=<int>]

Options:
    --port=<int>  Port used [default=8000]
"""
import os
import logging
from docopt import docopt
from flask import Flask
from flask import Response
from flask import request
from flask import jsonify




app = Flask(__name__)

# curl -X GET http://localhost:8080/isalive  #pour comm sur port 8080

@app.route('/isalive', methods=['GET'])
def is_alive():
    return Response(status=200)

# @app.route('/user', methods=['POST'])
# def register_user():
#   payload = request.json
#   ret = user.


# curl -i -H "Content-Type: application/json" -X POST -d '{"name":"MrPatapouf", "ip": "0000"}' http://localhost:2000/post_json
# -H : header "Content-Type: application/json", content-type est la cle
# -d : data
# -X : methode de requete (ici POST vu qu'on use http)

# message received in json format
@app.route('/post_json', methods=['POST']) 
def post_json():
    data = request.get_json()
    name = data.get('name', '')
    ip = data.get('ip', '')
    print(data)
    return data


# curl http://localhost:8080/post_dict -d "name=Patachou&ip=0000"

# message received in dict format
@app.route('/post_dict', methods=['POST']) 
def post_dict():
    data = request.form.to_dict(flat=False)
    name = request.form.get('name', '')
    ip = request.form.get('ip', '')
    return data

if __name__ == '__main__':
    ARGS = docopt(__doc__)
    print(ARGS['--port'])
    if ARGS['--port']:
        app.run(host='0.0.0.0', port=ARGS['--port'])
    else:
        logging.error("Wrong command line arguments")