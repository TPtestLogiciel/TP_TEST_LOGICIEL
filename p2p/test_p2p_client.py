import json
import shlex
import subprocess
import time
import unittest
from unittest.mock import MagicMock, patch

import p2p_client


class TestP2PClient(unittest.TestCase):
    user_subprocess = None
    server_subprocess = None

    username_1 = "Alice"
    username_2 = "Bob"
    port_user_1 = 8001
    port_user_2 = 8002
    msg_from_user_1 = "Hello Bob, it's a message from Alice!"
    msg_json_user_1 = {"username": username_2, "text": msg_from_user_1}
    msg_from_user_2 = "Hi Alice, it's a message from Bob!"
    msg_json_user_2 = {"username": username_1, "text": msg_from_user_2}

    local_ip = "0.0.0.0"
    server_port = 8000

    def setUp(self):
        # Launch server subprocess
        cmd_server = "python3 server.py"
        args_server = shlex.split(cmd_server)
        # launch command as a subprocess
        self.server_subprocess = subprocess.Popen(args_server)
        time.sleep(3)

        # Launch client p2p subprocess, Alice user
        cmd_client = "python3 p2p_client.py --buddy={} --port={}".format(
            self.username_2, self.port_user_1
        )
        args_client= shlex.split(cmd_client)
        # launch command as a subprocess
        self.user_subprocess = subprocess.Popen(args_client)
        time.sleep(3)


    def test_send_message(self):
        # Test Bob's client part, wants to talk to Alice user with a json msg
        (data_send, server_status, server_reason) = p2p_client.send_message(
            self.msg_from_user_2, self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["text"], self.msg_json_user_2["text"])
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertEqual(data_send, self.msg_json_user_2)
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

        # Test response and connection to Alice (server part) with client
        # Bob with an int msg
        (data_send, server_status, server_reason) = p2p_client.send_message(
            123456789, self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertNotEqual(data_send["text"], self.msg_json_user_2["text"])
        self.assertEqual(data_send["text"], 123456789)
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertNotEqual(data_send, self.msg_json_user_2)
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

        # Test response and connection to Alice (server part) with client
        # Bob with an empty string
        (data_send, server_status, server_reason) = p2p_client.send_message(
            "", self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["text"], "")
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

        # Test response and connection to Alice (server part) with client
        # Bob with a dictionnary
        (data_send, server_status, server_reason) = p2p_client.send_message(
            self.msg_json_user_2, self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        dico_msg = {
            "username": self.username_1,
            "text": {"username": self.username_1, "text": self.msg_from_user_2},
        }
        dico_msg = json.dumps(dico_msg)
        dico_msg = json.loads(dico_msg)
        self.assertEqual(data_send["text"], dico_msg["text"])
        self.assertNotEqual(data_send["text"], self.msg_json_user_2["text"])
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertEqual(data_send["text"]["username"], self.msg_json_user_2["username"])
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

        # Test response and connection to Alice (server part) with client
        # Bob with a list
        list_msg = ["bonjour", "comment tu vas?", 4, "byebye", 8]
        (data_send, server_status, server_reason) = p2p_client.send_message(
            list_msg, self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        self.assertEqual(data_send["text"], list_msg)
        self.assertEqual(data_send["text"][0], list_msg[0])
        self.assertNotEqual(data_send["text"][2], list_msg[0])
        self.assertEqual(data_send["text"][2], list_msg[2])
        self.assertNotEqual(data_send["text"], self.msg_json_user_2["text"])
        self.assertEqual(data_send["username"], self.msg_json_user_2["username"])
        self.assertEqual(server_status, 200)
        self.assertEqual(server_reason, "OK")

    def tearDown(self):
        print("killing subprocess user")
        self.user_subprocess.kill()
        self.user_subprocess.wait()
        print("killing subprocess server")
        self.server_subprocess.kill()
        self.server_subprocess.wait()


if __name__ == "__main__":
    unittest.main()
