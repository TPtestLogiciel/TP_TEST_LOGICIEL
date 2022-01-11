import unittest
import requests
import shlex
import subprocess
import time

class TestUserSrv(unittest.TestCase):

	SrvSubprocess = None

	TestPort = "99"
	SrvAddr = "127.0.0.1"
	SrvUrl = "http://" + SrvAddr + ":" + TestPort

	def setUp(self):
		cmd = "python3 serveur.py --port="+self.TestPort
		args = shlex.split(cmd)
		self.SrvSubprocess  = subprocess.Popen(args) # launch command as a subprocess
		time.sleep(3)

	def tearDown(self):
		print("killing subprocess serveur")
		self.SrvSubprocess.kill()
		self.SrvSubprocess.wait()

	def test_launchSrv(self):
		response = requests.get(self.SrvUrl+"/isalive")
		self.assertEqual(response.status_code,200)


	def test_nameIp(self):
		response=requests.post(self.SrvUrl+"/nameIp",json={"name":"Mohamed","ip":"0.0.0.2"})
		self.assertEqual(response.status_code,200)



if __name__ == '__main__':
	unittest.main()
