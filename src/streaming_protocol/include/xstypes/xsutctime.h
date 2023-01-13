#ifndef XSUTCTIME_H
#define XSUTCTIME_H

#include "xstimeinfo.h"

#ifdef __cplusplus
extern "C" {
#endif
#ifndef __cplusplus
#define XSUTCTIME_INITIALIZER	{ 0, 0 ,0, 0, 0, 0, 0, 0, 0}
#endif

// for backwards compatibility only, use XsTimeInfo instead
#define XsUtcTime XsTimeInfo
XSTYPES_DLL_API void XsUtcTime_currentTime(struct XsUtcTime* now);

#ifdef __cplusplus
} // extern "C"
#endif

#endif
