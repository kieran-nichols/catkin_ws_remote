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
from collections import deque
import sqlite3
# got help for the data saving correctly from https://stackoverflow.com/questions/48830056/use-data-from-multiple-topics-in-ros-python

class dataprocessing:
    def __init__(self):
        self.filename = ''
        self.notes = ''
        self.talker_data = numpy.array([0], dtype=numpy.float32)
        self.record_button = 0
        self.xsens_com_raw = Float32MultiArray()
        self.xsens_joint_angle_raw = Float32MultiArray()
        self.xsens_com = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)
        self.xsens_joint_angle = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)   
        self.brain_data = numpy.array([0], dtype=numpy.float32)
        self.imu_data = numpy.array([0,0,0,0,0,0,0,0], dtype=numpy.float32)
        self.europa_data = numpy.array([0,0,0], dtype=numpy.float32)
        self.gui_cmd = numpy.array([0,0], dtype=numpy.float32) # str('0,0')
        self.data_array = numpy.array([0], dtype=numpy.float32)
        self.prev_record = 0
        self.data_array = numpy.array([0], dtype=numpy.float32)
        self.tag = ''
        self.var_num = 5
        
        #self.gui_cmd_queue = deque(maxlen = 5)
        #self.europa_data_queue = deque(maxlen = 5)
        #self.imu_data_queue = deque(maxlen = 5)
        #self.xsens_joint_angle_queue = deque(maxlen = 5)
        #self.xsens_com_queue = deque(maxlen = 5)
        ## make an empty array for each item of gui_cmd_queue
        #for i in range(5):
        #    self.gui_cmd_queue.append(numpy.array([0,0], dtype=numpy.float32))
        #    self.europa_data_queue.append(numpy.array([0,0,0], dtype=numpy.float32))
        #    self.imu_data_queue.append(numpy.array([0,0,0,0,0,0,0,0], dtype=numpy.float32)) 
        #    self.xsens_joint_angle_queue.append(numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)) 
        #    self.xsens_com_queue.append(numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32))     
        #print('gui_cmd_queue', self.gui_cmd_queue)
        self.counter = 0
        
        # Connect to the database
        self.conn = sqlite3.connect('data.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        # Create a table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_1 TEXT,
                subscriber_2 TEXT
            )
        ''')
    
    # define callback functions for the ROS subscibers
    def xsens_com_callback(self, data):
        self.xsens_com = numpy.array(data.data)
        if len(self.xsens_com)!=9:
            self.xsens_com = numpy.array([0,0,0,0,0,0,0,0], dtype=numpy.float32)       
        self.tag = 'xsens_com'
        self.counter += 1
        # need to put this save function in each callback that needs to save data
        #self.data_save()
        # Insert the processed data into the database
        #cursor.execute('INSERT INTO data (subscriber_1) VALUES (?)', (self.xsens_com,))
        #conn.commit()
        
    def xsens_joint_angle_callback(self, data): 
        self.xsens_joint_angle = numpy.array(data.data)
        if len(self.xsens_joint_angle)!=24: 
            self.xsens_joint_angle = numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=numpy.float32)  
        self.tag = 'xsens_joint_angle'
        self.counter += 1
        # need to put this save function in each callback that needs to save data
        #self.data_save()
        # Insert the processed data into the database
        #cursor.execute('INSERT INTO data (subscriber_1) VALUES (?)', (self.xsens_com,))
        #conn.commit()
        
        
    def brain_callback(self, data):
        self.brain_data = data.data
    
    def imu_callback(self, data):
        self.imu_data = [data.accel_x, data.accel_y, data.accel_z, data.gyro_x, data.gyro_y, data.gyro_z, data.state, data.swing_time]
        # need to put this save function in each callback that needs to save data
        self.tag = 'imu_data'
        self.counter += 1
        self.data_save()
        # Insert the processed data into the database
        self.cursor.execute('INSERT INTO data (subscriber_1) VALUES (?)', (self.imu_data[0],))
        self.conn.commit()
        
    def europa_callback(self, data):
        self.europa_data = [data.mx, data.my, data.fz]
        # need to put this save function in each callback that needs to save data
        self.tag = 'europa_data'
        self.counter += 1
        self.data_save()
        # Insert the processed data into the database
        self.cursor.execute('INSERT INTO data (subscriber_2) VALUES (?)', (self.europa_data[0],))
        self.conn.commit()
    
    def gui_cmd_callback(self, data):
        self.gui_cmd = [float(x) for x in str(data.data).split()] #list(float(str(data.data).split(',')))
        if len(self.gui_cmd)!=2:
            self.gui_cmd = numpy.array([0,0], dtype=numpy.float32)
            
        # need to put this save function in each callback that needs to save data
        self.tag = 'gui_cmd'
        self.counter += 1
        #self.data_save()
        # Insert the processed data into the database
        #self.cursor.execute('INSERT INTO data (subscriber_1) VALUES (?)', (self.xsens_com,))
        #self.conn.commit()
        
    # need to find way to have the talker_callback save continuously to a file while the gui_callback can change the filename
    def talker_callback(self, data):
        self.talker_data = data.data[0:7]
              
    def notes_callback(self, data):
        self.notes = data.data
        current_time = time.strftime('%H-%M-%S', time.gmtime())
        if bool(self.record_button): 
            # Save the notes string to a notes file (txt) for the data
            timestamp = time.strftime('%Y-%m-%d', time.gmtime())
            notes_filename = ('catkin_ws/src/talker_listener/data/notes_{}.txt'.format(timestamp))
            with open(notes_filename, 'a') as f:
                # Save the headers only once when the file is opened
                f.write( current_time + ': ' + self.notes + '\n')
        
    def gui_callback(self, data):
        self.prev_record = self.record_button
        self.record_button = data.data[0]
        
        if bool(self.record_button - self.prev_record == 1): # moment when record botton is turned on
            # Save the data array to a CSV file with a time and date in the file name
            self.timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())
            self.filename = ('catkin_ws/src/talker_listener/data/data_{}.csv'.format(self.timestamp))
            #f = open(self.filename, 'x')
            #f.close()
            print('file created')
        
        # For testing purposes, this function doesn't have a variable that saves data to file
        # need to put this save function in each callback that needs to save data
        #self.data_save()
    #def tag_func(self, tag):
    #    self.tag = tag
    #    self.data_save()
    
    # function dedicated to saving for whichever callback that becomes active, if data is not streming from a topic (100 Hz), then data is saved only when the callback is called
    def data_save(self):
        # find unique values from each callback buffer
        #print(self.gui_cmd, self.gui_cmd_queue)
        #self.gui_cmd_queue = self.gui_cmd_queue.append(self.gui_cmd)
        #self.europa_data_queue = self.europa_data_queue.append(self.europa_data)
        #self.imu_data_queue = self.imu_data_queue.append(self.imu_data)
        #self.xsens_joint_angle_queue = self.xsens_joint_angle_queue.append(self.xsens_joint_angle)
        #self.xsens_com_queue = self.xsens_com_queue.append(self.xsens_com)
        #print('tag', self.tag, 'count', self.counter)
        #gui_cmd = self.gui_cmd
        #europa_data = self.europa_data
        #imu_data = self.imu_data
        #xsens_joint_angle = self.xsens_joint_angle
        #xsens_com = self.xsens_com
        #print('tag', self.tag, 'count', self.counter)
        #gui_cmd = numpy.array([0,0], dtype=numpy.float32)

        #if self.tag == 'imu_data': imu_data = self.imu_data
        #elif self.tag == 'europa_data': europa_data = self.europa_data
        #elif self.tag == 'xsens_joint_angle': xsens_joint_angle = self.xsens_joint_angle
        #elif self.tag == 'xsens_com': xsens_com = self.xsens_com
        #elif self.tag == 'gui_cmd': gui_cmd = self.gui_cmd
        #else: 
        #    print("nothing")
        #else: 
        #    gui_cmd = numpy.array([0,0], dtype=numpy.float32)
        #    europa_data = numpy.array([0,0,0], dtype=numpy.float32)
        #    imu_data = numpy.array([0,0,0,0,0,0,0,0], dtype=numpy.float32)
        #    xsens_joint_angle = numpy.array([0,0,0,0,0,0,0,0], dtype=numpy.float32)
        #    xsens_com = numpy.array([0,0,0], dtype=numpy.float32)
        #var_num = self.var_num
        #if self.counter//var_num == 0:
        #print('tag', self.tag)
        self.data_array = numpy.array([self.europa_data[0], self.europa_data[1], self.europa_data[2], self.imu_data[0], self.imu_data[1], self.imu_data[2], self.imu_data [3], self.imu_data[4], self.imu_data[5], self.imu_data[6], self.imu_data[7]])
                #numpy.array([gui_cmd[0], gui_cmd[1], europa_data[0], europa_data[1], europa_data[2], imu_data[0], imu_data[1], imu_data[2], imu_data [3], imu_data[4], imu_data[5], imu_data[6], imu_data[7],
                #xsens_joint_angle[0], xsens_joint_angle[1], xsens_joint_angle[2], xsens_joint_angle[3], xsens_joint_angle[4], xsens_joint_angle[5], xsens_joint_angle[6], xsens_joint_angle[7], 
                #xsens_joint_angle[8], xsens_joint_angle[9], xsens_joint_angle[10], xsens_joint_angle[11], xsens_joint_angle[12], xsens_joint_angle[13], xsens_joint_angle[14], xsens_joint_angle[15], 
                #xsens_joint_angle[16], xsens_joint_angle[17], xsens_joint_angle[18], xsens_joint_angle[19], xsens_joint_angle[20], xsens_joint_angle[21], xsens_joint_angle[22], xsens_joint_angle[23],
                #xsens_com[0],xsens_com[1],xsens_com[2],xsens_com[3],xsens_com[4],xsens_com[5],xsens_com[6], xsens_com[7],xsens_com[8]], dtype=numpy.float32)
  
        #self.data_array = numpy.unique(numpy.concatenate((self.gui_cmd, self.europa_data, self.imu_data, self.xsens_joint_angle, self.xsens_com)))
        #if self.tag == 'save':
            #print('tag', self.tag)
        #print(self.data_array)
        if bool(self.record_button):
            #time.sleep(0.1)
        #print(self.data_array)
        #print('record', self.record_button)
        #if bool(self.record_button):
            current_time = str(time.time_ns() // 1_000_000)
            with open(self.filename, 'a') as f:
                # Save the headers only once when the file is opened
                if f.tell() == 0:
                    #headers = ['time', 'index', 'ankle_angle', 'ankle_angle', 'ankle_angle', 'imu_ang_vel', 'imu_ang_vel', 'imu_ang_vel']
                    headers = ['time', 'theta', 'alpha', 'mx', 'my', 'fz', 'imu_ang_vel_x', 'imu_ang_vel_y', 'imu_ang_vel_z', 'imu_accel_x', 'imu_accel_y', 'imu_accel_z', 'State', 'Swing',
                                'Right_Hip_x', 'Right_Hip_y', 'Right_Hip_z', 'Right_Knee_x', 'Right_Knee_y', 'Right_Knee_z', 'Right_Ankle_x', 'Right_Ankle_y', 'Right_Ankle_z', 'Right_Ball_of_Foot_x', 'Right_Ball_of_Foot_y', 'Right_Ball_of_Foot_z','Left_Hip_x', 'Left_Hip_y', 'Left_Hip_z', 'Left_Knee_x', 'Left_Knee_y', 'Left_Knee_z', 'Left_Ankle_x', 'Left_Ankle_y', 'Left_Ankle_z', 'Left_Ball_of_Foot_x', 'Left_Ball_of_Foot_y', 'Left_Ball_of_Foot_z',
                                'Center_of_Mass_Position_x', 'Center_of_Mass_Position_y', 'Center_of_Mass_Position_z', 'Center_of_Mass_Velocity_x', 'Center_of_Mass_Velocity_y', 'Center_of_Mass_Velocity_z', 'Center_of_Mass_Acceleration_x', 'Center_of_Mass_Acceleration_y', 'Center_of_Mass_Acceleration_z']
                                #right_hip_x, right_hip_y, right_hip_z, ]
                    #['talker']#['Xsens', 'Brain', 'IMU', 'Europa']
                    f.write(','.join(headers) + '\n')
                f.write(current_time + ','.join([str(x) for x in self.data_array]) + '\n')
                
                #if bool(self.record_button - self.prev_record == -1): 
                #    f.close()
                #    print('file closed')
                #return self.data_array

if __name__ == '__main__':
    DataProcessing = dataprocessing()
    # Initialize the ROS node
    rospy.init_node('data_node')
    
    
    # Create subscribers for each of the four sensors and GUI node
    rospy.Subscriber('xsens_com', Float32MultiArray, DataProcessing.xsens_com_callback)
    rospy.Subscriber('xsens_joint_angle', Float32MultiArray, DataProcessing.xsens_joint_angle_callback)
    rospy.Subscriber('brain', numpy_msg(Floats), DataProcessing.brain_callback)
    rospy.Subscriber('sensing_topic', IMUDataMsg, DataProcessing.imu_callback)
    rospy.Subscriber('europa_topic', EuropaMsg, DataProcessing.europa_callback)
    rospy.Subscriber('chatter_control', numpy_msg(Floats), DataProcessing.gui_callback)
    rospy.Subscriber('chatter', numpy_msg(Floats), DataProcessing.talker_callback)
    rospy.Subscriber('notes', String, DataProcessing.notes_callback)
    rospy.Subscriber('gui_topic', String, DataProcessing.gui_cmd_callback)
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
