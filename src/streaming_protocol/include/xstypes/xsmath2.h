#ifndef XSMATH2_H
#define XSMATH2_H

#ifndef XSMATH_H
	#include "xsmath.h"
#endif

#ifdef __cplusplus
namespace XsMath
{
#ifdef __GNUC__
	#pragma GCC diagnostic push
	#pragma GCC diagnostic ignored "-Wunused-variable"
#endif
//! \brief The value e
XSMATHCONST XsReal e = XsMath_e;
//! \brief The value pi
XSMATHCONST XsReal pi = XsMath_pi;
//! \brief A really small value
XSMATHCONST XsReal tinyValue = XsMath_tinyValue;
//! \brief A convincingly large number
XSMATHCONST XsReal hugeValue = XsMath_hugeValue;
//! \brief A value related to the precision of floating point arithmetic (2.2204460492503131e-016)
XSMATHCONST XsReal epsilon = XsMath_epsilon;
/*! \brief Square root of epsilon
	\sa epsilon
*/
XSMATHCONST XsReal sqrtEpsilon = XsMath_sqrtEpsilon;
//! \brief Value that represents the subnormal number in floating point wizardry
XSMATHCONST XsReal denormalized = XsMath_denormalized;
/*! \brief Square root of denormalized
	\sa denormalized
*/
XSMATHCONST XsReal sqrtDenormalized = XsMath_sqrtDenormalized;
//! \brief Value to convert radians to degrees by multiplication
XSMATHCONST XsReal rad2degValue = XsMath_rad2degValue;
//! \brief Value to convert degrees to radians by multiplication
XSMATHCONST XsReal deg2radValue = XsMath_deg2radValue;
//! \brief 0
XSMATHCONST XsReal zero = XsMath_zero;
//! \brief 0.25
XSMATHCONST XsReal pt25 = XsMath_pt25;
//! \brief 0.5
XSMATHCONST XsReal pt5 = XsMath_pt5;
//! \brief -0.5
XSMATHCONST XsReal minusPt5 = XsMath_minusPt5;
//! \brief 1
XSMATHCONST XsReal one = XsMath_one;
//! \brief -1
XSMATHCONST XsReal minusOne = XsMath_minusOne;
//! \brief 2
XSMATHCONST XsReal two = XsMath_two;
//! \brief 4
XSMATHCONST XsReal four = XsMath_four;
//! \brief -2
XSMATHCONST XsReal minusTwo = XsMath_minusTwo;
//! \brief -pi/2
XSMATHCONST XsReal minusHalfPi = XsMath_minusHalfPi;
//! \brief pi/2
XSMATHCONST XsReal halfPi = XsMath_halfPi;
//! \brief 2*pi
XSMATHCONST XsReal twoPi = XsMath_twoPi;
//! \brief sqrt(2)
XSMATHCONST XsReal sqrt2 = XsMath_sqrt2;
//! \brief sqrt(0.5)
XSMATHCONST XsReal sqrtHalf = XsMath_sqrtHalf;
//! \brief infinity
XSMATHCONST XsReal infinity = XsMath_infinity;
#ifdef __GNUC__
	#pragma GCC diagnostic pop
#endif

//! \brief \copybrief XsMath_asinClamped
XSMATHINLINE XsReal asinClamped(XsReal x)
{
	return XsMath_asinClamped(x);
}

//! \brief \copybrief XsMath_rad2deg
XSMATHINLINE XsReal rad2deg(XsReal radians)
{
	return XsMath_rad2deg(radians);
}

//! \brief \copybrief XsMath_deg2rad
XSMATHINLINE XsReal deg2rad(XsReal degrees)
{
	return XsMath_deg2rad(degrees);
}

//! \brief \copybrief XsMath_pow2
XSMATHINLINE XsReal pow2(XsReal a)
{
	return XsMath_pow2(a);
}

//! \brief \copybrief XsMath_pow3
XSMATHINLINE XsReal pow3(XsReal a)
{
	return XsMath_pow3(a);
}

//! \brief \copybrief XsMath_doubleToLong
XSMATHINLINE2 int32_t doubleToLong(double d)
{
	return XsMath_doubleToLong(d);
}

#ifndef XSENS_NO_INT64
//! \brief \copybrief XsMath_doubleToInt64
XSMATHINLINE2 int64_t doubleToInt64(double d)
{
	return XsMath_doubleToInt64(d);
}
#endif
}	// namespace
#endif

#endif
