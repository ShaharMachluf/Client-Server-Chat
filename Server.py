from socket import *
from Client_details import ClientD
from threading import Thread
from Massage import Massage
from concurrent import futures

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

    # def listen(self):

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
        message = Massage("server", name+ " disconnect")
        self.send_message(message)

if __name__ == '__main__':
    server = Server()
    for i in range(16):
        server.port_dict[server.first_port + i] = None
    while True:
        freePort = 0
        for i in server.port_dict.keys():
            if server.port_dict[i] is None:
                freePort = i
                break
        if freePort == 0:
            continue
        connectionSocket, addr = server.serverSocket.accept()
        name = connectionSocket.recv(1024).decode()
        if name in server.name_dict:
            sentence = "this name is taken"
            connectionSocket.send(bytes(sentence.encode()))
            continue
        thread = Thread(target= ).start()
        client = ClientD(connectionSocket, addr, name, thread, freePort)
        server.port_dict[freePort] = client
        server.name_dict[name] = client
        sentence = "connection received"
        connectionSocket.send(bytes(sentence.encode()))
        message = Massage("server", name+ " is connected")
        server.send_message(message)
    server.serverSocket.close()


