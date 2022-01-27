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
# app.debug = True


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
        headers = {"Content-Type": "application/json"}
        message_signe, signature = sign_message(message, private_key, password)

        dataToServer = {
            "username": username,
            "text": message_signe,
            "signature": signature,
        }
        jsonData = json.dumps(dataToServer)
        print(jsonData)
        conn.request("POST", "/p2p_post_and_sign", jsonData, headers)
        response = conn.getresponse()
        msgReceived = response.read().decode()
        serverStatus = response.status
        serverReason = response.reason
        return msgReceived, serverStatus, serverReason
    except ConnectionRefusedError:
        print("Failed to connect to server. Try again later.")
        return -1, -1, -1


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
