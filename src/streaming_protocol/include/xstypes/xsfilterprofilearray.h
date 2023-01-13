#ifndef XSFILTERPROFILEARRAY_H
#define XSFILTERPROFILEARRAY_H

#include "xstypesconfig.h"
#include "xsarray.h"

#ifdef __cplusplus
#include "xsfilterprofile.h"
extern "C" {
#endif

extern XsArrayDescriptor const XSTYPES_DLL_API g_xsFilterProfileArrayDescriptor;

#ifndef __cplusplus
#define XSFILTERPROFILEARRAY_INITIALIZER	XSARRAY_INITIALIZER(&g_xsFilterProfileArrayDescriptor)

struct XsFilterProfile;

XSARRAY_STRUCT(XsFilterProfileArray, struct XsFilterProfile);
typedef struct XsFilterProfileArray XsFilterProfileArray;

XSTYPES_DLL_API void XsFilterProfileArray_construct(XsFilterProfileArray* thisPtr, XsSize count, struct XsFilterProfile const* src);
#else
} // extern "C"
#endif

#ifdef __cplusplus
	struct XsFilterProfileArray : public XsArrayImpl<XsFilterProfile, g_xsFilterProfileArrayDescriptor, XsFilterProfileArray>
	{
		//! \brief Constructs an XsFilterProfileArray
		inline explicit XsFilterProfileArray(XsSize sz = 0, XsFilterProfile const* src = 0)
			: ArrayImpl(sz, src)
		{
		}

		//! \brief Constructs an XsFilterProfileArray as a copy of \a other
		inline XsFilterProfileArray(XsFilterProfileArray const& other)
			: ArrayImpl(other)
		{
		}

		//! \brief Constructs an XsFilterProfileArray that references the data supplied in \a ref
		inline explicit XsFilterProfileArray(XsFilterProfile* ref, XsSize sz, XsDataFlags flags /* = XSDF_None */)
			: ArrayImpl(ref, sz, flags)
		{
		}

#ifndef SWIG
		/*! \brief Swap the contents the \a first and \a second array */
		friend void swap(XsFilterProfileArray& first, XsFilterProfileArray& second)
		{
			first.swap(second);
		}
#endif

#ifndef XSENS_NOITERATOR
		//! \brief Constructs an XsFilterProfileArray with the array bound by the supplied iterators \a beginIt and \a endIt
		template <typename Iterator>
		inline XsFilterProfileArray(Iterator beginIt, Iterator endIt)
			: ArrayImpl(beginIt, endIt)
		{
		}
#endif
	};
#endif
#endif
