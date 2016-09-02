/*
 *   dht11.c:
 *   Simple test program to test the wiringPi functions
 *   DHT11 test
 */

#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pcf8591.h>

#define PCF       120

#define MAXTIMINGS 85

#define DHTPIN 0

int dht11_dat[5] = {0,0,0,0,0};
int LCDAddr = 0x27;
int BLEN = 1;
int fd;
char *wifiCountFile="/home/pi/Hotspot/wifiCountFile";
char mqMsg[30];
char ttnMsg[30];



int read_dht11_dat()
{
	uint8_t laststate = HIGH;
	uint8_t counter = 0;
	uint8_t j = 0, i;
	float f; // fahrenheit

	dht11_dat[0] = dht11_dat[1] = dht11_dat[2] = dht11_dat[3] = dht11_dat[4] = 0;

	// pull pin down for 18 milliseconds
	pinMode(DHTPIN, OUTPUT);
	digitalWrite(DHTPIN, LOW);
	delay(18);
	// then pull it up for 40 microseconds
	digitalWrite(DHTPIN, HIGH);
	delayMicroseconds(40); 
	// prepare to read the pin
	pinMode(DHTPIN, INPUT);

	// detect change and read data
	for ( i=0; i< MAXTIMINGS; i++) {
		counter = 0;
		while (digitalRead(DHTPIN) == laststate) {
			counter++;
			delayMicroseconds(1);
			if (counter == 255) {
				break;
			}
		}
		laststate = digitalRead(DHTPIN);

		if (counter == 255) break;

		// ignore first 3 transitions
		if ((i >= 4) && (i%2 == 0)) {
			// shove each bit into the storage bytes
			dht11_dat[j/8] <<= 1;
			if (counter > 16)
				dht11_dat[j/8] |= 1;
			j++;
		}
	}

	// check we read 40 bits (8bit x 5 ) + verify checksum in the last byte
	// print it out if data is good
	if ((j >= 40) && 
			(dht11_dat[4] == ((dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]) & 0xFF)) ) {
		f = dht11_dat[2] * 9. / 5. + 32;
		printf("Humidity = %d.%d %% Temperature = %d.%d *C (%.1f *F)\n", 
				dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3], f);
		return(1);
	}
	else
	{
		printf("Data not good, skip\n");
		return(-1);
	}
}


/***************************/


int getPeakSound (int samples)
{
	int value;
	int peakSound=999;
	int count = 0;
	while(count<samples) // loop samples number of times
	{
		value = analogRead  (PCF + 0);
		if(peakSound>value) {
			peakSound=value;
		}
		count++;
	}
	return(153-peakSound);
}

int getMeanSound (int samples)
{
	int value;
	int totalSound=0;
	int count = 0;
	while(count<samples) // loop samples number of times
	{
		value = analogRead  (PCF + 0);
		//printf("Value: %d \n", value);
		totalSound+=value;
		delay(100);
		count++;
	}
	return(153-(totalSound/samples));
}


int main (int argc, char **argv)
{
	int wifiCount=0;
	int peakSound=0;
	int meanSound=0;
	int humAttempt=0;
	int averageStay =0;

	if(argc!=4) {
		printf("USAGE: hotspotmq <wificount> <duration> <people>\n");
		return;
	}
  
	// Setup pcf8591 on base pin 120, and address 0x48
	pcf8591Setup (PCF, 0x48);

	if (wiringPiSetup () == -1)
		exit (1) ;

	// Set up wifiCount if the parameter was passed
	if (argc>1) {
		wifiCount=atoi(argv[1]);
	}
	peakSound=getPeakSound(1000);
	meanSound=getMeanSound(100);
	while((read_dht11_dat()!=1)&& (humAttempt !=5)) {
		delay(1000);
		humAttempt++;
	}
 

	if((humAttempt==5)) {
		sprintf(ttnMsg,"python /home/pi/Hotspot/ttnpub.py \"%d,%d,%d,0,0,%s,%s\"", wifiCount, meanSound, peakSound,argv[2], argv[3]);
  
	} else {
		sprintf(ttnMsg,"python /home/pi/Hotspot/ttnpub.py \"%d,%d,%d,%d.%d,%d.%d,%s,%s\"", wifiCount, meanSound, peakSound, dht11_dat[0], dht11_dat[1], dht11_dat[2], dht11_dat[3],argv[2], argv[3]);
   printf("%s",ttnMsg);
	}
	printf("Try to send >> %s <<\n", ttnMsg);
	system(ttnMsg);
	
	return 0;
}
