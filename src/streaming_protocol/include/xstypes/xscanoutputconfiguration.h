#ifndef XSCANOUTPUTCONFIGURATION_H
#define XSCANOUTPUTCONFIGURATION_H

#include "xstypesconfig.h"
#include "pstdint.h"
#include "xscandataidentifier.h"
#include "xscanframeformat.h"

#define XS_MAX_CANOUTPUTCONFIGURATIONS			(16)

#ifdef __cplusplus
extern "C" {
#endif
#ifndef __cplusplus
#define XSCANOUTPUTCONFIGURATION_INITIALIZER		{ XCDI_None, 0 }
#endif

struct XsCanOutputConfiguration;

XSTYPES_DLL_API void XsCanOutputConfiguration_swap(struct XsCanOutputConfiguration* a, struct XsCanOutputConfiguration* b);

#ifdef __cplusplus
} // extern "C"
#endif


/*! \brief Single data type CAN output configuration
	\details This structure contains a single data type and the frequency at which it should be produced.
	If m_frequency is 0xFFFF and the %XsCanOutputConfiguration is used for input, the device will configure
	itself to its maximum frequency for the data type. If it is 0xFFFF and reported by the device,
	the data has no maximum frequency, but is sent along with appropriate packets (e.g. packet counter)
*/
struct XsCanOutputConfiguration
{
	XsCanFrameFormat m_frameFormat;			//!< The frame format of the CAN message
	XsCanDataIdentifier m_dataIdentifier;	//!< The data identifier
	uint32_t m_id;							//!< The 11 or 29 bit ID identifier
	uint16_t m_frequency;					//!< The frequency

#ifdef __cplusplus
	//! Constructor, initializes to an empty object
	inline XsCanOutputConfiguration()
		: m_frameFormat(XCFF_11Bit_Identifier)
		, m_dataIdentifier(XCDI_Invalid)
		, m_id(0)
		, m_frequency(0)
	{}

	//! Constructor, initializes to specified values
	inline XsCanOutputConfiguration(XsCanFrameFormat il, XsCanDataIdentifier di, uint32_t id, uint16_t freq)
		: m_frameFormat(il)
		, m_dataIdentifier(di)
		, m_id(id)
		, m_frequency(freq)
	{}

	//! Equality comparison operator
	inline bool operator == (const XsCanOutputConfiguration& other) const
	{
		return (m_frameFormat == other.m_frameFormat &&
				m_dataIdentifier == other.m_dataIdentifier &&
				m_id == other.m_id &&
				m_frequency == other.m_frequency);
	}

	//! Inequality comparison operator
	inline bool operator != (const XsCanOutputConfiguration& other) const
	{
		return !(*this == other);
	}
#endif
};
typedef struct XsCanOutputConfiguration XsCanOutputConfiguration;

#endif
