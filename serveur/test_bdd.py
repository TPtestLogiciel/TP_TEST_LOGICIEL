import os
import random
import sqlite3
import string
import unittest

import bdd


class test_bdd_srv(unittest.TestCase):

    test_db = "test_db.db"

    def setUp(self):
        if os.path.isfile(self.test_db):
            os.remove(self.test_db)
        bdd.bdd_creation(self.test_db)

    def tearDown(self):
        if os.path.isfile(self.test_db):
            os.remove(self.test_db)

    def test_bdd_creation(self):

        if os.path.isfile(self.test_db):
            os.remove(self.test_db)
        self.assertTrue(bdd.bdd_creation(self.test_db))
        # Let's check that the created db has all necessary tables and fields
        con = sqlite3.connect(self.test_db)
        cursor = con.execute("select * from BDD")

        names = list(map(lambda x: x[0], cursor.description))
        self.assertIn("username", names)
        self.assertIn("password", names)
        self.assertIn("ip", names)
        self.assertIn("clef_pub", names)

        self.assertFalse(
            bdd.bdd_creation(self.test_db)
        )  # verifying we cannot recreate the db

    def test_username(self):
        self.assertFalse(bdd.check_username(""))  # empty
        self.assertFalse(bdd.check_username("aaa"))  # bad size
        self.assertFalse(bdd.check_username("aaa#"))  # good size but special
        self.assertTrue(bdd.check_username("aaaaa"))  # good size
        self.assertTrue(bdd.check_username("aaaa9a"))  # good size with number
        self.assertTrue(bdd.check_username("aaAa9"))  # good size with number and MAJ

    def test_password(self):
        self.assertFalse(bdd.check_password(""))  # empty
        self.assertTrue(bdd.check_password("aAaa#a9aa"))  # good size MAJ Special number
        self.assertFalse(bdd.check_password("aAaa#a9"))  # bad size MAJ Special number
        self.assertFalse(
            bdd.check_password("aaaa#a9aa")
        )  # good size no MAJ Special number
        self.assertFalse(
            bdd.check_password("aAaaaa9aa")
        )  # good size MAJ no Special number
        self.assertFalse(
            bdd.check_password("aAaa#aaaa")
        )  # good size MAJ Special no number


    def test_check_key(self):
        self.assertTrue(
            bdd.check_key(
                bdd.create_random_string(64)
            )  # terrible code to generate a random string
        )
        self.assertFalse(
            bdd.check_key(
                bdd.create_random_string(63)
            )  # terrible code to generate a random string
        )
        self.assertFalse(bdd.check_key(""))



    def test_add(self):
        key = bdd.create_random_string(
            64
        )  # nobody said anything about using 4 times the same key (yet)
        self.assertEqual(
            bdd.bdd_add(
                self.test_db,
                "aaa",
                "aAaa#a9aa",
                bdd.create_random_ip(),
                key
            ),455
        )  # bad username
        self.assertEqual(
            bdd.bdd_add(
                self.test_db, "aaaa", "", bdd.create_random_ip(), key 
            ),457
        )  # bad password
        self.assertEqual(
            bdd.bdd_add(
                self.test_db,
                "aaaa",
                "aAaa#a9aa",
                bdd.create_random_ip(),
                bdd.create_random_string(63)
            ),458
        )  # bad key

        self.assertTrue(
            bdd.bdd_add(
                self.test_db,
                "aaaa",
                "aAaa#a9aa",
                bdd.create_random_ip(),
                key
            )
        )
        self.assertEqual(
            bdd.bdd_add(
                self.test_db,
                "aaaa",
                "aAaa#a9aa",
                bdd.create_random_ip(),
                key
            ),459
        )  # Not supposed to be able to add 2* same user

    def test_user_login(self):
        # Let's add a correct user :
        key = bdd.create_random_string(64)

        self.assertTrue(
            bdd.bdd_add(
                self.test_db,
                "cccc",
                "aAaa#a9aa",
                bdd.create_random_ip(),
                key
            )
        )
        self.assertTrue(bdd.check_user_login(self.test_db, "cccc", "aAaa#a9aa"))
        self.assertFalse(
            bdd.check_user_login(self.test_db, "cccc", "aAaa#a9a")
        )  # Bad Password
        self.assertFalse(
            bdd.check_user_login(self.test_db, "aaab", "aAaa#a9aa")
        )  # Bad Username

    def test_check_ip(self):
        self.assertTrue(bdd.check_ip(bdd.create_random_ip()))  # good Ip
        self.assertFalse(bdd.check_ip(""))  # empty list
        self.assertFalse(bdd.check_ip("1.4.126.79.78"))  # greater size
        self.assertFalse(bdd.check_ip("1.2"))  # lesser size
        self.assertFalse(bdd.check_ip("-128.-10.54.6"))  # negative value
        self.assertFalse(bdd.check_ip("500.200.128.3"))  # value < 255
        self.assertFalse(bdd.check_ip("30.100.128.a"))  # ascii letter
        self.assertFalse(bdd.check_ip("30.100.128.#"))  # special
        self.assertFalse(bdd.check_ip("30.100.128.A"))  # upper

        self.assertFalse(bdd.check_ip("30.100.128.12:"))  # empty port
        self.assertFalse(bdd.check_ip("30.100.128.12:-60"))  # negative port
        self.assertFalse(bdd.check_ip("30.100.128.12:afdeh"))  # non numerical port
        self.assertFalse(bdd.check_ip("30.100.128.12:108:200:300"))  # many ports ':'


    def test_get_ip(self):
        # Let's add a correct user :
        key = bdd.create_random_string(64)
        self.assertEqual(bdd.bdd_add(self.test_db,"cccc", "aAaa#a9aa", "192.168.0.1:8000", key),1)
        self.assertEqual(
            bdd.bdd_get_ip_port(self.test_db,"cccc"), ("192.168.0.1", "8000")
        )  # get the good IP
        self.assertEqual(
            bdd.bdd_get_ip_port(self.test_db,"aaab"), (False, False)
        )  # bad username


if __name__ == "__main__":
    unittest.main()