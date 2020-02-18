cdef extern from "MPU_6050.h":
    int DEVICE_ID
    int PWR_MGMT_1
    int SMPLRT_DIV
    int CONFIG
    int GYRO_CONFIG
    int INT_ENABLE
    int ACC_XOUT
    int ACC_YOUT
    int ACC_ZOUT
    int GYRO_XOUT
    int GYRO_YOUT
    int GYRO_ZOUT

cdef extern from "wiringPiI2C.h":
    int wiringPiI2CSetup(int id)
    int wiringPiI2CWriteReg8(int id, int addr, int val)
    short wiringPiI2CReadReg8(int id, int addr)

cdef int fd

cdef void MPU6050_init():
    fd = wiringPiI2CSetup(DEVICE_ID)

    wiringPiI2CWriteReg8(fd, SMPLRT_DIV, 0x07)
    wiringPiI2CWriteReg8(fd, PWR_MGMT_1, 0x01)
    wiringPiI2CWriteReg8(fd, CONFIG, 0)
    wiringPiI2CWriteReg8(fd, GYRO_CONFIG, 24)
    wiringPiI2CWriteReg8(fd, INT_ENABLE, 0x01)

cdef short read_raw_data(int addr):
    cdef short high_byte, low_byte, value
    high_byte = wiringPiI2CReadReg8(fd, addr)
    low_byte = wiringPiI2CReadReg8(fd, addr+1)
    value = (high_byte << 8) | low_byte
    return value

cdef short get_ax():
    cdef short Ax, Acc_x
    Acc_x = read_raw_data(ACC_XOUT)
    Ax = Acc_x / 16384
    return Ax

cdef short get_ay():
    cdef short Ay, Acc_y
    Acc_y = read_raw_data(ACC_YOUT)
    Ay = Acc_y / 16384
    return Ay

cdef short get_az():
    cdef short Az, Acc_z
    Acc_z = read_raw_data(ACC_ZOUT)
    Az = Acc_z / 16384
    return Az

cdef short get_gx():
    cdef short Gx, Gyro_x
    Gyro_x = read_raw_data(GYRO_XOUT)
    Gx = Gyro_x / 131
    return Gx

cdef short get_gy():
    cdef short Gy, Gyro_y
    Gyro_y = read_raw_data(GYRO_YOUT)
    Gy = Gyro_y / 131
    return Gy

cdef short get_gz():
    cdef short Gz, Gyro_z
    Gyro_z = read_raw_data(GYRO_ZOUT)
    Gz = Gyro_z / 131
    return Gz

def get_acc():
    return (get_ax(), get_ay(), get_az())

def get_gyr():
    return (get_gx(), get_gy(), get_gz())

def init():
    MPU6050_init()
