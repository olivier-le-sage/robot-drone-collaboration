# include <wiringPi.h>


int main (){
	#define IRPin_1  11;
	//#define IRPin_2  13;
	//#define IRPin_3  15;

	bool result = false;

	wiringPiSetupPhys();
	delay(100);

	// prepare to read the pins

	pinMode (IRPin_1, INPUT);
	//pinMode (IRPin_2, INPUT);
	//pinMode (IRPin_3, INPUT);


	// int digitalRead(int pin)
	// it return the value read at the given pin. it will b
	// HIGH  or LOW (1 or 0) depending on the logic level at the pin.

	if (digitalRead(IRPin_1) == 1){
		result = true;

	}
	else{
		result = false;
	}

	printf(result);

}
