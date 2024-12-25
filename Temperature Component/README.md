# SmartSystemsProject

Sensor => continously record data
=> write to temprecordings file

client => read temprecordings file
=> process the data
-> aggregate average temperature over a period of 1 minute
=> assign labels
-> if average > x : high temperature
--> this is normal
-> if average < x : low temperature
--> this is abnormal; trigger the actuator
=> write labels to tempreport file
send tempreport file to the server if label abnormal

Server => read the tempreport file
=> display on dashboard
=> further escalation

here is what I got:

clientModule
=> calls SensorModule to run
=> reads temperaure log file
-> gathers data every 30 seconds
-> analyses data to to check for trend below threthold
-> logs processed trends to an external file

SensorModule
=> logs temperature data to an external file

Client-ServerModule
=>establishes link to the server
=>transmits processed data to the server

for temp sensor
Yellow is power => 5v preferred
blue is ground => any
green is data transmission => logical pin 4

I think I'm done with the tenmp component.
Here is the system flow:

EdgeModule
=> Entry point for the system. Emulates Edge computing
=> Invokes all other modules.
=> processes temperature data. writes to an external file
=> controls LED module configuration

LedModule
=> operates the actuator

SensorModule
=> gets invoked by EdgeModule
=> records temperature data to an external file

ClientModule
=> initiates connection to the ServerModule
=> transmits processed data to the ServerModule.
=>receives configuration command from the ServerModule

ServerModule
=> listens for connectioon from the clientModule
=> receives processed data via the clientModule, writes to an external file
=> sends configuration commands to the EdgeModule via the clientModule
