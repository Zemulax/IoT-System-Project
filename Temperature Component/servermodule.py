
import socket
import sys
import time
import select
import threading
import os

host = '10.69.79.139'
port = 12345
FOLDER = "datalogs"
CLIENT_DATA_FILE = os.path.join(FOLDER, "client_data_report.log")

if not os.path.exists(FOLDER):
    os.makedirs(FOLDER) 

def server():
    """opens up connection to clients

    Returns:
        string: file contents received from client
    """
    print("Server initiated")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind((host, port))
        serversocket.listen(5)
        print("\nServer is listening for connections...\n")
        
        
        connection, address = serversocket.accept()
        print(f"connection established through{address}\n")
        
        with connection:
            command_thread = threading.Thread(target=send_commands, args=(connection,)) #command thread
            command_thread.daemon = True
            command_thread.start()
            
            
            while True:
                #receive the data size
                data_size = int.from_bytes(connection.recv(4), byteorder="big")
                
                #receive the file
                data = connection.recv(data_size).decode('utf-8')
                
                with open(CLIENT_DATA_FILE, 'a') as file:
                    file.writelines(data)
                    file.flush()

#AI*
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
                    new_threshold = input("Enter new threshold value: ").strip()
                    if new_threshold.isdigit():
                        threshold_value = str(new_threshold)
                        connection.sendall(threshold_value.encode('utf-8'))
                        time.sleep(30)
                    else:
                        print("\nPlease enter a number less than 40\n")
                except Exception as e:
                    print(f"\nThere was an error while setting threshold. please try again: {e}\n")

def main():
    server()

if __name__ == '__main__':
    main()