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
        self.assertIn("id",names)
        self.assertIn("username",names)
        self.assertIn("password",names)
        self.assertIn("ip",names)
        self.assertIn("clef_pub",names)
        self.assertIn("clef_priv",names)
    
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
				self.CreateRandomString(128)
			) # terrible code to generate a random string
		)
        self.assertFalse(
			bdd.CheckKey(
				self.CreateRandomString(127)
			) # terrible code to generate a random string
		)
        self.assertFalse(bdd.CheckKey(""))
        

    #def test_bdd_username():

		

if __name__ == '__main__':
	unittest.main()
