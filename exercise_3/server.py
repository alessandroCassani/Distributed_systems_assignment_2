import socket
from sys import argv
from threading import Thread, Lock
import Message_pb2

CLOSE_COMMAND = 'end'
NUM_USERS_COMMAND = "num_users"
lock = Lock()
user_counter = 0
id = 0

def server_operator():
    while True:
        try:
            command = input("enter 'num_users' to visualize how many clients are currently connected \n")
        except:
            raise ValueError
    
        if command == NUM_USERS_COMMAND:
            print(f"number of users currently connected: {get_clients_number()}")

def handle_client(conn, addr):
    try:
        id_client = add_client()
    
        with conn:
            print(f"Connected by {addr}")
            
            handshake = create_handshake_message(id_client)
            serialized_handshake_message = handshake.SerializeToString()
            conn.sendall(serialized_handshake_message)
        
            while True:
                object = Message_pb2.Object()
                data = conn.recv(1024)
                object.ParseFromString(data)
                print(f"Received: {object}")
                
                if object.msg == CLOSE_COMMAND:
                    break
                
                conn.sendall(object.SerializeToString())
                x
            print(f"Closing connection to {addr}")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        handshake_response = Message_pb2.Handshake()
        handshake_response.error = True
        conn.sendall(handshake_response.SerializeToString())
        
    finally:
        remove_client()


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
        Thread(target=server_operator, args =()).start()
        while True:
            try:
                conn, addr = s.accept()
                Thread(target=handle_client, args=(conn, addr)).start()
            except KeyboardInterrupt:
                break

def create_handshake_message(id_client):
    handshake = Message_pb2.Handshake()
    handshake.id = id_client
    handshake.error = False
    return handshake
    
def add_client():
    global user_counter
    global id
    
    lock.acquire()
    id +=1
    user_counter += 1
    lock.release()
    
    return id

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
