import unittest
import requests
import shlex
import subprocess
import time
from json import dumps

class TestUserSrv(unittest.TestCase):

	SrvSubprocess = None

	TestPort = "99"
	SrvAddr = "127.0.0.1"
	SrvUrl = "http://" + SrvAddr + ":" + TestPort

	def setUp(self):
		cmd = "python user_server.py --port="+self.TestPort
		args = shlex.split(cmd)
		self.SrvSubprocess  = subprocess.Popen(args) # launch command as a subprocess
		time.sleep(3)

	def tearDown(self):
		print("killing subprocess user_server")
		self.SrvSubprocess.kill()
		self.SrvSubprocess.wait()

	def test_launchSrv(self):
		response = requests.get(self.SrvUrl+"/isalive")
		self.assertEqual(response.status_code,200)

	def test_UserSrv(self):
		json = dumps({"name": "Patachou", "ip": "0"}, sort_keys=False)
		response = requests.post(self.SrvUrl+"/user", json)
		self.assertEqual(response.status_code,500)


if __name__ == '__main__':
	unittest.main()
