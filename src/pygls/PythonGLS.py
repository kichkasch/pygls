"""
Python library for GPS Location Sharing - entry point to library.

http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""

from ServerConnection import ServerConnection
import GLSException

#
#
# testing purposes - all this will be removed later on
#
# CathodioN,mysecretpassword

#s = ServerConnection("localhost", 47757, "2", "kichkasch", "secret", "DummyDevice", "OpenMoko")
s = ServerConnection("localhost", 47757, "2", "CathodioN", "mysecretpassword", "DummyDevice", "OpenMoko")
try:
    s.testConnection()
except GLSException.GLSException, e:
    print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()
    
#
# end - testing purposes
#
