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

#include "angularsegmentkinematicsdatagram.h"
#include <xstypes/xsmath.h>
#include "udpserver.h"
#include "streamer.h"
#include <conio.h>
#include <xstypes/xstime.h>
#include "ros/ros.h"
#include "std_msgs/Float32MultiArray.h"

/*! \class AngularSegmentKinematicsDatagram
	\brief a Angular Kinematics datagram (type 0x22)

	Information about each segment is sent as follows.

	4 bytes segment ID, in the range 1-30
	4 bytes q1 segment orientation quaternion component 1 (re)
	4 bytes q2 segment orientation quaternion component 1 (i)
	4 bytes q3 segment orientation quaternion component 1 (j)
	4 bytes q4 segment orientation quaternion component 1 (k)
	4 bytes angular velocity around segment x axis
	4 bytes angular velocity around segment y axis
	4 bytes angular velocity around segment z axis
	4 bytes angular acceleration around segment x axis
	4 bytes angular acceleration around segment y axis
	4 bytes angular acceleration around segment z axis

	Total: 44 bytes per segment

	The coordinates use a Z-Up, right-handed coordinate system.
*/

/*! Constructor */
AngularSegmentKinematicsDatagram::AngularSegmentKinematicsDatagram()
	: Datagram()
{
	setType(SPAngularSegmentKinematics);
}

/*! Destructor */
AngularSegmentKinematicsDatagram::~AngularSegmentKinematicsDatagram()
{
}

/*! Deserialize the data from \a arr
	\sa serializeData
*/
void AngularSegmentKinematicsDatagram::deserializeData(Streamer &inputStreamer)
{
	Streamer* streamer = &inputStreamer;

	for (int i = 0; i < dataCount(); i++)
	{
		Kinematics kin;

		// Store the segement Id -> 4 byte
		streamer->read(kin.segmentId);

		// Store the Segment orientation in a Vector -> 16 byte	(4 x 4 byte)
		for (int k = 0; k < 4; k++)
			streamer->read(kin.segmentOrien[k]);
		// trasform in degrees
		for (int k = 0; k < 4; k++)
			kin.segmentOrien[k] = XsMath_rad2deg(kin.segmentOrien[k]);

		// Store the Angular Velocity in a Vector -> 12 byte	(3 x 4 byte)
		for (int k = 0; k < 3; k++)
			streamer->read(kin.angularVeloc[k]);
		// trasform in degrees
		for (int k = 0; k < 3; k++)
			kin.angularVeloc[k] = XsMath_rad2deg(kin.angularVeloc[k]);

		// Store the Angular Acceleration in a Vector -> 12 byte	(3 x 4 byte)
		for (int k = 0; k < 3; k++)
			streamer->read(kin.angularAccel[k]);
		// trasform in degrees
		for (int k = 0; k < 3; k++)
			kin.angularAccel[k] = XsMath_rad2deg(kin.angularAccel[k]);

		m_data.push_back(kin);
	}
}

/*! Print Data datagram in a formatted way
*/
void AngularSegmentKinematicsDatagram::printData() const
{
	ros::NodeHandle s;
	ros::Publisher pub_angular_moments = s.advertise<std_msgs::Float32MultiArray>("angular_moments", 10);
	std_msgs::Float32MultiArray angular_moments;
	angular_moments.data.clear();

	std::vector<float> vec;//creating a publishing vector

	/////////////////////////time
	// Get the current time
	ros::Time::init();
	ros::Time now = ros::Time::now();

	int lowtime =  now.nsec/1000000; //getting the ms of time
	int hightime =  now.sec%100000;  //getting the seconds of time

	float lower_final_time =  (float) lowtime; //turning them into a float
	float high_final_time =  (float) hightime;
	float final_time = floorf(lower_final_time)/1000+high_final_time; //adding them up while trying to round it to just ms (which doesn't work)

	///////////////////////////////////

	vec.insert(vec.end(), { final_time });
	float who = m_data.at(0).segmentId;

	//adding only lower leg sensor's reading. Each number corresponds to a certain sensor which is why we iterate through some and skip others.
	vec.insert(vec.end(), { who, m_data.at(0).angularVeloc[0], m_data.at(0).angularVeloc[1],m_data.at(0).angularVeloc[2],
		m_data.at(0).angularAccel[0],m_data.at(0).angularAccel[1], m_data.at(0).angularAccel[2] });
	
	
	for (int i = 15; i < 22; i++)
	{
		if (i == 18) {
			continue;
		}
		float who = m_data.at(i).segmentId;
		vec.insert(vec.end(), { who, m_data.at(i).angularVeloc[0], m_data.at(i).angularVeloc[1],m_data.at(i).angularVeloc[2],
			m_data.at(i).angularAccel[0],m_data.at(i).angularAccel[1], m_data.at(i).angularAccel[2]});

		
	}
	angular_moments.data = (vec);
	pub_angular_moments.publish(angular_moments);
	ros::spinOnce();
	
}
