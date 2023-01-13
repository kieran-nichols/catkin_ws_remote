# !/usr/bin/env python3
import rospy
import pandas as pd
import numpy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

def callback(data):
  #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data[0])
  rospy.loginfo(data.data)

def listener():
  rospy.init_node('listener', anonymous=True)
  rospy.Subscriber('chatter', numpy_msg(Floats), callback)
  rospy.spin()

if __name__ == '__main__':
  listener()
