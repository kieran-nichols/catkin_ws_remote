#!/usr/bin/env python.exe
import rospy
import os
import sys
import signal
from tada_ros.msg import KillConfirmationMsg, IMUDataMsg, ReconDataMsg, EuropaMsg
from std_msgs.msg import Bool
from time import sleep
from std_msgs.msg import String
from tada_ros.sensors import IMU_controller
from IMU_controller import *


import smbus # SMBus module of I2C
import time
import os, sys
import math
from time import sleep
from enum import Enum
from tada_ros.msg import IMUDataMsg, ReconDataMsg
from tada_ros.global_info import constants
from tada_ros.sensors import IMU_controller

import numpy as np
import subprocess
import csv
DEBUG_FLAG = 0
linear_correction = 1

import subprocess
import csv

#some MPU6050 Registers and their Address
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
class SensorNode():
    bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
    Device_Address = 0x68   # MPU6050 device address
    m1_pos = 0
    m2_pos = 0
    # Initial variables
    state = 0
    start = time.time()
    start_time = time.time()
    initial_itr = 0
    swing_time = 0
    swing = [0, 0, 0]
    avg_swing = [0.7, 0.7, 0.7]
    avg_val_swing = 0
    initial_itr1 = 0
    gyro_thres = 5
    accel_thres = 0.5
    state=0
    swing_time=0


    pub_killed_confirm = None
            # killing the program is its own topic so that there's minimal delay

    def __init__(self):
        
        #rospy.Subscriber('kill_all_topic', Bool, handle_kill_command)
        print("initialized IN SENSOR")
        #MPU_Init()
        pub_sensing = rospy.Publisher('sensing_topic', IMUDataMsg, queue_size=10)
        self.imu_msg = IMUDataMsg()
        rospy.init_node('sensor_node', anonymous=True)
        rate = rospy.Rate(100)#100 hz
        imu = IMU_controller.IMUController()
        while not rospy.is_shutdown():
            imu_data = imu.get_data()
            #self.imu_msg.accel_x =
            #self.imu_msg.accel_y = 
            #self.imu_msg.accel_z = 
            #self.imu_msg.gyro_x =
            #self.imu_msg.gyro_y =
            #self.imu_msg.gyro_z =
            #self.imu_msg.state =
            #self.imu_msg.swing_time =
            msg_imu = imu_data.to_ROS_message()
            
            pub_sensing.publish(msg_imu)
            
            rate.sleep()
        
        
        
        # queue_size argument limits the number of queued messages if any
        # subscriber is not receiving them fast enough.
        
    
    def handle_kill_command( data):
        # for debugging
        print("")
        rospy.loginfo(rospy.get_caller_id() + " I heard kill boolean: %s", data.data)
        print("")
        if data.data == True:
            kill_sensors()

        # send confirmation message
        msg = KillConfirmationMsg(motors_killed=True, sensors_killed=False)
        pub_killed_confirm.publish(msg)

        # interrupt the program like a Keyboard Interrupt
        os.kill(os.getpid(), signal.SIGTERM)
            
    def MPU_Init():
        #write to sample rate register
        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

        #Write to power management register
        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

        #Write to Configuration register
        bus.write_byte_data(Device_Address, CONFIG, 0)

        #Write to Gyro configuration register
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

        #Write to interrupt enable register
        bus.write_byte_data(Device_Address, INT_ENABLE, 1)
         

    def kill_sensors():
        # TODO: sensor-specific code
        print("Killing Sensor Node")
if __name__ == '__main__':
    SensorNode()
#def Publishing_Sensor(void):
   # print("in sensor")
   # return SensorNode.talker()
