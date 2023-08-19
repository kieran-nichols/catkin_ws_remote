This folder is to talk to XSENS in order to get readings of angular kinematics, linear kinematics, center of mass, and joint angles for the lower body (hips and lower).


We heavily used https://www.xsens.com/hubfs/Downloads/usermanual/MVN_User_Manual.pdf for information. 

This table explains what topics are there to report.
![image](https://github.com/kieran-nichols/catkin_ws_remote/assets/71956317/d34d323e-8a86-4ab9-b12d-6dae74f903c3)


You can use table on page 94 (or 105 pdf) to referance numbers of the specific sensors. Be aware that python list start from 0 and not 1, so all numbers would be negetivly shifted by one.
![image](https://github.com/kieran-nichols/catkin_ws_remote/assets/71956317/b27e89ab-d4e3-4765-94c8-1eb3cb797ab2)


To edit angular kinematics, you need to edit angularsegmentkinematicsdatagram.cpp
