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



    def create_random_string(self, n):
        return "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation, k=n
            )
        )

    def create_random_ip(self):
        ip_temp = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        ip = ip_temp + ":"

        ip_final = ip + str(random.randint(0, 10000))
        return ip_final

    def test_launchSrv(self):
        response = requests.get(self.SrvUrl+"/isalive")
        self.assertEqual(response.status_code,200)


    def test_register(self):
        key1 = self.create_random_string(64)
        response=requests.post(self.SrvUrl+"/register",json={"username":"Mohamed","pwd":"aAaa#a9aa","ip":"192.0.0.2:5501","key":key1})
        self.assertEqual(response.status_code,200)
        
        #payload too small
        response=requests.post(self.SrvUrl+"/register",json={"pwd":"aAaa#a9aa","ip":"0.0.0.4","key":key1})
        self.assertEqual(response.status_code,454)

        #payload too big
        response=requests.post(self.SrvUrl+"/register",json={"name":"Ekdc","username":"Rtyu","pwd":"aAaa#a9aa","ip":"0.0.0.4","key":key1})
        self.assertEqual(response.status_code,454)

        #field name empty
        response=requests.post(self.SrvUrl+"/register",json={"username":"","pwd":"aAaa#a9aa","ip":"0.0.0.4","key":key1})
        self.assertEqual(response.status_code,455)
        #field ip empty
        response=requests.post(self.SrvUrl+"/register",json={"username":"Ekdc","pwd":"aAaa#a9aa","ip":"","key":key1})
        self.assertEqual(response.status_code,456)

        #field pwd empty
        response=requests.post(self.SrvUrl+"/register",json={"username":"Dkd5","pwd":"","ip":"192.0.0.8:5820","key":key1})
        self.assertEqual(response.status_code,457)

        #field key empty
        response=requests.post(self.SrvUrl+"/register",json={"username":"Mokdfz","pwd":"aAaa#a9aa","ip":"192.0.0.5:4412","key":""})
        self.assertEqual(response.status_code,458)

    def test_get_ip_port(self):
        #we register a new client
        ip1=self.create_random_ip()
        elem_ip=ip1.split(":")
        ip=elem_ip[0]
        port=elem_ip[1]
        response=requests.post(self.SrvUrl+"/register",json={"username":"Nani","pwd":"dj54fe5_S","ip":ip1,"key":self.create_random_string(64)})
        self.assertEqual(response.status_code,200)
        #have the ip of a user that is already present in the BDD
        response = requests.get(self.SrvUrl+"/get_ip_port",json={"username":"Nani"})
        self.assertEqual(response,{"username" :"Nani", "ip" : ip, "port" : port})
        self.assertEqual(response.status_code,200)
        #have the ip of a user that is not present in the BDD
        response = requests.get(self.SrvUrl+"/get_ip_port",json={"username":"kakarotto"})
        self.assertEqual(response.status_code,503)
        #test the content of response when username invalid
if __name__ == '__main__':
    unittest.main()
