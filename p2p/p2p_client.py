"""p2p_client

Usage:
    p2p_client.py --buddy=<buddy> --port_source=<int> --port_server=<int>

Options:
    -h --help  Show this screen for help
    --buddy=<buddy>  the user we want to talk to
    --port_source=<int>  source port
    --port_server=<int>  source server
"""

import http.client
import json
import threading

from docopt import docopt
from flask import Flask, Response, request

import bdd

app = Flask(__name__)


def input_register(server_ip, server_port, ip, source_port):
    name_user = input("Please enter your username : ")
    pwd = input("Please enter your password : ")
    (msg_received, status, reason) = register(
        server_ip, server_port, ip, source_port, name_user, pwd
    )
    return msg_received, status, reason


def register(server_ip, server_port, ip, source_port, name_user, pwd):
    try:
        conn = http.client.HTTPConnection(server_ip, server_port)
        http_headers = {"Content-Type": "application/json"}
        ip = ip + ":" + str(source_port)
        key = bdd.create_random_string(64)
        data_to_server = {"username": name_user, "pwd": pwd, "ip": ip, "key": key}
        json_data = json.dumps(data_to_server)

        conn.request("POST", "/register", json_data, http_headers)
        server_response = conn.getresponse()
        msg_received = server_response.read().decode()
        server_status = server_response.status
        server_reason = server_response.reason
        return msg_received, server_status, server_reason
    except ConnectionRefusedError:
        print("Failed to connect to {}. Try again later.".format(username))
        return -1, Response(status=503), -1


def get_ip_port(server_ip, server_port, user):
    try:
        conn_server = http.client.HTTPConnection(server_ip, server_port)
        conn_server.request("GET", "/isalive")
        if conn_server.getresponse().status == 200:
            conn_server.request("GET", "/get_ip_port/{}".format(user))

            server_response = conn_server.getresponse()
            msg_received = server_response.read().decode()
            server_status = server_response.status
            server_reason = server_response.reason
            return msg_received, server_status, server_reason
    except ConnectionRefusedError:
        print("Failed to connect to server. Try again later")
        return -1, Response(status=503), -1


def compose_message(target_ip, target_port, user):
    """
    Ask to enter a message as an input to be sent to user.
    """
    while True:
        text_input = input(">> ")
        send_message(text_input, target_ip, target_port, user)


def send_message(message, target_ip, target_port, username):
    """
    Send message to server of username. Return received message by username's
    server, server status and its reason.
    """
    try:
        conn = http.client.HTTPConnection(target_ip, target_port)
        http_headers = {"Content-Type": "application/json"}
        data_to_server = {"username": username, "text": message}
        json_data = json.dumps(data_to_server)

        conn.request("POST", "/p2p_post", json_data, http_headers)
        server_response = conn.getresponse()
        msg_received = server_response.read().decode()
        server_status = server_response.status
        server_reason = server_response.reason
        return msg_received, server_status, server_reason
    except ConnectionRefusedError:
        print("Failed to connect to {}. Try again later.".format(username))
        return -1, Response(status=503), -1


def server(ip_address, local_port, user):
    """
    Create server with ip address and port.
    """
    print("Lauch server :", local_port)
    app.run(host=ip_address, port=local_port)


@app.route("/isalive", methods=["GET"])
def is_alive():
    return Response(status=200)


@app.route("/p2p_post", methods=["POST"])
def p2p_post():
    """
    Receive and display client's message.
    """
    data = request.get_json()
    text = data.get("text", "")
    print("<< {} : {}".format(user, text))
    return data


if __name__ == "__main__":
    ARGS = docopt(__doc__)

    server_ip = "0.0.0.0"
    server_port = ARGS["--port_server"]
    user = ARGS["--buddy"]
    source_ip = "0.0.0.0"
    source_port = ARGS["--port_source"]

    # Register in database via server
    (msg_received, status, reason) = input_register(
        server_ip, server_port, source_ip, source_port
    )
    # Get user ip and port
    (msg_received, status, reason) = get_ip_port(server_ip, server_port, user)
    if status == 200:
        msg_json = json.loads(msg_received)

        target_port = msg_json["port"]
        ip = msg_json["ip"]
        try:
            thread1 = threading.Thread(
                target=compose_message, args=(ip, target_port, user)
            )
            thread2 = threading.Thread(target=server, args=(ip, source_port, user))
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
        except KeyboardInterrupt:
            print("Press Ctrl+C to remove server part")
    else:
        print("Server status : {}".format(status))
