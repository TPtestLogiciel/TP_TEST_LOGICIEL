import unittest
import requests
import shlex
import subprocess
import time
import json
# from json import dumps
import http.client
import p2p_client


# import sys
# import logging
# import threading
# from docopt import docopt
# from flask import Flask
# from flask import Response
# from flask import request
# import http.client
# import json

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


    def setUp(self):
        # Launch User1 Ground terminal
        cmdGround = "python3 p2p_client.py --port_dest={} --port_source={} \
                --buddy={}".format(self.portUser1, self.portUser2, self.buddyUsr2)
        argsGround = shlex.split(cmdGround)
        self.user1Subprocess = subprocess.Popen(argsGround) # launch command as a subprocess
        time.sleep(3)

        # Launch User2 Air terminal
        # cmdAir = "python3 p2p_client.py --port_dest={} --port_source={} \
        #         --buddy={}".format(self.port_dest, self.port_source, self.buddyUsr2)
        # argsAir = shlex.split(cmdAir)
        # self.user2Subprocess = subprocess.Popen(argsAir) # launch command as a subprocess
        # time.sleep(3)


    def test_send_message(self):
        # Test response and connection to server Ground with client Air with a string msg
        dataSend, serverStatus, serverReason = p2p_client.send_message(self.msgFromAir, self.ip, self.portUser2, self.buddyUsr1)
        dataSend = json.loads(dataSend)
        print("DataSend by Air to Ground : ", dataSend)
        self.assertEqual(dataSend['text'], self.msgJsonAir['text'])
        self.assertEqual(dataSend['username'], self.msgJsonAir['username'])
        self.assertEqual(dataSend, self.msgJsonAir)
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")

        # Test response and connection to server Ground with client Air with an int msg
        dataSend, serverStatus, serverReason = p2p_client.send_message(123456789, self.ip, self.portUser2, self.buddyUsr1)
        dataSend = json.loads(dataSend)
        print("DataSend by Air to Ground : ", dataSend)
        self.assertNotEqual(dataSend['text'], self.msgJsonAir['text'])
        self.assertEqual(dataSend['username'], self.msgJsonAir['username'])
        self.assertNotEqual(dataSend, self.msgJsonAir)
        self.assertEqual(serverStatus, 200)
        self.assertEqual(serverReason, "OK")


    def tearDown(self):
        print("killing subprocess user_server")
        self.user1Subprocess.kill()
        self.user1Subprocess.wait()

if __name__ == '__main__':
    unittest.main()