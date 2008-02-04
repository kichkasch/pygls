"""
Test program with graphical output for
Python library for GPS Location Sharing.
http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

The following site-packages (for Python) must be installed:
- tkinter
- pygls

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
PASSWORD = None # "test"
DEVICE = "DummyDevice"

SIZE_X = 550
SIZE_Y = 700
SIZE_X2 = 500
SIZE_Y2 = 500
DELAY = 5       # seconds between 2 updates
VIEWAREA = [0,0,50,50]

MAX_COUNT = 7
COLORS = ["blue", "red", "green", "brown", "cyan","magenta", "orange"]

from pygls.ServerConnection import ServerConnection
from pygls.PythonGLS import Position, Waypoint
import pygls.GLSException
from Tkinter import *
import time
import getopt, sys

def getPositions(s):
    try:
        posOthers = s.requestPositions()
        print "Position of others"
        for pos in posOthers.keys():
            print "\t" + pos + ":" + str(posOthers[pos])
##        x = 1         # get some more data here - stupid copy
##        while x < 8:
##            posOthers[posOthers.keys()[0]+"_copy_" + str(x)] = posOthers[posOthers.keys()[0]]  
##            x+=1
        return posOthers
    except pygls.GLSException.GLSException, e:
        print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()

def startup():
    print "Starting up"
    print "\tConnection parameters: %s|%s@%s:%d [group:%s]" %( USER , PASSWORD, SERVER, PORT, GROUP)
    print "\tPresentation parameters: (%d|%d) - (%d|%d)" %(VIEWAREA[0],VIEWAREA[1],VIEWAREA[2],VIEWAREA[3])
    s = ServerConnection(SERVER, PORT, PROTOCOL_VERSION, USER , PASSWORD, DEVICE , GROUP)
    try:
        print "\n\tJoining group %s" %(GROUP)
        s.joinGroup(GROUP)
        print "\t\tOK"

        root = Tk()
        root.title("Simple GLS Location visualiser")
        global canvas
        canvas = Canvas(root, width=SIZE_X, height=SIZE_Y)
        canvas.pack()
        #root.mainloop()

        return s, canvas
    except pygls.GLSException.GLSException, e:
        print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()
        return None, None
    

def _drawcircle(canv,x,y,rad, color):
    # transform into view area
    x = (x - VIEWAREA[0]) * ( SIZE_X2 / ( VIEWAREA[2] - VIEWAREA[0])) + 25
    y = (y - VIEWAREA[1]) * ( SIZE_Y2 / ( VIEWAREA[3] - VIEWAREA[1])) + 50
    return canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill=color)
     
def _drawLegend(canv):
    canvas.create_rectangle ( 25,55,525,545, stipple="gray75")
    canvas.create_text(SIZE_X / 2, 20, text = "GLS Locations",font="Arial 20")
    canvas.create_text(25, 45,  text= str(VIEWAREA[0]) +" | " +str(VIEWAREA[1]) , fill = "darkgray")
    canvas.create_text(525, 45,  text= str(VIEWAREA[2]) +" | " +str(VIEWAREA[1]), fill = "darkgray")
    canvas.create_text(25, 555,  text= str(VIEWAREA[0]) +" | " +str(VIEWAREA[3]), fill = "darkgray")
    canvas.create_text(525, 555,  text= str(VIEWAREA[2]) +" | " +str(VIEWAREA[3]), fill = "darkgray")
    
def drawStuff(canvas, positions):
    canvas.delete(ALL)
    _drawLegend(canvas)

    i = 0
    for posName in positions.keys():
        pos = positions[posName]
        if pos.getLatitude() < VIEWAREA[0] or pos.getLatitude() > VIEWAREA[2] or pos.getLongitude() < VIEWAREA[1] or pos.getLongitude() > VIEWAREA[3]:
            canvas.create_text(SIZE_X / 2, 560+20*i, text=posName + " (" + str(pos) + ") - out of view", fill = COLORS[i])
        else:
            _drawcircle(canvas, pos.getLatitude(),pos.getLongitude(),5,COLORS[i])
            canvas.create_text(SIZE_X / 2, 560+20*i, text=posName + " (" + str(pos) + ")", fill = COLORS[i])
        i+=1
        if i == MAX_COUNT:
            break
    canvas.pack()
    canvas.update_idletasks()    

    time.sleep(DELAY)

def _printHelp():
    print "\nSmall Python / TKinter app for visualising GPS positions from GLS server."
    print "Usage:"
    print "\t%s -h \t\tPrint this help" %(sys.argv[0])
    print "\t%s [-g GROUP] [-u USERNAME] [-s SECRET PASSWORD] [-h HOSTNAME] [-p PORT]" %(sys.argv[0])
    print "\t\t[-d DELAY BETWEEN DATA PULLS (s)] [-1 X-VALUE ViewAreaMin] [-2 Y-VALUE ViewAreaMin]"
    print "\t\t[-3 X-VALUE ViewAreaMax] [-4 Y-VALUE ViewAreaMax]"
    print "\t\t\t\tRun interface with given connection and updating parameters"

def _evaluateArgs():
    global GROUP, USER, PASSWORD, SERVER, PORT, DELAY, VIEWAREA
    optlist, args = getopt.getopt(sys.argv[1:], 'hg:u:s:h:p:d:1:2:3:4:')
    for o,a in optlist:
        if o == "-h":
            _printHelp()
            return 1
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
        if o == "-1":
            VIEWAREA[0] = int(a)
        if o == "-2":
            VIEWAREA[1] = int(a)
        if o == "-3":
            VIEWAREA[2] = int(a)
        if o == "-4":
            VIEWAREA[3] = int(a)
    return 0


if __name__ == "__main__":
    if not _evaluateArgs():
        s, canvas = startup()
        if s!=None:
            while 1:
                print "Updating positions"
                pos = getPositions(s)
                drawStuff(canvas, pos)
