#ifndef XSDEBUGCOUNTERS_H
#define XSDEBUGCOUNTERS_H

#include "xstypesconfig.h"

#ifdef XSENS_USE_DEBUG_COUNTERS
#ifdef __cplusplus
extern "C" {
#endif

extern XSTYPES_DLL_API int XsVector_resetDebugCounts(void);
extern XSTYPES_DLL_API int XsVector_allocCount(void);
extern XSTYPES_DLL_API int XsVector_freeCount(void);
extern int XsVector_incAllocCount(void);
extern int XsVector_incFreeCount(void);

extern XSTYPES_DLL_API int XsMatrix_resetDebugCounts(void);
extern XSTYPES_DLL_API int XsMatrix_allocCount(void);
extern XSTYPES_DLL_API int XsMatrix_freeCount(void);
extern int XsMatrix_incAllocCount(void);
extern int XsMatrix_incFreeCount(void);

extern XSTYPES_DLL_API int XsArray_resetDebugCounts(void);
extern XSTYPES_DLL_API int XsArray_allocCount(void);
extern XSTYPES_DLL_API int XsArray_freeCount(void);
extern int XsArray_incAllocCount(void);
extern int XsArray_incFreeCount(void);

#ifdef __cplusplus
} // extern "C"
#endif

#else

inline static int XsVector_resetDebugCounts(void)
{
	return 0;
}
inline static int XsVector_allocCount(void)
{
	return 0;
}
inline static int XsVector_freeCount(void)
{
	return 0;
}
inline static int XsVector_incAllocCount(void)
{
	return 0;
}
inline static int XsVector_incFreeCount(void)
{
	return 0;
}

inline static int XsMatrix_resetDebugCounts(void)
{
	return 0;
}
inline static int XsMatrix_allocCount(void)
{
	return 0;
}
inline static int XsMatrix_freeCount(void)
{
	return 0;
}
inline static int XsMatrix_incAllocCount(void)
{
	return 0;
}
inline static int XsMatrix_incFreeCount(void)
{
	return 0;
}

inline static int XsArray_resetDebugCounts(void)
{
	return 0;
}
inline static int XsArray_allocCount(void)
{
	return 0;
}
inline static int XsArray_freeCount(void)
{
	return 0;
}
inline static int XsArray_incAllocCount(void)
{
	return 0;
}
inline static int XsArray_incFreeCount(void)
{
	return 0;
}

#endif


#endif
