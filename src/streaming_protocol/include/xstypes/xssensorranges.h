#ifndef XSSENSORRANGES_H
#define XSSENSORRANGES_H

#include "xstypesconfig.h"
#include "xsstring.h"

#ifdef __cplusplus
extern "C" {
#endif

enum HardwareManufacturerType
{
	HMT_MT	= 0,
	HMT_None
};
typedef enum HardwareManufacturerType HardwareManufacturerType;

XSTYPES_DLL_API void findHardwareTypeC(const XsString* productCode, XsString* resultValue);
XSTYPES_DLL_API HardwareManufacturerType findHardwareManufacturerC(const XsString* productCode);

XSTYPES_DLL_API double accelerometerRangeC(const XsString* productCode, int32_t hwVersionMajor);
XSTYPES_DLL_API double gyroscopeRangeC(const XsString* productCode);

XSTYPES_DLL_API double actualAccelerometerRangeC(const XsString* productCode, int32_t hwVersionMajor);
XSTYPES_DLL_API double actualGyroscopeRangeC(const XsString* productCode);

#ifdef __cplusplus
}

inline static XsString findHardwareType(const XsString& productCode)
{
	XsString rv;
	findHardwareTypeC(&productCode, &rv);
	return rv;
}
inline static HardwareManufacturerType findHardwareManufacturer(const XsString& productCode)
{
	return findHardwareManufacturerC(&productCode);
}
inline static double accelerometerRange(const XsString& productCode, int32_t hwVersionMajor)
{
	return accelerometerRangeC(&productCode, hwVersionMajor);
}
inline static double gyroscopeRange(const XsString& productCode)
{
	return gyroscopeRangeC(&productCode);
}
inline static double actualAccelerometerRange(const XsString& productCode, int32_t hwVersionMajor)
{
	return actualAccelerometerRangeC(&productCode, hwVersionMajor);
}
inline static double actualGyroscopeRange(const XsString& productCode)
{
	return actualGyroscopeRangeC(&productCode);
}
#endif

#endif
