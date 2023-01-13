#ifndef XSQUATERNIONARRAY_H
#define XSQUATERNIONARRAY_H

#include "xsarray.h"

#ifdef __cplusplus
#include "xsquaternion.h"
extern "C" {
#endif

extern XsArrayDescriptor const XSTYPES_DLL_API g_xsQuaternionArrayDescriptor;

#ifndef __cplusplus
#define XSQUATERNIONARRAY_INITIALIZER	XSARRAY_INITIALIZER(&g_xsQuaternionArrayDescriptor)
struct XsQuaternion;

XSARRAY_STRUCT(XsQuaternionArray, struct XsQuaternion);
typedef struct XsQuaternionArray XsQuaternionArray;

XSTYPES_DLL_API void XsQuaternionArray_construct(XsQuaternionArray* thisPtr, XsSize count, struct XsQuaternion const* src);
#define XsQuaternionArray_destruct(thisPtr)		XsArray_destruct(thisPtr)
#endif

#ifdef __cplusplus
} // extern "C"
#endif

#ifdef __cplusplus
struct XsQuaternionArray : public XsArrayImpl<XsQuaternion, g_xsQuaternionArrayDescriptor, XsQuaternionArray>
{
	//! \brief Constructs an XsQuaternionArray
	inline explicit XsQuaternionArray(XsSize sz = 0, XsQuaternion const* src = 0)
		: ArrayImpl(sz, src)
	{
	}

	//! \brief Constructs an XsQuaternionArray as a copy of \a other
	inline XsQuaternionArray(XsQuaternionArray const& other)
		: ArrayImpl(other)
	{
	}

	//! \brief Constructs an XsQuaternionArray that references the data supplied in \a ref
	inline explicit XsQuaternionArray(XsQuaternion* ref, XsSize sz, XsDataFlags flags /* = XSDF_None */)
		: ArrayImpl(ref, sz, flags)
	{
	}

#ifndef SWIG
	/*! \brief Swap the contents the \a first and \a second array */
	friend void swap(XsQuaternionArray& first, XsQuaternionArray& second)
	{
		first.swap(second);
	}
#endif

#ifndef XSENS_NOITERATOR
	//! \brief Constructs an XsQuaternionArray with the array bound by the supplied iterators \a beginIt and \a endIt
	template <typename Iterator>
	inline XsQuaternionArray(Iterator beginIt, Iterator endIt)
		: ArrayImpl(beginIt, endIt)
	{
	}
#endif

};
#endif

#endif
