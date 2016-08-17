#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


void myHash(char *readStr, char *hashStr, int isApple) {
	int sum;
	for(int i = 0; i< strlen(readStr);i++){
		sum=sum+ ((readStr[i]+i)^2);
	}
	sum=sum*9;
	sum=sum%readStr[3]+sum;
	if (sum < 9999){
		sum*=10;
	}
	if(isApple) {
		sprintf(hashStr,"A%d",sum);
	} else {
		sprintf(hashStr,"%d",sum);
	}
}

int isThisAnApplePhone(char *first8Chars, FILE *applefp){
	char appleStr[20];
	char apple8[8];
	int compare=0;
	
	printf("first8 is %s\n",first8Chars);
	while(!feof(applefp)) {
		fgets(appleStr,20,applefp);
		strncpy(apple8,appleStr,8);
		apple8[8]='\0';
		compare=strcmp(apple8,first8Chars);
		if(compare==0) {
			//we hava a match!
			return(1);
		} else if (compare >0 ) {
			//we do not have a match
			return(0);
		}
		// no match yet
	}
}


int startsWith(const char *a, const char*b){
	if(strncmp(a,b,strlen(b))==0) return 1;
	return 0;

}

int main(int argc, char *argv[]) {
	FILE *infp;
	FILE *outfp;
	FILE *applefp;
	char readStr[200];
	char first8Chars[10];
	char hashStr[200];
	int isApple=0;
	int i=0;
	
	// Check we have some arguments
	// argv[1] - input file
	// argv[2] - output file
	// argv[3] - apple file

	if(argc!=4) {
		printf("USAGE: chash <inFile> <outFile> <appleFile>\n");
		return(-1);
	}
	
	applefp=fopen(argv[3],"r");
	if(applefp==NULL) {
		printf("ERROR: Could not open %s for writing. Check path/permission\n",argv[3]);
		return(-2);
	}
	outfp=fopen(argv[2],"w");
	if(outfp==NULL) {
		printf("ERROR: Could not open %s for writing. Check path/permission\n",argv[2]);
		return(-2);
	}
	if(infp=fopen(argv[1],"r")) {
		while(!feof(infp)) {
			fgets(readStr,200,infp);
			isApple=0;  //assume it isn't
			if((applefp!=NULL) && (!feof(applefp))) {
				strncpy(first8Chars,readStr,8);
				first8Chars[8]='\0';
				for(i=0;i<8;i++) {
					first8Chars[i]=toupper(first8Chars[i]);
					}
				isApple=isThisAnApplePhone(first8Chars, applefp);
				} else  if(feof(applefp)){
					fclose(applefp);
				}
			if(readStr[strlen(readStr)-1]==10) {
				readStr[strlen(readStr)-1]=0;
				myHash(readStr, hashStr, isApple);
				printf("In: %s  Out: %s  isApple: %d\n",readStr, hashStr, isApple);
				fputs(hashStr,outfp);
				fputs("\n",outfp);
			}
		}
		fclose(outfp);
		fclose(infp);
		fclose(applefp);
		return(0);
	} else {
		printf("ERROR: Could not open %s to read. Check path/permission\n",argv[1]);
		return(-3);
	}
}

