#ifdef __cplusplus
#ifndef XSEXCEPTION_H
#define XSEXCEPTION_H

#ifndef XSENS_NO_EXCEPTIONS

#include <exception>
#include "xsresultvalue.h"
#include "xsstring.h"

/*! \brief Exception class for Xsens public libraries. Inherits from std::exception
*/
class XsException : public std::exception
{
public:
	//! \brief Copy constructor
	XsException(XsException const& e)
		: std::exception()
		, m_code(e.m_code)
		, m_description(e.m_description)
	{
	}

	/*! \brief Initializing constructor
		\details This constructor uses the value in \a err and the supplied \a description to create a full
		text for when the user requests what() or text()
		\param err The error code that the exception should report
		\param description A description of the error. The constructor prefixes this with a textual
							description of the error code unless prefix is false.
	*/
	XsException(XsResultValue err, XsString const& description)
		: std::exception()
		, m_code(err)
		, m_description(description)
	{
	}

	/*! \brief Initializing constructor
		\param description A description of the error.
	*/
	explicit XsException(XsString const& description)
		: std::exception()
		, m_code(XRV_ERROR)
		, m_description(description)
	{
	}

	//! \brief Destructor
	virtual ~XsException() noexcept
	{
	}

	//! \brief Assignment operator, copies \a e to this
	XsException& operator = (XsException const& e)
	{
		if (this != &e)
		{
			m_code = e.m_code;
			m_description = e.m_description;
		}
		return *this;
	}

	//! \brief Returns the error value supplied during construction
	inline XsResultValue code() const noexcept
	{
		return m_code;
	}

	//! \brief Returns a description of the error that occurred as a char const*
	inline char const* what() const noexcept
	{
		return m_description.c_str();
	}

	//! \brief Returns a description of the error that occurred as a XsString
	inline XsString const& text() const noexcept
	{
		return m_description;
	}

private:
	XsResultValue m_code;	//!< The supplied error code
	XsString m_description;	//!< The supplied description, possibly prefixed with a description of the error code
};

#include <ostream>
inline static std::ostream& operator<< (std::ostream& os, const XsException& ex)
{
	if (ex.code() == XRV_OK)
		os << "XRV_OK";
	else
		os << "XRV " << ex.code();
	if (ex.code() != XRV_OK && !ex.text().empty())
		os << ": " << ex.text();
	return os;
}

#endif

#endif
#endif
