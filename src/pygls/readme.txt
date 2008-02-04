README for PythonGLS

Michael Pilgermann
Email to: michael.pilgermann@gmx.de
Licensed under the Genreal Public License (GPL) 

http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG


Content
1. Introduction
2. Installation
3. Usage
...


1. Introduction
---------------
...



2. Installation
---------------
Requirements
- Python (>=2.5) must be installed.

Step by step
- Unpack the archive
    * tar xzvf pygls-0.1.1.tar.gz
- Change into directory pygls
    * cd pygls-0.1.1
- Run Makefile with option install
    * make install  (you must have root privileges: e.g. sudo make install)

Off you go. The library is installed.


3. Usage
--------
PythonGLS is a library. You may use it from within your Python code to access functionality
from the GPS Location Sharing project. You have to import the moduel (pygls); afterwards you
have access to members of this package.

Here an example:

from pygls.ServerConnection import ServerConnection
from pygls.PythonGLS import Position, Waypoint
import pygls.GLSException

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
