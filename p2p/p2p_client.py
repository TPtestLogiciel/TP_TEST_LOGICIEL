"""p2p_client

Usage:
    p2p_client.py --port_source=<int> --port_server=<int>

Options:
    -h --help  Show this screen for help
    --port_source=<int>  source port
    --port_server=<int>  source server
"""

import base64
import hashlib
import http.client
import json
import logging
import os
import sys
import threading

import OpenSSL
from docopt import docopt
from flask import Flask, Response, request
from OpenSSL import crypto


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
        key_name = input("Donner la clé:")

        if os.path.exists(key_name):
            last_four_char = key_name[-4:]
            if last_four_char == ".pem":
                key_file = open(key_name, mode="r")
                key_content = key_file.read()
                key_file.close()
            else:
                print("Error : File is not a key")
        else:
            print("Error : File does not exist")
        key=key_content

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


def send_certificate(certificate, target_ip, target_port, username):
    """
    Arguments : certificate a envoyer (.pem), l'adresse IP du destinataire,
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

    if os.path.exists(certificate):
        last_four_char = certificate[-4:]
        if last_four_char == ".pem":
            certificate_file = open(certificate, mode="r")
            certificate_content = certificate_file.read()
            certificate_file.close()
        else:
            print("Error : File is not a certificate")
            return -1, -1, -1
    else:
        print("Error : File does not exist")
        return -1, -1, -1

    try:
        conn = http.client.HTTPConnection(target_ip, target_port)
        headers = {"Content-Type": "application/json"}
        dataToServer = {"username": username, "clef_pub": certificate_content}
        jsonData = json.dumps(dataToServer)

        conn.request("POST", "/p2p_post_key", jsonData, headers)
        response = conn.getresponse()
        msgReceived = response.read().decode()
        serverStatus = response.status
        serverReason = response.reason
        return msgReceived, serverStatus, serverReason
    except ConnectionRefusedError:
        print("Failed to connect to server. Try again later.")
        return -1, -1, -1


def sign_message(message, private_key, password):
    """
    Arguments : le message à signer (string)
                la private key pour signer le message(path)
                le password utiliser lors de la génération de la clé
    -Lire le contenue de la private_key
    -Charger la private key
    -Signer le message avec la private key

    Retourne : Le message signée (bytes) et la signature généré (bytes)
                -1,-1 en cas d'erreur
    """
    if os.path.exists(private_key):
        last_four_char = private_key[-4:]
        if last_four_char == ".pem":
            key_file = open(private_key, mode="r")
            key_content = key_file.read()
            key_file.close()
        else:
            print("Error : File is not a Private Key")
            return -1, -1
    else:
        print("Error : File does not exist")
        return -1, -1

    pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key_content, password.encode())

    bytes_message = message.encode()
    signature = crypto.sign(pkey, bytes_message, "sha256")
    signature_b64 = base64.b64encode(signature)
    signature_b64_string = signature_b64.decode()
    message = bytes_message.decode()
    return message, signature_b64_string


def verify_sign(message, signature_b64_string, certificate):
    """
    Arguments : le message signé à vérifier (string)
                lal signature du message(b64_string)
                le certificate pour vérifier la signature (path)
    -Lire le contenue du certificate
    -Charger le certificate
    -Vérification de la signature

    Retourne : -1,-1 en cas d'erreur
                0,0 Avec si le message à été signer ou non
    """
    if os.path.exists(certificate):
        last_four_char = certificate[-4:]
        if last_four_char == ".pem":
            certificate_file = open(certificate, mode="rb")
            certificate_content = certificate_file.read()
            certificate_file.close()
        else:
            print("Error : File is not a Certificate")
            return -1, -1
    else:
        print("Error : File does not exist")
        return -1, -1

    cert = crypto.load_certificate(crypto.FILETYPE_PEM, certificate_content)

    signature_b64 = signature_b64_string.encode()
    signature = base64.b64decode(signature_b64)
    bytes_message = message.encode()
    try:
        OpenSSL.crypto.verify(cert, signature, bytes_message, "sha256")
        message = bytes_message.decode()
        print("Message is signed")
    except:
        message = bytes_message.decode()
        print("Message is not signed")
    return 0, 0


def sign_and_send_message(
    message, private_key, password, target_ip, target_port, username
):
    """
    Arguments : message a envoyer,
                la clé privé pour signer le message
                le password de la clé privé
                l'adresse IP du destinataire,
                le port du destinataire et son username.
    - Creation d'une connexion HTTP avec l'IP et le port destinataire
    - Envoi d'un JSON avec l'username du destinataire, le coeur
    du message, et la signature
    - Requete POST a la partie serveur du destinataire
    - Recupere les reponses de la partie serveur du destinataire
    Retourne le message recu par le serveur, le status du serveur et
    la raison associee.
    """
    # print("-- post function called --")
    try:
        conn = http.client.HTTPConnection(target_ip, target_port)
        http_headers = {"Content-Type": "application/json"}
        message_signe, signature = sign_message(message, private_key, password)

        dataToServer = {
            "username": username,
            "text": message_signe,
            "signature": signature,
        }
        json_data = json.dumps(data_to_server)
        conn.request("POST", "/p2p_post_and_sign", json_data, http_headers)
        server_response = conn.getresponse()
        msg_received = server_response.read().decode()
        server_status = server_response.status
        server_reason = server_response.reason
        return msg_received, server_status, server_reason
    except ConnectionRefusedError:
        print("Failed to connect to server. Try again later.")
        return -1, -1, -1


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


def server(ipaddress, local_port):
    """
    Creer un serveur avec une adresse ip et un port passes en
    arguments
    """
    app.run(host=ipaddress, port=local_port)

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


@app.route("/p2p_post_key", methods=["POST"])
def p2p_post_key():
    """
    Recoit le message d'un client et l'affiche dans la console
    """
    data = request.get_json()
    clef_publique = data.get("clef_pub", "")
    print("<< {} : {}".format(user, clef_publique))
    return data


@app.route("/p2p_post_and_sign", methods=["POST"])
def p2p_post_and_sign():
    """
    Recoit le message d'un client et l'affiche dans la console
    """
    data = request.get_json()
    text = data.get("text", "")
    signature = data.get("signature", "")
    print("<< {} : {}".format(user, text, signature))
    return data

if __name__ == "__main__":
    ARGS = docopt(__doc__)

    server_ip = "0.0.0.0"
    server_port = ARGS["--port_server"]
    source_ip = "0.0.0.0"
    source_port = ARGS["--port_source"]

    # Register in database via server
    (msg_received, status, reason) = input_register(
        server_ip, server_port, source_ip, source_port
    )
    user = input("Who you want to talk to? Enter its username: ")
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
