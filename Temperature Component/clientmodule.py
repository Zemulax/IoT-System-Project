# echo_client.py
import socket
import os
import time
import fcntl as filelock

print("CLIENT WILL ATTEMPT TO INITIATE CONNECTION TO THE SERVER")
#variables
host = '10.69.79.139'
port = 12345
BUFFER_SIZE = 1024
FILENAME = "processeddata.log"

def client(filename):
   
   while True:
      try:
         with open(filename, "r") as file:
            filelock.flock(file, filelock.LOCK_SH)
            data = file.read()
            filelock.flock(file, filelock.LOCK_UN)
            
            return data
            
      except :
         print("unable to read file??")

def transmit_data():
   """_summary_
      send file contents to the server
   """
   print("Attempting data transmission to the server")
   try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
         clientsocket.connect((host, port))
         print("server connected")
         
         while True:
            start_time = time.time()
            while time.time() - start_time < 60: #]every 30 seconds
               data = client(FILENAME)
               
               if data:
                  print("transmitting data")
                  #send data length
                  clientsocket.sendall(len(data).to_bytes(4, byteorder='big'))
                  
                  #send the file data#
                  clientsocket.sendall(data.encode('utf-8'))
                  print('data sent successfully')
               else:
                  print("could not read file??")
                  
               time.sleep(30)
   except Exception as e:
            print(f"an error occured durinfg transmission: {e}")        

def main():
   transmit_data()
   
if __name__ == "__main__":
   main()
