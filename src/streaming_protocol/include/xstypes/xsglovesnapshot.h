#ifndef XSGLOVESNAPSHOT_H
#define XSGLOVESNAPSHOT_H

#include "xstypesconfig.h"
#include "xsdeviceid.h"

struct XsGloveSnapshot;

#ifdef __cplusplus
extern "C" {
#endif
#ifndef __cplusplus
#define XSGLOVESNAPSHOT_INITIALIZER {0, 0, 0, 0, \
		XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER, \
		XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER, XSFINGERSNAPSHOT_INITIALIZER}
#define XSFINGERSNAPSHOT_INITIALIZER {0,0,0, 0,0,0, 0,0,0, 0, 0, 0}
#endif

#ifdef __cplusplus
} // extern "C"
#endif

#include <math.h>       /* pow */

XS_PACKED_STRUCT_START
/*! \brief int24
*/
struct int24_t
{
	uint8_t m_vals[3]; /*!< \brief The data*/

#ifdef __cplusplus
	//! \brief convert int24 to double
	inline double toDouble() const
	{
		if (m_vals[0] & 0x80)
			return ((double)(int32_t)(((uint32_t)0xff000000) | (((uint32_t)m_vals[0]) << 16) | (((uint32_t)m_vals[1]) << 8) | ((uint32_t)m_vals[2])));
		else
			return (double)((((uint32_t)m_vals[0]) << 16) | (((uint32_t)m_vals[1]) << 8) | (uint32_t)m_vals[2]);
	}

#endif
#ifdef SWIG
};
#else
} XS_PACKED_STRUCT;
#endif
typedef struct int24_t int24_t;

/*! \brief A container for Finger Snapshot data
*/
struct XsFingerSnapshot
{
	int24_t m_iQ[3];		/*!< \brief The integrated orientation */
	int32_t m_iV[3];		/*!< \brief The integrated velocity */
	int16_t m_mag[3];		/*!< \brief The magnetic field */
	uint16_t m_flags;		/*!< \brief The flags */
	uint8_t m_accClippingCounter;		/*!< \brief The acceleration clipping counter */
	uint8_t m_gyrClippingCounter;		/*!< \brief The gyroscope clipping counter */
#ifdef SWIG
};
#else
} XS_PACKED_STRUCT;
#endif
typedef struct XsFingerSnapshot XsFingerSnapshot;

/*! \brief A container for Glove Snapshot data
*/
struct XsGloveSnapshot
{
	uint32_t m_frameNumber;			/*!< \brief The frame number associated with the fingerdata */
	uint16_t m_validSampleFlags;	/*!< \brief The valid sample flags */
	uint8_t m_padByte;				/*!< \brief A padded byte to align fingerdata*/
	XsFingerSnapshot m_fingers[12];	/*!< \brief The 12 fingers */
#if 0 // def __cplusplus
	/*! \brief Returns true if all fields of this and \a other are exactly identical */
	inline bool operator == (const XsGloveSnapshot& other) const
	{
		return true;
	}
#endif
#ifdef SWIG
};
#else
} XS_PACKED_STRUCT;
#endif
typedef struct XsGloveSnapshot XsGloveSnapshot;

XS_PACKED_STRUCT_END

#endif
