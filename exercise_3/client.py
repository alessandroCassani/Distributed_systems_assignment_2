import socket
from sys import argv
import Message_pb2

CLOSE_COMMAND = 'end'

def main():
    host = None
    port = None
    try:
        if len(argv) > 2:
            host = argv[1]
            port = int(argv[2])
        elif len(argv) > 1:
            port = int(argv[1])
        else:
            raise ValueError
    except:
        host = host or "127.0.0.1"
        port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to the server")
        
        handshake_response_data = s.recv(1024)
        handshake_response = Message_pb2.Handshake()
        handshake_response.ParseFromString(handshake_response_data)
        
        if handshake_response.error:
            print("Handshake failed. Closing connection.")
            return
        else:
            print(f"Handshake successful! Assigned ID: {handshake_response.id}")
        
        while True:
            try:
                data = create_object()
                
                if data.msg == CLOSE_COMMAND:
                    s.sendall(data.SerializeToString()) 
                    break
                
                s.sendall(data.SerializeToString())
                print("Message sent")
    
                msg = Message_pb2.Object()
                response = s.recv(1024)
                msg.ParseFromString(response)
                print(f"Received: {msg}")
            
            except Exception as e:
                print(f"exception: {e}")
                break
            
        print("Closing connection")


def create_object():
    while True:
        try:
            sender = int(input("Enter sender (int64): "))
            receiver = int(input("Enter receiver (int64): "))
            break  
        except ValueError:
            print("Error: only int64")
            
    msg = input("insert message: \n")
    
    obj = Message_pb2.Object()
    obj.sender = sender
    obj.receiver = receiver
    obj.msg = msg
    return obj
    
    
if __name__ == "__main__":
    main()
