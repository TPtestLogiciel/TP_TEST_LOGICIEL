import json
import shlex
import subprocess
import time
import unittest
from unittest.mock import MagicMock, patch

import p2p_client


class TestP2PClient(unittest.TestCase):
    user_subprocess = None

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
        # Launch client p2p subprocess, Alice user
        print("port_user_1 ", self.port_user_1)
        cmd_ground = "python3 p2p_client.py --buddy={} --port={}".format(
            self.username_2, self.port_user_1
        )
        args_ground = shlex.split(cmd_ground)
        # launch command as a subprocess
        self.user_subprocess = subprocess.Popen(args_ground)
        time.sleep(3)

    @patch("http.client.HTTPResponse")
    def test_get_ip_port(self, mock_response):
        # username_2 (Bob) wants to talk to username_1 (Alice), asks ip and port
        # to a mock server.
        expected_json_msg = {
            "username": self.username_1,
            "ip_address": self.local_ip,
            "port": self.port_user_1,
        }
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value.decode.return_value = expected_json_msg

        with patch("http.client.HTTPConnection") as HTTPConnectionMock:
            conn_server = HTTPConnectionMock()

            with patch.object(
                conn_server, "getresponse", return_value=mock_response
            ) as response:
                (msg_received, server_status, server_reason) = p2p_client.get_ip_port(
                    self.local_ip, self.server_port, self.username_1
                )
                self.assertEqual(msg_received, expected_json_msg)
                self.assertEqual(server_status, 200)
                self.assertEqual(server_reason, "OK")

    def test_send_message(self):
        # Test response and connection to server Ground with client
        # Air with a string msg
        print("port1 :", self.port_user_1)
        (data_send, server_status, server_reason) = p2p_client.send_message(
            self.msg_from_user_2, self.local_ip, self.port_user_1, self.username_1
        )
        data_send = json.loads(data_send)
        # self.assertEqual(data_send["text"], self.msg_json_user_1["text"])
        # self.assertEqual(data_send["username"], self.msg_json_user_1["username"])
        # self.assertEqual(data_send, self.msg_json_user_1)
        # self.assertEqual(server_status, 200)
        # self.assertEqual(server_reason, "OK")

    #     # Test response and connection to server Ground with client
    #     # Air with an int msg
    #     (data_send, server_status, server_reason) = p2p_client.send_message(
    #         123456789, self.ip_address, self.port_user_2, self.user_1
    #     )
    #     data_send = json.loads(data_send)
    #     self.assertNotEqual(data_send["text"], self.msg_json_air["text"])
    #     self.assertEqual(data_send["text"], 123456789)
    #     self.assertEqual(data_send["username"], self.msg_json_air["username"])
    #     self.assertNotEqual(data_send, self.msg_json_air)
    #     self.assertEqual(server_status, 200)
    #     self.assertEqual(server_reason, "OK")

    #     # Test response and connection to server Ground with client
    #     # Air with an empty string
    #     (data_send, server_status, server_reason) = p2p_client.send_message(
    #         "", self.ip_address, self.port_user_2, self.user_1
    #     )
    #     data_send = json.loads(data_send)
    #     self.assertEqual(data_send["text"], "")
    #     self.assertEqual(data_send["username"], self.msg_json_air["username"])
    #     self.assertEqual(server_status, 200)
    #     self.assertEqual(server_reason, "OK")

    #     # Test response and connection to server Ground with client
    #     # Air with a dictionnary
    #     (data_send, server_status, server_reason) = p2p_client.send_message(
    #         self.msg_json_air, self.ip_address, self.port_user_2, self.user_1
    #     )
    #     data_send = json.loads(data_send)
    #     dico_msg = {
    #         "username": self.user_1,
    #         "text": {"username": self.user_1, "text": self.msg_from_air},
    #     }
    #     dico_msg = json.dumps(dico_msg)
    #     dico_msg = json.loads(dico_msg)
    #     self.assertEqual(data_send["text"], dico_msg["text"])
    #     self.assertNotEqual(data_send["text"], self.msg_json_air["text"])
    #     self.assertEqual(data_send["username"], self.msg_json_air["username"])
    #     self.assertEqual(data_send["text"]["username"], self.msg_json_air["username"])
    #     self.assertEqual(server_status, 200)
    #     self.assertEqual(server_reason, "OK")

    #     # Test response and connection to server Ground with client
    #     # Air with a list
    #     list_msg = ["bonjour", "comment tu vas?", 4, "byebye", 8]
    #     (data_send, server_status, server_reason) = p2p_client.send_message(
    #         list_msg, self.ip_address, self.port_user_2, self.user_1
    #     )
    #     data_send = json.loads(data_send)
    #     self.assertEqual(data_send["text"], list_msg)
    #     self.assertEqual(data_send["text"][0], list_msg[0])
    #     self.assertNotEqual(data_send["text"][2], list_msg[0])
    #     self.assertEqual(data_send["text"][2], list_msg[2])
    #     self.assertNotEqual(data_send["text"], self.msg_json_air["text"])
    #     self.assertEqual(data_send["username"], self.msg_json_air["username"])
    #     self.assertEqual(server_status, 200)
    #     self.assertEqual(server_reason, "OK")

    def tearDown(self):
        print("killing subprocess user_server")
        self.user_subprocess.kill()
        self.user_subprocess.wait()


if __name__ == "__main__":
    unittest.main()
