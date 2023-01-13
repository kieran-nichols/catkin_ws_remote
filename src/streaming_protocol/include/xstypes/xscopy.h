#ifndef XSCOPY_H
#define XSCOPY_H

#define XSLISTCOPY(C)	\
	if (copy == thisPtr)\
	{\
		return;\
	}\
	C##_assign(copy, thisPtr->m_size, thisPtr->m_data)

#define XSLISTSWAP3(C, B, S)	\
	if ((!a->m_data || (a->m_flags & XSDF_Managed)) && (!b->m_data || (b->m_flags & XSDF_Managed))) {\
		B tmp;\
		*((C**) &tmp.m_data) = a->m_data;\
		*((XsSize*) &tmp.m_size) = a->m_size;\
		*((XsSize*) &tmp.m_flags) = a->m_flags;\
		*((C**) &a->m_data) = b->m_data;\
		*((XsSize*) &a->m_size) = b->m_size;\
		*((XsSize*) &a->m_flags) = b->m_flags;\
		*((C**) &b->m_data) = tmp.m_data;\
		*((XsSize*) &b->m_size) = tmp.m_size;\
		*((XsSize*) &b->m_flags) = tmp.m_flags;\
	} else {	/* elementwise swap */ \
		XsSize i;\
		assert(a->m_size == b->m_size);\
		for (i = 0; i < a->m_size; ++i) S(&a->m_data[i], &b->m_data[i]);\
	}

#define XSLISTSWAP2(C, B)	XSLISTSWAP3(C, B, C##_swap)

#define XSLISTSWAP(C)	XSLISTSWAP2(C, C##Array)

#ifdef __cplusplus
/*! \brief Byte-wise copy for data (de-)serialization
	\details The function essentially performs a memcpy from \a src to \a tgt using the size of \a tgt
	\param tgt The destination of the copy (reference)
	\param src The source of the copy (pointer)
*/
template <typename T>
inline static void xsByteCopy(T& tgt, void const* src)
{
	memcpy(&tgt, src, sizeof(T));
}

/*! \brief Byte-wise copy for data (de-)serialization followed by a multiplication
	\details The function essentially performs a memcpy from \a src to \a tgt using the size of \a tgt
	\param tgt The destination of the copy (reference)
	\param src The source of the copy (pointer)
	\param mul The multiplication value
*/
template <typename T>
inline static void xsByteCopyMultiply(T& tgt, void const* src, T mul)
{
	memcpy(&tgt, src, sizeof(T));
	tgt *= mul;
}
#endif

#endif
