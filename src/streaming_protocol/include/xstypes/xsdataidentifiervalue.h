#ifndef XSDATAIDENTIFIERVALUE_H
#define XSDATAIDENTIFIERVALUE_H

#include "pstdint.h"
#define XDI_MAX_FREQUENCY_VAL	0xFFFF
#define XDI_MAX_FREQUENCY		((uint16_t) XDI_MAX_FREQUENCY_VAL)

//////////////////////////////////////////////////////////////////////////////////////////
/*!	\addtogroup enums Global enumerations
	@{
*/

/*!	\enum XsDataIdentifierValue
	\brief Defines some convenience values for use with the data identifiers

	Refer to the Low Level Communication Protocol for more details.
*/
enum XsDataIdentifierValue
{
	XDIV_MaxFrequency			= XDI_MAX_FREQUENCY_VAL,	//!< Maximum / no frequency
};
/*! @} */

typedef enum XsDataIdentifierValue XsDataIdentifierValue;

#endif
