#ifndef XSCANDATAIDENTIFIER_H
#define XSCANDATAIDENTIFIER_H

//! \brief Max frequency values for can interface
#define XCDI_MAX_FREQUENCY_VAL	0x07FF
#define XCDI_MAX_FREQUENCY		((uint16_t) XCDI_MAX_FREQUENCY_VAL)

//////////////////////////////////////////////////////////////////////////////////////////
/*!	\addtogroup enums Global enumerations
	@{
*/

//AUTO namespace xstypes {
/*!	\enum XsCanDataIdentifier
	\brief Defines the data identifiers for CAN messages

*/
enum XsCanDataIdentifier
{
	XCDI_Invalid			= 0x00,

	/* Group Information & Timestamp Messages */
	XCDI_Error				= 0x01,
	XCDI_Warning			= 0x02,

	XCDI_SampleTime			= 0x05,	//!< Sample Time in us
	XCDI_GroupCounter		= 0x06,
	XCDI_UtcTime			= 0x07,

	/* Group Status Messages */
	XCDI_StatusWord		= 0x11,

	/* Group Quaternion Messages */
	XCDI_Quaternion			= 0x21,
	XCDI_EulerAngles		= 0x22,
	XCDI_RotationMatrix		= 0x23,

	/* Group Inertial Data Messages */
	XCDI_DeltaV				= 0x31,	//!< DeltaV SDI data output
	XCDI_RateOfTurn			= 0x32,
	XCDI_DeltaQ				= 0x33,	//!< DeltaQ SDI data
	XCDI_Acceleration		= 0x34,
	XCDI_FreeAcceleration	= 0x35,

	/* Group Magnetic Field */
	XCDI_MagneticField		= 0x41,	//!< Magnetic field data in a.u.

	/* Group Temperature & Pressure Messages */
	XCDI_Temperature		= 0x51,	//!< Temperature
	XCDI_BaroPressure		= 0x52,	//!< Pressure output recorded from the barometer

	/* Group High-Rate Data Messages */
	XCDI_RateOfTurnHR		= 0x61,
	XCDI_AccelerationHR		= 0x62,

	/* Group Position & Velocity Messages */
	XCDI_LatLong			= 0x71,
	XCDI_AltitudeEllipsoid	= 0x72,
	XCDI_PositionEcef_X		= 0x73,
	XCDI_PositionEcef_Y		= 0x74,
	XCDI_PositionEcef_Z		= 0x75,
	XCDI_Velocity			= 0x76,
	XCDI_Latitude			= 0x77,
	XCDI_Longitude			= 0x78,
	XCDI_GnssReceiverStatus	= 0x79,
	XCDI_GnssReceiverDop	= 0x7A,

	XCDI_EndOfGroup, //Keep this entry second to last.
	XCDI_HighestIdentifier, //Keep this entry last. Don't assign IDs with a higher value than this.
};
/*! @} */

typedef enum XsCanDataIdentifier XsCanDataIdentifier;

#endif
