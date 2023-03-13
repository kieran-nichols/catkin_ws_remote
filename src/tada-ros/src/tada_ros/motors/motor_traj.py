#!/usr/bin/env python
import rospy
from rospy.numpy_msg import numpy_msg
from tada_ros.msg import MotorDataMsg
from tada_ros.msg import MotorListenMsg
import numpy as np
import math

class motor_traj():
    # motor_command = [0, 0, 180,180, 1500, 1500] # motor mode, time to complete, motor1 position, motor2 position, motor1 torque, motor2 torque
    # Motor mode: 0 is move one direction, 1 is move one direction and then move back to initial
    # Time to complete: if 0, move as fast as possible, if more than 0, move within that time (more helpful for swing
   
    # Initialization and declaration of global-like (self) variables
    def __init__(self):
        rospy.init_node('motor_traj', anonymous=True)
        # Publisher: motor
        self.pub = rospy.Publisher('motor_command', MotorDataMsg, queue_size=10) 
        self.motor_command = MotorDataMsg()
        # Subscribers: brain; considered getting directly from motor but the brain has important info and decisions to make with the motor info
        self.sub = rospy.Subscriber('brain', BrainListenMsg, self.listener)
        self.curr_pos1 = 0; self.curr_pos2 = 0
        ## Add rospy.Subscriber with self, its necessary global-like variables, and appropiate listeners (aka callback functions)
        
        # Initialize the global-like variables
        self.homed1 = 0; self.homed2 = 0
        self.cnts_per_rev = 567
                
        ## Add variables for IMU and Europa here
        
    # defining the listener functions for the subscibed nodes
    def listener(self,data):
        self.homed1 = data.homed1
        self.homed2 = data.homed2
        self.initial_tada_angle = data.initial_tada_angle
        self.dorsiflexed_tada_angle = data.dorsiflexed_tada_angle
        
    ## Add functions for IMU and Europa
                             
    # Main function that will continuous iterate; it will have a mixture of publishing and subscribing
    def action(self):
        # Initialize the local variables
        var1 = 0; var2 = 0
        prev_var1 = 0; prev_var2 = 0
        var = []
        rate = rospy.Rate(100) # every 0.1 sec
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
        
        # function to calculate the trajectory of motors for dorsiflexion
        def move_swing(self):
            # initial pos to dorsiflexion back to intial position
            
            
        # main loop that controls the TADA
        while not rospy.is_shutdown(): #and rospy.on_shutdown(hook):
            # repurpose and shorten the self variables to be local variables
            motor_command = self.motor_command
            curr_pos1 = self.curr_pos1; curr_pos2 = self.curr_pos2
            homed1 = self.homed1; homed2 = self.homed2
            ## add IMU and Europa variables here that need to be read
            ## variables that are called here are updated to be used in this while loop
                        
            # read input from the terminal; expecting between 1 and 3 inputs
            raw_var = list(input("Enter motor 1 and 2 movement: ").split())
            
            # assigns the raw input data to var and ignores error if no input was given
            if raw_var: 
                var = raw_var
            else:
                var = [False] 
            
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
                  
            # if only 2 commands are given then calculate motor angle as a function of the ankle angles which are the inputs
            elif len(var)==2:
                self.theta_deg = int(var[0])
                self.alpha_deg = int(var[1])
                # Convert input of PF, EV, inclination angle to motor angles from homed
                motor = TADA_angle(self)
                var1 = int(motor[0]) 
                var2 = int(motor[1])
                print("Moving to", var1, var2,"\n")
             
             # if first command is m, then send global motor commands
            elif len(var)==2 and var[0]== "m":
                var1 = int(var[1]) 
                var2 = int(var[2])
                
            elif len(var)==3 and var[0]== "swing":
                self.initial_tada_angle = int(var[1]) 
                self.dorsiflexed_tada_angle = int(var[2])
                move_swing(self)
                               
            # else statement to keep motor position the same; consider also to return to home     
            else:
                var1 = curr_pos1 # 180
                var2 = curr_pos2 # 567
                print("Kept current position", var1, var2,"\n")
            
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
            rate.sleep()
            
        
if __name__ == '__main__':
    try:
        BrainNode().action()
    except rospy.ROSInterruptException: # ensures stopping if node is shut down
        pass

