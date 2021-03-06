"""
Python library for GPS Location Sharing - defines all Types for exception handling.
http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)

@var EC_UNKNOWN_ERROR: Error code - unkown error
@type EC_UNKNOWN_ERROR: C{int}
@var EC_VERSION_NOT_SUPPORTED: Error code - version of protocol not supported
@type EC_VERSION_NOT_SUPPORTED: C{int}
@var EC_AUTHENTICATION_ERROR: Error code - authentication error when connecting to server
@type EC_AUTHENTICATION_ERROR: C{int}
"""
EC_UNKNOWN_ERROR = 0
EC_VERSION_NOT_SUPPORTED = 1     
EC_AUTHENTICATION_ERROR = 2
EC_VIOLATION_BUSINESS_RULES = 3
EC_VALIDATION_ERROR = 4

class GLSException(Exception):
    """
    GLS specific exception to cover error states.
    """
    
    def __init__(self, msg, errorCode = None, longMsg = None):
        """
        Constructor
        
        @param msg: Short message to identify the error (1 line)
        @type msg: C{String}
        @param errorCode: Code for identifying the type of problem. See constants in the module for details.
        @type errorCode: C{int}
        @param longMsg: More detailed error information for the problem (stack trace, etc)
        @type longMsg: C{String}
        """
        self._msg = msg
        self._errorCode = errorCode
        self._longMsg = longMsg
        
    def __str__(self):
        """
        Computes a string representation of the content of this exception instance.
        
        This representation is made up by the short message of the exception.
        
        @return: String representation of object content
        @rtype: C{String}
        """
        return msg

    def getMsg(self):
        """
        GETTER
        """
        return self._msg
        
    def getErrorCode(self):
        """
        GETTER
        """
        return self._errorCode
        
    def getLongMsg(self):
        """
        GETTER
        """
        return self._longMsg
