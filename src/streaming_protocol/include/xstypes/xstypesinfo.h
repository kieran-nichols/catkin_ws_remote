#ifndef XSTYPESINFO_H
#define XSTYPESINFO_H

#include "xstypesconfig.h"

struct XsVersion;

#ifdef __cplusplus
	#include "xsversion.h"
	extern "C"
#endif
XSTYPES_DLL_API void xsTypesVersion(struct XsVersion* version);
#define XsTypesInfoGetVersion(a)	xsTypesVersion(a)

#ifdef __cplusplus
/*! \brief Return the version information of the XsTypes library */
inline static XsVersion xsTypesVersion()
{
	XsVersion v;
	xsTypesVersion(&v);
	return v;
}
#endif

#endif
