import socket
from sys import argv
from threading import Thread, Lock

NUM_USERS_COUNTER = 0
NUM_USERS_COMMAND = "num_users"
lock = Lock()


def handle_client(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(f"Received: {data.decode()}")
            if data == b"exit":
                break
            conn.sendall(data)
        print("Closing connection to {addr}")
     
    lock.acquire() 
    NUM_USERS_COUNTER = NUM_USERS_COUNTER - 1
    lock.release()
        
        
def server_operator():
    while True:
        try:
            command = input("enter 'num_users' to visualize how many clients are currently connected \n")
        except:
            raise ValueError
    
        if command == NUM_USERS_COMMAND:
            print(f"number of users currently connected: {NUM_USERS_COUNTER}")
    

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
        Thread(target=server_operator).start()
        while True:
            try:
                conn, addr = s.accept()
                lock.acquire()
                NUM_USERS_COUNTER = NUM_USERS_COUNTER + 1
                lock.release()
                Thread(target=handle_client, args=(conn, addr)).start()
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    main()
