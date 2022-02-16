from socket import *
from Massage import Massage
import threading
import easygui
import time


class Client:
    def __init__(self, name, server):
        flag = True
        self.listen = True
        self.name = name
        self.lock = threading.Lock()
        serverName = server
        serverPort = 50001
        while flag:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((serverName, serverPort))
            sentence = "" + self.name
            self.socket.send(bytes(sentence.encode()))
            # see if the connection was accepted
            text = self.socket.recv(1024).decode()
            easygui.msgbox(text, "connection to server")
            if text == "this name is taken, try again":
                self.socket.close()
                self.name = easygui.enterbox("enter your user name:", "Log in")
            else:
                flag = False
        threading.Thread(target=self.get_message).start()

    def disconnect(self):
        # disconnect from server
        self.socket.send(bytes(("disconnect " + self.name + "").encode()))
        time.sleep(3)
        self.socket.close()
        self.listen = False

    def send_message(self, text, dest=None):
        # send a message to another user or to everyone (if dest = None)
        message = Massage(self.name, text, dest)
        sentence = repr(message)
        self.socket.send(bytes(sentence.encode()))
        return sentence

    def get_list(self):
        # get a list of users from the server
        self.socket.send(bytes(("get_list " + self.name + "").encode()))

    def get_message(self):
        # receive messages from other users
        while self.listen:
            self.lock.acquire()
            try:
                massage = self.socket.recv(1024).decode()
                if massage != "":
                    easygui.msgbox("you got new massage:\n" + massage, "new massage")
                self.lock.release()
            except OSError:
                break
