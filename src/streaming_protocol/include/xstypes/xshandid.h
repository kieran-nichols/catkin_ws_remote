#ifndef XSHANDID_H
#define XSHANDID_H

/*!	\addtogroup enums
	@{
*/

/*! \brief This is an enumerator that contains the left and right hand.
	\details These values are to be used when addressing the left or right hand (or either).
*/
enum XsHandId
{
	XHI_LeftHand = 0,	//!< The Left Hand
	XHI_RightHand = 1,	//!< The Right Hand
	XHI_Unknown			//!< Used as uninitialized or unknown side
};

//! @}

typedef enum XsHandId XsHandId;

#endif
