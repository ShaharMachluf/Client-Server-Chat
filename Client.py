from socket import *
from Massage import Massage
import threading

class Client:
    def __init__(self, name, server):
        self.name = name
        self.lock = threading.Lock()
        serverName = server
        serverPort = 50000
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((serverName, serverPort))
        sentence = "" + name
        self.socket.send(sentence.encode())
        # see if the connection was accepted
        print(self.socket.recv(1024))
        listen = threading.Thread(target=self.get_message).start()

    def disconnect(self):
        # disconnect from server
        self.socket.send(("disconnect " + self.name + "").encode())
        self.socket.close()

    def send_message(self, text, dest=None):
        # send a message to another user or to everyone (if dest = None)
        message = Massage(self.name, text, dest)
        sentence = repr(message)
        self.socket.send(sentence.encode())
        print(self.socket.recv(1024))

    def get_list(self):
        # get a list of users from the server
        self.socket.send(("get_list " + self.name + "").encode())
        return self.socket.recv(1024)

    def get_message(self):
        # receive messages from other users
        while True:
            self.lock.acquire()
            print(self.socket.recv(1024))
            self.lock.release()
