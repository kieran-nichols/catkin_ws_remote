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
// https://www.theconstructsim.com/ros-qa-045-publish-subscribe-array-vector-message/
#include "jointanglesdatagram.h"
#include "streamer.h"
#include <conio.h>
#include "ros/ros.h"
#include <iostream>
#include <vector>
#include "std_msgs/Float32MultiArray.h"
#include <chrono>
#include <cstdint>
#include <iostream>


/*! \class JointAnglesDatagram
	\brief a Joint Angle datagram (type 0x20)

	Information about each joint is sent as follows.

	4 bytes parent connection identifier: 256 * segment ID + point ID
	4 bytes child connection identifer: 256 * segment ID + point ID
	4 bytes x rotation
	4 bytes y rotation
	4 bytes z rotation

	Total: 20 bytes per joint

	The coordinates use a Z-Up, right-handed coordinate system.
*/
// Set up ROS publisher that streams data via UDP
//ros::init(argc, argv, "streaming");
//std::cout << "Streaming node initialized" << std::endl;


/*! Constructor */
JointAnglesDatagram::JointAnglesDatagram()
	: Datagram()
{
	setType(SPJointAngles);
}

/*! Destructor */
JointAnglesDatagram::~JointAnglesDatagram()
{
}

/*! Deserialize the data from \a arr
	\sa serializeData
*/
void JointAnglesDatagram::deserializeData(Streamer &inputStreamer)
{

	Streamer* streamer = &inputStreamer;

		for (int i = 0; i < dataCount(); i++)
		{
			Joint joint;

			// Parent Connection ID  -> 4 byte
			streamer->read(joint.parent);

			// Child Connection ID -> 4 byte
			streamer->read(joint.child);

			// Store the Rotation in a Vector -> 12 byte	(3 x 4 byte)
			for (int k = 0; k < 3; k++)
				streamer->read(joint.rotation[k]);

			m_data.push_back(joint);
		}
		
}


/*! Print Data datagram in a formatted way
*/
using namespace std::chrono;
void JointAnglesDatagram::printData() const
{
	ros::NodeHandle s;
	ros::Publisher pub_xsens_joint_angle = s.advertise<std_msgs::Float32MultiArray>("xsens_joint_angle", 10);
	
	std_msgs::Float32MultiArray xsens_joint_angle;
	//Clear array
	xsens_joint_angle.data.clear();
	std::vector<float> vec;//vector for publishing

	///////////////////////////
	///This is where we ROSify the code
	///This is where you want to edit
	///////////////////////////
	
	ros::Time::init();//we initialize time
	ros::Time now = ros::Time::now(); //we record the starting time

	//We have to cut-off parts of time because the float is too big to report. 
	//We report in a similar time format across the project.
	int lowtime =  now.nsec/1000000; //getting the ms of time
	int hightime =  now.sec%100000;  //getting the seconds of time

	float lower_final_time =  (float) lowtime; //turning them into a float
	float high_final_time =  (float) hightime;//turning seconds time into a float
	float final_time = floorf(lower_final_time)/1000+high_final_time; //adding them up while trying to round it to just ms

	//This is where we find the reported values of angular kinematics
	vec.insert(vec.end(), { final_time }); //getting the vector
	
	//If you want to edit which parts we report, you need to do it here by choosing which segment (i) we add.
	for (int i = 14; i < 24; i++)
	{

		float parent = m_data.at(i).parent; //getting it's parent
		float child = m_data.at(i).child; //getting it's child
		//inserting the segment's reported values into the vector
		vec.insert(vec.end(), {parent,child, (m_data.at(i).rotation[0]), (m_data.at(i).rotation[1]), (m_data.at(i).rotation[2]) });
	}


	xsens_joint_angle.data = (vec);  //we are formating the reported values
	pub_xsens_joint_angle.publish(xsens_joint_angle); //publishing the reported
	ros::spinOnce(); //continue reporting

	///////////////////////////
	///This is where we end ROSification
	///////////////////////////
	

}
