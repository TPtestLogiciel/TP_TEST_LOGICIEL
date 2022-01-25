import unittest
import requests
import shlex
import subprocess
import time
import bdd
import random
import string
import os

class TestUserSrv(unittest.TestCase):

    SrvSubprocess = None

    TestPort = "5000"
    SrvAddr = "127.0.0.1"
    SrvUrl = "http://" + SrvAddr + ":" + TestPort

    bdd.bdd_creation()

    def setUp(self):
        cmd = "python3 serveur.py --port="+self.TestPort
        args = shlex.split(cmd)
        self.SrvSubprocess  = subprocess.Popen(args) # launch command as a subprocess
        time.sleep(3)

    def tearDown(self):
        print("killing subprocess serveur")
        self.SrvSubprocess.kill()
        self.SrvSubprocess.wait()


    def CreateRandomString(self,n):
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k = n))


    def CreateRandomIP(self):
        ip = ".".join(map(str, (random.randint(0, 255) 
                        for _ in range(4))))
        print(ip)
        return ip
    
    def test_launchSrv(self):
        response = requests.get(self.SrvUrl+"/isalive")
        self.assertEqual(response.status_code,200)


    def test_nameIp(self):
        key1 = self.CreateRandomString(64)
        response=requests.post(self.SrvUrl+"/nameIp",json={"name":"Mohamed","pwd":"aAaa#a9aa","ip":"192.0.0.2","key":key1})
        self.assertEqual(response.status_code,200)

        #name vide
        response=requests.post(self.SrvUrl+"/nameIp",json={"name":"","pwd":"aAaa#a9aa","ip":"0.0.0.4","key":key1})
        self.assertEqual(response.status_code,455)
        #ip vide
        response=requests.post(self.SrvUrl+"/nameIp",json={"name":"Ekdc","pwd":"aAaa#a9aa","ip":"","key":key1})
        self.assertEqual(response.status_code,456)

        #pwd vide
        response=requests.post(self.SrvUrl+"/nameIp",json={"name":"Dkd5","pwd":"","ip":"192.0.0.8","key":key1})
        self.assertEqual(response.status_code,457)

        #key vide
        response=requests.post(self.SrvUrl+"/nameIp",json={"name":"Mokdfz","pwd":"aAaa#a9aa","ip":"192.0.0.5","key":""})
        self.assertEqual(response.status_code,458)

if __name__ == '__main__':
    unittest.main()
