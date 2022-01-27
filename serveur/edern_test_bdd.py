import random
import string
import unittest

import edern_bdd

class test_bdd_srv(unittest.TestCase):

    def create_random_string(self, n):
        return "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation, k=n
            )
        )

    def test_get_ip(self):
        # Let's add a correct user :
        key = self.create_random_string(64)
        self.assertTrue(edern_bdd.bdd_add("cccc", "aAaa#a9aa", "192.168.0.1:8000", key))
        self.assertEqual(edern_bdd.bdd_get_ip_port("cccc"),("192.168.0.1", "8000")) # get the good IP
        self.assertEqual(edern_bdd.bdd_get_ip_port("aaab"),(False, False)) # bad username

if __name__ == "__main__":
    unittest.main()