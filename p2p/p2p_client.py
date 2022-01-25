"""p2p_client

Usage:
    p2p_client.py --buddy=<buddy> [--ip=<ip>] [--port_dest=<int>] [--port_source=<int>]

Options:
    -h --help  Show this screen for help
    --buddy=<buddy>  buddy username
    --ip=<ip>  ip used [default: 0.0.0.0]
    --port_dest=<int>  port destinataire [default: 8080]
    --port_source=<int>  port source [default: 8000]
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


app = Flask(__name__)
# app.debug = True


def send_message(message, target_ip, target_port, username):
    """
    Arguments : message a envoyer, l'adresse IP du destinataire,
    le port du destinataire et son username.
    - Creation d'une connexion HTTP avec l'IP et le port destinataire
    - Envoi d'un JSON avec l'username du destinataire et le coeur
    du message
    - Requete POST a la partie serveur du destinataire
    - Recupere les reponses de la partie serveur du destinataire
    Retourne le message recu par le serveur, le status du serveur et
    la raison associee.
    """
    # print("-- post function called --")
    try:
        conn = http.client.HTTPConnection(target_ip, target_port)
        headers = {"Content-Type": "application/json"}
        dataToServer = {"username": username, "text": message}
        jsonData = json.dumps(dataToServer)
        print(jsonData)

        conn.request("POST", "/p2p_post", jsonData, headers)
        response = conn.getresponse()
        msgReceived = response.read().decode()
        serverStatus = response.status
        serverReason = response.reason
        return msgReceived, serverStatus, serverReason
    except ConnectionRefusedError:
        print("Failed to connect to server. Try again later.")
        return -1, -1, -1


def compose_message(target_ip, target_port, user):
    """
    Arguments : adresse IP du destinataire, le port du destinataire,
    username du destinataire
    Demande a l'utilisateur un message en input pour envoyer au
    destinataire.
    """
    while True:
        text_input = input(">> ")
        (data_send, server_status, server_reason) = send_message(
            text_input, target_ip, target_port, user
        )


def server(ipaddress, local_port, user):
    """
    Creer un serveur avec une adresse ip et un port passes en
    arguments
    """
    app.run(host=ipaddress, port=local_port)


@app.route("/p2p_post", methods=["POST"])
def p2p_post():
    """
    Recoit le message d'un client et l'affiche dans la console
    """
    data = request.get_json()
    text = data.get("text", "")
    ip = data.get("ip", "")
    print("<< {} : {}".format(user, text))
    return data


if __name__ == "__main__":
    ARGS = docopt(__doc__)

    user = ARGS["--buddy"]
    target_ip = ARGS["--ip"]
    target_port = ARGS["--port_dest"]
    ip = ARGS["--ip"]
    source_port = ARGS["--port_source"]
    try:
        thread1 = threading.Thread(
            target=compose_message, args=(target_ip, target_port, user)
        )
        thread2 = threading.Thread(target=server, args=(ip, source_port, user))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
    except KeyboardInterrupt:
        print("Press Ctrl+C to remove server part")
