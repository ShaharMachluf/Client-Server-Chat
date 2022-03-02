# Network-final_project
<img width="497" alt="2022-03-02 (2)" src="https://user-images.githubusercontent.com/85555432/156410028-c356fc7d-1cac-47ff-939d-6cffacca16b6.png">  

## About the Project
In this project we created a program that function as a messanger.  
This project includes a server and a client, you can run as many clients as you like and they will connect to the server.  
One of the things we did in this program is creating RDT over UDP with congestion control when the client downloads a file from the server. 

## The Main Classes
### Server
In this class we implemented the server side of the program.  
The server has number of threads:  
- The main thread runs the server's GUI.
- A thread that runs the function "start" that is responsible to listen to connection requests from clients (TCP).
- When a client is connected to the server, a thread starts running the function "listen" which is responsible to listening to requests that come from that certain client and takes care of them.
### Client
In this class we implemented the client side of the program.  
A client is able to connect to the server (TCP), recieve messages(TCP), get a list of the clients that are connected to the server (TCP), send messages to other clients (TCP), disconnect from the server, get a list of the files in the server (TCP), request a file from the server (TCP) and download is (UDP).  
The client has to threads:
- The main thread runs the client's GUI and from there the client can do all of the actions that are listed above.
- A thread that runs "get_message" which is responsible to listen to incoming messages from the server and other clients.

## How to Run
First, because this program is using the libraries "pygame" and "easygui" you need to make sure you have them installed on your computer in order for this program to work. If you don't, this is how to install them:  
**Windows**  
pip install easygui  
pip install pygame  
**Ubuntu**  
sudo apt-get install python3-pygame  
sudo apt-get install python3-easygui

Now, in order to activate the chat you have to first run the file "Server.py" in order to activate the server.  
After running it a window will apear with the button "start" - pressing the button will open the server's socket to connections.  
Afterwards, in order to activate the client you'll need to run the file "client_gui.py" and connect to the server by pressing the "log in" button.  
After the connection other buttons will appear and with them the client can to all the actions that are detailed above.  
(If you want to run other clients you just have to run "client_gui.py" again).
