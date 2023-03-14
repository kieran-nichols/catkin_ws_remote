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

#include "centerofmassdatagram.h"
#include "ros/ros.h"
#include <iostream>
#include <vector>
#include "std_msgs/Float32MultiArray.h"

/*! \class CenterOfMassDatagram
  \brief a Center of Mass datagram (type 0x24)

  Information about the segment of mass is sent as follows.

  4 bytes x�coordinate of position
  4 bytes y�coordinate of position
  4 bytes z�coordinate of position

  Total: 12 bytes

  The coordinates use a Z-Up, right-handed coordinate system.
 */

/*! Constructor */
CenterOfMassDatagram::CenterOfMassDatagram()
	: Datagram()
{
	setType(SPCenterOfMass);
}

/*! Destructor */
CenterOfMassDatagram::~CenterOfMassDatagram()
{
}

/*! Deserialize the data from \a arr
	\sa serializeData
*/
void CenterOfMassDatagram::deserializeData(Streamer &inputStreamer)
{
	Streamer* streamer = &inputStreamer;

	// extract the coordinates of the position
	for (int k = 0; k < 3; k++)
		streamer->read(m_pos[k]);

	// extract the coordinates of the velocity
	for (int k = 0; k < 3; k++)
		streamer->read(m_vel[k]);

	// extract the coordinates of the acc
	for (int k = 0; k < 3; k++)
		streamer->read(m_acc[k]);
}

/*! Print Data datagram in a formatted way
*/
void CenterOfMassDatagram::printData() const
{
	ros::NodeHandle s;
	ros::Publisher pub_xsens_com= s.advertise<std_msgs::Float32MultiArray>("xsens_com", 10);
	std_msgs::Float32MultiArray xsens_com;
	//Clear array
	xsens_com.data.clear();
	std::vector<float> vec; //creating publishing vector

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
	//adding in certain sensor information
	vec.insert(vec.end(), { m_pos[0], m_pos[1], m_pos[2], 
		m_vel[0], m_vel[1], m_vel[2],
		m_acc[0], m_acc[1], m_acc[2] });
	
	xsens_com.data = (vec);
	pub_xsens_com.publish(xsens_com);
	ros::spinOnce();
}
