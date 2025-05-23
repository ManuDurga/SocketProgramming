import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())#Automatically gets IP for server
ADDR = (SERVER,PORT)#address format 
FORMAT = 'utf-8'
#utf-8 is used to encode because it formats the string into its ascii value,
#further converted in binary form.
DISCONNECT_MESSAGE = "!DISCONNECT"
TALK_MESSAGE="!TALK"
T_bool=False

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#socket construction
server.bind(ADDR)
def handle_client(conn, addr):
    global T_bool
    print(f"\nNEW CONNECTION {addr} connected.")
    connected = True
    while connected:
        message = conn.recv(HEADER).decode(FORMAT)
        msg_length=len(message)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"{addr} {msg.rstrip()}")
            conn.send("MESSAGE RECEIVED".encode(FORMAT))
            if msg == TALK_MESSAGE:
                print(msg)
                T_bool=True
                talk(conn,addr)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
    conn.close()
    print(f"DISCONNECTING {addr[0]}....")
def send(conn,msg):
    message = msg.encode(FORMAT)
    msg_length =len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length = send_length + b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
def receive(conn):
    global T_bool
    message = conn.recv(HEADER).decode(FORMAT)
    msg_length=len(message)
    if msg_length:
        msg_length = int(msg_length)
        msg=conn.recv(HEADER).decode(FORMAT)
        print(msg)
        if msg.lower()=='talk over':
            print(msg.upper())
        return msg.lower()

def talk(conn,addr):
    global T_bool
    print("TALK MODE")
    while T_bool:
        if receive(conn)=="talk over":
            T_bool=False
            return
        msg=input("ENTER: ")
        send(conn,msg)
    
def start():
    server.listen()
    print(f"LISTENING, the server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"\nACTIVE CONNECTION ,{threading.active_count()-2}")
        
#each time handle_client as a thread is started it is because a new client has connected
#Threading is used to branch out the flow of the code from the main code to just a function,
#optimal in handling multiple clients for a single server 
print("STARTING, the server is starting...")
start() 
