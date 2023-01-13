#ifndef XSTYPEDEFS_H
#define XSTYPEDEFS_H

#include "xstypesconfig.h"
#include "pstdint.h"

#ifndef XSENS_SINGLE_PRECISION
	#include <stddef.h>
	typedef double XsReal;	//!< Defines the floating point type used by the Xsens libraries
	typedef size_t XsSize;	//!< XsSize must be unsigned number!
	typedef ptrdiff_t XsSizeSigned;	//!< signed variant of XsSize
	#define XSREAL_ALLOWS_MEMCPY	1
	#ifndef PRINTF_SIZET_MODIFIER
		#if defined(XSENS_64BIT)
			#if defined(__APPLE__)
				#define PRINTF_SIZET_MODIFIER "l"
			#else
				#define PRINTF_SIZET_MODIFIER PRINTF_INT64_MODIFIER
			#endif
		#else
			#if defined(__APPLE__)
				#define PRINTF_SIZET_MODIFIER "l"
			#else
				#define PRINTF_SIZET_MODIFIER PRINTF_INT32_MODIFIER
			#endif
		#endif
	#endif // PRINTF_SIZET_MODIFIER
#else
	typedef float XsReal;			//!< Defines the floating point type used by the Xsens libraries
	typedef unsigned int XsSize;	//!< XsSize must be unsigned number!
	typedef int XsSizeSigned;		//!< signed variant of XsSize
	#define XSREAL_ALLOWS_MEMCPY	1
	#define PRINTF_SIZET_MODIFIER ""
#endif // XSENS_SINGLE_PRECISION


/*!	\addtogroup enums Global enumerations
	@{
*/
/*! \brief These flags define the behaviour of data contained by Xsens data structures
	\details Normally, the user should never need to use these directly.
*/
enum XsDataFlags
{
	XSDF_None		= 0,	//!< No flag set
	XSDF_Managed	= 1,	//!< The contained data should be managed (freed) by the object, when false, the object assumes the memory is freed by some other process after its destruction
	XSDF_FixedSize	= 2,	//!< The contained data points to a fixed-size buffer, this allows creation of dynamic objects on the stack without malloc/free overhead.
	XSDF_Empty		= 4,	//!< The object contains undefined data / should be considered empty. Usually only relevant when XSDF_FixedSize is also set, as otherwise the data pointer will be NULL and empty-ness is implicit.
	XSDF_BadAlloc	= 8,	//!< The last memory allocation in the object failed, the contents are now erased
};
/*! @} */
typedef enum XsDataFlags XsDataFlags;

#ifdef __cplusplus
extern "C" {
#endif

XSTYPES_DLL_API const char* XsDataFlags_toString(XsDataFlags f);

#ifdef __cplusplus
} // extern "C"

/*! \brief boolean xor function, since C++ does not provide this and operator ^ is not guaranteed to work */
inline bool xorBool(bool a, bool b)
{
	return (a && !b) || (b && !a);
}

/*! \brief \copybrief XsDataFlags_toString \sa XsDataFlags_toString */
inline const char* toString(XsDataFlags s)
{
	return XsDataFlags_toString(s);
}
#endif
#ifdef SWIG
	// note that there is no XSDEPRECATED_END, deprecated definitions are expected to be the last definitions in a list
	#define XSDEPRECATED_START	private: /* deprecated start */
#else
	// note that there is no XSDEPRECATED_END, deprecated definitions are expected to be the last definitions in a list
	#define XSDEPRECATED_START	/* deprecated start */
#endif
#ifndef __cplusplus
	// define BOOL, TRUE and FALSE
	#ifndef BOOL
		typedef int BOOL;
	#endif

	#ifndef TRUE
		#define TRUE (1)
	#endif

	#ifndef FALSE
		#define FALSE (0)
	#endif
	#define XSFALLTHROUGH	/* fallthrough */
	#define XSNORETURN		/* noreturn */
	#define XSDEPRECATED	/* deprecated */
#else
	#if __cplusplus >= 201703L
		#define XSFALLTHROUGH	[[fallthrough]] /* FALLTHRU fallthrough */
		#define XSNORETURN		[[noreturn]] /* noreturn */
		#define XSDEPRECATED	[[deprecated]] /* deprecated */
	#else
		#if defined(__GNUC__)
			#define XSFALLTHROUGH	[[fallthrough]] /* FALLTHRU fallthrough */
			#define XSNORETURN		[[noreturn]] /* noreturn */
		#else
			#define XSFALLTHROUGH	/* FALLTHRU fallthrough */
			#define XSNORETURN		/* noreturn */
		#endif
		#if __cplusplus >= 201402L
			#define XSDEPRECATED	[[deprecated]] /* deprecated */
		#else
			#define XSDEPRECATED	/* deprecated */
		#endif
	#endif
#endif // __cplusplus

#define XS_ENUM_TO_STR_CASE(value) case value: return #value

// different alignment commands for gcc / MSVS for structures that need to be 1-byte aligned.
#if defined (SWIG)
	#define XS_PACKED_STRUCT_START
	#define XS_PACKED_STRUCT_END
#elif defined (_MSC_VER)
	#define XS_PACKED_STRUCT_START __pragma(pack(push, 1));
	#define XS_PACKED_STRUCT_END __pragma(pack(pop));
#elif defined (__ICCARM__)
	#define XS_PACKED_STRUCT_START _Pragma("pack(push, 1)");
	#define XS_PACKED_STRUCT_END _Pragma("pack(pop)");
#elif defined (__ICC8051__)
	#define XS_PACKED_STRUCT_START
	#define XS_PACKED_STRUCT_END
#elif defined (__GNUC__)
	#define XS_PACKED_STRUCT_START
	#define XS_PACKED_STRUCT_END
#elif (defined(__arm__) && defined(__ARMCC_VERSION))
	#define XS_PACKED_STRUCT_START
	#define XS_PACKED_STRUCT_END
#elif (defined(__ADSP21000__))
	#define XS_PACKED_STRUCT_START
	#define XS_PACKED_STRUCT_END
#else
	#error "Structure packing macros not defined for this compiler"
	#define XS_PACKED_STRUCT_START
	#define XS_PACKED_STRUCT_END
#endif

#ifdef __GNUC__
	#define XS_PACKED_STRUCT __attribute__((__packed__))
#else
	#define XS_PACKED_STRUCT	/* */
#endif

#if defined (__ICCARM__)
	#define XS_PACKED_POINTER __packed
#else
	#define XS_PACKED_POINTER
#endif

#endif
