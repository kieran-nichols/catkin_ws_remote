#ifndef XSFLOATMATH_H
/* Rename some <math.h> functions to their single precision equivalents for non-C++ code */
#ifdef XSENS_SINGLE_PRECISION
#define atan2 atan2f
#define cos cosf
#define sin sinf
#define sqrt sqrtf
#define asin asinf
#endif
#endif // XSFLOATMATH_H
