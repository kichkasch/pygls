"""
Test program for
Python library for GPS Location Sharing.
http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""

from pygls.ServerConnection import ServerConnection
import pygls.GLSException

def testConnection():
    #s = ServerConnection("localhost", 47757, "2", "kichkasch", "secret", "DummyDevice", "OpenMoko")
    s = ServerConnection("localhost", 47757, "2", "CathodioN", "test", "DummyDevice", "OpenMoko")
    try:
        s.testConnection()
    except GLSException.GLSException, e:
        print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()
    
