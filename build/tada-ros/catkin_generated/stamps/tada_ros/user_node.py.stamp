#!/usr/bin/env python

import rospy
import sys
from tada_ros.msg import UserChoiceMsg
from std_msgs.msg import Bool, String
from tada_ros.user_interface import user_choice_enum as enum
from tada_ros.global_info import constants

class UserNode():
    def __init__(self):
        # anonymous=True ensures that the name is unique by adding random numbers
        rospy.init_node('user_node', anonymous=True)
        rate = rospy.Rate(10) # 10hz

        rospy.Subscriber('user_message_topic', String, self.handle_message)

        # queue_size argument limits the number of queued messages if any
        # subscriber is not receiving them fast enough.
        pub_user_choice = rospy.Publisher('selection_topic', UserChoiceMsg, queue_size=10)
        pub_kill_all = rospy.Publisher('kill_all_topic', Bool, queue_size=1) # queue_size 1 is minimum allowed

        first_time = True
        while not rospy.is_shutdown():
            # receive user input
            char = None
            user_choice = None
            angle_choice = constants.NO_ANGLE   # indicates not chosen
            try:
                if first_time:
                    first_time = False
                else:
                    print("")
                print("""Choose Configuration:
                [P],[D],[I],[E],[C == Choose Angle],
                [c == current config],[A == AUTOHOME],[SPACE == KILL],
                [S == SWEEP], [G == Test Gyro], [H == DEBUG]\n""")
                char = sys.stdin.read(1) # gets one character from user
                # flush any extra characters and the newline
                # (sys.stdin.flush() not working)
                while(sys.stdin.read(1) != "\n"):
                    pass
            except ValueError:
                print("Invalid choice. Please enter a single character.")
                continue

            # process user input
            if char == "P":
                user_choice = enum.UserChoiceEnum.PLANTARFLEXION
            elif char == "D":
                user_choice = enum.UserChoiceEnum.DORSIFLEXION
            elif char == "I":
                user_choice = enum.UserChoiceEnum.INVERSION
            elif char == "E":
                user_choice = enum.UserChoiceEnum.EVERSION
            elif char == "D":
                user_choice = enum.UserChoiceEnum.DORSIFLEXION
            elif char == "C":
                user_choice = enum.UserChoiceEnum.CHOOSE_ANGLE
                # request user input until they select a valid angle
                valid_choice = False
                while not valid_choice:
                    try:
                        input_str = input("--> Desired angle from foreward " \
                            "(press B to go back to the main menu): ")
                        if input_str.isalpha() and len(input_str) == 1 and input_str[0] == "B":
                            break   # pressed "B"
                        angle_choice = int(input_str)
                    except ValueError:  # didn't input a positive integer
                        print("Invalid angle choice. Choose an angle between %s and %s.\n" \
                            % (constants.MIN_ANGLE_CHOICE, constants.MAX_ANGLE_CHOICE))
                        continue
                    if angle_choice < constants.MIN_ANGLE_CHOICE or \
                       angle_choice > constants.MAX_ANGLE_CHOICE: # didn't input a valid angle
                        print("Invalid angle choice. Choose an angle between %s and %s.\n" \
                            % (constants.MIN_ANGLE_CHOICE, constants.MAX_ANGLE_CHOICE))
                        continue
                    else:
                        valid_choice = True
                if not valid_choice:
                    continue
            elif char == "A":
                user_choice = enum.UserChoiceEnum.AUTOHOME
            elif char == " ":
                user_choice = enum.UserChoiceEnum.KILL
                pub_kill_all.publish(1)  # immediately kill the motors and sensors
            elif char == "S":
                user_choice = enum.UserChoiceEnum.SWEEP
            elif char == "G":
                user_choice = enum.UserChoiceEnum.TEST_GYRO
            elif char == "c":
                user_choice = enum.UserChoiceEnum.CURRENT_CONFIG
            elif char == "H":
                user_choice = enum.UserChoiceEnum.DEBUG
            else:
                print("Invalid choice. Please select one of the options.")
                continue

            # send user input to topic
            # .value turns enum object into its numerical value
            msg = UserChoiceMsg(user_choice.value, angle_choice)
            pub_user_choice.publish(msg)

            # for debugging
            print("")
            rospy.loginfo(msg)
            print("")

            rate.sleep() # sleeps to maintain selected rate

    def handle_message(self, data):
        print("Message from Brain:\n")
        print(data.data)
        print("")

if __name__ == '__main__':
    try:
        UserNode()
    except rospy.ROSInterruptException: # ensures stopping if node is shut down
        pass
