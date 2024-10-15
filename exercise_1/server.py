import socket
from sys import argv
from threading import Thread, Lock

NUM_USERS_COMMAND = "num_users"
lock = Lock()
user_counter = 0


def handle_client(conn, addr):
    add_client()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(f"Received: {data.decode()}")
            if data == b"end":
                break
            conn.sendall(data)
        print("Closing connection to {addr}")
     
    remove_client()
        
        
def server_operator():
    while True:
        try:
            command = input("enter 'num_users' to visualize how many clients are currently connected \n")
        except:
            raise ValueError
    
        if command == NUM_USERS_COMMAND:
            print(f"number of users currently connected: {get_clients_number()}")
    

def main():
    try:
        port = int(argv[1])
    except:
        port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        print(f"Server started on port {port}")
        print("Waiting for a client...")
        s.listen()
        
        Thread(target=server_operator, daemon=True).start()
        
        while True:
            try:
                conn, addr = s.accept()
                Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            except KeyboardInterrupt:
                break

def add_client():
    global user_counter
    lock.acquire()
    user_counter += 1
    lock.release()

def remove_client():
    global user_counter
    lock.acquire()
    user_counter -= 1
    lock.release()
    
def get_clients_number():
    global user_counter
    return user_counter
    
if __name__ == "__main__":
    main()
