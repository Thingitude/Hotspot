#  TTNpub.py - sends data to TTN for publishing
#  Written by Mark Stanley
#
#  25 Feb 17 - heavy revision to 
#              a) only join when required
#              b) avoid collisions with random delays

# Import functions;

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error run in sudo mode")
	
# External module imports
import time, sys, tty, termios, serial, base64, random

# Check usage
if len(sys.argv) != 2:
	print("USAGE: ttnpub.py <\"message\">")
	sys.exit(2)

thisMsg=sys.argv[1].encode('hex')
#thisMsg=sys.argv[1].encode('base64')

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
# Sub-Routines 
########################################################################

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
# Subroutine to return the status of the radio - eg joined or not
def getStatus(statusQuery):
    port.write("mac get status\r\n")
    statusBits = readlineCR(port)
    if statusBits=="":
    	resetRadio()
        statusBits="00000000"
    print("Status bits are ")
    print(statusBits.strip())
    print(" and the last one is ")
    print(statusBits.strip()[7])
    if statusQuery=="joined":
    	if statusBits.strip()[7]=="1":		# bit 1 says whether joined
    		print("Device already joined network.\r\n")
    		return "yes"
    	else:
    		print("Device not joined network yet.\r\n")
    		return "no"



########################################################################
# Subroutine to reset the RN2483 radio (rarely used)
def resetRadio():
    GPIO.output(LED1, GPIO.LOW)			# LED1 on
    GPIO.output(LED2, GPIO.LOW)			# LED2 on
    GPIO.output(Reset, GPIO.LOW)		#RN2483 reset - active low
    time.sleep(1)
    GPIO.output(Reset, GPIO.HIGH)
    time.sleep(5)				# 5 seconds stability
    port.write("sys reset\r\n")
    rcv = readlineCR(port)
    rcv = readlineCR(port)
    print("Reset - Device Version\r\n" + (rcv))
    time.sleep(3)
    GPIO.output(LED1, GPIO.HIGH)		# LED1 off
    GPIO.output(LED2, GPIO.HIGH)		# LED2 off
    port.write("mac pause\r\n")
    rcv = readlineCR(port)
    print("MAC pause - "+(rcv))
    time.sleep(1)
    port.write("mac set adr on\r\n")
    rcv = readlineCR(port)
    print("ADR set "+(rcv))
    time.sleep(1)
    # port.write("mac set pwridx 1\r\n")
    port.write("mac set pwridx 3\r\n")
    rcv = readlineCR(port)
    print("PWRIDX set "+(rcv))
    time.sleep(1)
    # port.write("mac set dr 5\r\n")
    port.write("mac set dr 1\r\n")
    rcv = readlineCR(port)
    print("DR set "+(rcv))
    time.sleep(1)
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
    port.write("mac resume\r\n")
    rcv = readlineCR(port)
    print("MAC resume - "+(rcv))
    time.sleep(1)


########################################################################
# Subroutine to JOIN the network
def joinNetwork():
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

########################################################################
# End of subroutines
########################################################################

# Start script - Basic system checks

if sys.argv[1]=="reset":
    resetRadio()
    joinNetwork()
    sys.exit(0)

port.write("mac get deveui\r\n")
rcv = readlineCR(port)
thisDevEUI = rcv[1:]
print("Script starts - Device EUI " + (thisDevEUI))
time.sleep(1)

port.write("radio get mod\r\n")
rcv = readlineCR(port)
print("System Mode:" + (rcv))
time.sleep(1)

port.write("radio get freq\r\n")
rcv = readlineCR(port)
print("Frequency Band:(in Hertz)" + (rcv))
time.sleep(1)


# If we successfully joined, lets have a go at sending the message
if getStatus("joined")=="no":
	resetRadio()
	joinNetwork()

if getStatus("joined")=="yes":
	# Pause for a random 1-60 seconds to avoid collision with other devices
	# scheduled to send at the same sort of time
	random.seed(thisDevEUI)		# Seed number generator 
	time.sleep(random.randint(1,60))

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
