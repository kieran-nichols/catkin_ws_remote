#ifndef XSCANBAUDCODE_H
#define XSCANBAUDCODE_H

#include "xstypesconfig.h"

/*! \brief Internal baud rate configuration codes
*/

enum XSNOCOMEXPORT XsCanBaudCode
{
	// Baudrate codes for SetBaudrate message
	XCBC_1M			= 0x0C,
	XCBC_800k		= 0x0B,
	XCBC_500k		= 0x0A,
	XCBC_250k		= 0x00,
	XCBC_125k		= 0x01,
	XCBC_100k		= 0x02,
	XCBC_83k3		= 0x03,
	XCBC_62k5		= 0x04,
	XCBC_50k		= 0x05,
	XCBC_33k3		= 0x06,
	XCBC_20k		= 0x07,
	XCBC_10k		= 0x08,
	XCBC_5k			= 0x09,
	XCBC_Invalid	= 0xFF
};

#endif
