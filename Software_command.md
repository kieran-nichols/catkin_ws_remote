# catkin_ws_remote

## Software command document for the TADA nodes

## Dependecies
This repo acts as additive functionality to the tadaros package:
https://github.com/kieran-nichols/catkin_ws_tadaros.git

## General Instruction to run TADA software
### Cellular device
* For connection of raspi and Windows computer
* Turn on hotspot
* Turn on windows computer
* Turn on raspi by plugging in batteries  
* Motor driver x2 (black-ground, white-power) into 12 V battery 
* Pi (black-ground, white-power) into 12 V battery 
* Fan (brown-ground, red-power) into 3.7 V battery 

### Windows computer 
* For Xsens, rosbag, GUI (optional)
* Connect to hotspot and turn on raspi. Give the raspi one minute to connect to the hotspot. 
* Use Angry Scanner IP to get IP addresses of raspi and windows computer (hit "start scanning")
* After it finishes click “sort hostname” to find the IP (should be connected to 3 things) 
#### VNCViewer
* In VNC viewer type in ###.###.##.##:1 from the angry IP scanner to connect to it (Pi password: raspberry) 
* Open up RealVNC, enter the raspi IP address, and open up the raspi GUI
* If the raspi does not connect to the hotspot, hook up the raspi to a monitor, mouse, and keyboard to connect it.
* Open Bash terminal (Ctrl+T)
* Type in “roscore” (Need to do this first so if you relaunch the launch file, you don't mess with the Xsens connection)
* Type in “roslaunch catkin_ws/src/launch_with_motors” 
 
#### Xsens
* open mvn analyze 
* Plug in the license and antenna dongles 
* Make sure all sensors are green and connected and in the right locations 
* Place sensors on person
* Get body dimensions and enter it into body model
* Hit the tree button and make sure port=8000 (and is the same as in the code) Check mark: time code, linear segment kinematics, angular segment kinematics, COM, and joint angles 

#### Visual Studio
 * Type in “rosrun streaming_protocol streaming_protocol_node” (keep this running in the background during collection). If it doesn’t work  go into “catkin_ws remote\devel” and type “setup.bat”  
 * Check things are working by typing in “rostopic list” and all the topics you want to record should pop out including the xsens. Eg xsens_com 
 * Navigate to the folder you want to store data in and type “rosbag record -a -O whateverfilename.bag” 
 * Periodically check rostopic echo to make sure Europa and all the other topics are still working 

## Individual nodes
#### Brain node
rosrun tada_ros brain_node.py

#### Motor node
rosrun soem simple_test 
(this command may not work as you may need to include some arguments, check the launch file)

#### IMU node
rosrun tada_ros sensor_node.py
  
#### Europa node
rosrun tada_ros ble_server.py

#### Xsens node
rosrun streaming_protocol streaming_protocol_node

#### rosbag function
rosbag record -a -O test.bag

#### GUI node
rosrun talker_listener scripts/listener_control.py
rosrun talker_listener scripts/data_processing.py

## To update the repositories
* git add .   (this adds everything) 
* git commit -m “type a message here” 
* git pull  (find HEAD…. And fix merge conflicts) 
* git push 

## Authors
Kieran Nichols, Sofya Akhetova, Becca Roembke, Peter Adamczyk

## License
University of Wisconsin BADGER lab? 

## Acknowledgements
Thanks to the current team and the past work from Ryan Moreno, Mike Greene, Preston Lewis,

## References

Copyright (c) <2022>, <Kieran Nichols>
All rights reserved.

This source code is licensed under the MIT-style license found in the
LICENSE file in the root directory of this source tree.
