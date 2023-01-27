#!/usr/bin/env python

import rospy
import os
import signal
from tada_ros.msg import KillConfirmationMsg
from std_msgs.msg import String, Bool

class MotorNode():
    pub_killed_confirm = None

    def __init__(self):
        # anonymous=True ensures that the name is unique by adding random numbers
        rospy.init_node('motor_node', anonymous=True)
        print("initialized IN MOTOR")
        rospy.Subscriber('movement_topic', String, self.handle_movement_command)
        # killing the program is its own topic so that there's minimal delay
        rospy.Subscriber('kill_all_topic', Bool, self.handle_kill_command)

        # queue_size argument limits the number of queued messages if any
        # subscriber is not receiving them fast enough.
        self.pub_killed_confirm = rospy.Publisher('kill_confirmation_topic', KillConfirmationMsg, queue_size=10)

        rospy.spin() # keeps python from exiting until this node is stopped

    def handle_movement_command(self, data):
        # for debugging
        print("")
        rospy.loginfo(rospy.get_caller_id() + " I heard movement: %s", data.data)
        print("")

    def handle_kill_command(self, data):
        # for debugging
        print("")
        rospy.loginfo(rospy.get_caller_id() + " I heard kill boolean: %s", data.data)
        print("")
        if data.data == True:
            self.kill_motors()

        # send confirmation message
        msg = KillConfirmationMsg(motors_killed=True, sensors_killed=False)
        self.pub_killed_confirm.publish(msg)

        # interrupt the program like a Keyboard Interrupt
        os.kill(os.getpid(), signal.SIGTERM)

    def kill_motors(self):
        # TODO: motordependent code
        print("Killing Motor Node")

if __name__ == '__main__':
    MotorNode()
