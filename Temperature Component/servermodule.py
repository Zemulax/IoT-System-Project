
import socket

host = '10.69.79.139'
port = 12345

def server():
    print("server initiated")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind((host, port))
        serversocket.listen(5)
        print("server is listening for connections")
        
        connection, address = serversocket.accept()
        with connection:
            print(f"connection established through{address}")
            while True:
                #receive the data size
                data_size = int.from_bytes(connection.recv(4), byteorder="big")
                
                #receive the file
                data = connection.recv(data_size).decode('utf-8')
                
                if data:
                    print(f"Received data: {data}")
                else:
                    print("failed to receive data")
    return data

def record_client_report():
    with open("client_reported", 'w') as file:
        x = server()
        file.write(x)

def main():
    record_client_report()

if __name__ == '__main__':
    main()