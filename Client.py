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
        self.serverName = server
        serverPort = 50001
        self.udp_serverPort = 50002
        while flag:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.serverName, serverPort))
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
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
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

    def get_files(self):
        self.socket.send(bytes(("get_files " + self.name + "").encode()))

    def request_file(self):
        SEPARATOR = "<SEPARATOR>"
        file = easygui.enterbox("enter file name:", "file")
        self.socket.send(bytes(("file " + file + " " + self.name + "").encode()))  # request a file
        time.sleep(1)  # wait for the server to be ready
        self.udp_socket.sendto("ok".encode(), (self.serverName, self.udp_serverPort))  # open udp connection
        ack = 0
        with open(file, "wb") as f:
            while True:
                massage, address = self.udp_socket.recvfrom(64000)
                massage = massage.decode()
                if massage == "the file sent successfully":  # finished sending file
                    easygui.msgbox("the file sent successfully", "file")
                    return
                data, seq = massage.split(SEPARATOR)
                if int(seq) == ack:
                    f.write(data.encode())  # write to the file
                    self.udp_socket.sendto(str(ack).encode(), (self.serverName, self.udp_serverPort))  # ack
                    ack += 1

    def get_message(self):
        # receive messages from other users
        while self.listen:
            self.lock.acquire()
            try:
                massage = self.socket.recv(1024).decode()
                if massage != "":
                    if massage == 'you like to proceed?':
                        bool = easygui.ynbox(massage, "file", ['Yes', 'No'])
                        if bool:
                            self.udp_socket.sendto("yes".encode(), (self.serverName, self.udp_serverPort))
                    else:
                        easygui.msgbox("you got new massage:\n" + massage, "new massage")
                self.lock.release()
            except OSError:
                break
