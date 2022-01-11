import unittest
import requests
import shlex
import subprocess
import time
from json import dumps
import http.client
import client

class TestClient(unittest.TestCase):

    SrvSubprocess = None

    TestPort = "99"
    SrvAddr = "127.0.0.1"
    SrvUrl = "http://" + SrvAddr + ":" + TestPort
    BuddyUsr = "Ground"
    MsgTest = "Hello, it's a test from client!"
    MsgJson = {'message': MsgTest, 'username': BuddyUsr}


    def setUp(self):
        # Launch server first
        cmd = "python ../serveur/user_server.py --port={}".format(self.TestPort)
        args = shlex.split(cmd)
        self.SrvSubprocess  = subprocess.Popen(args) # launch command as a subprocess
        time.sleep(3)


    def test_send_message(self):
        data_send, server_status, server_reason = client.send_message(self.SrvAddr, self.TestPort, self.MsgTest)
        self.assertEqual(data_send, self.MsgJsonFinal)
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")


    def tearDown(self):
        print("killing subprocess user_server")
        self.SrvSubprocess.kill()
        self.SrvSubprocess.wait()

if __name__ == '__main__':
    unittest.main()
