# XSENS

## This directory serves the purpose of communicating with XSENS to obtain measurements related to angular kinematics, linear kinematics, center of mass, and joint angles concerning the lower body, specifically the hips and lower region.

We heavily referenced https://www.xsens.com/hubfs/Downloads/usermanual/MVN_User_Manual.pdf for information. 

This table from page 55 (or 66 pdf) explains what topics are there to report.
![image](https://github.com/kieran-nichols/catkin_ws_remote/assets/71956317/d34d323e-8a86-4ab9-b12d-6dae74f903c3)


You can use table on page 94 (or 105 pdf) to reference the numbers of the specific sensors. Be aware that python's lists start from 0 and not 1, so all numbers would be negatively shifted by one.

![image](https://github.com/kieran-nichols/catkin_ws_remote/assets/71956317/b27e89ab-d4e3-4765-94c8-1eb3cb797ab2)


To edit angular kinematics, you need to edit angularsegmentkinematicsdatagram.cpp starting line 125.

To edit linear kinematics, you need to edit linearsegmentkinematicsdatagram.cpp starting line 113.

To edit center of mass, you need to edit centerofmassdatagram.cpp starting line 95.

To edit joint angles, you need to edit jointanglesdatagram.cpp starting line 117.

udpserver.cpp send all the recorded packages. You shouldn't be editing it but it can be used to be troubleshooting. 
