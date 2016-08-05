#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void myHash(char *readStr, char *hashStr) {

int sum;
 for(int i = 0; i< strlen(readStr);i++){
 sum=sum+ ((readStr[i]+i)^2);
 

 
 }
  sum=sum*9;
sum=sum%readStr[3]+sum;
if (sum < 9999){
sum*=10;

}
 sprintf(hashStr,"%d",sum);
 
}


int main(int argc, char *argv[]) {
	FILE *infp;
	FILE *outfp;
	char readStr[200];
	char hashStr[200];
	
	// Check we have some arguments
	// argv[1] - input file
	// argv[2] - output file

	if(argc!=3) {
		printf("USAGE: chash <inFile> <outFile>\n");
		return(-1);
	}
	
	outfp=fopen(argv[2],"w");
	if(outfp==NULL) {
		printf("ERROR: Could not open %s for writing. Check path/permission\n",argv[2]);
		return(-2);
	}
	if(infp=fopen(argv[1],"r")) {
		while(!feof(infp)) {
			fgets(readStr,200,infp);
			if(readStr[strlen(readStr)-1]==10) {
				readStr[strlen(readStr)-1]=0;
				myHash(readStr, hashStr);
				printf("In: %s  Out: %s\n",readStr, hashStr);
				fputs(hashStr,outfp);
				fputs("\n",outfp);
			}
		}
		fclose(outfp);
		fclose(infp);
		return(0);
	} else {
		printf("ERROR: Could not open %s to read. Check path/permission\n",argv[1]);
		return(-3);
	}
}

