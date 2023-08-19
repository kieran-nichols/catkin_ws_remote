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

#include "linearsegmentkinematicsdatagram.h"
#include "udpserver.h"
#include "streamer.h"
#include <conio.h>
#include <xstypes/xstime.h>
#include "ros/ros.h"
#include "std_msgs/Float32MultiArray.h"
/*! \class LinearSegmentKinematicsDatagram
	\brief a Linear Segment Kinematics datagram (type 0x21)

	Information about each segment is sent as follows.

	4 bytes segment ID, in the range 1-30
	4 bytes x�coordinate of segment position
	4 bytes y�coordinate of segment position
	4 bytes z�coordinate of segment position
	4 bytes x�coordinate of segment velocity
	4 bytes y�coordinate of segment velocity
	4 bytes z�coordinate of segment velocity
	4 bytes x�coordinate of segment acceleration
	4 bytes y�coordinate of segment acceleration
	4 bytes z�coordinate of segment acceleration

	Total: 40 bytes per segment

	The coordinates use a Z-Up, right-handed coordinate system.
	*/

/*! Constructor */
LinearSegmentKinematicsDatagram::LinearSegmentKinematicsDatagram()
	: Datagram()
{
	setType(SPLinearSegmentKinematics);
}

/*! Destructor */
LinearSegmentKinematicsDatagram::~LinearSegmentKinematicsDatagram()
{
}

/*! Deserialize the data from \a arr
	\sa serializeData
*/
void LinearSegmentKinematicsDatagram::deserializeData(Streamer &inputStreamer)
{
	Streamer* streamer = &inputStreamer;

	for (int i = 0; i < dataCount(); i++)
	{
		Kinematics kin;

		// Store the segement Id -> 4 byte
		streamer->read(kin.segmentId);

		// Store the Segment Position in a Vector -> 12 byte	(3 x 4 byte)
		for (int k = 0; k < 3; k++)
			streamer->read(kin.pos[k]);

		// Store the Segment Velocity in a Vector -> 12 byte	(3 x 4 byte)
		for (int k = 0; k < 3; k++)
			streamer->read(kin.velocity[k]);

		// Store the Segmetn Acceleration in a Vector -> 12 byte	(3 x 4 byte)
		for (int k = 0; k < 3; k++)
			streamer->read(kin.acceleration[k]);

		m_data.push_back(kin);
	}
}

/*! Print Data datagram in a formatted way
*/
void LinearSegmentKinematicsDatagram::printData() const
{
	ros::NodeHandle s;
	ros::Publisher pub_linear_moments = s.advertise<std_msgs::Float32MultiArray>("linear_moments", 10);
	std_msgs::Float32MultiArray linear_moments;
	//Clear array
	linear_moments.data.clear();
	std::vector<float> vec;//creating a vector for publishing

	///////////////////////////
	///This is where we ROSify the code
	///This is where you want to edit
	///////////////////////////
	
	ros::Time::init();  //we initialize time
	ros::Time now = ros::Time::now(); //we record the starting time

	int lowtime =  now.nsec/1000000; //getting the ms of time
	int hightime =  now.sec%100000;  //getting the seconds of time

	//We have to cut-off parts of time because the float is too big to report. 
	//We report in a similar time format across the project.
	float lower_final_time =  (float) lowtime; //turning them into a float
	float high_final_time =  (float) hightime; //turning seconds time into a float
	float final_time = floorf(lower_final_time)/1000+high_final_time; //adding them up while trying to round it to just ms 

	//This is where we find the reported values of angular kinematics
	vec.insert(vec.end(), { final_time }); //getting the vector
	float who = m_data.at(0).segmentId; //identifying the vector's id

	//adding only lower leg sensor's reading. Each number corresponds to a certain sensor which is why we have a 0 (pelv) and iterate through others)
	vec.insert(vec.end(), { who, m_data.at(0).velocity[0], m_data.at(0).velocity[1], m_data.at(0).velocity[2], m_data.at(0).acceleration[0], m_data.at(0).acceleration[1],m_data.at(0).acceleration[2] });

	//If you want to edit which parts we report, you need to do it here by choosing which segment (i) we add.
	for (int i = 15; i < 22; i++)
	{
		//Which ones we are skipping
		if (i == 18) {
			continue;
		}
		
		float who = m_data.at(i).segmentId; //getting segment's ID
		//inserting the segment's reported values into the vector
		vec.insert(vec.end(), { who, m_data.at(i).velocity[0], m_data.at(i).velocity[1], m_data.at(i).velocity[2], m_data.at(i).acceleration[0], m_data.at(i).acceleration[1],m_data.at(i).acceleration[2] });
	
	}
	
	linear_moments.data = (vec);//we are formating the reported values
	pub_linear_moments.publish(linear_moments);//publishing the reported
	ros::spinOnce(); //continue reporting

	///////////////////////////
	///This is where we end ROSification
	///////////////////////////
}
