/* thingithonmq.c - publishes MAC addresses picked up by the hotspot monitor
 *                  to the Thingitude server's MQTT broker.
 *
 * Copyright 2016 Mark Stanley.
 *
 */

#include <string.h>
#include <stdlib.h>
#include <stdio.h>



int main(int argc, char *argv[])
{
	char *macFile;
	char *timeNow;
	int messagesToSend;
	FILE *fp;
	char buff[255];
	char macString[255];
	char msgToSend[255];

	/* argv[1] is the filename, argv[2] is the number of MAC addresses argv[3] is the timestamp */
	printf("Argc is %d \n", argc);
	if(argc>=4) {
		macFile=argv[1];
		messagesToSend=atoi(argv[2]);
		timeNow=argv[3];
	}
		
	printf("Opening file\n");
	fp=fopen(macFile, "r");
	while(!feof(fp)){
		fgets(buff,255, (FILE *)fp);
		if(!feof(fp)) {
			printf("Constructing message\n");
			printf("Buff is %s with length %d\n", buff, strlen(buff)-1);
			strncpy(macString,buff,strlen(buff)-1);
			sprintf(msgToSend,"{\"mac\":\"%s\",\"time\":\"%s\"}",macString, timeNow);
			printf("Message >> %s <<\n",msgToSend);
		}
	}
	fclose(fp);
	return(0);
}
