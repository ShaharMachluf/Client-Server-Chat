from unittest import TestCase

from Client import Client
from Server import Server


class TestClient(TestCase):
    # in order to do these tests you need to run the server

    def test_send_message(self):
        client1 = Client("Shahar", "localhost")
        client2 = Client("Chen", "localhost")
        sentence = client1.send_message("hello", "Chen")
        self.assertEqual(sentence, "from: Shahar to: Chen \nhello")

    def test_get_list(self):
        server = Server()
        server.name_dict["Shahar"] = 55000
        server.name_dict["Chen"] = 55001
        expected = ["Shahar", "Chen"]
        received = server.get_list()
        self.assertEqual(expected, received)

    def test_disconnect(self):
        client1 = Client("Shahar", "localhost")
        client2 = Client("Chen", "localhost")
        client1.disconnect()
        client2.send_message("hello", "Shahar")  # need to show "this destination does not exist"
