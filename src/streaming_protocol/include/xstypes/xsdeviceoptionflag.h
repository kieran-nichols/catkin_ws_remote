#ifndef XSDEVICEOPTIONFLAG_H
#define XSDEVICEOPTIONFLAG_H

/*!	\addtogroup enums Global enumerations
	@{
*/
/*! \brief Used to enable or disable some device options
	\sa XsDevice::setDeviceOptionFlags
	\note Not all devices support all options.
*/
enum XsDeviceOptionFlag
{
	XDOF_DisableAutoStore				= 0x00000001,	//!< When set to 1, automatic writing of configuration will be disabled.
	XDOF_DisableAutoMeasurement			= 0x00000002,	//!< When set to 1, the MT will stay in Config Mode upon start up.
	XDOF_EnableBeidou					= 0x00000004,	//!< When set to 1, enables Beidou, disables GLONASS (MTi-G).
	XDOF_DisableGps						= 0x00000008,	//!< When set to 1, disables GPS (MTi-G).
	XDOF_EnableAhs						= 0x00000010,	//!< When set to 1, the MTi will have Active Heading Stabilization (AHS) enabled.
	XDOF_EnableOrientationSmoother		= 0x00000020,	//!< When set to 1, the MTi will have Orientation Smoother enabled. Only applicable to MTi-G-710, MTi-7, MTi-670 and MTi-680
	XDOF_EnableConfigurableBusId		= 0x00000040,	//!< When set to 1, allows to configure the BUS ID.
	XDOF_EnableInrunCompassCalibration	= 0x00000080,	//!< When set to 1, the MTi will have In-run Compass Calibration (ICC) enabled.
	XDOF_DisableSleepMode				= 0x00000100,	//!< When set to 1, an MTw will not enter sleep mode after a scan timeout. It will scan indefinitely.
	XDOF_EnableConfigMessageAtStartup	= 0x00000200,	//!< When set to 1, the MT will send the Configuration to the Master at start-up
	XDOF_EnableColdFilterResets			= 0x00000400,	//!< When set to 1, The MT performs a cold filter reset every time it goes to measurement
	XDOF_EnablePositionVelocitySmoother	= 0x00000800,	//!< When set to 1, the MTi will have Position/Velocity Smoother enabled. Only applicable to MTi-680
	XDOF_EnableContinuousZRU			= 0x00001000,	//!< When set to 1, the MTi filter will perform continuous Zero Rotation Updates for gyroscope bias and noise.
	XDOF_EnableRawGnssInputForwarding	= 0x00002000,	//!< When set to 1, the MTi will forward the raw input coming from the GNSS receiver encapsulated in an Xbus message.

	XDOF_None							= 0x00000000,	//!< When set to 1, disables all option flags.
	XDOF_All							= 0x7FFFFFFF	//!< When set to 1, enables all option flags.
};
/*! @} */
typedef enum  XsDeviceOptionFlag XsDeviceOptionFlag;

#ifdef __cplusplus
//! \brief Logical OR operator for XsDeviceOptionFlag values
inline XsDeviceOptionFlag operator | (XsDeviceOptionFlag a, XsDeviceOptionFlag b)
{
	return (XsDeviceOptionFlag)((int)a | (int)b);
}

//! \brief Logical AND operator for XsDeviceOptionFlag values
inline XsDeviceOptionFlag operator & (XsDeviceOptionFlag a, XsDeviceOptionFlag b)
{
	return (XsDeviceOptionFlag)((int)a & (int)b);
}

//! \brief Logical XOR operator for XsDeviceOptionFlag values
inline XsDeviceOptionFlag operator ^ (XsDeviceOptionFlag a, XsDeviceOptionFlag b)
{
	return (XsDeviceOptionFlag)((int)a ^ (int)b);
}

//! \brief Logical NEG operator for XsDeviceOptionFlag values
inline XsDeviceOptionFlag operator ~(XsDeviceOptionFlag a)
{
	return (XsDeviceOptionFlag)(~(int)a);
}
#endif

#endif
