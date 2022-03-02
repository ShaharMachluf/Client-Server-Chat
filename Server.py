import socket
import threading
import os
import time
from socket import *

import easygui

from Client_details import ClientD
from threading import Thread
from Massage import Massage
from server_gui import ServerGUI


class Server:
    def __init__(self):
        self.serverPort = 50001
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', self.serverPort))
        self.serverSocket.listen(1000)
        self.udpPort = 50002
        self.udpSocket = socket(AF_INET, SOCK_DGRAM)
        self.udpSocket.bind(('', self.udpPort))
        self.udpPort2 = 50003
        self.udpSocket2 = socket(AF_INET, SOCK_DGRAM)
        self.udpSocket2.bind(('', self.udpPort2))
        print("the server is ready to receive")
        self.port_dict = {}
        self.name_dict = {}
        self.first_port = 55000
        self.ack_list = []
        self.serverSocket.settimeout(3)
        self.udpSocket.settimeout(0.2)
        self.file_list = ["1mb.txt", "project.pdf", "HelloWorld.html"]

    # this function works as the listener to the clients
    def listen(self, socket, name, lock):
        while True:
            if name not in self.name_dict.keys():  # user is disconnected
                break
            lock.acquire()
            try:
                data = socket.recv(1024).decode()
            except Exception:
                lock.release()
                continue
            list1 = data.split()
            if list1[0] == "disconnect":
                self.disconnect(list1[1])
                break
            if list1[0] == "get_files":
                files = self.get_files()
                sock = self.name_dict[list1[1]].socket
                sock.send(bytes(str(files).encode()))
                lock.release()
                continue
            if list1[0] == "file":
                self.send_file(list1[1], name)
                lock.release()
                continue
            if list1[0] == "get_list":
                name_list = self.get_list()
                sock = self.name_dict[list1[1]].socket
                sock.send(bytes(str(name_list).encode()))
                lock.release()
                continue
            text = ""  # this is a message that needs to be sent
            for i in range(4, len(list1)):
                text = text + list1[i] + " "
            message = Massage(list1[1], text, list1[3])
            self.send_message(message)
            lock.release()

    def get_files(self):
        return self.file_list

    # this function return the list of all the users.
    def get_list(self) -> []:
        name_list = []
        for i in self.name_dict.keys():
            name_list.append(i)
        return name_list

    # this function get a message and sent it to the destination.
    def send_message(self, message):
        dest = message.dest
        if dest == "all":
            sentence = repr(message)
            for i in self.name_dict.values():  # send to everyone
                sock = i.socket
                sock.send(bytes(sentence.encode()))
            src = message.src
            if src != "server":  # let the sender know that his message was sent successfully
                sock = self.name_dict[src].socket
                sentence2 = "the message sent"
                sock.send(bytes(sentence2.encode()))
            return
        if dest not in self.name_dict.keys():
            src = message.src
            sock = self.name_dict[src].socket
            sentence = "this destination does not exist"
            sock.send(bytes(sentence.encode()))
            return
        sock = self.name_dict[dest].socket
        sentence = repr(message)
        sock.send(bytes(sentence.encode()))
        src = message.src
        if src != "server":
            sock = self.name_dict[src].socket
            sentence2 = "the message sent"  # let the sender know that his message was sent successfully
            sock.send(bytes(sentence2.encode()))

    def send_file(self, file, name):
        while True:
            try:
                connection, address = self.udpSocket.recvfrom(1024)  # receive client's socket details
            except Exception:
                continue
            if connection.decode() != "":
                break
        if file not in self.file_list:  # check if file exist
            self.udpSocket.sendto("this file not exist".encode(), address)
            return
        SEPARATOR = "<SEPARATOR>"
        sent = 0
        wnd_size = 1
        PACKET_SIZE = 63000
        file_size = os.path.getsize("files/" + file)
        packet_list = []
        end_wnd = 0
        with open("files/" + file, "rb") as f:
            for i in range(file_size):  # separate the file to packets
                outputdata = f.read(PACKET_SIZE)
                if not outputdata:
                    break
                packet_list.append(outputdata)
            ssthresh = len(packet_list)
            while sent < len(packet_list)/2:  # send 50% of the file
                threading.Thread(target=self.ack_listener, args=[wnd_size, sent]).start()  # follow the acks
                for j in range(wnd_size):
                    try:
                        self.udpSocket.sendto(packet_list[sent] + SEPARATOR.encode() + str(sent).encode(),
                                          address)
                    except Exception:
                        j -= 1
                        continue
                    sent += 1
                time.sleep(0.2)
                if -1 in self.ack_list:  # timeout
                    sent = self.ack_list.index(-1) + end_wnd
                    ssthresh = wnd_size
                    wnd_size = 1
                elif -2 in self.ack_list:  # wrong sequence
                    sent = self.ack_list.index(-2) + end_wnd
                    ssthresh = wnd_size
                    wnd_size = max(1, int(wnd_size/2))
                else:
                    end_wnd += wnd_size
                    if (wnd_size*2) < ssthresh:  # slow start
                        wnd_size *= 2
                    else:  # congestion avoidance
                        wnd_size += 1
            self.udpSocket2.sendto('sent 50%, you like to proceed?'.encode(),
                                  address)
            while True:
                try:
                    answer, address = self.udpSocket2.recvfrom(1024)
                    break
                except Exception:
                    continue
            answer2 = answer.decode()
            if answer2 != "yes":
                self.udpSocket.sendto("stop".encode(), address)
                return
            wnd_size = 1
            while sent < len(packet_list):  # send the rest of the file
                threading.Thread(target=self.ack_listener, args=[wnd_size, sent]).start()
                for j in range(wnd_size):
                    try:
                        self.udpSocket.sendto(packet_list[sent] + SEPARATOR.encode() + str(sent).encode(),
                                          address)
                    except Exception:
                        j -= 1
                        continue
                    sent += 1
                    if sent >= len(packet_list):
                        break
                time.sleep(0.2)
                if -1 in self.ack_list:
                    sent = self.ack_list.index(-1) + end_wnd
                    ssthresh = wnd_size
                    wnd_size = 1
                elif -2 in self.ack_list:
                    sent = self.ack_list.index(-2) + end_wnd
                    ssthresh = wnd_size
                    wnd_size = max(1, int(wnd_size/2))
                else:
                    end_wnd += wnd_size
                    if (wnd_size * 2) < ssthresh:
                        if (wnd_size*2 + sent) > len(packet_list):
                            wnd_size = len(packet_list) - sent
                        else:
                            wnd_size *= 2
                    else:
                        wnd_size += 1
            self.udpSocket.sendto("the file sent successfully".encode(),
                                  address)

    # listen to acks from the client
    def ack_listener(self, size, sent):
        self.ack_list = [0] * size
        acked = sent + 1
        for i in range(size):
            try:
                ack, address = self.udpSocket.recvfrom(1024)
                self.ack_list[i] = int(ack.decode())
                if self.ack_list[i] != acked:
                    self.ack_list[i] = -2
                    return
                acked += 1
            except Exception:  # timeout
                self.ack_list[i] = -1
                return

    # this function disconnect the client
    def disconnect(self, name):
        message1 = Massage("server", "you are disconnected", name)
        self.send_message(message1)
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
                server.port_dict[server.first_port + i] = None  # init all the ports
            while gui.button_start.is_pressed:
                freePort = 0
                for i in server.port_dict.keys():  # check if there is a free port
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
                if name in server.name_dict.keys():
                    sentence = "this name is taken, try again"
                    connectionSocket.send(bytes(sentence.encode()))
                    continue
                client = ClientD(connectionSocket, addr, name, freePort)
                server.port_dict[freePort] = client
                server.name_dict[name] = client
                lock = threading.Lock()
                # open thread that listens to this client
                thread = threading.Thread(target=server.listen, args=[connectionSocket, name, lock]).start()
                sentence = "connection received"
                connectionSocket.send(bytes(sentence.encode()))
                message = Massage("server", name + " is connected")
                server.send_message(message)
            for i in server.name_dict.keys():
                massage =Massage("server", "server is disconnected, please press \"log out\"", i)
                server.send_message(massage)
            time.sleep(3)
            server.serverSocket.close()
            print("the server is closed")
            exit(0)


if __name__ == '__main__':
    gui = ServerGUI()
    server_thread = threading.Thread(target=start, args=[gui]).start()
    gui.display()
