"""
Test program for
Python library for GPS Location Sharing.
http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

This client is a dummy gps device, starting at a predifined GPS location and walking around randomly.

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""

GROUP = "OpenMoko"
SERVER = "localhost"
PORT = 47757
PROTOCOL_VERSION = "2"
USER = "CathodioN"
PASSWORD = "test"
DEVICE = "DummyDevice"

DELAY = 5       # seconds between 2 updates
LOOPS = 0       # infinite


from pygls.ServerConnection import ServerConnection
from pygls.PythonGLS import Position, Waypoint
import pygls.GLSException
import time
import random
import getopt, sys

def _evaluateArgs():
    global GROUP, USER, PASSWORD, SERVER, PORT, DELAY, LOOPS
    optlist, args = getopt.getopt(sys.argv[1:], 'g:u:s:h:p:d:l:')
    for o,a in optlist:
        if o == "-g":
            GROUP = a
        if o == "-u":
            USER = a
        if o == "-s":
            PASSWORD = a
            if PASSWORD == "None":
                PASSWORD = None
        if o == "-h":
            SERVER = a
        if o == "-p":
            PORT = int(a)
        if o == "-d":
            DELAY = int(a)
        if o == "-l":
            LOOPS = int(a)
    return 0


def moveAround(loops, delay):
    print "Starting up"
    print "\tConnection parameters: %s|%s@%s:%d [group:%s]" %( USER , PASSWORD, SERVER, PORT, GROUP)
    print "\tDoing %d updates with %d seconds delay in between 2 updates." %(loops, delay)
    s = ServerConnection(SERVER, PORT, PROTOCOL_VERSION, USER, PASSWORD, DEVICE, GROUP)
    try:
        print "\n\tJoining group %s" %(GROUP)
        s.joinGroup(GROUP)
        print "\t\tOK"
        
        pos = Position(23.4545,25.345345,1234.34,89.63,180)
        current = 0
        while loops == 0 or current < loops:
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

_evaluateArgs()
moveAround(LOOPS, DELAY)
