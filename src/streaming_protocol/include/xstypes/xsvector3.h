#ifndef XSVECTOR3_H
#define XSVECTOR3_H

#include "xsvector.h"

struct XsVector3;
#ifdef __cplusplus
extern "C" {
#endif
#ifndef __cplusplus
typedef struct XsVector3 XsVector3;
#endif

XSTYPES_DLL_API void XsVector3_construct(XsVector3* thisPtr, const XsReal* src);
XSTYPES_DLL_API void XsVector3_assign(XsVector3* thisPtr, const XsReal* src);
XSTYPES_DLL_API void XsVector3_destruct(XsVector3* thisPtr);
XSTYPES_DLL_API void XsVector3_copy(XsVector* copy, XsVector3 const* src);

#ifdef __cplusplus
} // extern "C"
#endif

#ifdef __cplusplus
/*  This is allowed since the C standard says that no padding appears before the first member of a struct.
	Basically we're defining a union between a C++ inherited type and a C encapsulated type.
*/
struct XsVector3 : public XsVector
{
	XSCPPPROTECTED
#else
struct XsVector3
{
	XsVector m_vector;		//!< The underlying vector
#endif
	XsReal m_fixedData[3];				//!< Fixed size storage for the components in the vector

#ifdef __cplusplus
public:
	//! \brief Constructs an empty vector3
	XsVector3() : XsVector(m_fixedData, 3, XSDF_FixedSize)
	{
		//XsVector3_construct(this, 0);
	}

	//! \brief Constructs a vector3 from an \a other XsVector
	XsVector3(XsVector3 const& other) : XsVector(other, m_fixedData, 3, XSDF_FixedSize)
	{
	}

	//! \brief Constructs a vector3 from an \a other XsVector
	XsVector3(XsVector const& other) : XsVector(other, m_fixedData, 3, XSDF_FixedSize)
	{
	}

	//! \brief Constructs a vector3 using the values \a x, \a y, \a z
	XsVector3(XsReal x, XsReal y, XsReal z) : XsVector(m_fixedData, 3, XSDF_FixedSize)
	{
		m_data[0] = x;
		m_data[1] = y;
		m_data[2] = z;
	}

	//! \brief Return a 3-element zero vector
	static XsVector3 const& zero3()
	{
		static const XsVector3 rv(XsMath_zero, XsMath_zero, XsMath_zero);
		return rv;
	}

	using XsVector::operator=;
	//! \brief Assignment operator. Copies from \a other into this
	inline XsVector3& operator=(const XsVector3& other)
	{
		XsVector_copy(this, &other);
		return *this;
	}

	using XsVector::assign;
	//! \brief Assignment, directly assigns values.
	inline void assign(XsReal x, XsReal y, XsReal z)
	{
		m_data[0] = x;
		m_data[1] = y;
		m_data[2] = z;
		const_cast<XsSize&>(m_flags) &= ~XSDF_Empty;
	}
	//	using XsVector::operator[];
#endif
};

#endif
