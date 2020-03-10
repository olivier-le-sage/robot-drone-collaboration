#!/usr/bin/python3
# Python interface for MPU6050
# Provides structured access to MPU6050 routines

from ctypes import *
import os
from smbus2 import SMBus # i2c support
import pyximport; pyximport.install() # cython support
import src.MPU_6050.MPU_6050_Module as MPU6050 # import .so file from cython

SHARED_OBJ_LIB_PATH = '/home/pi/robot-drone-collaboration/src/MPU_6050/'

# MPU6050-related data addresses on the i2c bus
MPU_ADDR     = 0x68
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

class MPU6050Interface:

    def __init__(self):
        '''
            Python interface for MPU6050.
            Provides python wrappers around C-level MPU6050 routines
        '''
        # setup c routines by loading shared object library
        self.so_file = "MPU_6050_Module.so" # .so on Linux, .pyd on Windows

        # open i2c bus 1
        self.bus = SMBus(1)

        # initialize hardware
        # MPU6050.init()
        self.bus.write_byte_data(MPU_ADDR, SMPLRT_DIV, 0x07)
        self.bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0x01)
        self.bus.write_byte_data(MPU_ADDR, CONFIG, 0)
        self.bus.write_byte_data(MPU_ADDR, GYRO_CONFIG, 24)
        self.bus.write_byte_data(MPU_ADDR, INT_ENABLE, 0x01)

    def read_raw_data(addr):
        ''' returns a 16-bit value from a certain address '''
        high_byte = self.bus.read_byte_data(MPU_ADDR, addr)
        low_byte = self.bus.read_byte_data(MPU_ADDR, addr+1)
        value = (high_byte << 8) | low_byte
        return value

    def get_acc_xyz(self):
        ''' returns accelerometer readings in g '''
        Ax = self.bus.read_raw_data(ACCEL_XOUT_H)
        Ay = self.bus.read_raw_data(ACCEL_YOUT_H)
        Az = self.bus.read_raw_data(ACCEL_ZOUT_H)

        # divide by sensitivity scale factor
        Ax /= 16384
        Ay /= 16384
        Az /= 16384

        return (Ax, Ay, Az)

    def get_gyr_xyz(self):
        ''' returns accelerometer readings in g '''
        Gx = self.bus.read_raw_data(GYRO_XOUT_H)
        Gy = self.bus.read_raw_data(GYRO_YOUT_H)
        Gz = self.bus.read_raw_data(GYRO_ZOUT_H)

        # divide by sensitivity scale factor
        Gx /= 131
        Gy /= 131
        Gz /= 131
        return (Gx, Gy, Gz)

#    def get_acc_xyz(self):
#        ''' returns accelerometer readings in g '''
#        Ax, Ay, Az = MPU6050.get_acc()
#
#        if (Ax == 0) and (Ay == 0) and (Az == 0):
#            print("Sensor Error: accelerometer not connected.")
#
#        return (Ax, Ay, Az)

#    def get_gyr_xyz(self):
#        ''' returns gyroscope readings in degrees/sec '''
#        Gx, Gy, Gz = MPU6050.get_gyr()
#
#        if (Gx == 0) and (Gy == 0) and (Gz == 0):
#            print("Sensor Error: gyroscope not connected.")
#
#        return (Gx, Gy, Gz)
