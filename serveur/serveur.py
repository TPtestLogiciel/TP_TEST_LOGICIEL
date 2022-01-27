"""test_server

Usage:
    dtb_user.py [--port=<int>]

Options:
    --port=<int>  Port used [default=8000]
"""

import json
import logging
import os
import sqlite3

from docopt import docopt
from flask import Flask, Response, jsonify, request

import bdd

APP = Flask(__name__)


@APP.route("/isalive", methods=["GET"])
def is_alive():
    return Response(status=200)


# message received in json format
@APP.route("/post_json", methods=["POST"])
def post_json():
    data = request.get_json()
    name = data.get("name", "")
    ip = data.get("ip", "")
    return data


@APP.route("/register", methods=["POST"])
def register():

    payload = request.json
    print("payload:", payload)

    error = None

    if len(payload) != 4:
        error = "field(s) missing."
        print("|!| Error 454 :", error)
        return Response(status=454)

    code = bdd.bdd_add("data.db",
        payload["username"], payload["pwd"], payload["ip"], payload["key"]
    )

    if code == 455:
        error = "username is empty or incorrect."
        print("|!| Error ", code, ":", error)
        return Response(status=code)

    elif code == 456:
        error = "ip is empty or incorrect."
        print("|!| Error ", code, ":", error)
        return Response(status=code)
    elif code == 457:
        error = "password is empty or incorrect."
        print("|!| Error ", code, ":", error)
        return Response(status=code)

    elif code == 458:
        error = "key is empty or incorrect."
        print("|!| Error ", code, ":", error)
        return Response(status=code)
    elif code == 459:
        error = "Username already used. Choose another."
        print("|!| Error ", code, ":", error)
        return Response(status=code)

    return payload


@APP.route("/get_ip_port/<username>", methods=["GET"])
def get_ip_port(username):
    """
    Receive and display client's message.
    """
    print("username in get_ip_port : ", username)
    (ip, port) = bdd.bdd_get_ip_port("data.db",username)
    if (ip, port) != (False, False):
        response = {"username": username, "ip": ip, "port": port}
    else:
        return Response(status=503)

    return response


if __name__ == "__main__":
    ARGS = docopt(__doc__)
    if ARGS["--port"]:
        bdd.bdd_creation("data.db")
        bdd.bdd_add("data.db",
                "Maurice",
                "aAaa#a9aa",
                "0.0.0.0:6840",
                bdd.create_random_string(64))
        APP.run(host="0.0.0.0", port=ARGS["--port"])
    else:
        logging.error("Wrong command line arguments")
