#ifndef XSSTRINGOUTPUTTYPEARRAY_H
#define XSSTRINGOUTPUTTYPEARRAY_H

#include "xsstringoutputtype.h"
#include "xsarray.h"

#ifdef __cplusplus
extern "C" {
#endif

extern XsArrayDescriptor const XSTYPES_DLL_API g_xsStringOutputTypeArrayDescriptor;

#ifndef __cplusplus
#define XSSTRINGOUTPUTTYPEARRAY_INITIALIZER	XSARRAY_INITIALIZER(&g_xsStringOutputTypeArrayDescriptor)

XSARRAY_STRUCT(XsStringOutputTypeArray, XsStringOutputType);
typedef struct XsStringOutputTypeArray XsStringOutputTypeArray;

XSTYPES_DLL_API void XsStringOutputTypeArray_construct(XsStringOutputTypeArray* thisPtr, XsSize count, XsStringOutputType const* src);
#else
} // extern "C"
#endif

#ifdef __cplusplus
	struct XsStringOutputTypeArray : public XsArrayImpl<XsStringOutputType, g_xsStringOutputTypeArrayDescriptor, XsStringOutputTypeArray>
	{
		//! \brief Constructs an XsStringOutputTypeArray
		inline explicit XsStringOutputTypeArray(XsSize sz = 0, XsStringOutputType const* src = 0)
			: ArrayImpl(sz, src)
		{
		}

		//! \brief Constructs an XsStringOutputTypeArray as a copy of \a other
		inline XsStringOutputTypeArray(XsStringOutputTypeArray const& other)
			: ArrayImpl(other)
		{
		}

		//! \brief Constructs an XsStringOutputTypeArray that references the data supplied in \a ref
		inline explicit XsStringOutputTypeArray(XsStringOutputType* ref, XsSize sz, XsDataFlags flags /* = XSDF_None */)
			: ArrayImpl(ref, sz, flags)
		{
		}

#ifndef SWIG
		/*! \brief Swap the contents the \a first and \a second array */
		friend void swap(XsStringOutputTypeArray& first, XsStringOutputTypeArray& second)
		{
			first.swap(second);
		}
#endif

#ifndef XSENS_NOITERATOR
		//! \brief Constructs an XsStringOutputTypeArray with the array bound by the supplied iterators \a beginIt and \a endIt
		template <typename Iterator>
		inline XsStringOutputTypeArray(Iterator beginIt, Iterator endIt)
			: ArrayImpl(beginIt, endIt)
		{
		}
#endif
	};
#endif
#endif
