# !/usr/bin/env python3
import rospy
from time import time
from datetime import datetime
import numpy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from std_msgs.msg import String, Float32MultiArray, MultiArrayDimension
from std_msgs.msg import String
from tada_ros.msg import EuropaMsg
from tada_ros.msg import IMUDataMsg
from multiprocessing import Process, Manager, freeze_support, Pool, Pipe, Queue
# import inspect module
import inspect
import message_filters
from collections import deque
import sqlite3
# got help for the data saving correctly from https://stackoverflow.com/questions/48830056/use-data-from-multiple-topics-in-ros-python

#class dataprocessing:
#    def __init__(self):
notes = ''
talker_data = numpy.array([0], dtype=numpy.float32)
record_button = 0
xsens_com_raw = Float32MultiArray()
xsens_joint_angle_raw = Float32MultiArray()
xsens_com = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)
xsens_joint_angle = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)   
brain_data = numpy.array([0], dtype=numpy.float32)
imu_data = numpy.array([0,0,0,0,0,0,0,0], dtype=numpy.float32)
europa_data = numpy.array([0,0,0], dtype=numpy.float32)
gui_cmd = numpy.array([0,0], dtype=numpy.float32) # str('0,0')
data_array = numpy.array([0], dtype=numpy.float32)
prev_record = 0
data_array = numpy.array([0], dtype=numpy.float32)
tag = ''
var_num = 5     
counter = 0
start_time = rospy.Time().nsecs/1_000_000 #time.time_ns() // 1_000_000
print('start of callback')
# define callback functions for the ROS subscibers
#def callback(xsens_com_sub, xsens_joint_angle_sub, imu_data_sub, europa_data_sub, chatter_control_sub, notes_sub, gui_topic_sub):
def callback(imu_data_sub, europa_data_sub):
    filename = ('catkin_ws/src/talker_listener/data/data_test.csv') #''
    current_time = rospy.Time.now().nsecs/1_000_000 - start_time #str(time.time_ns() // 1_000_000 - start_time)
    #xsens_com = numpy.array(xsens_com_sub.data)
    #if len(xsens_com)!=9:
    #    xsens_com = numpy.array([0,0,0,0,0,0,0,0], dtype=numpy.float32)       
        
    #xsens_joint_angle = numpy.array(xsens_joint_angle_sub.data)
    #if len(xsens_joint_angle)!=24: 
    #    xsens_joint_angle = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32) 
    
    #gui_cmd = [float(x) for x in str(chatter_control_sub.data).split()] #list(float(str(data.data).split(',')))
    #if len(gui_cmd)!=2:
    #    gui_cmd = numpy.array([0,0], dtype=numpy.float32)
        
    #notes = notes_sub.data
    #if bool(record_button): 
    #     Save the notes string to a notes file (txt) for the data
    #    timestamp = time.strftime('%Y-%m-%d', time.gmtime())
    #    notes_filename = ('catkin_ws/src/talker_listener/data/notes_{}.txt'.format(timestamp))
    #    with open(notes_filename, 'a') as f:
    #         Save the headers only once when the file is opened
    #        f.write( current_time + ': ' + notes + '\n')
        
    #prev_record = record_button
    #record_button = gui_topic_sub.data[0] 
    
    imu_data = [imu_data_sub.accel_x, imu_data_sub.accel_y, imu_data_sub.accel_z, imu_data_sub.gyro_x, imu_data_sub.gyro_y, imu_data_sub.gyro_z, imu_data_sub.state, imu_data_sub.swing_time]
        
    europa_data = [europa_data_sub.mx, europa_data_sub.my, europa_data_sub.fz]
        
    #if bool(record_button - prev_record == 1): # moment when record botton is turned on
    #    # Save the data array to a CSV file with a time and date in the file name
    #    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())
    #    filename = ('catkin_ws/src/talker_listener/data/data_{}.csv'.format(timestamp))
    #    #f = open(filename, 'x')
    #    #f.close()
    #    print('file created')
        
    
# function dedicated to saving for whichever callback that becomes active, if data is not streming from a topic (100 Hz), then data is saved only when the callback is called
#def data_save(self):

    data_array = numpy.array([current_time, europa_data[0], europa_data[1], europa_data[2], imu_data[0], imu_data[1], imu_data[2], imu_data [3], imu_data[4], imu_data[5], imu_data[6], imu_data[7]])
    #print(data_array)
            #numpy.array([gui_cmd[0], gui_cmd[1], europa_data[0], europa_data[1], europa_data[2], imu_data[0], imu_data[1], imu_data[2], imu_data [3], imu_data[4], imu_data[5], imu_data[6], imu_data[7],
            #xsens_joint_angle[0], xsens_joint_angle[1], xsens_joint_angle[2], xsens_joint_angle[3], xsens_joint_angle[4], xsens_joint_angle[5], xsens_joint_angle[6], xsens_joint_angle[7], 
            #xsens_joint_angle[8], xsens_joint_angle[9], xsens_joint_angle[10], xsens_joint_angle[11], xsens_joint_angle[12], xsens_joint_angle[13], xsens_joint_angle[14], xsens_joint_angle[15], 
            #xsens_joint_angle[16], xsens_joint_angle[17], xsens_joint_angle[18], xsens_joint_angle[19], xsens_joint_angle[20], xsens_joint_angle[21], xsens_joint_angle[22], xsens_joint_angle[23],
            #xsens_com[0],xsens_com[1],xsens_com[2],xsens_com[3],xsens_com[4],xsens_com[5],xsens_com[6], xsens_com[7],xsens_com[8]], dtype=numpy.float32)
    #print(data_array)
    #if bool(record_button):
    #    current_time = str(time.time_ns() // 1_000_000)
    with open(filename, 'a') as f:
        # Save the headers only once when the file is opened
        if f.tell() == 0:
            print("file opened")
            #headers = ['time', 'index', 'ankle_angle', 'ankle_angle', 'ankle_angle', 'imu_ang_vel', 'imu_ang_vel', 'imu_ang_vel']
            headers = ['time', 'theta', 'alpha', 'mx', 'my', 'fz', 'imu_ang_vel_x', 'imu_ang_vel_y', 'imu_ang_vel_z', 'imu_accel_x', 'imu_accel_y', 'imu_accel_z', 'State', 'Swing',
                        'Right_Hip_x', 'Right_Hip_y', 'Right_Hip_z', 'Right_Knee_x', 'Right_Knee_y', 'Right_Knee_z', 'Right_Ankle_x', 'Right_Ankle_y', 'Right_Ankle_z', 'Right_Ball_of_Foot_x', 'Right_Ball_of_Foot_y', 'Right_Ball_of_Foot_z','Left_Hip_x', 'Left_Hip_y', 'Left_Hip_z', 'Left_Knee_x', 'Left_Knee_y', 'Left_Knee_z', 'Left_Ankle_x', 'Left_Ankle_y', 'Left_Ankle_z', 'Left_Ball_of_Foot_x', 'Left_Ball_of_Foot_y', 'Left_Ball_of_Foot_z',
                        'Center_of_Mass_Position_x', 'Center_of_Mass_Position_y', 'Center_of_Mass_Position_z', 'Center_of_Mass_Velocity_x', 'Center_of_Mass_Velocity_y', 'Center_of_Mass_Velocity_z', 'Center_of_Mass_Acceleration_x', 'Center_of_Mass_Acceleration_y', 'Center_of_Mass_Acceleration_z']
                        #right_hip_x, right_hip_y, right_hip_z, ]
            #['talker']#['Xsens', 'Brain', 'IMU', 'Europa']
            f.write(','.join(headers) + '\n')
        f.write(','.join([str(x) for x in data_array]) + '\n')
                
            #if bool(record_button - prev_record == -1): 
            #    f.close()
            #    print('file closed')


if __name__ == '__main__':
    # Initialize the ROS node
    rospy.init_node('data_node')
    print('data_node initialized')
    # Create subscribers for each of the four sensors and GUI node
    xsens_com_sub = message_filters.Subscriber('xsens_com', Float32MultiArray)
    xsens_joint_angle_sub = message_filters.Subscriber('xsens_joint_angle', Float32MultiArray)
    #brain = message_filters.Subscriber('brain', numpy_msg(Floats))
    imu_data_sub = message_filters.Subscriber('sensing_topic', IMUDataMsg)
    europa_data_sub = message_filters.Subscriber('europa_topic', EuropaMsg)
    chatter_control_sub = message_filters.Subscriber('chatter_control', numpy_msg(Floats))
    #message_filters.Subscriber('chatter', numpy_msg(Floats))
    notes_sub = message_filters.Subscriber('notes', String)
    gui_topic_sub = message_filters.Subscriber('gui_topic', String)
    #ts = message_filters.ApproximateTimeSynchronizer([imu_data_sub, europa_data_sub, chatter_control_sub, notes_sub, gui_topic_sub,xsens_com_sub, xsens_joint_angle_sub], 1, 0.01, allow_headerless=True )
    #ts = message_filters.ApproximateTimeSynchronizer([imu_data_sub, europa_data_sub, chatter_control_sub, notes_sub, gui_topic_sub] 1, 0.01, allow_headerless=True )    
    ts = message_filters.TimeSynchronizer([imu_data_sub, europa_data_sub], 100)# slop is error between messages
    ts.registerCallback(callback)
    print('data_node subscribed to topics')
    rospy.spin()
    
    #rospy.Subscriber('processed_data', numpy_msg(Floats), processed_data_callback)
    #pub = rospy.Publisher('processed_data', numpy_msg(Floats), queue_size=10)
    
    ## Start the data publishing loop
    #rate = rospy.Rate(10) # 20Hz fastest I could go without having repeat rows in saving the data
    #while not rospy.is_shutdown():  
    #    # Publish the data array to the GUI node
    #    tag_var = 'save'
    #    #dataprocessing().tag_func(tag_var)
    #    #pub.publish(data_array)   
    #    rate.sleep()
