import socket
from sys import argv
import Object_pb2


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
        
        while True:
            try:
                msg = input("insert message \n")
                data = create_object(msg)
            except:
                data = create_object('end')
                
            s.sendall(data.SerializeToString())
            print("Message sent")
            if data.msg == "end":
                break
            
            obj = Object_pb2.Object()
            response = s.recv(1024)
            obj.ParseFromString(response)
            print(f"Received: {obj}")
        print("Closing connection")


def create_object(msg):
    obj = Object_pb2.Object()
    obj.sender = 1
    obj.receiver = 2
    obj.msg = msg
    return obj
    
    
if __name__ == "__main__":
    main()
