import unittest
import requests
import shlex
import subprocess
import time
import json
import http.client
import p2p_client

import io
import sys

class TestP2PClient(unittest.TestCase):

    user1Subprocess = None
    user2Subprocess = None

    portUser1 = "8080"
    portUser2 = "8000"
    ip = "0.0.0.0"

    buddyUsr1 = "Ground"
    buddyUsr2 = "Air"
    msgFromGround = "Hello Air, it's a message from Ground!"
    msgJsonGround = {'username': buddyUsr2, 'text': msgFromGround}
    msgFromAir = "Hi Ground, it's a message from Air!"
    msgJsonAir = {'username': buddyUsr1, 'text': msgFromAir}
    
    #Variable pour test crypto
    key_from_air="/home/steven/cert.pem" #path du certificat.pem

    def setUp(self):
        # Launch User1 Ground terminal
        cmdGround = "python3 p2p_client.py --buddy={} --port_dest={}\
                    --port_source={}".format(self.buddyUsr2,
                                             self.portUser1, 
                                             self.portUser2)
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
        (dataSend,
            serverStatus, 
            serverReason) = p2p_client.send_message(self.msgFromAir,
                                                    self.ip,
                                                    self.portUser2, 
                                                    self.buddyUsr1)
        dataSend = json.loads(dataSend)
        self.assertEqual(dataSend['text'], self.msgJsonAir['text'])
        self.assertEqual(dataSend['username'], 
                         self.msgJsonAir['username'])
        self.assertEqual(dataSend, self.msgJsonAir)
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

        # Test response and connection to server Ground with client
        # Air with an int msg
        (dataSend, 
            serverStatus, 
            serverReason) = p2p_client.send_message(123456789, 
                                                    self.ip, 
                                                    self.portUser2, 
                                                    self.buddyUsr1)
        dataSend = json.loads(dataSend)
        self.assertNotEqual(dataSend['text'], self.msgJsonAir['text'])
        self.assertEqual(dataSend['text'], 123456789)
        self.assertEqual(dataSend['username'], 
                         self.msgJsonAir['username'])
        self.assertNotEqual(dataSend, self.msgJsonAir)
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

        # Test response and connection to server Ground with client 
        # Air with an empty string
        (dataSend, 
            serverStatus, 
            serverReason) = p2p_client.send_message("", self.ip, 
                                                    self.portUser2, 
                                                    self.buddyUsr1)
        dataSend = json.loads(dataSend)
        self.assertEqual(dataSend['text'], "")
        self.assertEqual(dataSend['username'], 
                            self.msgJsonAir['username'])
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

        # Test response and connection to server Ground with client
        # Air with a dictionnary
        (dataSend, 
            serverStatus, 
            serverReason) = p2p_client.send_message(self.msgJsonAir, 
                                                    self.ip, 
                                                    self.portUser2, 
                                                    self.buddyUsr1)
        dataSend = json.loads(dataSend)
        dico = {'username' : self.buddyUsr1,
                'text' : {'username': self.buddyUsr1, 
                            'text': self.msgFromAir}}
        dico = json.dumps(dico)
        dico = json.loads(dico)
        self.assertEqual(dataSend['text'], dico['text'])
        self.assertNotEqual(dataSend['text'], self.msgJsonAir['text'])
        self.assertEqual(dataSend['username'], 
                            self.msgJsonAir['username'])
        self.assertEqual(dataSend['text']['username'], 
                            self.msgJsonAir['username'])
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

        # Test response and connection to server Ground with client
         # Air with a list
        listMsg = ["bonjour", "comment tu vas?", 4, "byebye", 8]
        (dataSend, 
            serverStatus, 
            serverReason) = p2p_client.send_message(listMsg, 
                                                    self.ip, 
                                                    self.portUser2, 
                                                    self.buddyUsr1)
        dataSend = json.loads(dataSend)
        self.assertEqual(dataSend['text'], listMsg)
        self.assertEqual(dataSend['text'][0], listMsg[0])
        self.assertNotEqual(dataSend['text'][2], listMsg[0])
        self.assertEqual(dataSend['text'][2], listMsg[2])
        self.assertNotEqual(dataSend['text'], 
                            self.msgJsonAir['text'])
        self.assertEqual(dataSend['username'], 
                        self.msgJsonAir['username'])
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")



    def tearDown(self):
        print("killing subprocess user_server")
        self.user1Subprocess.kill()
        self.user1Subprocess.wait()


    #Test de la fonction send_public_key()
    def test_send_public_key(self):

        #Test du fichier envoyé
        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        self.assertEqual(p2p_client.send_public_key("fichier_inexistant","0.0.0.0","8000","8080"),(-1,-1,-1))
        sys.stdout = sys.__stdout__
        self.assertEqual("Erreur : Le fichier n'existe pas\n",get_printed_output.getvalue())

        get_printed_output = io.StringIO()
        sys.stdout = get_printed_output
        self.assertEqual(p2p_client.send_public_key("p2p_client.py","0.0.0.0","8000","8080"),(-1,-1,-1))
        sys.stdout = sys.__stdout__
        self.assertEqual("Erreur : Le fichier n'est pas une clé publique\n",get_printed_output.getvalue())

        (dataSend,
            serverStatus, 
            serverReason) = p2p_client.send_public_key(self.key_from_air,
                                                        self.ip,
                                                        self.portUser2, 
                                                        self.buddyUsr1)
        dataSend = json.loads(dataSend)

        #test contenu du fichier 
        self.assertEqual(len(dataSend['clef_pub']), 1428)
        self.assertEqual(dataSend['clef_pub'][:28], '-----BEGIN CERTIFICATE-----\n')
        self.assertEqual((dataSend['clef_pub'][-26:]), '-----END CERTIFICATE-----\n')




if __name__ == '__main__':
    unittest.main()