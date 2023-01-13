#ifndef XSDATAPACKETPTRARRAY_H
#define XSDATAPACKETPTRARRAY_H

#include "xstypesconfig.h"
#include "xsdatapacket.h"
#include "xsarray.h"
#include "xsdatapacketptr.h"

#ifdef __cplusplus
extern "C" {
#endif

extern XsArrayDescriptor const XSTYPES_DLL_API g_xsDataPacketPtrArrayDescriptor;

#ifndef __cplusplus
#define XSDATAPACKETPTRARRAY_INITIALIZER	XSARRAY_INITIALIZER(&g_xsDataPacketPtrArrayDescriptor)

XSARRAY_STRUCT(XsDataPacketPtrArray, XsDataPacketPtr);
typedef struct XsDataPacketPtrArray XsDataPacketPtrArray;

XSTYPES_DLL_API void XsDataPacketPtrArray_construct(XsDataPacketPtrArray* thisPtr, XsSize count, XsDataPacketPtr const* src);
#else
} // extern "C"
#endif

#ifdef __cplusplus
	struct XsDataPacketPtrArray : public XsArrayImpl<XsDataPacketPtr, g_xsDataPacketPtrArrayDescriptor, XsDataPacketPtrArray>
	{
		//! \brief Constructs an XsDataPacketPtrArray
		inline explicit XsDataPacketPtrArray(XsSize sz = 0, XsDataPacketPtr const* src = 0)
			: ArrayImpl(sz, src)
		{
		}

		//! \brief Constructs an XsDataPacketPtrArray as a copy of \a other
		inline XsDataPacketPtrArray(XsDataPacketPtrArray const& other)
			: ArrayImpl(other)
		{
		}

		//! \brief Constructs an XsDataPacketPtrArray that references the data supplied in \a ref
		inline explicit XsDataPacketPtrArray(XsDataPacketPtr* ref, XsSize sz, XsDataFlags flags /* = XSDF_None */)
			: ArrayImpl(ref, sz, flags)
		{
		}

#ifndef SWIG
		/*! \brief Swap the contents the \a first and \a second array */
		friend void swap(XsDataPacketPtrArray& first, XsDataPacketPtrArray& second)
		{
			first.swap(second);
		}
#endif

#ifndef XSENS_NOITERATOR
		//! \brief Constructs an XsDataPacketPtrArray with the array bound by the supplied iterators \a beginIt and \a endIt
		template <typename Iterator>
		inline XsDataPacketPtrArray(Iterator beginIt, Iterator endIt)
			: ArrayImpl(beginIt, endIt)
		{
		}
#endif
	};
#endif
#endif
