#!/usr/bin/python3
# Python interface for MPU6050
# Provides structured access to MPU6050 routines

from ctypes import *
import os
import pyximport; pyximport.install()
import src.MPU_6050.MPU_6050_Module.pyx as MPU6050 # import .so file from cython

SHARED_OBJ_LIB_PATH = '/home/pi/robot-drone-collaboration/src/MPU_6050/'

class MPU6050Interface:

    def __init__(self):
        '''
            Python interface for MPU6050.
            Provides python wrappers around C-level MPU6050 routines
        '''
        # setup c routines by loading shared object library
        self.so_file = "MPU_6050_Module.so" # .so on Linux, .pyd on Windows
        #self.functions = CDLL(self.so_file)
        #self.functions = CDLL(SHARED_OBJ_LIB_PATH+self.so_file)

        # initialize hardware
        MPU6050.MPU6050_init()

    def get_acc(self):
        ''' returns accelerometer readings in g '''
        Ax = MPU6050.get_ax()
        Ay = MPU6050.get_ay()
        Az = MPU6050.get_az()

        if (Ax == 0) and (Ay == 0) and (Az == 0):
            print("Sensor Error: accelerometer not connected.")

        return (Ax, Ay, Az)

    def get_gyr(self):
        ''' returns gyroscope readings in degrees/sec '''
        Gx = MPU6050.get_gx()
        Gy = MPU6050.get_gy()
        Gz = MPU6050.get_gz()

        if (Gx == 0) and (Gy == 0) and (Gz == 0):
            print("Sensor Error: gyroscope not connected.")

        return (Gx, Gy, Gz)
