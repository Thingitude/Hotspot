#include <string.h>
#include <stdio.h>
#include <mosquitto.h>

char mqMsg[30];

void my_message_callback(struct mosquitto *mosq, void *userdata, const struct mosquitto_message *message)
{
	if(message->payloadlen){
		printf("BANANA %s %s\n", message->topic, message->payload);
	}else{
		printf("BONONO %s (null)\n", message->topic);
	}
	fflush(stdout);
}

void my_connect_callback(struct mosquitto *mosq, void *userdata, int result)
{
	int i;
	if(!result){
		mosquitto_publish(mosq, NULL, "hello/world", strlen(mqMsg), mqMsg, 2, 0);
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
	/* We've published so lets exit nicely */
	mosquitto_disconnect(mosq);
}

int main(int argc, char *argv[])
{
	int i;
	char *host = "5.44.237.19";
	int port = 1883;
	int keepalive = 60;
	bool clean_session = true;
	struct mosquitto *mosq = NULL;

	sprintf(mqMsg,"%s",argv[1]);
	printf("And the word is >> %s <<\n", mqMsg);

	mosquitto_lib_init();
	mosq = mosquitto_new(NULL, clean_session, NULL);
	if(!mosq){
		fprintf(stderr, "Error: Out of memory.\n");
		return 1;
	}
	mosquitto_log_callback_set(mosq, my_log_callback);
	mosquitto_connect_callback_set(mosq, my_connect_callback);
	mosquitto_message_callback_set(mosq, my_message_callback);
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
