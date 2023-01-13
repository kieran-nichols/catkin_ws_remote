#!/usr/bin/env python3
import rospy
#from std_msgs.msg import String
import pandas as pd
import numpy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

# Main talker function to read the csv file and sends the data to the listener node
def talker():
    df = pd.read_csv('csv_file')
    index = df['index'].to_numpy()
    ankle_angle = df['ankle_angle'].to_numpy()
    imu_ang_vel = df['imu_ang_vel'].to_numpy()
    stride_frame_index = df['stride_frame_index'].to_numpy()
    swing_data_peak = df['swing_data_peak'].to_numpy()
    ankle_stride_peak = df['ankle_stride_peak'].to_numpy()
    output_info = ankle_stride_peak #get the same size array
    i = 0

    #pub = rospy.Publisher('chatter', String, queue_size=10)
    pub = rospy.Publisher('chatter', numpy_msg(Floats), queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        # Data is sorted in three rows: raw data, swing peaks, stance peaks
        hello_str = numpy.array([index[i], ankle_angle[i], ankle_angle[i], ankle_angle[i], imu_ang_vel[i], imu_ang_vel[i], imu_ang_vel[i],
                                 stride_frame_index[i], ankle_stride_peak[i], ankle_stride_peak[i], ankle_stride_peak[i], swing_data_peak[i], swing_data_peak[i], swing_data_peak[i],
                                  stride_frame_index[i], ankle_stride_peak[i], ankle_stride_peak[i], ankle_stride_peak[i], swing_data_peak[i], swing_data_peak[i], swing_data_peak[i]],
                               dtype=numpy.float32) #str(ankle_angle[i])
        #rospy.loginfo(hello_str[0])
        pub.publish(hello_str)
        i = i + 1
        rate.sleep()
if __name__ == '__main__':
  try:
    talker()
  except rospy.ROSInterruptException:
    pass
