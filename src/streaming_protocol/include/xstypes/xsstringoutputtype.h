#ifndef XSSTRINGOUTPUTTYPE_H
#define XSSTRINGOUTPUTTYPE_H

/*!	\addtogroup enums Global enumerations
	@{
*/
//! String output types
enum XsStringOutputType
{
	XSOT_None		= 0x0000
	, XSOT_HCHDM		= 0x0001 //!< NMEA string with Magnetic Heading
	, XSOT_HCHDG		= 0x0002 //!< NMEA string with Heading and Magnetic Variation
	, XSOT_TSS2		= 0x0004 //!< Proprietry string with Heading, Heave, Roll and Pitch
	, XSOT_PHTRO		= 0x0008 //!< Proprietry NMEA string with Pitch and Roll
	, XSOT_PRDID		= 0x0010 //!< Proprietry NMEA string with Pitch, Roll and Heading
	, XSOT_EM1000	= 0x0020 //!< Binary format suitable for use with Simrad EM1000 mulitibeam sounders with Roll, Pitch, Heave and Heading
	, XSOT_PSONCMS	= 0x0040 //!< NMEA string with Xsens Compass Motion Sensor information
	, XSOT_HCMTW		= 0x0080 //!< NMEA string with (water) Temperature
	, XSOT_HEHDT		= 0x0100 //!< NMEA string with True Heading
	, XSOT_HEROT		= 0x0200 //!< NMEA string with Rate of Turn
	, XSOT_GPGGA		= 0x0400 //!< NMEA string with Global Positioning system fix data
	, XSOT_PTCF		= 0x0800 //!< NMEA string with motion data
	, XSOT_XSVEL		= 0x1000 //!< Proprietry NMEA string with velocity data
	, XSOT_GPZDA		= 0x2000 //!< NMEA string with date and time
	, XSOT_GPRMC		= 0x4000 //!< NMEA string with recommended minimum specific GPS/Transit data
};
/*! @} */
typedef enum XsStringOutputType XsStringOutputType;

#endif
