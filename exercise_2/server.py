import socket
from sys import argv
from threading import Thread
import Object_pb2

def handle_client(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            object = Object_pb2.Object()
            data = conn.recv(1024)
            
            object.ParseFromString(data)
            print(f"Received: {object}")
            
            if object.msg == b"end":
                break
            conn.sendall(object.SerializeToString())
        print("Closing connection to {addr}")


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
        
        while True:
            try:
                conn, addr = s.accept()
                Thread(target=handle_client, args=(conn, addr)).start()
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
    
