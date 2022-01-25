"""p2p_client

Usage:
    p2p_client.py --buddy=<buddy> [--ip=<ip>] --port_dest=<int> --port_source=<int>

Options:
    -h --help  Show this screen for help
    --buddy=<buddy>  buddy username
    --ip=<ip>  ip used [default: 0.0.0.0]
    --port_dest=<int>  port destinataire
    --port_source=<int>  port source
"""

import http.client
import json
import threading

from docopt import docopt
from flask import Flask, request

app = Flask(__name__)


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
        print(json_data)

        conn.request("POST", "/p2p_post", json_data, http_headers)
        server_response = conn.getresponse()
        msg_received = server_response.read().decode()
        server_status = server_response.status
        server_reason = server_response.reason
        return msg_received, server_status, server_reason
    except ConnectionRefusedError:
        print("Failed to connect to server. Try again later.")
        return -1, -1, -1


def compose_message(target_ip, target_port, user):
    """
    Ask to enter a message as an input to be sent to user.
    """
    while True:
        text_input = input(">> ")
        send_message(text_input, target_ip, target_port, user)


def server(ip_address, local_port, user):
    """
    Create server with ip address and port.
    """
    app.run(host=ip_address, port=local_port)


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

    user = ARGS["--buddy"]
    target_port = ARGS["--port_dest"]
    source_port = ARGS["--port_source"]
    ip_address = ARGS["--ip"]
    try:
        thread1 = threading.Thread(
            target=compose_message, args=(ip_address, target_port, user)
        )
        thread2 = threading.Thread(target=server, args=(ip_address, source_port, user))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except KeyboardInterrupt:
        print("Press Ctrl+C to remove server part")
