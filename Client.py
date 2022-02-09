from socket import *
from Server import Server
from Massage import Massage
import threading

class Client:
    def __init__(self, name, server: Server):
        self.name = name
        self.server = server
        serverName = 'localhost'
        serverPort = server.serverPort
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((serverName, serverPort))
        sentence = "" + name
        self.socket.send(sentence.encode())
        # אם ביצענו send הטרד השני צריך לחכות שנקבל אישור
        print(self.socket.recv(1024))

    def disconnect(self):
        self.server.disconnect(self.name)
        self.socket.close()

    def send_message(self, text, dest=None):
        message = Massage(self.name, text, dest)
        sentence = repr(message)
        self.socket.send(sentence.encode())
        print(self.socket.recv(1024))

    def get_list(self):
        return self.server.get_list()


    # def get_message(self):
