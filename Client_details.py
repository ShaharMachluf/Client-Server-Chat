from threading import Thread


class ClientD:
    def __init__(self, socket, ip, name, thread, port):
        self.socket = socket
        self.ip = ip
        self.name = name
        self.thread = thread
        self.port = port
