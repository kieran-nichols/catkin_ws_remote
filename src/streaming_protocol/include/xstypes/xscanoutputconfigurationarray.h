#ifndef XSCANOUTPUTCONFIGURATIONARRAY_H
#define XSCANOUTPUTCONFIGURATIONARRAY_H

#include "xsarray.h"

#ifdef __cplusplus
#include "xscanoutputconfiguration.h"
extern "C" {
#endif

extern XsArrayDescriptor const XSTYPES_DLL_API g_xsCanOutputConfigurationArrayDescriptor;

#ifndef __cplusplus
#define XSCANOUTPUTCONFIGURATIONARRAY_INITIALIZER	XSARRAY_INITIALIZER(&g_xsCanOutputConfigurationArrayDescriptor)
struct XsCanOutputConfiguration;

XSARRAY_STRUCT(XsCanOutputConfigurationArray, struct XsCanOutputConfiguration);
typedef struct XsCanOutputConfigurationArray XsCanOutputConfigurationArray;

XSTYPES_DLL_API void XsCanOutputConfigurationArray_construct(XsCanOutputConfigurationArray* thisPtr, XsSize count, struct XsCanOutputConfiguration const* src);
#endif

#ifdef __cplusplus
} // extern "C"

struct XsCanOutputConfigurationArray : public XsArrayImpl<XsCanOutputConfiguration, g_xsCanOutputConfigurationArrayDescriptor, XsCanOutputConfigurationArray>
{
	//! \brief Constructs an XsCanOutputConfigurationArray
	inline explicit XsCanOutputConfigurationArray(XsSize sz = 0, XsCanOutputConfiguration const* src = 0)
		: ArrayImpl(sz, src)
	{
	}

	//! \brief Constructs an XsCanOutputConfigurationArray as a copy of \a other
	inline XsCanOutputConfigurationArray(XsCanOutputConfigurationArray const& other)
		: ArrayImpl(other)
	{
	}

	//! \brief Constructs an XsCanOutputConfigurationArray that references the data supplied in \a ref
	inline explicit XsCanOutputConfigurationArray(XsCanOutputConfiguration* ref, XsSize sz, XsDataFlags flags /* = XSDF_None */)
		: ArrayImpl(ref, sz, flags)
	{
	}

#ifndef SWIG
	/*! \brief Swap the contents the \a first and \a second array */
	friend void swap(XsCanOutputConfigurationArray& first, XsCanOutputConfigurationArray& second)
	{
		first.swap(second);
	}
#endif

#ifndef XSENS_NOITERATOR
	//! \brief Constructs an XsCanOutputConfigurationArray with the array bound by the supplied iterators \a beginIt and \a endIt
	template <typename Iterator>
	inline XsCanOutputConfigurationArray(Iterator beginIt, Iterator endIt)
		: ArrayImpl(beginIt, endIt)
	{
	}
#endif
};
#endif

#endif
