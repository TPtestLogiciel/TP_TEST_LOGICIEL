import unittest
import random
import string
import os
import bdd

class TestBddSrv(unittest.TestCase):

    def test_bdd_creation(self):
        bdd.bdd_creation()
        cursor = bdd.conn.execute('select * from BDD')
        names = list(map(lambda x: x[0], cursor.description))
        self.assertIn("username",names)
        self.assertIn("password",names)
        self.assertIn("ip",names)
        self.assertIn("clef_pub",names)
    
    def test_username(self):
        self.assertFalse(bdd.CheckUsername("")) # empty
        self.assertFalse(bdd.CheckUsername("aaa")) # bad size
        self.assertFalse(bdd.CheckUsername("aaa#")) # good size but special
        self.assertTrue(bdd.CheckUsername("aaaaa")) # good size
        self.assertTrue(bdd.CheckUsername("aaaa9a")) # good size with number
        self.assertTrue(bdd.CheckUsername("aaAa9")) # good size with number and MAJ
    
    def test_password(self):
        self.assertFalse(bdd.CheckPassword("")) # empty
        self.assertTrue(bdd.CheckPassword("aAaa#a9aa")) # good size MAJ Special number
        self.assertFalse(bdd.CheckPassword("aAaa#a9")) # bad size MAJ Special number
        self.assertFalse(bdd.CheckPassword("aaaa#a9aa")) # good size no MAJ Special number
        self.assertFalse(bdd.CheckPassword("aAaaaa9aa")) # good size MAJ no Special number
        self.assertFalse(bdd.CheckPassword("aAaa#aaaa")) # good size MAJ Special no number
    
    def CreateRandomString(self,n):
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k = n))

    def test_CheckKey(self):
        self.assertTrue(
			bdd.CheckKey(
				self.CreateRandomString(64)
			) # terrible code to generate a random string
		)
        self.assertFalse(
			bdd.CheckKey(
				self.CreateRandomString(63)
			) # terrible code to generate a random string
		)
        self.assertFalse(bdd.CheckKey(""))

    def CreateRandomIP(self):
        ip_temp = ".".join(map(str, (random.randint(0, 255) 
                        for _ in range(4))))
        ip=ip_temp + ":"

        ip_final= ip + str(random.randint(0, 10000))

        print(ip_final)
        return ip_final
    
    def test_Ajout(self):
        key = self.CreateRandomString(64) # nobody said anything about using 4 times the same key (yet)
        self.assertFalse(bdd.bdd_ajout("aaa","aAaa#a9aa",self.CreateRandomIP(),key)) # bad username
        self.assertFalse(bdd.bdd_ajout("aaaa","",self.CreateRandomIP(),key)) # bad password
        self.assertFalse(bdd.bdd_ajout("aaaa","aAaa#a9aa",self.CreateRandomIP(),self.CreateRandomString(63))) # bad key
        self.assertTrue(bdd.bdd_ajout("aaaa","aAaa#a9aa",self.CreateRandomIP(),key))
        self.assertFalse(bdd.bdd_ajout("aaaa","aAaa#a9aa",self.CreateRandomIP(),key)) # Not supposed to be able to add 2* same user
        
    def test_UserLogin(self):
		# Let's add a correct user :
        key = self.CreateRandomString(64)
        self.assertTrue(bdd.bdd_ajout("cccc","aAaa#a9aa",self.CreateRandomIP(),key))
        self.assertTrue(bdd.CheckUserLogin("cccc","aAaa#a9aa"))
        self.assertFalse(bdd.CheckUserLogin("cccc","aAaa#a9a")) # Bad Password
        self.assertFalse(bdd.CheckUserLogin("aaab","aAaa#a9aa")) # Bad Username
    
    def test_CheckIP(self):
        self.assertTrue(bdd.CheckIP(self.CreateRandomIP())) # IP fonctionnelle
        self.assertFalse(bdd.CheckIP("")) # Liste vide
        self.assertFalse(bdd.CheckIP("1.4.126.79.78")) # Taille trop grande
        self.assertFalse(bdd.CheckIP("1.2")) # Taille trop petite
        self.assertFalse(bdd.CheckIP("-128.-10.54.6")) # une valeur negative
        self.assertFalse(bdd.CheckIP("500.200.128.3")) # une valeur < 255
        self.assertFalse(bdd.CheckIP("30.100.128.a")) # lettre ascii
        self.assertFalse(bdd.CheckIP("30.100.128.#")) # caractere special
        self.assertFalse(bdd.CheckIP("30.100.128.A")) # majuscule ascii
        
        self.assertFalse(bdd.CheckIP("30.100.128.12:")) # Ip fonctionelle port vide 
        self.assertFalse(bdd.CheckIP("30.100.128.12:-60")) # port negatif
        self.assertFalse(bdd.CheckIP("30.100.128.12:afdeh")) # port non numeric
        self.assertFalse(bdd.CheckIP("30.100.128.12:108:200:300")) # plusieur ports

if __name__ == '__main__':
    unittest.main()
    
