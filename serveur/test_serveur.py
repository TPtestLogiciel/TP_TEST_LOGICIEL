import unittest
import requests
import shlex
import subprocess
import time

class TestUserSrv(unittest.TestCase):

	SrvSubprocess = None

	TestPort = "5000"
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

		#régler les erreurs aux tests ci-dessous et 
		#rajouter des tests pour cas où on envoie pas tous les champs
		response=requests.post(self.SrvUrl+"/nameIp",json={"name":"","ip":"0.0.0.4"})
		self.assertEqual(response.status_code,455)
		response=requests.post(self.SrvUrl+"/nameIp",json={"name":"Mister","ip":""})
		self.assertEqual(response.status_code,456)



if __name__ == '__main__':
	unittest.main()
