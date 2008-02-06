"""
Module for pyroute to integrate with pygls.

This module can be loaded by pyroute in order to be used to access functionality of the pygls library
and this way to the conntection to the GPS Location Sharing server (GLS).

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)

@VAR FILENAME_GLSSETTINGS: Location and file name of file for GLS settings
@TYPE FILENAME_GLSSETTINGS: C{String}
@VAR PROTOCOL_VERSION: Version of GLS Protocol to be used for communication with GLS server
@TYPE PROTOCOL_VERSION: C{String}
"""
FILENAME_GLSSETTINGS = "Setup/glssettings.txt"
PROTOCOL_VERSION = "2"

from  poi_base import *
from pygls.ServerConnection import ServerConnection
from pygls.PythonGLS import Position, Waypoint
import pygls.GLSException
import thread
import time
import ConfigParser

class pyglsPoiModule(poiModule):
    """
    Maintains connection to the GLS server and requests information from there when necessary.
    """
    def __init__(self, modules, parent):
        print "Starting up module GPS location sharing (GLS) in background."
        self._parent = parent
        poiModule.__init__(self, modules)
        if self._startup() == 0:
            self.draw = True
        else:
            self.draw = False
        
    def __del__(self):
        """
        Setting local variable to "false" in order to notify threads about termination.
        """
        self._up = 0
 
    def _loadSettings(self):
        """
        Loads all settings for the GLS module from a configuration file.
        """
        config = ConfigParser.ConfigParser()
        try:
            config.read(FILENAME_GLSSETTINGS)
            self._servername =  config.get("pygls", "server")
            self._port =  int(config.get("pygls", "port"))
            self._groupname =  config.get("pygls", "group")
            self._username =  config.get("pygls", "user")
            self._password =  config.get("pygls", "password")
            self._device =  config.get("pygls", "device")
            self._delay =  int(config.get("pygls", "delay"))
            self._forceRedraw = int(config.get("pygls", "forceredraw"))
            if self._password.strip == "" or self._password == "None":
                self._password = None
        except:
            print "Could not load settings for GLS module (%s)." %(FILENAME_GLSSETTINGS)
            return -1
        return 0
        
    def _startup(self):
        """
        Establishes the connection to the GLS server and sets up a continous download of position data.
        
        A new thread is started that will perform updates on the GPS position data on a regular basis.
        
        Applies its settings from a configuration file located in Setup/glssettings.txt
        """
        if self._loadSettings() != 0:
            return -1

        self._s = ServerConnection(self._servername, self._port, PROTOCOL_VERSION, self._username , self._password, self._device , self._groupname)
        self._group = poiGroup(self._groupname)
        self.groups.append(self._group)
        thread.start_new_thread(self._updatePositionsPeriodically, () )
        self._up = 1
        return 0
               
    def _updatePositionsPeriodically(self):
        """"
        Initiates a pull of gps positions from the server periodically.
        """
        while self._up:
            self._loadPositionsFromServer()
            if self._forceRedraw:
                self._parent.forceRedraw()
            time.sleep(self._delay)

    def _loadPositionsFromServer(self):
        """
        Performs a single download of all available positions on the server.
        """
##        print "pyglsModule: Loading GLS positions from GLS server."
        # clear last positions
        del self._group.items[:]
        
        try:
            self._s.joinGroup(self._groupname)
            posOthers = self._s.requestPositions()
            self._s.closeConnection()
            for pos in posOthers.keys():
##                print "\t" + pos + ":" + str(posOthers[pos])
                item = poi(posOthers[pos].getLatitude(), posOthers[pos].getLongitude())
                item.title = "GLS:%s (OpenMoko)" %(pos)
                self._group.items.append(item)
            return posOthers
        except pygls.GLSException.GLSException, e:
            print "Connection error: " + e.getMsg() + "\n\t" + e.getLongMsg()
