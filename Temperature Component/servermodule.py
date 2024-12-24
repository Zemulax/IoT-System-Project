
import socket
import sys
import time
import select
import threading

host = '10.69.79.139'
port = 12345

def server():
    """opens up connection to clients

    Returns:
        string: file contents received from client
    """
    print("server initiated")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind((host, port))
        serversocket.listen(5)
        print("server is listening for connections")
        
        
        connection, address = serversocket.accept()
        print(f"connection established through{address}")
        
        with connection:
            command_thread = threading.Thread(target=send_commands, args=(connection,)) #command thread
            command_thread.daemon = True
            command_thread.start()
            
            
            while True:
                #receive the data size
                data_size = int.from_bytes(connection.recv(4), byteorder="big")
                
                #receive the file
                data = connection.recv(data_size).decode('utf-8')
                
    return data

def send_commands(connection):
    """sends a command to the client

    Args:
        connection (socket): the client socket to send data through
    """
    
    while True:
        #print("Press t to adjust the threshold")
        key, _, _ = select.select([sys.stdin], [], [], 0.1)
        if key:
            user_input = sys.stdin.read(1)
            if user_input == "t":
                try:
                    new_threshold = input("Enter new threshold: ").strip()
                    if new_threshold.isdigit():
                        threshold_value = str(new_threshold)
                        connection.sendall(threshold_value.encode('utf-8'))
                        time.sleep(30)
                    else:
                        print("please enter a number less than 40")
                except Exception as e:
                    print(f"error while setting threshold: {e}")
    

def record_client_report():
    """records the data received from client
    """
    with open("client_reported", 'w') as file:
        x = server()
        file.write(x)

def main():
    record_client_report()

if __name__ == '__main__':
    main()