#ifndef XSCANCONFIGIDENTIFIER_H
#define XSCANCONFIGIDENTIFIER_H

#include "xscandataidentifier.h"
//////////////////////////////////////////////////////////////////////////////////////////
/*!	\addtogroup enums Global enumerations
	@{
*/

//AUTO namespace xstypes {
/*!	\enum XsCanConfigIdentifier
	\brief Defines the config identifiers for CAN messages

	\note Have to be higher than XCDI_HighestIdentifier in xscandataidentifier.h
*/
enum XsCanConfigIdentifier
{
	XCCI_LowestIdentifier	= 0xA0,

	XCCI_DeviceIdReq		= 0xAA,
	XCCI_DeviceId			= 0xAB,
	XCCI_GotoConfig			= 0xAC,
	XCCI_GotoMeasurement	= 0xAD,
	XCCI_Reset				= 0xAE,


	XCCI_HighestIdentifier, //Keep this entry last. Don't assign IDs with a higher value than this.
};
/*! @} */

#if __cplusplus >= 201103L || _MSVC_LANG >= 201103L
	static_assert(int(XCCI_LowestIdentifier) >= int(XCDI_HighestIdentifier), "XsCanConfigIdentifier and XsCanDataIdentifier ranges must be mutually exclusive");
#endif

typedef enum XsCanConfigIdentifier XsCanConfigIdentifier;

#endif
