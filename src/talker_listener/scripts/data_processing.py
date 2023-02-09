# !/usr/bin/env python3
import rospy
import time
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

xsens_com_queue = []
xsens_joint_angle_queue = []
imu_queue = []
europa_queue = []

# define callback functions for the ROS subscibers
def xsens_com_callback(data):
    #print("in the calback ")
    #print(data.data)
    xsens_com = numpy.array(data.data)
    xsens_com_queue.append(xsens_com)
    #print(xsens_com)
    #xsens_com = xsens_com.reshape(data.layout.dim[0].size, data.layout.dim[1].size)
    
def xsens_joint_angle_callback(data):

    xsens_joint_angle = numpy.array(data.data)
    xsens_joint_angle_queue.append(xsens_joint_angle)
    #print(len(xsens_joint_angle))
    #xsens_joint_angle = xsens_joint_angle.reshape(data.layout.dim[0].size, data.layout.dim[1].size)

def brain_callback(data):
    global brain_data
    brain_data = data.data
    
def imu_callback(data):
    #print("data: ")
    print('local: ', data.accel_x)
    #prev_imu_data = imu_data
    imu_data = [data.accel_x, data.accel_y, data.accel_z, data.gyro_x, data.gyro_y, data.gyro_z, data.state, data.swing_time]
    imu_queue.append(imu_data)
    #if imu_data != prev_imu_data:
    #    prev_imu_data = imu_data
    #print("imu_data: ")
    #print(imu_data)

def europa_callback(data):
    europa_data = [data.mx, data.my, data.fz]
    europa_queue.append(europa_data)
    #print(europa_data)
    

       
def data_save():
    global record_button, filename, xsens_com, xsens_joint_angle, brain_data, imu_data, europa_data, gui_cmd
    #print(data.data)
    #data_array = [current_time, gui_cmd, gui_cmd, xsens_com, xsens_joint_angle, brain_data, imu_data, europa_data]
    #if (len(xsens_joint_angle)!=24 or len(xsens_com)!=9):
        #data_array = [current_time, gui_cmd[0], gui_cmd[1], europa_data[0], europa_data[1], europa_data[2], imu_data[0], imu_data[1], imu_data[2], imu_data [3], imu_data[4], imu_data[5],  imu_data[6],  imu_data[7],
        #         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        #         0, 0, 0, 0, 0, 0, 0, 0, 0]
    #else:
    #print(xsens_com)

    xsens_com = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)
    xsens_joint_angle = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)   
    brain_data = numpy.array([0], dtype=numpy.float32)
    imu_data = numpy.array([0,0,0,0,0,0,0,0], dtype=numpy.float32)
    europa_data = numpy.array([0,0,0], dtype=numpy.float32)
    gui_cmd = numpy.array([0,0], dtype=numpy.float32) # str('0,0')

    if not xsens_com_queue.empty():
        xsens_com = xsens_com_queue.pop()

    if not xsens_joint_angle_queue.empty():
        xsens_joint_angle = xsens_joint_angle_queue.pop()

    if not imu_queue.empty():
        imu_data = imu_queue.pop()

    if not europa_queue.empty():
        europa_data = europa_queue.pop()

    data_array = numpy.array([gui_cmd[0], gui_cmd[1], europa_data[0], europa_data[1], europa_data[2], imu_data[0], imu_data[1], imu_data[2], imu_data [3], imu_data[4], imu_data[5],  imu_data[6],  imu_data[7],
                    xsens_joint_angle[0], xsens_joint_angle[1], xsens_joint_angle[2], xsens_joint_angle[3], xsens_joint_angle[4], xsens_joint_angle[5], xsens_joint_angle[6], xsens_joint_angle[7], 
                    xsens_joint_angle[8], xsens_joint_angle[9], xsens_joint_angle[10], xsens_joint_angle[11], xsens_joint_angle[12], xsens_joint_angle[13], xsens_joint_angle[14], xsens_joint_angle[15], 
                    xsens_joint_angle[16], xsens_joint_angle[17], xsens_joint_angle[18], xsens_joint_angle[19], xsens_joint_angle[20], xsens_joint_angle[21], xsens_joint_angle[22], xsens_joint_angle[23],
                    xsens_com[0],xsens_com[1],xsens_com[2],xsens_com[3],xsens_com[4],xsens_com[5],xsens_com[6], xsens_com[7],xsens_com[8]], dtype=numpy.float32)
    print('global: ', data_array[5])
    #if bool(record_button):               
    #    with open(filename, 'a') as f:
    #        # Save the headers only once when the file is opened
    #        if f.tell() == 0:
    #            #headers = ['time', 'index', 'ankle_angle', 'ankle_angle', 'ankle_angle', 'imu_ang_vel', 'imu_ang_vel', 'imu_ang_vel']
    #            headers = ['time', 'theta', 'alpha', 'mx', 'my', 'fz', 'imu_ang_vel_x', 'imu_ang_vel_y', 'imu_ang_vel_z', 'imu_accel_x', 'imu_accel_y', 'imu_accel_z', 'State', 'Swing',
    #                       'Right_Hip_x', 'Right_Hip_y', 'Right_Hip_z', 'Right_Knee_x', 'Right_Knee_y', 'Right_Knee_z', 'Right_Ankle_x', 'Right_Ankle_y', 'Right_Ankle_z', 'Right_Ball_of_Foot_x', 'Right_Ball_of_Foot_y', 'Right_Ball_of_Foot_z','Left_Hip_x', 'Left_Hip_y', 'Left_Hip_z', 'Left_Knee_x', 'Left_Knee_y', 'Left_Knee_z', 'Left_Ankle_x', 'Left_Ankle_y', 'Left_Ankle_z', 'Left_Ball_of_Foot_x', 'Left_Ball_of_Foot_y', 'Left_Ball_of_Foot_z',
    #                       'Center_of_Mass_Position_x', 'Center_of_Mass_Position_y', 'Center_of_Mass_Position_z', 'Center_of_Mass_Velocity_x', 'Center_of_Mass_Velocity_y', 'Center_of_Mass_Velocity_z', 'Center_of_Mass_Acceleration_x', 'Center_of_Mass_Acceleration_y', 'Center_of_Mass_Acceleration_z']
    #                       #right_hip_x, right_hip_y, right_hip_z, ]
    #            #['talker']#['Xsens', 'Brain', 'IMU', 'Europa']
    #            f.write(','.join(headers) + '\n')
    #        f.write(','.join([str(x) for x in data_array]) + '\n')
    return data_array

def processed_data_callback(data):
    global record_button
    current_time = (datetime.now().strftime('%H-%M-%S-%f'))
    data_array = numpy.array(data.data)
    
    if bool(record_button):               
        with open(filename, 'a') as f:
            # Save the headers only once when the file is opened
            if f.tell() == 0:
                #headers = ['time', 'index', 'ankle_angle', 'ankle_angle', 'ankle_angle', 'imu_ang_vel', 'imu_ang_vel', 'imu_ang_vel']
                headers = ['time', 'theta', 'alpha', 'mx', 'my', 'fz', 'imu_ang_vel_x', 'imu_ang_vel_y', 'imu_ang_vel_z', 'imu_accel_x', 'imu_accel_y', 'imu_accel_z', 'State', 'Swing',
                           'Right_Hip_x', 'Right_Hip_y', 'Right_Hip_z', 'Right_Knee_x', 'Right_Knee_y', 'Right_Knee_z', 'Right_Ankle_x', 'Right_Ankle_y', 'Right_Ankle_z', 'Right_Ball_of_Foot_x', 'Right_Ball_of_Foot_y', 'Right_Ball_of_Foot_z','Left_Hip_x', 'Left_Hip_y', 'Left_Hip_z', 'Left_Knee_x', 'Left_Knee_y', 'Left_Knee_z', 'Left_Ankle_x', 'Left_Ankle_y', 'Left_Ankle_z', 'Left_Ball_of_Foot_x', 'Left_Ball_of_Foot_y', 'Left_Ball_of_Foot_z',
                           'Center_of_Mass_Position_x', 'Center_of_Mass_Position_y', 'Center_of_Mass_Position_z', 'Center_of_Mass_Velocity_x', 'Center_of_Mass_Velocity_y', 'Center_of_Mass_Velocity_z', 'Center_of_Mass_Acceleration_x', 'Center_of_Mass_Acceleration_y', 'Center_of_Mass_Acceleration_z']
                           #right_hip_x, right_hip_y, right_hip_z, ]
                #['talker']#['Xsens', 'Brain', 'IMU', 'Europa']
                f.write(','.join(headers) + '\n')
            f.write(current_time + ','.join([str(x) for x in data_array]) + '\n')
    
def main():
    global xsens_com_raw, xsens_joint_angle_raw, xsens_com, xsens_joint_angle, brain_data, imu_data, europa_data, record_button, talker_data, filename, notes, gui_cmd, prev_record
    filename = ''
    notes = ''
    talker_data = numpy.array([0], dtype=numpy.float32)
    record_button = 0
    xsens_com_raw = Float32MultiArray()
    xsens_joint_angle_raw = Float32MultiArray()
    
    data_array = numpy.array([0], dtype=numpy.float32)
    prev_record = 0
      
    # Initialize the ROS node
    rospy.init_node('data_node')
    
    # Create subscribers for each of the four sensors and GUI node
    # Ensure that messages are called in this order
    rospy.Subscriber('xsens_com', Float32MultiArray, xsens_com_callback)
    rospy.Subscriber('xsens_joint_angle', Float32MultiArray, xsens_joint_angle_callback)
    rospy.Subscriber('brain', numpy_msg(Floats), brain_callback)
    rospy.Subscriber('sensing_topic', IMUDataMsg, imu_callback)
    rospy.Subscriber('europa_topic', EuropaMsg, europa_callback)
    #rospy.Subscriber('chatter_control', numpy_msg(Floats), gui_callback)
    #rospy.Subscriber('chatter', numpy_msg(Floats), talker_callback)
    #rospy.Subscriber('notes', String, notes_callback)
    #rospy.Subscriber('gui_topic', String, gui_cmd_callback)
    
    rospy.Subscriber('processed_data', numpy_msg(Floats), processed_data_callback)
    #pub = rospy.Publisher('processed_data', numpy_msg(Floats), queue_size=10)
    # wait for subscibers to be made
    #time.sleep(1)
    
    ## Start the data publishing loop
    rate = rospy.Rate(100) # 20Hz fastest I could go without having repeat rows in saving the data
    while not rospy.is_shutdown():
        # Compile the subscribed data into a 1D float array
        #data_array = numpy.concatenate((xsens_com, xsens_joint_angle))
        # Create a 1D string array with the headers of the subscribed data
        #headers = ['Xsens_com', 'Xsens_joint_angles']    
        # Publish the data array to the GUI node
        pub = rospy.Publisher('processed_data', numpy_msg(Floats), queue_size=10)
        #print(data_array)
        data_array = data_save()
        pub.publish(data_array)   
        rate.sleep()

if __name__ == '__main__':
    main()

