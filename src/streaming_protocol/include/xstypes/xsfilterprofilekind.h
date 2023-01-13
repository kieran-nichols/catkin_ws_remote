#ifndef XSFILTERPROFILEKIND_H
#define XSFILTERPROFILEKIND_H

/*! \brief Filter Profile Kinds */
enum XsFilterProfileKind
{
	XFPK_Unknown		= 0,		//!< Unknown profile kind
	XFPK_Base			= 195,		//!< Indicates a base profile
	XFPK_Additional		= 196,		//!< Indicates an additional profile
	XFPK_Heading		= 197		//!< Indicates a heading profile
};

typedef enum XsFilterProfileKind XsFilterProfileKind;

#endif

