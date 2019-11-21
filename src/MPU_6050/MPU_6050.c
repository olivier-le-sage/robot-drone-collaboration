
#include <stdio.h>
#include <wiringPiI2C.h>

#define ACCX_OUT 0x3B
#define ACCY_OUT 0x3D
#define ACCZ_OUT 0x3F

#define devid_id 0x68

int fd = wiringPiI2CSetup(devid_id);
// read data by

int read_data(int address){
	int value;
	// for now reg8 but we can make it 16
	// this will read an 8 bit value from the device register given
	value = wiringPiI2CReadReg8(fd, address);
	return value;
}

int main(){
	int Ax, Ay, Az;
	int Ax_s, Ay_s, Az_s;

	while(1){
		Ax = read_data(ACCX_OUT);
		Ay = read_data(ACCY_OUT);
		Az = read_data(ACCZ_OUT);

		// divied value by sensitivity scale factor

		Ax_s = Ax / 16384.0;
		Ay_s = Ay / 16384.0;;
		Az_s = Az / 16384.0;

		printf("Ax: %d\nAy: %d\nAz: %d\n", Ax_s, Ay_s, Az_s);

	}
}
