#include "stdio.h"
#include "rotaryencoder.h"
int main(){
	printf("Hello!\n");
	wiringPiSetup () ;
	/*using pins 23/24*/
	struct encoder *encoder = setupencoder(0,7);
	long value;
	while (1){
		 updateEncoders();
		 long l = encoder->value;
  		 if(l!=value){
   			  printf("value: %d\n", (void *)l);
    			  value = l;
  		 }
	}
return(0);
}

