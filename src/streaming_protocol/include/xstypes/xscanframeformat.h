#ifndef XSCANFRAMEFORMAT_H
#define XSCANFRAMEFORMAT_H

//////////////////////////////////////////////////////////////////////////////////////////
/*!	\addtogroup enums Global enumerations
	@{
*/

//AUTO namespace xstypes {
/*!	\enum XsCanFrameFormat
	\brief Defines the Frame format for CAN messages

*/
enum XsCanFrameFormat
{
	XCFF_11Bit_Identifier	= 0,
	XCFF_29Bit_Identifier	= 1,
};
/*! @} */

typedef enum XsCanFrameFormat XsCanFrameFormat;

#endif
