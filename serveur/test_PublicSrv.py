import unittest
import requests
import shlex
import subprocess
import time

class TestUserSrv(unittest.TestCase):

	SrvSubprocess = None

	TestPort = "80"
	SrvAddr = "siliciumboy.pythonanywhere.com"
	SrvUrl = "http://" + SrvAddr + ":" + TestPort

	def test_launchSrv(self):
		response = requests.get(self.SrvUrl+"/isalive")
		self.assertEqual(response.status_code,200)

if __name__ == '__main__':
	unittest.main()
