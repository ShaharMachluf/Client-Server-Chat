import socket
import threading
from socket import *
from Client_details import ClientD
from threading import Thread
from Massage import Massage
from server_gui import ServerGUI


class Server:
    def __init__(self):
        self.serverPort = 50000
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('127.0.0.1', self.serverPort))
        self.serverSocket.listen(1000)
        print("the server is ready to receive")
        self.port_dict = {}
        self.name_dict = {}
        self.first_port = 55000
        self.serverSocket.settimeout(3)
        self.lock = threading.Lock()

    # this function works as the listener to the clients
    def listen(self):
        while len(self.name_dict) > 0:
            self.lock.acquire()
            data = self.serverSocket.recv(1024).decode()
            list1 = data.split()  # todo: check \n
            if list1[0] == "disconnect":
                self.disconnect(data[1])
                continue
            if list1[0] == "get_list":
                name_list = self.get_list()
                sock = self.name_dict[list1[1]].socket
                sock.send(bytes(str(name_list).encode()))
                continue
            text = ""
            for i in range(4, len(list1)):
                text = text + list1[i] + " "
            message = Massage(list1[1], text, list1[3])
            self.send_message(message)
            self.lock.release()

    # this function return the list of all the users.
    def get_list(self) -> []:
        name_list = []
        for i in self.port_dict.values():
            name_list.append(i.name)
        return name_list

    # this function get a message and sent it to the destination.
    def send_message(self, message):
        dest = message.dest
        if dest is None:
            sentence = repr(message)
            for i in self.name_dict.values():
                sock = i.socket
                sock.send(bytes(sentence.encode()))
            src = message.src
            sock = self.name_dict[src].socket
            sentence2 = "the message sent"
            sock.send(bytes(sentence2.encode()))
            return
        if dest not in self.name_dict:
            src = message.src
            sock = self.name_dict[src].socket
            sentence = "this destination does not exist"
            sock.send(bytes(sentence.encode()))
            return
        sock = self.name_dict[dest].socket
        sentence = repr(message)
        sock.send(bytes(sentence.encode()))
        src = message.src
        sock = self.name_dict[src].socket
        sentence2 = "the message sent"
        sock.send(bytes(sentence2.encode()))

    # this function disconnect the client
    def disconnect(self, name):
        port = self.name_dict[name].port
        self.name_dict[name].socket.close()
        self.name_dict.pop(name)
        self.port_dict[port] = None
        message = Massage("server", name + " disconnected")
        self.send_message(message)


def start(gui: ServerGUI):
    while True:
        if gui.button_start.is_pressed:
            server = Server()
            for i in range(16):
                server.port_dict[server.first_port + i] = None
            thread = Thread(target=server.listen).start()
            while gui.button_start.is_pressed:
                freePort = 0
                for i in server.port_dict.keys():
                    if server.port_dict[i] is None:
                        freePort = i
                        break
                if freePort == 0:
                    print("connection was not accepted")
                    continue
                try:
                    connectionSocket, addr = server.serverSocket.accept()
                except Exception:
                    continue
                name = connectionSocket.recv(1024).decode()
                if name in server.name_dict:
                    sentence = "this name is taken"
                    connectionSocket.send(bytes(sentence.encode()))
                    continue
                client = ClientD(connectionSocket, addr, name, freePort)
                server.port_dict[freePort] = client
                server.name_dict[name] = client
                sentence = "connection received"
                connectionSocket.send(bytes(sentence.encode()))
                message = Massage("server", name + " is connected")
                server.send_message(message)
            server.serverSocket.close()
            print("the server is closed")


if __name__ == '__main__':
    gui = ServerGUI()
    # gui_thread = threading.Thread(target=gui.display).start()
    server_thread = threading.Thread(target=start, args=[gui]).start()
    gui.display()
