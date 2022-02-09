import http.client
import io
import json
import os
import shlex
import subprocess
import sys
import time
import unittest
from unittest.mock import MagicMock, patch

import requests

import p2p_client

# To generate a private key:
# $ openssl genrsa -aes128 -passout pass:<password> -out private.pem 4096

# To generate a public key from a private key:
# $ openssl rsa -in private.pem -passin pass:<password> -pubout -out public.pem

# To generate certificat from a private key:
# $ openssl req -new -x509 -sha256 -key private.pem -out cert.pem -days <int>
# NE PAS OUBLIER DE MODIFIER LES PATH DANS LES VARIABLES
# DO NOT FORGET TO MODIFIED PATH IN VARIABLES
# key_password is password used to generate keys !!!!!


class TestP2PClient(unittest.TestCase):
    certificate1 = "cert.pem"  # path certificat.pem
    certificate2 = "cert2.pem"
    private_key = "private.pem"
    key_password = "azertyuiop"

    server_subprocess = None

    username_1 = "Alice"
    username_2 = "Bob"
    port_user_1 = "8001"
    port_user_2 = "8002"
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
    signature = "oui"

    def setUp(self):
        # Launch server subprocess
        print("LAUNCH SERVEUR SUBPROCESS\n")
        cmd_server = "python3 ../serveur/serveur.py --port={}".format(self.server_port)
        args_server = shlex.split(cmd_server)
        # launch command as a subprocess
        self.server_subprocess = subprocess.Popen(args_server)
        time.sleep(1)

    def tearDown(self):
        print("killing subprocess server")
        self.server_subprocess.kill()
        self.server_subprocess.wait()

    def test_register(self):
        print("TEST REGISTER\n")
        if os.path.exists(self.certificate1):
            last_four_char = self.certificate1[-4:]
            if last_four_char == ".pem":
                key_file = open(self.certificate1, mode="r")
                key_content = key_file.read()
                key_file.close()
            else:
                print("Error : File is not a key")
        else:
            print("Error : File does not exist")
        (data_send, server_status, server_reason) = p2p_client.register(
            self.local_ip,
            self.server_port,
            self.local_ip,
            self.port_user_1,
            self.username_1,
            self.pwd_user_1,
            key_content,
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["username"], self.register_username_1["username"])
        self.assertEqual(data_send["ip"], self.register_username_1["ip"])
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

    def test_get_ip_port(self):
        print("TEST GET_IP_PORT\n")
        # Register username_1
        if os.path.exists(self.certificate1):
            last_four_char = self.certificate1[-4:]
            if last_four_char == ".pem":
                key_file = open(self.certificate1, mode="r")
                key_content = key_file.read()
                key_file.close()
            else:
                print("Error : File is not a key")
        else:
            print("Error : File does not exist")
        (data_send, server_status, server_reason) = p2p_client.register(
            self.local_ip,
            self.server_port,
            self.local_ip,
            self.port_user_1,
            self.username_1,
            self.pwd_user_1,
            key_content,
        )
        # Test get_ip_port result
        (data_send, server_status, server_reason) = p2p_client.get_ip_port(
            self.local_ip, self.server_port, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["username"], self.json_from_server["username"])
        self.assertEqual(data_send["ip"], self.json_from_server["ip"])
        self.assertEqual(data_send["port"], self.json_from_server["port"])
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

    @patch("http.client.HTTPResponse")
    def test_send_message_msg_str(self, mock_response):
        print("TEST SEND_MESSAGE WITH STR MSG\n")
        # username_2's client part (Bob) send message to username_1's server part (Alice).
        expected_json_msg = {"username": self.username_1, "text": self.msg_from_user_2}
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value.decode.return_value = expected_json_msg

        with patch("http.client.HTTPConnection") as HTTPConnectionMock:
            conn_server = HTTPConnectionMock()

            with patch.object(
                conn_server, "getresponse", return_value=mock_response
            ) as response:
                (msg_received, server_status, server_reason) = p2p_client.send_message(
                    self.msg_from_user_2,
                    self.local_ip,
                    self.port_user_1,
                    self.username_1,
                )
                self.assertEqual(msg_received, expected_json_msg)
                self.assertEqual(server_status, 200)
                self.assertEqual(server_reason, "OK")

    @patch("http.client.HTTPResponse")
    def test_send_message_msg_int(self, mock_response):
        print("TEST SEND_MESSAGE WITH INT MSG\n")
        # Test response and connection to Alice (server part) with client
        # Bob with an int msg
        int_msg = 123456789
        expected_json_msg = {"username": self.username_1, "text": int_msg}
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value.decode.return_value = expected_json_msg

        with patch("http.client.HTTPConnection") as HTTPConnectionMock:
            conn_server = HTTPConnectionMock()
            with patch.object(
                conn_server, "getresponse", return_value=mock_response
            ) as response:
                (data_send, server_status, server_reason) = p2p_client.send_message(
                    int_msg, self.local_ip, self.port_user_1, self.username_1
                )
                self.assertNotEqual(data_send["text"], self.msg_json_user_2["text"])
                self.assertEqual(data_send["text"], int_msg)
                self.assertEqual(
                    data_send["username"], self.msg_json_user_2["username"]
                )
                self.assertNotEqual(data_send, self.msg_json_user_2)
                self.assertEqual(server_status, 200)
                self.assertEqual(server_reason, "OK")

    @patch("http.client.HTTPResponse")
    def test_send_message_msg_empty_str(self, mock_response):
        print("TEST SEND_MESSAGE WITH EMPTY STR MSG\n")
        # Test response and connection to Alice (server part) with client
        # Bob with an empty string
        empty_str = ""
        expected_json_msg = {"username": self.username_1, "text": empty_str}
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value.decode.return_value = expected_json_msg

        with patch("http.client.HTTPConnection") as HTTPConnectionMock:
            conn_server = HTTPConnectionMock()
            with patch.object(
                conn_server, "getresponse", return_value=mock_response
            ) as response:
                (data_send, server_status, server_reason) = p2p_client.send_message(
                    empty_str, self.local_ip, self.port_user_1, self.username_1
                )
                self.assertEqual(data_send["text"], empty_str)
                self.assertEqual(data_send["username"], self.username_1)
                self.assertNotEqual(data_send["username"], self.username_2)
                self.assertEqual(server_status, 200)
                self.assertEqual(server_reason, "OK")

    @patch("http.client.HTTPResponse")
    def test_send_message_msg_dico(self, mock_response):
        print("TEST SEND_MESSAGE WITH DICO MSG\n")
        # Test response and connection to Alice (server part) with client
        # Bob with a dictionnary
        dico_msg = {"username": self.username_2, "text": self.msg_from_user_2}

        expected_json_msg = {"username": self.username_1, "text": dico_msg}
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value.decode.return_value = expected_json_msg

        with patch("http.client.HTTPConnection") as HTTPConnectionMock:
            conn_server = HTTPConnectionMock()
            with patch.object(
                conn_server, "getresponse", return_value=mock_response
            ) as response:
                (data_send, server_status, server_reason) = p2p_client.send_message(
                    self.msg_json_user_2,
                    self.local_ip,
                    self.port_user_1,
                    self.username_1,
                )
                self.assertEqual(data_send["text"], dico_msg)
                self.assertEqual(data_send["username"], self.username_1)
                self.assertNotEqual(data_send["username"], self.username_2)
                self.assertEqual(data_send["text"]["username"], dico_msg["username"])
                self.assertNotEqual(data_send["text"]["username"], self.username_1)
                self.assertEqual(server_status, 200)
                self.assertEqual(server_reason, "OK")

    @patch("http.client.HTTPResponse")
    def test_send_message_msg_list(self, mock_response):
        print("TEST SEND_MESSAGE WITH LIST MSG\n")
        # Test response and connection to Alice (server part) with client
        # Bob with a list
        list_msg = ["bonjour", "comment tu vas?", 4, "byebye", 8]
        expected_json_msg = {"username": self.username_1, "text": list_msg}
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value.decode.return_value = expected_json_msg

        with patch("http.client.HTTPConnection") as HTTPConnectionMock:
            conn_server = HTTPConnectionMock()
            with patch.object(
                conn_server, "getresponse", return_value=mock_response
            ) as response:
                (data_send, server_status, server_reason) = p2p_client.send_message(
                    list_msg, self.local_ip, self.port_user_1, self.username_1
                )
                self.assertEqual(data_send["text"], list_msg)
                self.assertEqual(data_send["text"][0], list_msg[0])
                self.assertNotEqual(data_send["text"][2], list_msg[0])
                self.assertEqual(data_send["text"][2], list_msg[2])
                self.assertEqual(data_send["username"], self.username_1)
                self.assertEqual(server_status, 200)
                self.assertEqual(server_reason, "OK")

    # Test de la fonction send_certificate()
    @patch("http.client.HTTPResponse")
    def test_certificate_key(self, mock_response):
        print("TEST CERTIFICATE_KEY\n")
        # Test sent file
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output

        if os.path.exists(self.certificate1):
            last_four_char = self.certificate1[-4:]
            if last_four_char == ".pem":
                certificate_file = open(self.certificate1, mode="r")
                certificate_content = certificate_file.read()
                certificate_file.close()

        expected_json_msg = {
            "username": self.username_1,
            "clef_pub": certificate_content,
        }
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value.decode.return_value = expected_json_msg

        with patch("http.client.HTTPConnection") as HTTPConnectionMock:
            conn_server = HTTPConnectionMock()
            with patch.object(
                conn_server, "getresponse", return_value=mock_response
            ) as response:
                self.assertEqual(
                    p2p_client.send_certificate(
                        "file_not_found", "0.0.0.0", "8000", "8080"
                    ),
                    (-1, -1, -1),
                )
                sys.stdout = sys.__stdout__
                self.assertEqual(
                    "Error : File does not exist\n", get_printed_output.getvalue()
                )

                get_printed_output = io.StringIO()
                sys.stdout = get_printed_output
                self.assertEqual(
                    p2p_client.send_certificate(
                        "p2p_client.py", "0.0.0.0", "8000", "8080"
                    ),
                    (-1, -1, -1),
                )
                sys.stdout = sys.__stdout__
                self.assertEqual(
                    "Error : File is not a certificate\n", get_printed_output.getvalue()
                )
                (dataSend, serverStatus, serverReason) = p2p_client.send_certificate(
                    self.certificate1, self.local_ip, self.port_user_2, self.username_1
                )

                # test contenu du fichier
                self.assertEqual(len(dataSend["clef_pub"]), 1428)
                self.assertEqual(
                    dataSend["clef_pub"][:28], "-----BEGIN CERTIFICATE-----\n"
                )
                self.assertEqual(
                    (dataSend["clef_pub"][-26:]), "-----END CERTIFICATE-----\n"
                )

    def test_sign_and_verif_message(self):
        print("TEST SIGN_AND_VERIF_MESSAGE\n")
        # Test signed message and sign verification
        (signed_message, sign) = p2p_client.sign_message(
            "Message to sign", self.private_key, self.key_password
        )
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        p2p_client.verify_sign(signed_message, sign, self.certificate1)
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is signed\n", get_printed_output.getvalue())

        # Test non signed message verification and random sign
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        p2p_client.verify_sign("Non signed message", sign, self.certificate1)
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is not signed\n", get_printed_output.getvalue())

        # Test signed message then message modification and sign verification
        (signed_message, sign) = p2p_client.sign_message(
            "New message to sign", self.private_key, self.key_password
        )
        signed_message += "Message modification"
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        p2p_client.verify_sign(signed_message, sign, self.certificate1)
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is not signed\n", get_printed_output.getvalue())

        # Test signed message and verification with another certificate
        (signed_message, sign) = p2p_client.sign_message(
            "Last message to sign", self.private_key, self.key_password
        )
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        p2p_client.verify_sign(signed_message, sign, self.certificate2)
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is not signed\n", get_printed_output.getvalue())

    @patch("http.client.HTTPResponse")
    def test_sign_and_send_message(self, mock_response):
        print("TEST SIGN_AND_SEND_MESSAGE\n")
        # Test response and connection to server username_1 with client
        # username_2 with a string msg and sign
        (signed_message, sign) = p2p_client.sign_message(
            "Last message to sign", self.private_key, self.key_password
        )
        expected_json_msg = {
            "username": self.username_1,
            "text": "Last message to sign",
            "signature": sign,
        }
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value.decode.return_value = expected_json_msg

        with patch("http.client.HTTPConnection") as HTTPConnectionMock:
            conn_server = HTTPConnectionMock()
            with patch.object(
                conn_server, "getresponse", return_value=mock_response
            ) as response:
                (
                    data_send,
                    server_status,
                    server_reason,
                ) = p2p_client.sign_and_send_message(
                    self.msg_from_user_1,
                    self.private_key,
                    self.key_password,
                    self.local_ip,
                    self.port_user_1,
                    self.username_1,
                )

                get_printed_output = io.StringIO()
                sys.stdout = get_printed_output
                text = data_send["text"]
                signature = data_send["signature"]
                p2p_client.verify_sign(
                    data_send["text"], data_send["signature"], self.certificate1
                )
                sys.stdout = sys.__stdout__
                self.assertEqual("Message is signed\n", get_printed_output.getvalue())
                self.assertEqual(server_status, 200)
                self.assertEqual(server_reason, "OK")


if __name__ == "__main__":
    unittest.main()
