# catkin_ws_remote

## Windows Remote controller for Two axis Adaptable Ankle (TADA) prosthetic device

## Dependecies
This repo acts as additive functionality to the tadaros package:
https://github.com/kieran-nichols/catkin_ws_tadaros.git

## Prerequisites
* Linux
* Python 3.7
* ROS Noetic
* Visual Studio 22

## Hardware
* Windows laptop (can potentially use Linux or Mac)

## Installation


## Project description


## How to use
### How to set up Remote bridge:
Helpful links: https://husarion.com/tutorials/ros-tutorials/5-running-ros-on-multiple-machines/ 
https://github.com/Brabalawuka/RosOnWindows

#### Key instructions for remote windows:
1. Change ROS_MASTER URI (The rasp pi will be running roscore). You won't need to start roscore but you can if you want to run rostopic or rqt_plot
2. Create a .txt including following content: (Use your raspi ip address)
	```	
	@echo off 
	set ROS_MASTER_URI=http://192.168.1.19:11311
	set ROS_IP=192.168.1.249
	```
	Save as C:\bashrc.cmd at disk C (or another non-catkin_ws location).
3. (Optional) Following step 2, open regedit: -> Win+R and enter regedit. Find [HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor] and add a string key named Autorun, value is C:\bashrc.cmd"
4. Run the cmd file in the Developer Command Prompt in VS22 "C:\bashrc.cmd". There were some issues with it autorunning in item 3.
5. Use rosrun to execute the individual programs on remote machine.

#### Key instructions for raspi:
1. On the raspi device open the .bashrc file, then add the lines:
	```
	export ROS_MASTER_URI=http://192.168.1.19:11311
	export ROS_IP=192.168.1.19
	```
2. Start roscore
  
## Issues and Error Handling
If you have any issues, please refer to the issue folder first as someone in our group could have dealt with it already. Also, please post your solutions to your general issues in there.


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
