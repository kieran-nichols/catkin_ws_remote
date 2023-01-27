#!/usr/bin/env python
import rospy
import os
import time
import sys
import signal
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from std_msgs.msg import String
from tada_ros.msg import MotorDataMsg
from tada_ros.msg import MotorListenMsg
from tada_ros.msg import IMUDataMsg
from tada_ros.msg import EuropaMsg
#from tada_ros.europa import EuropaBLE
from tada_ros.sensors import sensor_node
import numpy as np
import math
import os
import threading

class BrainNode():
    # motor_command = [0, 0, 180,180, 1500, 1500] # motor mode, time to complete, motor1 position, motor2 position, motor1 torque, motor2 torque
    # Motor mode: 0 is move one direction, 1 is move one direction and then move back to initial
    # Time to complete: if 0, move as fast as possible, if more than 0, move within that time (more helpful for swing
   
    # Initialization and declaration of global-like (self) variables
    def __init__(self):
        #rospy.init_node('sensor_node', anonymous=True)
        #rospy.init_node('IMU_controller', anonymous=True)
        rospy.init_node('brain', anonymous=True)
        #Subscribbing to some topics
        print("init brain")
        rospy.Subscriber('europa_topic', EuropaMsg, self.handle_europa_input)
        rospy.Subscriber('sensing_topic', IMUDataMsg, self.handle_sensor_input)
        rospy.Subscriber('gui_topic', String, self.GUI_input)

        #imu_sensor = sensor_node.SensorNode()
        #self.sensor_info = Sensor()
        # Publisher: motor
        self.pub = rospy.Publisher('motor_command', MotorDataMsg, queue_size=10)
                
        self.motor_command = MotorDataMsg()
        # Subscribers: motors, IMU, Europa; subscribe command with it necessary variables that will be attached to self
        self.sub = rospy.Subscriber('motor_listen', MotorListenMsg, self.listener)
        self.curr_pos1 = 0; self.curr_pos2 = 0
        #rospy.spin() # keeps python from exiting until this node is stopped
        ## Add rospy.Subscriber with self, its necessary global-like variables, and appropiate listeners (aka callback functions)
        #handling the sensor data
        # Initialize the global-like variables
        self.homed1 = 0; self.homed2 = 0
        self.cnts_per_rev = 567
        self.raw_var = [False]
        
        def input_thread():
            while not rospy.is_shutdown():
                # sleep function so other commands can be typed first
                time.sleep(0.1)
                print("type 'help' for description of full instructions")
                print("Enter command(s): ")
                self.raw_var = list(input().split())
#                 return raw_var
    
        input_thread = threading.Thread(target=input_thread, args=())
        input_thread.start()
    
    ## Functions for IMU and Europa
    def handle_sensor_input(self, msg_data):
        # translates IMUDataMsg ROS message to IMUData class and stores
        #print("handler trg")
        self.current_IMU_data = IMU_controller.ROS_message_to_IMUData(msg_data)
        
    def handle_europa_input(self, msg_data):
        # translates IMUDataMsg ROS message to IMUData class and stores
        # ~ print("in the brain")
        # ~ print(msg_data)
        pass # temporary
        #self.current_europa_data = IMU_controller.ROS_message_to_IMUData(msg_data)
    
    def GUI_input(self, msg_data):
        # translates IMUDataMsg ROS message to IMUData class and stores
        #print("handler trg")
        string = str(msg_data.data)
#         print("Enter command(s): ")
#         print(string)
        self.raw_var = list(string.split())

        ## Add variables for IMU and Europa here
        
    # defining the listener functions for the subscibed nodes
    def listener(self,data):
        self.curr_pos1 = data.curr_pos1
        self.curr_pos2 = data.curr_pos2
    
    # Main function that will continuous iterate; it will have a mixture of publishing and subscribing
    def action(self):
        # Initialize the local variables
        var1 = 0; var2 = 0
        prev_var1 = 0; prev_var2 = 0
        var = []
#         rate_motor = rospy.Rate(10) # every 0.1 sec
        rate = rospy.Rate(10) # every 0.1 sec # slowest control loop 
        # specify home when the motor is turned on to be the motor positions at start
        self.homed1 = self.curr_pos1; self.homed2 = self.curr_pos2
            
        def TADA_angle(self):
            theta_deg = self.theta_deg; alpha_deg = self.alpha_deg
            homed1 = self.homed1; homed2 = self.homed2
            
            theta = theta_deg*math.pi/180
            beta = 5*math.pi/180
            q3 = 2*(np.arccos(np.sin(theta/2)/np.sin(beta))) # arccos in python always returns real values
#             alpha = np.arctan2(PF*math.pi/180, EV*math.pi/180)
            alpha = alpha_deg*math.pi/180
            M1 = 180/math.pi*(alpha - np.arctan2(np.tan(q3/2),np.cos(beta))) 
            M2 = -180/math.pi*(-(alpha + np.arctan2(np.tan(q3/2), np.cos(beta))))
            # print motor angles in non-TADA ref frame
            print("Motor angles from homed", M1, M2)
            # Wrapping function that ensures that the angle is between 180 and -180;
            ## need to finish verify
            M1 = np.degrees(np.arctan2(np.sin(np.radians(M1)), np.cos(np.radians(M1))))
            M2 = np.degrees(np.arctan2(np.sin(np.radians(M2)), np.cos(np.radians(M2))))
            print("Wrapped motor angles from homed", M1, M2)
            # Convert to counts for motor movement
            M1 = M1*self.cnts_per_rev/360 + homed1
            M2 = M2*self.cnts_per_rev/360 + homed2
            print("Global motor angles", M1, M2,"")
            return [M1, M2]
        
        # Test for sagittal only ankle movement from neutral to dorsiflexed and back to neutral
        # Inpput array: [initial0 (deg), final1 (deg)   , time (ms), increments (unitless), return (0,1), initial2 (deg)]
        # Sample array: [theta0, alpha0, theta1, alpha1 , 200      , 5                    , 1           , theta2, alpha2]
        # Sample array: [theta0, 0     , theta1, 0      , 300      , 3                    , 0           , 0     , 0     ]
        # All alphas will be 0 or 180 to keep sagittal only movements (0 for plantarflexion and 180 for dors
        def move_swing(self):
            print("need to complete")
            
        # main loop that controls the TADA
        while not rospy.is_shutdown(): #and rospy.on_shutdown(hook):
            # repurpose and shorten the self variables to be local variables
            motor_command = self.motor_command
            curr_pos1 = self.curr_pos1; curr_pos2 = self.curr_pos2
            homed1 = self.homed1; homed2 = self.homed2
            ## add IMU and Europa variables here that need to be read
            ## variables that are called here are updated to be used in this while loop
                       
            # read input from the terminal; expecting between 1 and 3 inputs
#             print("type 'help' for description of full instructions")
#             raw_var = list(input("Enter command(s): ").split())
#             self.raw_var = self.input_thread
            
            # assigns the raw input data to var and ignores error if no input was given
            if self.raw_var: 
                var = self.raw_var
            else:
                var = [False] 
            
            # if first command is h then kill motor node; launch file will restart it in 2 seconds
            ## need smarter way to restart the motor node
            if len(var)== 2:
                if var[0]=="kill":
                    if var[1]=="m":
                        os.system("rosnode kill /motor")
                        print("motor node will restart\n")
    #                     os.system("roslaunch ~/catkin_ws/src/motor_node.launch") # does not work as intended
                    elif var[1]=="a":
                        os.system("rosnode kill -a")
                        os.system("killall -9 rosmaster")
                        print("ROS has been killed")
                        
                    else:
                        print("Please enter options 'm' or 'a'\n")
                 
                 # if only 2 commands are given then calculate motor angle as a function of the ankle angles which are the inputs
                else:
                    self.theta_deg = float(var[0])
                    self.alpha_deg = float(var[1])
                    # Convert input of PF, EV, inclination angle to motor angles from homed
                    motor = TADA_angle(self)
                    var1 = int(motor[0]) 
                    var2 = int(motor[1])
                    print("Moving to", var1, var2,"\n")
                
            elif len(var)== 1:
                # print statement to describe instructions
                if var[0]=="help":                
                    print("\nTo command motor movement: 'm num num' (num is motor ticks where 567 for full rev)")
                    print("To command ankle angles: 'theta(0 to 10 deg) alpha(-180 to 180 deg)'")
                    print("Use 'h' to home, 'r' to return to home, 'c' for print current position")
                    print("Use 'i' to read IMU, 'e' to read Europa, 'kill m' or 'kill a' to kill motor or all systems\n")
#                     self.raw_var = [False]
                    
                # if first command is h then assign current position as homed values
                ## need to fix homing the current position; it seems that the correct value comes in the future iteration
                if var[0]=="h":
                    self.homed1 = curr_pos1
                    self.homed2 = curr_pos2
                    print(curr_pos1, curr_pos2)
                    print("created new homed positions:", self.homed1, self.homed2,"\n")     
                
                # if first command is r then return the motors back to home
                elif var[0]=="r":
                # create new homed value and specify the movement toward the new home which should be the same position as the old home
    #                 var1 = cnts_per_rev*round(homed1*cnts_per_rev)
    #                 var2 = cnts_per_rev*round(homed2*cnts_per_rev)
                    var1 = homed1
                    var2 = homed2
                    print("returned to home\n")  
                
                # if first command is c then print the current motor positions
                elif var[0]=="c":
                    print("Current motor positions:", curr_pos1, curr_pos2,"\n")
                    var1 = curr_pos1 # 180
                    var2 = curr_pos2 # 567
                
                ## if first command is i then read the IMU's state
                elif var[0]=="i":
                    print() 
                
                ## if first command is i then read the Eropa's sagittal and frontal moments
                elif var[0]=="e":
                    print()
                
                # do nothing
                else:
                    pass
#                     print("Did nothing")
                    
            elif len(var)== 3:             
                # if first command is m, then send global motor commands
                if var[0] == "m":
                    var1 = int(var[1]) 
                    var2 = int(var[2])
                    
                elif var[0]== "swing":
                    # Test for sagittal only ankle movement from neutral to dorsiflexed and back to neutral
                    # Inpput array: [initial0 (deg), final1 (deg)   , time (ms), increments (unitless), return (0,1), initial2 (deg)]
                    # Sample array: [theta0, alpha0, theta1, alpha1 , 200      , 5                    , 1           , theta2, alpha2]
                    # Sample array: [theta0, 0     , theta1, 0      , 300      , 3                    , 0           , 0     , 0     ]
                    # All alphas will be 0 or 180 to keep sagittal only movements (0 for plantarflexion and 180 for dorsiflexion)
                    self.swing_test = [float(var[1]), 0, float(var[2]), 0, 300, 3, 1, 0, 0]
                    move_swing(self)
                    
                # do nothing
                else:
                    pass
#                     print("Did nothing")
                               
            # else statement to keep motor position the same; consider also to return to home     
            else:
                var1 = curr_pos1 # 180
                var2 = curr_pos2 # 567
                print("Kept current position", var1, var2,"\n")
            
            # cmd to refresh terminal entry variable
            self.raw_var = [False]
            
            # set up object to publish to motor node
            motor_command.mode = 0
            motor_command.duration = 0
            motor_command.motor1_move = var1
            motor_command.motor2_move = var2
            motor_command.motor1_torque = 1500 # be careful with torque values, max torque is dependent on the motor loads
            motor_command.motor2_torque = 1500 # 1000 for no load, above 1500 for assembled TADA
            prev_var1 = var1
            prev_var2 = var2
#             rospy.loginfo(motor_command) 
            self.pub.publish(motor_command)
#             rate_motor.sleep()
            rate.sleep()
            
if __name__ == '__main__':
    try:
        BrainNode().action()
        pass
    except rospy.ROSInterruptException: # ensures stopping if node is shut down
        pass
