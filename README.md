# catkin_ws_remote

# Windows Remote controller for Two axis Adaptable Ankle (TADA) prosthetic device

# Dependecies
This repo acts as additive functionality to the tadaros package:
https://github.com/kieran-nichols/catkin_ws_tadaros.git

## Prerequisites
* Windows laptop (can potentially use Linux or Mac)
* Linux
* Python 3.7
* ROS Noetic
* Visual Studio 22

## Hardware
* Raspberry Pi


## Installation


## Project description


## How to use
* "roscore" # run the ROS master node from a terminal
* To run the TADA system, use "roslaunch launch_file.launch" from the catkin_ws_tadaros/src" folder
* To run individual nodes, use "rosrun tada_ros [NAME_NODE].py" ex: "rosrun tada_ros sensor_node.py" # run
   each node in a new terminal
* If you want to plot the data being sent across topics on a graph, you can use
  the command "rqt_plot topic1/field1:field2:field3" and then run the nodes.
  For example "rqt_plot recon_topic/pos_x:vel_x:accel_x"
  
## Issues and Error Handling
If you have any issues, please refer to the issue folder first as someone in our group could have dealt with it already. Also, please post your solutions to your general issues in there.

* When trying to run the nodes, I got an error on "import rospy".


## Authors
Kieran Nichols, Sofya Akhetova, Becca Roembke, Peter Adamczyk

## License
University of Wisconsin BADGER lab? # TODO

## Acknowledgements
Thanks to the current team and the past work from Ryan Moreno, Mike Greene, Preston Lewis,

## References

Copyright (c) <2022>, <Kieran Nichols>
All rights reserved.

This source code is licensed under the MIT-style license found in the
LICENSE file in the root directory of this source tree.
