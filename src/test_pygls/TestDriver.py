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
from pygls.PythonGLS import Position, Waypoint
import pygls.GLSException
import time
import random

def testConnection():
    #s = ServerConnection("localhost", 47757, "2", "kichkasch", "secret", "DummyDevice", "OpenMoko")
    s = ServerConnection("localhost", 47757, "2", "CathodioN", "test", "DummyDevice", "OpenMoko")
    try:
        s.testConnection()
    except pygls.GLSException.GLSException, e:
        print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()

def testMore():
    s = ServerConnection("localhost", 47757, "2", "CathodioN", "test", "DummyDevice", "OpenMoko")
    try:
        print "Available groups are: "
        groups =  s.requestGroups()
        for x in groups:
            print "\t%s" %x
        print "Joining group %s" %(groups[0])
        s.joinGroup(groups[0])
        print "\tOK"
        
        pos = Position(23.4545,45.345345,1234.34,89.63,180)
        print "Sending my position: " + str(pos)
        s.sendPosition(pos)
        print "\tOK"
        
        wp = Waypoint(23.234,234.34343,125,"Carpool Parking Space")
        print "Sending my waypoint: " + str(wp)
        s.sendWaypoint(wp)
        print "\tOK"
        
        posOthers = s.requestPositions()
        print "Position of others"
        for pos in posOthers.keys():
            print "\t" + pos + ":" + str(posOthers[pos])

        wpOthers = s.requestWaypoints()
        print "Waypoints of others"
        for wp in wpOthers.keys():
            print "\t" + wp + ":" + str(wpOthers[wp])

    except pygls.GLSException.GLSException, e:
        print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()


def moveAround(loops, delay):
    s = ServerConnection("localhost", 47757, "2", "CathodioN", "test", "DummyDevice", "OpenMoko")
    try:
        print "Available groups are: "
        groups =  s.requestGroups()
        for x in groups:
            print "\t%s" %x
        print "Joining group %s" %(groups[0])
        s.joinGroup(groups[0])
        print "\tOK"
        
        pos = Position(23.4545,25.345345,1234.34,89.63,180)
        current = 0
        while current < loops:
            deltaX = random.random()*4 - 2
            deltaY = random.random()*4 - 2
            print "\tMoving %f / %f." %(deltaX, deltaY)
            pos = Position(pos.getLatitude()+deltaX,pos.getLongitude()+deltaY,1234.34,89.63,180)
            print "Sending my position: " + str(pos)
            s.sendPosition(pos)
            print "\tOK"
            current +=1
            time.sleep(delay)
        

    except pygls.GLSException.GLSException, e:
        print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()

    
#testConnection()
#testMore()
moveAround(10, 5)
