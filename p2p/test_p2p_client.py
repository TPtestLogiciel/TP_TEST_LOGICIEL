import http.client
import io

import json
import shlex
import subprocess
import sys
import time
import unittest

import requests
import p2p_client

# Pour generer une cle privé :
# $ openssl genrsa -aes128 -passout pass:<password> -out private.pem 4096

# Pour generer une cle publique a partir de la cle privé
# $ openssl rsa -in private.pem -passin pass:<password> -pubout -out public.pem

# Pour generer un certificat a partir de la cle privé
# $ openssl req -new -x509 -sha256 -key private.pem -out cert.pem -days <int>
# NE PAS OUBLIER DE MODIFIER LES PATH DANS LES VARIABLES


class TestP2PClient(unittest.TestCase):

    certificate_from_air = "cert.pem"  # path du certificat.pem
    private_key = "private.pem"
    password = "azertyuiop"
    certificate2 = "cert2.pem"

    user_subprocess = None
    server_subprocess = None

    username_1 = "Alice"
    username_2 = "Bob"
    port_user_1 = 8001
    port_user_2 = 8002
    msg_from_user_1 = "Hello Bob, it's a message from Alice!"
    msg_json_user_1 = {"username": username_2, "text": msg_from_user_1}
    msg_from_user_2 = "Hi Alice, it's a message from Bob!"
    msg_json_user_2 = {"username": username_1, "text": msg_from_user_2}

    local_ip = "0.0.0.0"
    server_port = 8000
    ip_register = local_ip + ":" + str(port_user_1)
    json_from_server = {
        "username": username_1,
        "ip": local_ip,
        "port": port_user_1,
    }
    pwd_user_1 = "zlldo#58DDZF"
    register_username_1 = {
        "username": username_1,
        "pwd": "zlldo#58DDZF",
        "ip": ip_register,
        "key": "",
    }

    def setUp(self):
        # Launch server subprocess
        print("LAUNCH SERVEUR SUBPROCESS\n")
        cmd_server = "python3 server.py"
        args_server = shlex.split(cmd_server)
        # launch command as a subprocess
        self.server_subprocess = subprocess.Popen(args_server)
        time.sleep(3)

        # Launch client p2p subprocess, Alice user
        print("LAUNCH ALICE SUBPROCESS\n")
        cmd_client = "python3 p2p_client.py --buddy={} --port_source={} --port_server={}".format(
            self.username_2, self.port_user_1, self.server_port
        )
        args_client = shlex.split(cmd_client)
        # launch command as a subprocess
        self.user_subprocess = subprocess.Popen(args_client)
        time.sleep(10)

    def test_register(self):
        (data_send, server_status, server_reason) = p2p_client.register(
            self.local_ip,
            self.server_port,
            self.local_ip,
            self.port_user_1,
            self.username_1,
            self.pwd_user_1,
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["username"], self.register_username_1["username"])
        self.assertEqual(data_send["ip"], self.register_username_1["ip"])
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

    def test_get_ip_port(self):
        (data_send, server_status, server_reason) = p2p_client.get_ip_port(
            self.local_ip, self.server_port, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["username"], self.json_from_server["username"])
        self.assertEqual(data_send["ip"], self.json_from_server["ip"])
        self.assertEqual(data_send["port"], self.json_from_server["port"])
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

    def test_send_message(self):
        # Test Bob's client part, wants to talk to Alice user with a json msg
        (data_send, server_status, server_reason) = p2p_client.send_message(
            self.msg_from_user_2, self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["text"], self.msg_json_user_2["text"])
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertEqual(data_send, self.msg_json_user_2)
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

        # Test response and connection to Alice (server part) with client
        # Bob with an int msg
        (data_send, server_status, server_reason) = p2p_client.send_message(
            123456789, self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertNotEqual(data_send["text"], self.msg_json_user_2["text"])
        self.assertEqual(data_send["text"], 123456789)
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertNotEqual(data_send, self.msg_json_user_2)
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

        # Test response and connection to Alice (server part) with client
        # Bob with an empty string
        (data_send, server_status, server_reason) = p2p_client.send_message(
            "", self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["text"], "")
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

        # Test response and connection to Alice (server part) with client
        # Bob with a dictionnary
        (data_send, server_status, server_reason) = p2p_client.send_message(
            self.msg_json_user_2, self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        dico_msg = {
            "username": self.username_1,
            "text": {"username": self.username_1, "text": self.msg_from_user_2},
        }
        dico_msg = json.dumps(dico_msg)
        dico_msg = json.loads(dico_msg)
        self.assertEqual(data_send["text"], dico_msg["text"])
        self.assertNotEqual(data_send["text"], self.msg_json_user_2["text"])
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertEqual(
            data_send["text"]["username"], self.msg_json_user_2["username"]
        )
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

        # Test response and connection to Alice (server part) with client
        # Bob with a list
        list_msg = ["bonjour", "comment tu vas?", 4, "byebye", 8]
        (data_send, server_status, server_reason) = p2p_client.send_message(
            list_msg, self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["text"], list_msg)
        self.assertEqual(data_send["text"][0], list_msg[0])
        self.assertNotEqual(data_send["text"][2], list_msg[0])
        self.assertEqual(data_send["text"][2], list_msg[2])
        self.assertNotEqual(data_send["text"], self.msg_json_user_2["text"])
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

    def tearDown(self):
        print("killing subprocess user")
        self.user_subprocess.kill()
        self.user_subprocess.wait()
        print("killing subprocess server")
        self.server_subprocess.kill()
        self.server_subprocess.wait()


    # Test de la fonction send_public_key()
    def test_certificate_key(self):

        # Test du fichier envoyé
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        self.assertEqual(
            p2p_client.send_certificate("file_not_found", "0.0.0.0", "8000", "8080"),
            (-1, -1, -1),
        )
        sys.stdout = sys.__stdout__
        self.assertEqual("Error : File does not exist\n", get_printed_output.getvalue())

        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        self.assertEqual(
            p2p_client.send_certificate("p2p_client.py", "0.0.0.0", "8000", "8080"),
            (-1, -1, -1),
        )
        sys.stdout = sys.__stdout__
        self.assertEqual(
            "Error : File is not a certificate\n", get_printed_output.getvalue()
        )

        (dataSend, serverStatus, serverReason) = p2p_client.send_certificate(
            self.certificate_from_air, self.ip, self.portUser2, self.buddyUsr1
        )
        dataSend = json.loads(dataSend)

        # test contenu du fichier
        self.assertEqual(len(dataSend["clef_pub"]), 1428)
        self.assertEqual(dataSend["clef_pub"][:28], "-----BEGIN CERTIFICATE-----\n")
        self.assertEqual((dataSend["clef_pub"][-26:]), "-----END CERTIFICATE-----\n")

    def test_sign_and_verif_message(self):
        # Test message signé et verification de la signature
        (signed_message, sign) = p2p_client.sign_message(
            "Message a signer", self.private_key, self.password
        )
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        p2p_client.verify_sign(signed_message, sign, self.certificate_from_air)
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is signed\n", get_printed_output.getvalue())

        # Test Vérification d'un message non signé et d'une signature random
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        p2p_client.verify_sign("Message non signée", sign, self.certificate_from_air)
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is not signed\n", get_printed_output.getvalue())

        # Test message signé puis modification du message et verification signature
        (signed_message, sign) = p2p_client.sign_message(
            "Nouveau message à signer", self.private_key, self.password
        )
        signed_message += "Modification du message"
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        p2p_client.verify_sign(signed_message, sign, self.certificate_from_air)
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is not signed\n", get_printed_output.getvalue())

        # Test message signé et Vérification avec un autre certificat
        (signed_message, sign) = p2p_client.sign_message(
            "Dernier message a signer", self.private_key, self.password
        )
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        p2p_client.verify_sign(signed_message, sign, self.certificate2)
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is not signed\n", get_printed_output.getvalue())

    def test_sign_and_send_message(self):
        # Test response and connection to server Ground with client
        # Air with a string msg and sign
        (dataSend, serverStatus, serverReason) = p2p_client.sign_and_send_message(
            self.msgFromAir,
            self.private_key,
            self.password,
            self.ip,
            self.portUser2,
            self.buddyUsr1,
        )
        dataSend = json.loads(dataSend)

        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        text = dataSend["text"]
        signature = dataSend["signature"]
        p2p_client.verify_sign(
            dataSend["text"], dataSend["signature"], self.certificate_from_air
        )
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is signed\n", get_printed_output.getvalue())

        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")


if __name__ == "__main__":
    unittest.main()
