"""
Test program with graphical output for
Python library for GPS Location Sharing.
http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""

GROUP = "OpenMoko"
SERVER = "localhost"
PORT = 47757
PROTOCOL_VERSION = "2"
USER = "Guest" # "CathodioN"
PASSWORT = None # "test"
DEVICE = "DummyDevice"

SIZE_X = 500
SIZE_Y = 600
DELAY = 5       # seconds between 2 updates
VIEWAREA = [0,0,50,50]

from pygls.ServerConnection import ServerConnection
from pygls.PythonGLS import Position, Waypoint
import pygls.GLSException
from Tkinter import *
import time

def getPositions(s):
    try:
        posOthers = s.requestPositions()
        print "Position of others"
        for pos in posOthers.keys():
            print "\t" + pos + ":" + str(posOthers[pos])
        return posOthers
    except pygls.GLSException.GLSException, e:
        print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()

def startup():
    s = ServerConnection(SERVER, PORT, PROTOCOL_VERSION, USER , PASSWORT, DEVICE , GROUP)
    try:
        print "Joining group %s" %(GROUP)
        s.joinGroup(GROUP)
        print "\tOK"

        root = Tk()
        global canvas
        canvas = Canvas(root, width=SIZE_X, height=SIZE_Y)
        canvas.pack()
        #root.mainloop()

        return s, canvas
    except pygls.GLSException.GLSException, e:
        print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()
    

def _drawcircle(canv,x,y,rad, color):
    # transform into view area
    print x, y
    x = (x - VIEWAREA[0]) * ( SIZE_X / ( VIEWAREA[2] - VIEWAREA[0]))
    y = (y - VIEWAREA[1]) * ( SIZE_Y / ( VIEWAREA[3] - VIEWAREA[1]))
    print x, y
    return canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill=color)
     
    
def drawStuff(canvas, positions):
    canvas.delete(ALL)
    for posName in positions.keys():
        pos = positions[posName]
        _drawcircle(canvas, pos.getLatitude(),pos.getLongitude(),5,"blue")
    canvas.pack()
    canvas.update_idletasks()    

    time.sleep(DELAY)

#testConnection()
s, canvas = startup()
while 1:
    print "Updating positions"
    pos = getPositions(s)
    drawStuff(canvas, pos)
