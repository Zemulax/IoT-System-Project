# echo_client.py
import socket
import time
import fcntl as filelock



print("\n===================CLIENT INITIATED=================\n")
#variables
host = '10.69.79.139'
port = 12345

#constants
BUFFER_SIZE = 1024
PROCESSED_DATA_FILE = "./datalogs/processedtemperaturedata.log"
THRESH_FILENAME = "./datalogs/thresholdconfiguration.log"

def write_thresh( filename, thresh_value):
   """writes threshold values to asn external file

   Args:
       filename (_string): name of file
       thresh_value (string): value to write
   """
   with open(filename, 'w') as file:
      filelock.flock(file, filelock.LOCK_EX)
      file.write(thresh_value)
      filelock.flock(file, filelock.LOCK_UN)
      
def client(filename):
   """opens processeda data file for reading

   Args:
       filename (string): name of the file

   Returns:
       string: data from the file
   """
   while True:
      try:
         with open(filename, "r") as file:
            filelock.flock(file, filelock.LOCK_SH)
            data = file.read()
            filelock.flock(file, filelock.LOCK_UN)
            
            return data
            
      except :
         print("\nNo data has been processed yet\n")
         return None

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
               data = client(PROCESSED_DATA_FILE)
               
               if data:
                  print("transmitting data")
                  #send data length
                  clientsocket.sendall(len(data).to_bytes(4, byteorder='big'))
                  
                  #send the file data#
                  clientsocket.sendall(data.encode('utf-8'))
                  print('data sent successfully')
               else:
                  print("could not read file data") #adda prooper error message
                  
               try:
                     new_thresh = clientsocket.recv(2).decode('utf-8')
                     write_thresh(THRESH_FILENAME, new_thresh)
               except Exception as e:
                  print (f"error. could not read received config value: {e}")
               #time.sleep(30)
                  
   except Exception as e:
            print(f"an error occured during transmission: {e}")   


   
def main():
   transmit_data()
   
if __name__ == "__main__":
   main()
