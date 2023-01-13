import rospy
import time
import numpy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from std_msgs.msg import String, Float32MultiArray, MultiArrayDimension
from std_msgs.msg import String
from multiprocessing import Process, Manager, freeze_support, Pool, Pipe, Queue
# import inspect module
import inspect

# define callback functions for the ROS subscibers
def xsens_com_callback(data):
    global xsens_com_raw, xsens_com
    #print(data.data)
    xsens_com = numpy.array(data.data)
    #xsens_com = xsens_com.reshape(data.layout.dim[0].size, data.layout.dim[1].size)
    
def xsens_joint_angle_callback(data):
    global xsens_joint_angle_raw, xsens_joint_angle
    #print(data.data)
    xsens_joint_angle = numpy.array(data.data)
    #xsens_joint_angle = xsens_joint_angle.reshape(data.layout.dim[0].size, data.layout.dim[1].size)

def brain_callback(data):
    global brain_data
    brain_data = data.data

def imu_callback(data):
    global imu_data
    imu_data = data.data

def europa_callback(data):
    global europa_data
    europa_data = data.data

# need to find way to have the talker_callback save continuously to a file while the gui_callback can change the filename
def talker_callback(data):
    global record_button, filename, notes
    data_array = data.data[0:7]
    #print(record_button)
    if bool(record_button[0]):  
        with open(filename, 'a') as f:
            # Save the headers only once when the file is opened
            if f.tell() == 0:
                headers = ['index', 'ankle_angle', 'ankle_angle', 'ankle_angle', 'imu_ang_vel', 'imu_ang_vel', 'imu_ang_vel']
                #['talker']#['Xsens', 'Brain', 'IMU', 'Europa']
                f.write(','.join(headers) + '\n')
            f.write(','.join([str(x) for x in data_array]) + '\n')
    #print(args[0])  

def gui_callback(data):
    global record_button, filename
    #print(data.data)
    record_button = data.data
    if bool(data.data[0]): 
        # Save the data array to a CSV file with a time and date in the file name
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.gmtime())
        filename = ('catkin_ws/src/talker_listener/data/data_{}.csv'.format(timestamp))
        print('file created')

#def notes_callback(data):
#    global record_button, notes
#    #print(data.data)
#    notes = data.data
#    if bool(data.data[0]): 
#        # Save the notes string to a notes file (txt) for the data
#        timestamp = time.strftime('%Y-%m-%d', time.gmtime())
#        notes_filename = ('catkin_ws/src/talker_listener/data/notes_{}.txt'.format(timestamp))
#        with open(notes_filename, 'a') as f:
#            # Save the headers only once when the file is opened
#            f.write(notes + '\n')
#        #print('file created')  
    
def main():
    global xsens_com_raw, xsens_joint_angle_raw, xsens_com, xsens_joint_angle, brain_data, imu_data, europa_data, record_button, talker_data, filename#, notes
    filename = ''
    #notes = ''
    talker_data = numpy.array([0], dtype=numpy.float32)
    record_button = numpy.array([0], dtype=numpy.float32)
    xsens_com_raw = Float32MultiArray()
    xsens_joint_angle_raw = Float32MultiArray()
    xsens_com = numpy.array([0], dtype=numpy.float32)
    xsens_joint_angle = numpy.array([0], dtype=numpy.float32)
    
      
    # Initialize the ROS node
    rospy.init_node('data_node')
    
    # Create subscribers for each of the four sensors and GUI node
    rospy.Subscriber('xsens_com', Float32MultiArray, xsens_com_callback)
    rospy.Subscriber('xsens_joint_angle', Float32MultiArray, xsens_joint_angle_callback)
    rospy.Subscriber('brain', numpy_msg(Floats), brain_callback)
    rospy.Subscriber('imu', numpy_msg(Floats), imu_callback)
    rospy.Subscriber('europa', numpy_msg(Floats), europa_callback)
    rospy.Subscriber('chatter_control', numpy_msg(Floats), gui_callback)
    rospy.Subscriber('chatter', numpy_msg(Floats), talker_callback)
    #rospy.Subscriber('notes', String, notes_callback)
 
    
    ## Start the data publishing loop
    rate = rospy.Rate(100)
    while not rospy.is_shutdown():
        # Compile the subscribed data into a 1D float array
        data_array = numpy.concatenate((xsens_com, xsens_joint_angle))
        # Create a 1D string array with the headers of the subscribed data
        headers = ['Xsens_com', 'Xsens_joint_angles']    
        # Publish the data array to the GUI node
        pub = rospy.Publisher('processed_data', numpy_msg(Floats), queue_size=10)
        #print(data_array)
        pub.publish(data_array)   
        rate.sleep()

if __name__ == '__main__':
    main()

