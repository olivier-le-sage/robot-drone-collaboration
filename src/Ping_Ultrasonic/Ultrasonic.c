#include <stdio.h>
#include <wiringPi.h>
#include <time.h>

#define Pin_Trigger 16
#define pin_ECHO 18

int main(){
	double time_taken;
	double distance;
	double stop, start;

	printf("Setting up pins");
	wiringPiSetupPhys();

	printf("wiringPi set up, setting pin modes");
	pinMode (Pin_Trigger, OUTPUT);
	pinMode (pin_ECHO, INPUT);

   //void digitalWrite (int pin, int value) ;
   //Writes the value HIGH or LOW (1 or 0) to the given pin which
   // must have been previously set as an output.
	// send 10us pulse to trigger
	printf("writing values to pins");
	digitalWrite (Pin_Trigger, 1);
	delay(0.00001);

	digitalWrite(Pin_Trigger , 0);
	start = clock();

	printf("reading values from pins");
	if (digitalRead(pin_ECHO) == 0){
		start = clock();
	}

	if (digitalRead(pin_ECHO) == 1){
		//stop = clock() - stop
		stop = clock();
	}

	//Calculate time taken
	//double time_taken = ((double t)/ CLOCKS_PER_SEC);
	time_taken = stop - start;

	// Distance travelled in that time multiplied by speed of sound
	distance = (time_taken * 34300) / 2;

	printf("%s\n", distance);

}
