/*! \file
	\section FileCopyright Copyright Notice
	This is free and unencumbered software released into the public domain.

	Anyone is free to copy, modify, publish, use, compile, sell, or
	distribute this software, either in source code form or as a compiled
	binary, for any purpose, commercial or non-commercial, and by any
	means.

	In jurisdictions that recognize copyright laws, the author or authors
	of this software dedicate any and all copyright interest in the
	software to the public domain. We make this dedication for the benefit
	of the public at large and to the detriment of our heirs and
	successors. We intend this dedication to be an overt act of
	relinquishment in perpetuity of all present and future rights to this
	software under copyright law.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
	IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
	OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
	ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
	OTHER DEALINGS IN THE SOFTWARE.
*/

#include "udpserver.h"
#include "streamer.h"
#include <conio.h>
#include <xstypes/xstime.h>
#include "ros/ros.h"
#include "std_msgs/Float32MultiArray.h"

int main(int argc, char *argv[])
{
	ros::init(argc, argv, "streaming");
	std::cout << "Streaming node initialized" << std::endl;
	ros::NodeHandle s;
	ros::Publisher pub_xsens_com = s.advertise<std_msgs::Float32MultiArray>("xsens_com", 10);
	ros::Publisher pub_xsens_joint_angle = s.advertise<std_msgs::Float32MultiArray>("xsens_joint_angle", 10);
	ros::Publisher pub_xsens_angular_moments = s.advertise<std_msgs::Float32MultiArray>("angular_moments", 10);
	ros::Publisher pub_xsens_linear_moments = s.advertise<std_msgs::Float32MultiArray>("linear_moments", 10);

	//ros::spinOnce();
	//ros::Rate rate(55); this does not affect the publishing rate of individual threads

	std::string hostDestinationAddress = "localhost";
	int port = 8000;

	UdpServer udpServer(hostDestinationAddress, (uint16_t)port);

	while (!_kbhit())
		//XsTime::msleep(1);
		//rate.sleep();
		continue;

	return 0;
}
