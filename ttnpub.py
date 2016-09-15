#  TTNpub.py - sends data to TTN for publishing
#  Written by Mark Stanley
#

# Import functions;

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error run in sudo mode")
	
# External module imports
import time, sys, tty, termios, serial, base64

# Check usage
if len(sys.argv) != 2:
	print("USAGE: ttnpub.py <\"message\">")
	sys.exit(2)

thisMsg=sys.argv[1].encode('hex')

print("Message is: ")
print(sys.argv[1])
print("Encoded is: ")
print(thisMsg)

########################################################################
# Serial Port Definition from RPi towards RN2483 module
########################################################################
# Baud Rate 57600

port = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=5.0)

########################################################################
# Pin Definitions on LoRaWAN PI board
########################################################################

LED1 = 5	# Pin GPIO 5
LED2 = 6	# Pin GPIO 6
Reset = 13	# Reset line of RN2483 module

########################################################################
# Pin Setup
# Define PINs as input or outputs, any default status and if pullup
# are required.
########################################################################
GPIO.setmode(GPIO.BCM) # Broadcom pin numbering
GPIO.setwarnings(False)	# Disable warnings for GPIO

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(Reset, GPIO.OUT)

# No imput pins are configured, as data is acquired via I2C bus

########################################################################
# Setup initial states (eg: all LEDs off)
########################################################################

GPIO.output(LED1, GPIO.HIGH)			# Turn off
GPIO.output(LED2, GPIO.HIGH)			# Turn off

########################################################################
# Sub-Routines - Read data from radio
########################################################################

# Used to read-in RN2483 data responses pending a Carriage return;
def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv


########################################################################
# Start-up Code
########################################################################

# Execute RN2483 system reset;

# Reset RN2483 Module

GPIO.output(LED1, GPIO.LOW)			# Turn on
GPIO.output(LED2, GPIO.LOW)			# Turn on 

GPIO.output(Reset, GPIO.LOW)			#RN2483 reset - active low
time.sleep(1)
GPIO.output(Reset, GPIO.HIGH)
time.sleep(5)					# 5 seconds stability

GPIO.output(LED1, GPIO.HIGH)			# Turn off
GPIO.output(LED2, GPIO.HIGH)			# Turn off

########################################################################

# Basic system checks

#port.write("sys factoryRESET\r\n")
port.write("sys reset\r\n")

rcv = readlineCR(port)
rcv = readlineCR(port)
print("Reset - Device Version\r\n" + (rcv))
time.sleep(3)

port.write("mac get deveui\r\n")
rcv = readlineCR(port)
thisDevEUI = rcv[1:]
print("Device EUI " + (thisDevEUI))
time.sleep(1)

port.write("radio get mod\r\n")
rcv = readlineCR(port)
print("System Mode:" + (rcv))
time.sleep(1)

port.write("radio get freq\r\n")
rcv = readlineCR(port)
print("Frequency Band:(in Hertz)" + (rcv))
time.sleep(1)

# Set up the radio

port.write("mac set adr on\r\n")
rcv = readlineCR(port)
print("ADR set "+(rcv))
time.sleep(1)

port.write("mac set pwridx 1\r\n")
rcv = readlineCR(port)
print("PWRIDX set "+(rcv))
time.sleep(1)

port.write("mac set dr 5\r\n")
rcv = readlineCR(port)
print("DR set "+(rcv))
time.sleep(1)


########################################################################
# Setup System (Thingithon Keys)
########################################################################

port.write("mac set appeui 70B3D57ED0000CD9\r\n")
while True:
	tdata = readlineCR(port)
	if tdata.strip() == "ok":
		print("Application EUI is Valid")
		break
port.write("mac set appkey 3B49BB48C995D2E2522393CB8DE1AF74\r\n")
while True:
	tdata = readlineCR(port)
	if tdata.strip() == "ok":
		print("Application Key is Valid")
		break


print("Joining the network.")
GPIO.output(LED1, GPIO.LOW)			# Turn on
port.write("mac join otaa\r\n")
tryCount=0
while tryCount < 6:
	tryCount=tryCount+1
	time.sleep(2)
	tdata = readlineCR(port)
	print(tdata.strip())
	if tdata.strip() == "ok":
		print("Join request is fine")
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.25)
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
	if tdata.strip() == "accepted":
		print("Join accepted")
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(2)
		break
	if tdata.strip() == "denied":
		print("Error State - join not accepted")
		GPIO.output(LED1, GPIO.HIGH)	# Turn off
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.25)
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(0.25)
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.25)
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(2)
		GPIO.output(LED1, GPIO.LOW)	# Turn on
		port.write("mac join otaa\r\n")
	if tdata.strip() == "busy":
		print("Error State - busy")
		GPIO.output(LED1, GPIO.HIGH)	# Turn off
		time.sleep(0.5)
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(1)
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(8)
		GPIO.output(LED1, GPIO.LOW)	# Turn on
		port.write("mac join otaa\r\n")
	if tdata.strip() == "no_free_ch":
		print("Error State - no free channel")
		GPIO.output(LED1, GPIO.HIGH)	# Turn off
		time.sleep(1)
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.5)
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(1)
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.5)
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(1)
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.5)
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(20)
		GPIO.output(LED1, GPIO.LOW)	# Turn on
		port.write("mac join otaa\r\n")

GPIO.output(LED1, GPIO.HIGH)	# Turn off
GPIO.output(LED2, GPIO.HIGH)	# Turn off

# If we successfully joined, lets have a go at sending the message
if tdata.strip()=="accepted":
	# Try to send the message
	print("SEND MESSAGE")
	GPIO.output(LED1, GPIO.LOW)	# Turn on
	GPIO.output(LED2, GPIO.LOW)	# Turn on
	port.write("mac tx uncnf 1 " + thisMsg + "\r\n" )
	print("mac tx uncnf 1 " + thisMsg + "\r\n" )
	tryCount=0
	while tryCount < 5:
		tryCount=tryCount+1
		tdata = readlineCR(port)
		print("Getting response..")
		print(tdata.strip())
		if tdata.strip() == "not_joined":
			print("Error - not joined gateway, abort attempt.")
			break
		if tdata.strip() == "ok":
			print("Data Sent to TX buffer")
			break
		if tdata.strip() == "busy":
			print("Please Wait")
			time.sleep(10)
			print("BUSY - RE-SEND MESSAGE")
			port.write("mac tx uncnf 1 " + thisMsg + "\r\n" )
			print("mac tx uncnf 1 " + thisMsg + "\r\n" )
		if tdata.strip() == "no_free_ch":	
			print("Please Wait - Duty Cycle exceeed for <1%")
			time.sleep(30)
			print("NO FREE CH - RE-SEND MESSAGE")
			port.write("mac tx uncnf 1 " + thisMsg + "\r\n" )
			print("mac tx uncnf 1 " + thisMsg + "\r\n" )
	
	GPIO.output(LED1, GPIO.HIGH)	# Turn off
	GPIO.output(LED2, GPIO.HIGH)	# Turn off
	tdata = readlineCR(port)

	if tdata.strip() == "mac_tx_ok":
		print("Data Sent OTA")
		GPIO.output(LED1, GPIO.LOW)	# Turn on
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(0.5)
		GPIO.output(LED1, GPIO.HIGH)	# Turn off
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.5)
		GPIO.output(LED1, GPIO.LOW)	# Turn on
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(0.5)
		GPIO.output(LED1, GPIO.HIGH)	# Turn off
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.5)
		GPIO.output(LED1, GPIO.LOW)	# Turn on
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(0.5)
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(1)
		GPIO.output(LED1, GPIO.HIGH)	# Turn off
		GPIO.output(LED2, GPIO.HIGH)	# Turn off

	
	if tdata.strip() == "mac_err":
		print("Please Wait - MAC error - Data will be passed to RN2483 module for final time - else data is ditched this loop")
		GPIO.output(LED1, GPIO.LOW)	# Turn on
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.5)
		GPIO.output(LED1, GPIO.HIGH)	# Turn off
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(0.5)
		GPIO.output(LED1, GPIO.LOW)	# Turn on
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.5)
		GPIO.output(LED1, GPIO.HIGH)	# Turn off
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(0.5)
		GPIO.output(LED1, GPIO.LOW)	# Turn on
		GPIO.output(LED2, GPIO.LOW)	# Turn on
		time.sleep(0.5)
		GPIO.output(LED1, GPIO.HIGH)	# Turn off
		GPIO.output(LED2, GPIO.HIGH)	# Turn off
		time.sleep(5)
		print("TRANSMIT ERROR - TRY TO RE-SEND MESSAGE")
		port.write("mac tx uncnf 1 " + thisMsg + "\r\n")
		
# Clean up GPIO ports on program end; 
GPIO.cleanup()
