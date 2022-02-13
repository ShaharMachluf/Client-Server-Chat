import sys
from client_gui import ClientGUI
if __name__ == '__main__':
    list_args = sys.argv
    num_of_clients = list_args[1]
    num = int(num_of_clients)
    # todo: open gui for any client
    for i in range(num):
        ClientGUI()
