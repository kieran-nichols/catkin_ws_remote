# catkin_ws_remote

## Troubleshooting document for all of the TADA nodes

## Dependecies
This repo acts as additive functionality to the tadaros package:
https://github.com/kieran-nichols/catkin_ws_tadaros.git

## Brain node
1) If this node reports a Python error (math, entry errors), you will need to restart this node. The code needs to be updated to handle more error cased using try/except Python functions.


## Motor node
1) If the motor node continuously crashes, 
* Check to see if the batteries for the motor and motor drivers are above 12V. 
* Then physically check to see if a wire is dislodged, then connect to Elmo to see if the motor moves. 
* If not, try "Quick Tune" or "Expert Tune" to deduce the error (usually hall sensor wire dislodged). Sometimes running the motors through Elmo, helps reset the motors and the weird resetting issues disappears.

## IMU node
  1) If the IMU disconnects, wait 10 seconds. If it does not reconnect, then restart the launch file (shutdown program and restart).
  
## Europa node
1) If the Europa disconnects, wait 10 seconds to see if would reconnect. 
2) If not, try to put the raspi within 1 foot of the Europa for it to reconnect. After it reconnects, you can separate the raspi and Europa up to 6 feet.

## Xsens node
Ensure that the Xsens MVM software is running on the Windows computer and it is streaming all of the topics that you care about.

## rosbag function
Ensure that rosbag displays all of your wanted topics. If not, stop rosbag, check the nodes, and restart rosbag.

## GUI node
Work in progress

## Other
1) check wires are all connected correctly 
2) check wires breaking 
3) check batteries are all charged 
4) type in “roswtf” 
5) make sure motor driver lights are all green-if red connection or power is bad 
in Pi manually type export ROS_MASTER_URI=http://(ip from pi):11311 and ROS_IP=(ip from pie) 
if rosrun streaming protocol shows nothing go to src/streaming_protocol/lib/xstypes64.dll and take the xstypes64.dll and put it in devel/lib/streaming_protocol/xstyles64.dll 
6) catkin_make 
7) Source ~devel/setup.bash (or a variation of this) 
8) Make sure to run it in the command prompt and not the powershell 
9) Sometimes close out the taskset window a few times to make it more stable 
10) taskset -c 1,2 roslaunch ….. 
11) M 0 0 to home if it’s setup right….. 
12) Make sure roscore has the 192 and not 169, rerun it if it does not (this was an old note somewhere I’m not sure if it’s still applicable) 
13) Set soldering iron for 3.5 for the heat set inserts 

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
