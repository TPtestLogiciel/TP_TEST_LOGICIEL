import json
import shlex
import subprocess
import time
import unittest
from unittest.mock import patch, MagicMock

import p2p_client


class TestP2PClient(unittest.TestCase):
    user_subprocess = None

    port_user_1 = "8001"
    port_user_2 = "8002"
    server_ip = "0.0.0.0"
    server_port = 8000

    username_1 = "Ground"
    username_2 = "Air"
    msg_from_ground = "Hello Air, it's a message from Ground!"
    msg_from_air = "Hi Ground, it's a message from Air!"
    msg_json_air = {"username": username_1, "text": msg_from_air}

    # def setUp(self):
        # Launch client p2p subprocess
        # cmd_ground = "python3 p2p_client.py --buddy={} ".format(self.username_2)
        # args_ground = shlex.split(cmd_ground)
        # launch command as a subprocess
        # self.user_subprocess = subprocess.Popen(args_ground)
        # time.sleep(3)

    @patch("http.client.HTTPResponse")
    def test_get_ip_port(self, mock_response):
        expected_json_msg = {"username" : self.username_1, "ip_address" : self.server_ip, "port" : self.server_port}
        mock_response.status = 200
        mock_response.reason = "OK"
        mock_response.read.return_value.decode.return_value = expected_json_msg

        with patch("http.client.HTTPConnection") as HTTPConnectionMock:
            conn_server = HTTPConnectionMock()

            with patch.object(conn_server, "getresponse", return_value=mock_response) as response:
                (msg_received, server_status, server_reason) = p2p_client.get_ip_port(self.server_ip, self.server_port, self.username_1)

                self.assertEqual(msg_received, expected_json_msg)
                self.assertEqual(server_status, 200)
                self.assertEqual(server_reason, "OK")


    # def test_send_message(self):
    #     # Test response and connection to server Ground with client
    #     # Air with a string msg
    #     (data_send, server_status, server_reason) = p2p_client.send_message(
    #         self.msg_from_air, self.ip_address, self.port_user_2, self.user_1
    #     )
    #     data_send = json.loads(data_send)
    #     self.assertEqual(data_send["text"], self.msg_json_air["text"])
    #     self.assertEqual(data_send["username"], self.msg_json_air["username"])
    #     self.assertEqual(data_send, self.msg_json_air)
    #     self.assertEqual(server_status, 200)
    #     self.assertEqual(server_reason, "OK")

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


    # def tearDown(self):
    #     print("killing subprocess user_server")
    #     self.user_subprocess.kill()
    #     self.user_subprocess.wait()


if __name__ == "__main__":
    unittest.main()
