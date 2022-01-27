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

    user1Subprocess = None
    user2Subprocess = None

    portUser1 = "8080"
    portUser2 = "8000"
    ip = "0.0.0.0"

    buddyUsr1 = "Ground"
    buddyUsr2 = "Air"
    msgFromGround = "Hello Air, it's a message from Ground!"
    msgJsonGround = {"username": buddyUsr2, "text": msgFromGround}
    msgFromAir = "Hi Ground, it's a message from Air!"
    msgJsonAir = {"username": buddyUsr1, "text": msgFromAir}

    certificate_from_air = "/home/steven/cert.pem"  # path du certificat.pem
    private_key = "/home/steven/private.pem"
    password = "azertyuiop"
    certificate2 = "/home/steven/cert2.pem"


    def setUp(self):
        # Launch User1 Ground terminal
        cmdGround = "python3 p2p_client.py --buddy={} --port_dest={}\
                    --port_source={}".format(
            self.buddyUsr2, self.portUser1, self.portUser2
        )
        argsGround = shlex.split(cmdGround)
        # launch command as a subprocess
        self.user1Subprocess = subprocess.Popen(argsGround)
        time.sleep(3)

        # Launch User2 Air terminal
        # cmdAir = "python3 p2p_client.py --port_dest={} --port_source={} \
        #         --buddy={}".format(self.port_dest,
        # self.port_source,
        # self.buddyUsr2)
        # argsAir = shlex.split(cmdAir)
        # self.user2Subprocess = subprocess.Popen(argsAir)
        # time.sleep(3)

    def test_send_message(self):
        # Test response and connection to server Ground with client
        # Air with a string msg
        (dataSend, serverStatus, serverReason) = p2p_client.send_message(
            self.msgFromAir, self.ip, self.portUser2, self.buddyUsr1
        )
        dataSend = json.loads(dataSend)
        self.assertEqual(dataSend["text"], self.msgJsonAir["text"])
        self.assertEqual(dataSend["username"], self.msgJsonAir["username"])
        self.assertEqual(dataSend, self.msgJsonAir)
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

        # Test response and connection to server Ground with client
        # Air with an int msg
        (dataSend, serverStatus, serverReason) = p2p_client.send_message(
            123456789, self.ip, self.portUser2, self.buddyUsr1
        )
        dataSend = json.loads(dataSend)
        self.assertNotEqual(dataSend["text"], self.msgJsonAir["text"])
        self.assertEqual(dataSend["text"], 123456789)
        self.assertEqual(dataSend["username"], self.msgJsonAir["username"])
        self.assertNotEqual(dataSend, self.msgJsonAir)
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

        # Test response and connection to server Ground with client
        # Air with an empty string
        (dataSend, serverStatus, serverReason) = p2p_client.send_message(
            "", self.ip, self.portUser2, self.buddyUsr1
        )
        dataSend = json.loads(dataSend)
        self.assertEqual(dataSend["text"], "")
        self.assertEqual(dataSend["username"], self.msgJsonAir["username"])
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

        # Test response and connection to server Ground with client
        # Air with a dictionnary
        (dataSend, serverStatus, serverReason) = p2p_client.send_message(
            self.msgJsonAir, self.ip, self.portUser2, self.buddyUsr1
        )
        dataSend = json.loads(dataSend)
        dico = {
            "username": self.buddyUsr1,
            "text": {"username": self.buddyUsr1, "text": self.msgFromAir},
        }
        dico = json.dumps(dico)
        dico = json.loads(dico)
        self.assertEqual(dataSend["text"], dico["text"])
        self.assertNotEqual(dataSend["text"], self.msgJsonAir["text"])
        self.assertEqual(dataSend["username"], self.msgJsonAir["username"])
        self.assertEqual(dataSend["text"]["username"], self.msgJsonAir["username"])
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

        # Test response and connection to server Ground with client
        # Air with a list
        listMsg = ["bonjour", "comment tu vas?", 4, "byebye", 8]
        (dataSend, serverStatus, serverReason) = p2p_client.send_message(
            listMsg, self.ip, self.portUser2, self.buddyUsr1
        )
        dataSend = json.loads(dataSend)
        self.assertEqual(dataSend["text"], listMsg)
        self.assertEqual(dataSend["text"][0], listMsg[0])
        self.assertNotEqual(dataSend["text"][2], listMsg[0])
        self.assertEqual(dataSend["text"][2], listMsg[2])
        self.assertNotEqual(dataSend["text"], self.msgJsonAir["text"])
        self.assertEqual(dataSend["username"], self.msgJsonAir["username"])
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

    def tearDown(self):
        print("killing subprocess user_server")
        self.user1Subprocess.kill()
        self.user1Subprocess.wait()

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
        p2p_client.verify_sign(
            str.encode("Message non signée"), sign, self.certificate_from_air
        )
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is not signed\n", get_printed_output.getvalue())

        # Test message signé puis modification du message et verification signature
        (signed_message, sign) = p2p_client.sign_message(
            "Nouveau message à signer", self.private_key, self.password
        )
        signed_message += str.encode("Modification du message")
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
            self.msgFromAir,self.private_key,self.password, self.ip, self.portUser2, self.buddyUsr1
        )
        dataSend = json.loads(dataSend)

        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        p2p_client.verify_sign(dataSend["text"],dataSend["signature"], self.certificate2)
        sys.stdout = sys.__stdout__
        self.assertEqual("Message is signed\n", get_printed_output.getvalue())
        
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

if __name__ == "__main__":
    unittest.main()
