"""server

Usage:
    server.py [--port=<int>]

Options:
    -h --help  Show this screen for help
    --port=<int>  server port [default: 8000]
"""

import http.client
import json
import threading

from docopt import docopt
from flask import Flask, Response, request

app = Flask(__name__)


@app.route("/isalive", methods=["GET"])
def is_alive():
    return Response(status=200)


@app.route("/get_ip_port/<username>", methods=["GET"])
def get_ip_port(username):
    """
    Receive and display client's message.
    """
    # Test isalive du client demande
    # conn_server = http.client.HTTPConnection(server_ip, server_port)
    # conn_server.request("GET", "/isalive")
    ip_address = "0.0.0.0"
    if username == "karine":
        port = 8001
    elif username == "croissant":
        port = 8002
    else:
        return Response(status=503)
    response = {"username": username, "ip_address": ip_address, "port": port}
    return response


if __name__ == "__main__":
    ARGS = docopt(__doc__)
    if ARGS["--port"]:
        app.run(host="0.0.0.0", port=ARGS["--port"])
    else:
        logging.error("Wrong command line arguments")
