########################################################################
# LoRaWAN RN2483 BMP180 Sensor Software for RaspberryPi
# Grahame Collins  
# This SW collects the readings a BMP 180 pressure sensor and attempts
# to send them to The Things Network (TTN) using the RN2483 radio module
# Data is also shown locally on an OLED screen
# Both BMP180 and OLED use the I2C interface
#
# Note: Software is coded to cover many of the most common command &
# responses, however not all are covered. See RN2483 Release Notes. 
#
# LoRa Pi Board by Andrew D Lindsay - Thing Innovations
#
########################################################################
# Import functions;

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error run in sudo mode")
	
# External module imports
import time, sys, tty, termios, serial, base64

# i2c screen uses Adafruit drivers
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Image
import ImageDraw
import ImageFont

# i2c sensor uses Adafruit drivers
import Adafruit_BMP.BMP085 as BMP085

# Check usage
if len(sys.argv) != 2:
	print("USAGE: ttnpub.py <\"message\">")
	sys.exit(2)

#thisMsg=base64.b64encode(bytes(sys.argv[1]),"utf-8")

thisMsg=sys.argv[1].encode('hex')

#print(thisMsg)

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

# Raspberry Pi pin configuration for OLED display:
RST = 24

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

# Define variables initial values
count = 48
counthex = 30
tdata = 0
temp_decimal = 00 
temp_ascii = 00
presure_decimal = 00
presure_ascii = 00	
alt_decimal = 00
alt_ascii = 00
compensate = 101285

########################################################################
# Setup Screen - i2c from Adafruit
########################################################################
# 128x32 display with hardware I2C:
RST = 24
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)


########################################################################
# Sub-Routines - Read data and display
########################################################################

# Used to read-in RN2483 data responses pending a Carriage return;
def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv

# Used to update screen and OLED with current data;
def displaydata():
	return()
	
def screenWelcome():
# Write three lines of text.
	
	return()

def screenBlank():
# Clear Display 
# Draw a black filled box to clear the image.
	return()

def screenID():
	return()

def screenConnected():
	return()

def screenTransmitted():
	return()

########################################################################
# Start-up Code
########################################################################

# Execute RN2483 system reset;

# Reset RN2483 Module

print("SYSEM RESET")
GPIO.output(LED1, GPIO.LOW)			# Turn on
GPIO.output(LED2, GPIO.LOW)			# Turn on 

GPIO.output(Reset, GPIO.LOW)		#RN2483 reset - active low
time.sleep(1)
GPIO.output(Reset, GPIO.HIGH)
time.sleep(5)						# 10 seconds stability

print("SYSEM RESET COMPLETED")
GPIO.output(LED1, GPIO.HIGH)			# Turn off
GPIO.output(LED2, GPIO.HIGH)			# Turn off

########################################################################

# Basic system checks

port.write("sys factoryRESET\r\n")
rcv = readlineCR(port)
print("Factory RESET Ordered - Device Version\r\n" + (rcv))
time.sleep(1)

port.write("sys get hweui\r\n")
rcv = readlineCR(port)
print("HW EUI" + (rcv))
time.sleep(1)

port.write("mac get deveui\r\n")
rcv = readlineCR(port)
thisDeveui = rcv[1:]
print("Device EUI " + (thisDeveui))
time.sleep(1)

port.write("radio get mod\r\n")
rcv = readlineCR(port)
print("System Mode:" + (rcv))
time.sleep(1)

port.write("radio set freq 868000000\r\n")
rcv = readlineCR(port)
print("SET Frequency Band:(in Hertz)" + (rcv))
time.sleep(1)

port.write("radio get freq\r\n")
rcv = readlineCR(port)
print("Frequency Band:(in Hertz)" + (rcv))
time.sleep(1)

########################################################################
# Setup System (Thingithon Keys)
########################################################################

port.write("mac set appeui 70B3D57ED00004CD\r\n")
while True:
	tdata = readlineCR(port)
	if tdata.strip() == "ok":
		print("Application EUI is Valid")
		break
port.write("mac set appkey 3E3E8548702408B34FADB0167871513F\r\n")
while True:
	tdata = readlineCR(port)
	if tdata.strip() == "ok":
		print("Application Key is Valid")
		break
port.write("mac join otaa\r\n")
while True:
	tdata = readlineCR(port)
	print(tdata.strip())
	if tdata.strip() == "accepted":
		print("Join accepted")
		break
	if tdata.strip() == "denied":
		print("Error State - join not accepted")
		time.sleep(5)
		port.write("mac join otaa\r\n")
	if tdata.strip() == "busy":
		print("Error State - busy")
		time.sleep(5)
		port.write("mac join otaa\r\n")

time.sleep(3)


# Confirm device ID on TTN;
		
print("MAC GET STATUS")
port.write("mac get status\r\n")
while True:
	tdata = readlineCR(port)
	print(tdata.strip())
	if tdata.strip() == "0001":
		print("System Ready - MAC level Confirmed Ready")
		time.sleep(1)
		break
	if tdata.strip() == "0000":
		print("Please Wait")
		time.sleep(5)
		port.write("mac get status\r\n")
	if tdata.strip() == "00000401":
		print("Not sure what this means... try anyway")
		break
		

print("Config complete, now attempting to send message")

# Try to send the message

print("SEND MESSAGE")
port.write("mac tx uncnf 1 " + thisMsg + "\r\n" )
print("mac tx uncnf 1 " + thisMsg + "\r\n" )
print("Port Write")
while True:
	tdata = readlineCR(port)
	print("post-send")
	print(tdata.strip())
	if tdata.strip() == "ok":
		print("Data Sent to TX buffer")
		break
	if tdata.strip() == "busy":
		print("Please Wait")
		time.sleep(30)
		port.write("mac tx uncnf 1 " + thisMsg + "\r\n")
	if tdata.strip() == "no_free_ch":	
		print("Please Wait - Duty Cycle exceeed for <1%")
		time.sleep(30)
		print("Resending Data.....")
		port.write("mac tx uncnf 1 " + thisMsg + "\r\n")
		print(port.write)
		print("Data Re-sent")
	
while True:
	tdata = readlineCR(port)
	if tdata.strip() == "mac_tx_ok":
		print("Data Sent OTA")
		screenBlank()
		screenTransmitted()
		time.sleep(1)
		break
	if tdata.strip() == "mac_err":
		print("Please Wait - MAC error - Data will be passed to RN2483 module for final time - else data is ditched this loop")
		time.sleep(10)
		port.write("mac tx uncnf 1 " + thisMsg + "\r\n")
		break					# Note it would be possible here with data failing, to reset/re-loop - however decided to skip this loop; 
		
# Clean up GPIO ports on program end; 
GPIO.cleanup()
