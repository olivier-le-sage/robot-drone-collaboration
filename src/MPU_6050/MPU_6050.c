/*
	Set of functions used to setup the MPU6050 accelerometer and provide hooks
		to read accelerometer and gyroscope values from its I2C interface.
*/
#include <Python.h>
#include <wiringPiI2C.h>

#define DEVICE_ID 0x68

#define PWR_MGMT_1   0x6B
#define SMPLRT_DIV   0x19
#define CONFIG       0x1A
#define GYRO_CONFIG  0x1B
#define INT_ENABLE   0x38
#define ACC_XOUT     0x3B
#define ACC_YOUT     0x3D
#define ACC_ZOUT     0x3F
#define GYRO_XOUT    0x43
#define GYRO_YOUT    0x45
#define GYRO_ZOUT    0x47

int fd;

// Python bindings
static PyObject* py_MPU6050_init(PyObject* self)
{

}
static PyObject* py_read_raw_data(PyObject* self, PyObject* args)
{
	int addr;
	if (!PyArg_ParseTuple(args, "i", &addr)) return NULL;

	short high_byte, low_byte, value;
	high_byte = wiringPiI2CReadReg8(fd, addr);
	low_byte = wiringPiI2CReadReg8(fd, addr+1);
	value = (high_byte << 8) | low_byte;

	return Py_BuildValue("h", value);
}
static PyObject* py_get_ax(PyObject* self)
{
	int Ax, Acc_x;

	Acc_x = read_raw_data(ACC_XOUT);
	Ax = Acc_x / 16384.0; // divide value by sensitivity scale factor

	return Py_BuildValue("i", Ax);
}
static PyObject* py_get_ay(PyObject* self)
{
	int Ay, Acc_y;

	Acc_y = read_raw_data(ACC_YOUT);
	Ay = Acc_y / 16384.0; // divide value by sensitivity scale factor

	return Py_BuildValue("i", Ay);
}
static PyObject* py_get_az(PyObject* self)
{
	int Az, Acc_z;

	Acc_z = read_raw_data(ACC_ZOUT);
	Az = Acc_z / 16384.0; // divide value by sensitivity scale factor

	return Py_BuildValue("i", Az);
}
static PyObject* py_get_gx(PyObject* self)
{
	int Gx, Gyro_x;

	Gyro_x = read_raw_data(GYRO_XOUT);
	Gx = Gyro_x / 131; // divide value by sensitivity scale factor

	return Py_BuildValue("i", Gx);
}
static PyObject* py_get_gy(PyObject* self)
{
	int Gy, Gyro_y;

	Gyro_y = read_raw_data(GYRO_YOUT);
	Gy = Gyro_y / 131; // divide value by sensitivity scale factor

	return Py_BuildValue("i", Gy);
}
static PyObject* py_get_gz(PyObject* self)
{
	int Gz, Gyro_z;

	Gyro_z = read_raw_data(GYRO_ZOUT);
	Gz = Gyro_z / 131; // divide value by sensitivity scale factor

	return Py_BuildValue("i", Gz);
}

// Mapping between python and c function names.
static PyMethodDef MPU_6050_Module_methods[] = {
    {"MPU6050_init",  py_MPU6050_init,  METH_VARARGS},
    {"read_raw_data", py_read_raw_data, METH_VARARGS},
    {"get_ax",        py_get_ax,        METH_VARARGS},
    {"get_ay",        py_get_ay,        METH_VARARGS},
    {"get_az",        py_get_az,        METH_VARARGS},
    {"get_gx",        py_get_gx,        METH_VARARGS},
    {"get_gy",        py_get_gy,        METH_VARARGS},
    {"get_gz",        py_get_gz,        METH_VARARGS},
    {NULL, NULL}
};

// Python Module initialisation routine.
void init_MPU_6050(void)
{
    // Init module.
    (void) Py_InitModule("MPU_6050", MPU_6050_Module_methods);
}

/* Hardware Initialization: Must be run before anything else. */
void MPU6050_init(){

	fd = wiringPiI2CSetup(DEVICE_ID);

	wiringPiI2CWriteReg8 (fd, SMPLRT_DIV, 0x07);	/* Write to sample rate register */
	wiringPiI2CWriteReg8 (fd, PWR_MGMT_1, 0x01);	/* Write to power management register */
	wiringPiI2CWriteReg8 (fd, CONFIG, 0);			/* Write to Configuration register */
	wiringPiI2CWriteReg8 (fd, GYRO_CONFIG, 24);		/* Write to Gyro Configuration register */
	wiringPiI2CWriteReg8 (fd, INT_ENABLE, 0x01);	/*Write to interrupt enable register */
}

/* reads data from h/w registers */
short read_raw_data(int addr){
	short high_byte, low_byte, value;
	high_byte = wiringPiI2CReadReg8(fd, addr);
	low_byte = wiringPiI2CReadReg8(fd, addr+1);
	value = (high_byte << 8) | low_byte;
	return value;
}

/* Hook functions meant to be integrated into python */
/* accelerometer values in g, gyroscope values in degrees/second */

int get_ax(){
	int Ax, Acc_x;

	Acc_x = read_raw_data(ACC_XOUT);
	Ax = Acc_x / 16384.0; // divide value by sensitivity scale factor

	return Ax;
}

int get_ay(){
	int Ay, Acc_y;

	Acc_y = read_raw_data(ACC_YOUT);
	Ay = Acc_y / 16384.0; // divide value by sensitivity scale factor

	return Ay;
}

int get_az(){
	int Az, Acc_z;

	Acc_z = read_raw_data(ACC_ZOUT);
	Az = Acc_z / 16384.0; // divide value by sensitivity scale factor

	return Az;
}

int get_gx(){
	int Gx, Gyro_x;

	Gyro_x = read_raw_data(GYRO_XOUT);
	Gx = Gyro_x / 131; // divide value by sensitivity scale factor

	return Gx;
}

int get_gy(){
	int Gy, Gyro_y;

	Gyro_y = read_raw_data(GYRO_YOUT);
	Gy = Gyro_y / 131; // divide value by sensitivity scale factor

	return Gy;
}

int get_gz(){
	int Gz, Gyro_z;

	Gyro_z = read_raw_data(GYRO_ZOUT);
	Gz = Gyro_z / 131; // divide value by sensitivity scale factor

	return Gz;
}
