#ifndef XSCALIBRATEDDATA_H
#define XSCALIBRATEDDATA_H

#include "xstypesconfig.h"
#include "xsvector3.h"

struct XsCalibratedData;

#ifdef __cplusplus
extern "C" {
#endif
#ifndef __cplusplus
#define XSCALIBRATEDDATA_INITIALIZER {XSVECTOR3_INITIALIZER, XSVECTOR3_INITIALIZER, XSVECTOR3_INITIALIZER}
#endif

XSTYPES_DLL_API void XsCalibratedData_construct(struct XsCalibratedData* thisPtr, const XsReal* acc, const XsReal* gyr, const XsReal* mag);
XSTYPES_DLL_API void XsCalibratedData_destruct(struct XsCalibratedData* thisPtr);

#ifdef __cplusplus
} // extern "C"
#endif

struct XsCalibratedData
{
	XsVector3 m_acc;	//!< Accelerometer data
	XsVector3 m_gyr;	//!< Gyroscope data
	XsVector3 m_mag;	//!< Magnetometer data

#ifdef __cplusplus
	//! \brief Constructor \sa XsCalibratedData_construct
	inline XsCalibratedData()
		: m_acc(0, 0, 0)
		, m_gyr(0, 0, 0)
		, m_mag(0, 0, 0)
	{
	}

	//! \brief Copy constructor, copies the values from \a other to this
	inline XsCalibratedData(const XsCalibratedData& other)
		: m_acc(other.m_acc)
		, m_gyr(other.m_gyr)
		, m_mag(other.m_mag)
	{
	}

	//! \brief Destructor
	inline ~XsCalibratedData()
	{}

	//! \brief Assignment operator, copies the values from \a other to this
	inline XsCalibratedData& operator = (const XsCalibratedData& other)
	{
		if (this != &other)
		{
			m_acc = other.m_acc;
			m_gyr = other.m_gyr;
			m_mag = other.m_mag;
		}
		return *this;
	}
#endif
};
typedef struct XsCalibratedData XsCalibratedData;

#endif
