#ifndef XSPROTOCOL_H
#define XSPROTOCOL_H

/*!	\addtogroup enums Global enumerations
	@{
*/
//! Protocol types, used for MTi6x0 devices.
enum XsProtocol
{
	XP_None				= 0,	//!< None
	XP_Xbus				= 1,	//!< The Xsens Xbus protocol
	XP_Nmea				= 5,	//!< The NMEA protocol
	XP_Rtcm				= 6,	//!< RTCM protocol for RTK
};
/*! @} */
typedef enum XsProtocol XsProtocol;

#endif
