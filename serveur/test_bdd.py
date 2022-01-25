import unittest
import random
import string
import bdd

class test_bdd_srv(unittest.TestCase):

    def test_bdd_creation(self):
        bdd.bdd_creation()
        cursor = bdd.conn.execute('select * from BDD')
        names = list(map(lambda x: x[0], cursor.description))
        self.assertIn("username",names)
        self.assertIn("password",names)
        self.assertIn("ip",names)
        self.assertIn("clef_pub",names)
    
    def test_username(self):
        self.assertFalse(bdd.check_username("")) # empty
        self.assertFalse(bdd.check_username("aaa")) # bad size
        self.assertFalse(bdd.check_username("aaa#")) # good size but special
        self.assertTrue(bdd.check_username("aaaaa")) # good size
        self.assertTrue(bdd.check_username("aaaa9a")) # good size with number
        self.assertTrue(bdd.check_username("aaAa9")) # good size with number and MAJ
    
    def test_password(self):
        self.assertFalse(bdd.check_password("")) # empty
        self.assertTrue(bdd.check_password("aAaa#a9aa")) # good size MAJ Special number
        self.assertFalse(bdd.check_password("aAaa#a9")) # bad size MAJ Special number
        self.assertFalse(bdd.check_password("aaaa#a9aa")) # good size no MAJ Special number
        self.assertFalse(bdd.check_password("aAaaaa9aa")) # good size MAJ no Special number
        self.assertFalse(bdd.check_password("aAaa#aaaa")) # good size MAJ Special no number
    
    def create_random_string(self,n):
        return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k = n))

    def test_check_key(self):
        self.assertTrue(
			bdd.check_key(
				self.create_random_string(64)
			) # terrible code to generate a random string
		)
        self.assertFalse(
			bdd.check_key(
				self.create_random_string(63)
			) # terrible code to generate a random string
		)
        self.assertFalse(bdd.check_key(""))

    def create_random_ip(self):
        ip_temp = ".".join(map(str, (random.randint(0, 255) 
                        for _ in range(4))))
        ip=ip_temp + ":"

        ip_final= ip + str(random.randint(0, 10000))
        return ip_final
    
    def test_add(self):
        key = self.create_random_string(64) # nobody said anything about using 4 times the same key (yet)
        self.assertFalse(bdd.bdd_add("aaa","aAaa#a9aa",self.create_random_ip(),key)) # bad username
        self.assertFalse(bdd.bdd_add("aaaa","",self.create_random_ip(),key)) # bad password
        self.assertFalse(bdd.bdd_add("aaaa","aAaa#a9aa",self.create_random_ip(),self.create_random_string(63))) # bad key
        self.assertTrue(bdd.bdd_add("aaaa","aAaa#a9aa",self.create_random_ip(),key))
        self.assertFalse(bdd.bdd_add("aaaa","aAaa#a9aa",self.create_random_ip(),key)) # Not supposed to be able to add 2* same user
        
    def test_user_login(self):
		# Let's add a correct user :
        key = self.create_random_string(64)
        self.assertTrue(bdd.bdd_add("cccc","aAaa#a9aa",self.create_random_ip(),key))
        self.assertTrue(bdd.check_user_login("cccc","aAaa#a9aa"))
        self.assertFalse(bdd.check_user_login("cccc","aAaa#a9a")) # Bad Password
        self.assertFalse(bdd.check_user_login("aaab","aAaa#a9aa")) # Bad Username
    
    def test_check_ip(self):
        self.assertTrue(bdd.check_ip(self.create_random_ip())) # IP fonctionnelle
        self.assertFalse(bdd.check_ip("")) # Liste vide
        self.assertFalse(bdd.check_ip("1.4.126.79.78")) # Taille trop grande
        self.assertFalse(bdd.check_ip("1.2")) # Taille trop petite
        self.assertFalse(bdd.check_ip("-128.-10.54.6")) # une valeur negative
        self.assertFalse(bdd.check_ip("500.200.128.3")) # une valeur < 255
        self.assertFalse(bdd.check_ip("30.100.128.a")) # lettre ascii
        self.assertFalse(bdd.check_ip("30.100.128.#")) # caractere special
        self.assertFalse(bdd.check_ip("30.100.128.A")) # majuscule ascii
        
        self.assertFalse(bdd.check_ip("30.100.128.12:")) # Ip fonctionelle port vide 
        self.assertFalse(bdd.check_ip("30.100.128.12:-60")) # port negatif
        self.assertFalse(bdd.check_ip("30.100.128.12:afdeh")) # port non numeric
        self.assertFalse(bdd.check_ip("30.100.128.12:108:200:300")) # plusieur ports

if __name__ == '__main__':
    unittest.main()
    
