/* thingithonmq.c - publishes MAC addresses picked up by the hotspot monitor
 *                  to the Thingitude server's MQTT broker.
 *
 * Copyright 2016 Mark Stanley.
 *
 */

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <mosquitto.h>

char *macFile;
char *timeNow;
int messagesToSend;

void my_connect_callback(struct mosquitto *mosq, void *userdata, int result)
{
	FILE *fp;
	char buff[255]="";
	char msgToSend[255]="";
	char macString[255]="";
	
	if(!result){
		fp=fopen(macFile, "r");
		while(!feof(fp)){
			fgets(buff,255, (FILE *)fp);
			if(!feof(fp)) {
				strncpy(macString,buff,strlen(buff)-1);
				sprintf(msgToSend,"{\"mac\":\"%s\",\"time\":\"%s\"}",macString, timeNow);
				printf("Sending >> %s <<\n",msgToSend);
				mosquitto_publish(mosq, NULL, "thingithon/mac", strlen(msgToSend), msgToSend, 2, 0);
			}
		}
		fclose(fp);
	}else{
		fprintf(stderr, "Connect failed\n");
	}
}

void my_log_callback(struct mosquitto *mosq, void *userdata, int level, const char *str)
{
	/* Pring all log messages regardless of level. */
	printf("%s\n", str);
}

void my_publish_callback(struct mosquitto *mosq, void *userdata, int usernumber)
{
	/* We've published so lets countdown the messages and exit nicely */
	printf("Published message %d \n",messagesToSend);
	messagesToSend--;
	printf("Messages left to send %d \n",messagesToSend);
	if(messagesToSend==0) {
		mosquitto_disconnect(mosq);
	}
}

int main(int argc, char *argv[])
{
	char *host = "5.44.237.19";
	int port = 1883;
	int keepalive = 60;
	bool clean_session = true;
	struct mosquitto *mosq = NULL;

	/* argv[1] is the filename, argv[2] is the number of MAC addresses */
	/* and argv[3] is the timestamp in secs since the epoch            */

	if(argc==4) {
		macFile=argv[1];
		messagesToSend=atoi(argv[2]);
		if(messagesToSend==0) {
			return 1;
		}
		timeNow=argv[3];
	} else {
		printf("USAGE: thingithonmq macFileName numRecords timeStamp\n       Where timeStamp is in seconds, like date +\%s\n");
		return 1;
	}
		
	/* Start up Mosquitto                                              */

	mosquitto_lib_init();
	mosq = mosquitto_new(NULL, clean_session, NULL);
	if(!mosq){
		fprintf(stderr, "Error: Out of memory.\n");
		return 1;
	}
	mosquitto_log_callback_set(mosq, my_log_callback);
	mosquitto_connect_callback_set(mosq, my_connect_callback);
	mosquitto_publish_callback_set(mosq, my_publish_callback);

	if(mosquitto_connect(mosq, host, port, keepalive)){
		fprintf(stderr, "Unable to connect.\n");
		return 1;
	}

	mosquitto_loop_forever(mosq, -1, 1);

	mosquitto_destroy(mosq);
	mosquitto_lib_cleanup();
	return 0;
}
