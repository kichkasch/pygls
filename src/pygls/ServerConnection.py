"""
Python library for GPS Location Sharing - responsible for the connection to the GLS Server.

http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""
import socket
import GLSException
import GLSCommands
from PythonGLS import Position, Waypoint

class ServerConnection:
    """
    An instance of this class maintains one connection to the GLS server.
    
    It may be reused for several commands.
    
    Connection will be established automatically as soon as the first command is to be sent to the server. Connection
    will be shut down from the client as soon as the destructor is called.
    
    There is no need (and way) to establish or shut down the connection to the server manually.
    
    @ivar _hostName: Hostname or IP address of the GLS server
    @type _hostName: C{String}
    @ivar _port: Port, the GLS server is listening on
    @type _port: C{int}
    @ivar _version: Version of the GLS protocol to use for the communication to GLS server
    @type _version: C{String}
    @ivar _clientName: Name of the client for logging into the GSL server
    @type _clientName: C{String}
    @ivar _password: Password for logging into the GLS server
    @type _password: C{String}
    @ivar _deviceName: Name of the GPS device
    @type _deviceName: C{String}
    @ivar _groupName: Name of the group to be used for this session
    @type _groupName: C{String}
    @ivar _serverVersion: Versions of the GLS specification supported by the server
    @type _serverVersion: C{String}
    @ivar _connected: Connection state (0 is not connected, 1 is connected)
    @type _connected: C{int}
    @ivar _s: Socket for the connection to GLS server
    @type _s: L{socket.socket}
    """
    
    def __init__(self, hostName, port, version, clientName, password, deviceName, groupName):
        """
        Constructor
        
        Only stores the given parameters in instance variables. No connection is being established here.
        
        Available versions for server (L{_serverVersion}) is set to C{None}. Connection state (L{_connected}) is set to 0.
        
        @param hostName: Hostname or IP address of the GLS server
        @type hostName: C{String}
        @param port: Port, the GLS server is listening on
        @type port: C{int}
        @param version: Version of the GLS protocol to use for the communication to GLS server
        @type version: C{String}
        @param clientName: Name of the client for logging into the GSL server
        @type clientName: C{String}
        @param password: Password for logging into the GLS server
        @type password: C{String}
        @param deviceName: Name of the GPS device
        @type deviceName: C{String}
        @param groupName: Name of the group to be used for this session
        @type groupName: C{String}
        """
        self._hostName = hostName
        self._port = port
        self._version = version
        self._clientName = clientName
        self._password = password
        self._deviceName = deviceName
        self_groupName = groupName
        self._serverVersion = None
        self._connected = 0
        self._s = None
        
    def __del__(self):
        """
        Destructor
        
        Closes connection to server.
        """
        self._closeConnection()
        
    def _sendCommand(self, command, initMode = 0):
        """
        Sends exactly one command to the GLS server.
        
        The command is extended by a line feed before sending. The line feed from the line(s) in the reply
        is / are removed before the value is returned.
        
        Replies, which are made up by several lines are returned as a list of Strings (in contrast to single line replies,
        which are returned as a single String). Multi-Line-Replies are currently indicated by a leading "P" (position of others)
        ,a leading "W" (waypoints of others) or a leading "G" (available groups). The sequence is terminated by a line made 
        up by an "F". This last line will be part of the returned list as well.
        
        The replies are checked for error messages. If the reply is either a "C" or an "E" an L{GLSException.GLSException}
        will be raised.
        
        @param command: Command to be sent to the server
        @type command: C{String}
        @param initMode: When sending this command the connection is in initialisation mode; meaning, it shall no be checked, whether a connection is establised already
        @type initMode: C{int}
        @return: Received reply from the server. A String in case of a single line reply; an array of strings in case of multi line reply.
        @rtype: C{String} or C{List} of C{String}
        """
##        print "Sending %s" %command
        if not self._connected and not initMode:
            self._establishConnection()
        self._s.send(command +'\n')
        data, tmp = self._s.recvfrom(1024)
        data = data[:len(data)-1]   # remove line feed

        if len(data) < 1:
            raise GLSException.GLSException("No data from server.", GLSException.EC_VALIDATION_ERROR, "No data was returned from the server for the command " + command)

        if data[0] == GLSCommands.RE_CHANGE:
            raise GLSException.GLSException("Violation of business rules (C) when sending the command.", GLSException.EC_VIOLATION_BUSINESS_RULES, "A business rule was violated when sending the command " + command)
        if data[0] == GLSCommands.RE_ERROR:
            raise GLSException.GLSException("Validation error (E) when sending the command.", GLSException.EC_VALIDATION_ERROR, "A validation error occured when sending the command " + command)

        if data[0] == GLSCommands.RE_POSITION or data[0] == GLSCommands.RE_WAYPOINT or data[0] == GLSCommands.RE_GROUP or data[0] == GLSCommands.RE_FINISHED:
            ret = []
            ret.append(data)
            while data[0] != GLSCommands.RE_FINISHED:   # fill up return list until the FINISH line comes in
                data, tmp = self._s.recvfrom(1024)
                data = data[:len(data)-1]   # remove line feed
                ret.append(data)
            data = ret
##        print "\tReceived %s" %data
        return data
    
    def _sendCommands(self, commands, initMode = 0):
        """
        Sends an array of commands to the GLS server (line by line).
        
        Each item in the lists is sent to the GLS server. Before sending, a line feed is appended.
        
        Received results are stored in a dictionary - the list of commands makes up the keys in the dictionary,
        the received results are the values. (Values might either be a simple string or a list of strings in case of
        several lines are sent back by the server for a command.
        
        @param commands: Commands to be send to the GLS server. They must not contain the line feed.
        @type commands: C{List}
        @param initMode: When sending this command the connection is in initialisation mode; meaning, it shall no be checked, whether a connection is establised already
        @type initMode: C{int}
        @return: Received results for all command
        @rtype: C{Dict} of C{String} and C{String} | C{List}
        """
        results = {}
        for item in commands:
            result = self._sendCommand(item, initMode)
            results[item] = result
        return results
        
    def _establishConnection(self):
        """
        Starts up the connection to the GLS server.
        
        The method is going through the full handshake (V, N, D) with the GLS server. If a password
        is available for this connection, it is used - if no password is available, the connection is being established
        without providing one.
        
        The socket is stored in the 
        instance reference (L{_s}) and the state of the connection (L{_connected}) is set to 1. The reply of the
        server with the supported versions is stored in the instance reference (L{_serverVersion}).
        """
        if self._connected:
            return
##        print "Connection attempt for %s." %self._hostName
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((self._hostName, self._port))
        data, tmp = self._s.recvfrom(1024)
        self._serverVersion = data[:len(data)-1]
        
        try:
            res = self._sendCommand(GLSCommands.CO_VERSION +self._version, 1)
        except GLSException.GLSException:
            raise GLSException.GLSException("Requested version of GLS specification not supported by server.", GLSException.EC_VERSION_NOT_SUPPORTED, "Version mismatch - server understands %s; client wants to speak %s" % (self._serverVersion, self._version))
        
        if self._password:
            comm = GLSCommands.CO_LOGIN + self._clientName + "," + self._password
        else:
            comm = GLSCommands.CO_LOGIN + self._clientName

        try:
            res = self._sendCommand(comm, 1)
        except GLSException.GLSException:
            raise GLSException.GLSException("Authentication error when connecting to GLS server.", GLSException.EC_AUTHENTICATION_ERROR, "The client (%s) could not be authenticated on the server." %(self._clientName))
        
        try:
            res = self._sendCommand(GLSCommands.CO_DEVICE + self._deviceName, 1)  
        except GLSException.GLSException:
            raise GLSException.GLSException("Device not accepted by server.", GLSException.EC_UNKNOWN_ERROR, "The server did not accept the device (%s) for the connection establishment." %(self._deviceName))

        self._connected = 1
##        print "Connected to %s " %self._hostName
        
        
    def _closeConnection(self):
        """
        Closes down the socket to the server.
        """
        if not self._connected:
            return
##        print "Closing connection to GLS server"
        self._sendCommand(GLSCommands.CO_QUIT)
        self._s.close()
##        print "\tConnection closed"

        
    def testConnection(self):
        """
        Tests connectivity to the GLS server.
        
        Sends a testing request to the server. As there is nothing like a "ping" implemented in the protocol it is
        requesting the list of available groups.
        
        An exception is raised if not sucessful.
        """
        try:
            res = self._sendCommand(GLSCommands.CO_GROUP)    # for test - request list of available groups
        except Exception, e:
            if isinstance(e, GLSException.GLSException):
                raise e
            raise GLSException.GLSException("Connection to server could not be established.", GLSException.EC_UNKNOWN_ERROR, "Underlaying error: " + str(e))

    def requestGroups(self):
        """
        Requests a list of available groups from the server.
        
        @return: The list of available groups as returned from the server
        @rtype: C{List} of C{String}
        """
        try:
            res = self._sendCommand(GLSCommands.CO_GROUP)    
            ret = []
            for item in res:
                if item[0]!= GLSCommands.RE_FINISHED:
                    ret.append(item[1:])
            return ret
        except Exception, e:
            if isinstance(e, GLSException.GLSException):
                raise e
            raise GLSException.GLSException("Could not request groups from server.", GLSException.EC_UNKNOWN_ERROR, "Underlaying error: " + str(e))
        
    def joinGroup(self, groupName):
        """
        Makes an attempt to join a group on the server.
        
        Raises an L{GLSException.GLSException} if the attempt was not sucessful.
        
        @param groupName: Name of the group, which shall be joined
        @type groupName: C{String}
        """
        try:
            res = self._sendCommand(GLSCommands.CO_GROUP + groupName) 
        except Exception, e:
            if isinstance(e, GLSException.GLSException):
                raise e
            raise GLSException.GLSException("Could not join group on server.", GLSException.EC_UNKNOWN_ERROR, "Underlaying error: " + str(e))

    def _packFloatsInString(self, floats, separator = ","):
        """
        Supporting function to pack together a bunch of floats in a string.
        
        @param floats: Numbers to be packed
        @type floats: C{List} of C{Float}
        @param separator: Character to put between two numbers
        @type separator: C{String}
        @return: String containing all the given numbers
        @rtype: C{String}
        """
        st = ""
        for nr in floats:
            st += str(nr) + separator
        st = st[:len(st) - len(separator)]
        return st
        
    def _extractFloatsFromString(self, st, separator = ","):
        """
        Supporting function to unpack a bunch of floats from a string.
        
        All items from the list, which cannot be transformed into floats, will be returned as strings within the list.
        
        @param st: String containing the numbers
        @type st: C{String}
        @param separator: Character to put between two numbers
        @type separator: C{String}
        @return: List containing the unpacked numbers
        @rtype: C{List} of C{Float}
        """
        items = st.split(separator)
        ret = []
        for item in items:
            try:
                ret.append(float(item))
            except ValueError:
                ret.append(item)
        return ret
        

    def sendPosition(self, position):
        """
        Sends a GPS position to the server.
        
        @param position: GPS position to be sent to the server
        @type position: L{PythonGLS.Position}
        """
        numbers = [position.getLatitude(), position.getLongitude(), position.getAltitude(), position.getSpeed(), position.getBearing()]
        posStr = self._packFloatsInString(numbers)
        try:
            res = self._sendCommand(GLSCommands.CO_POSITION + posStr) 
        except Exception, e:
            if isinstance(e, GLSException.GLSException):
                raise e
            raise GLSException.GLSException("Could not send position to server.", GLSException.EC_UNKNOWN_ERROR, "Underlaying error: " + str(e))

    def sendWaypoint(self, waypoint):
        """
        Sends a waypoint to the server.
        
        @param waypoint: Waypoint to be sent to the server
        @type waypoint: L[PythonGLS.Waypoint}
        """
        numbers = [waypoint.getLatitude(), waypoint.getLongitude(), waypoint.getAltitude()]
        wpStr = self._packFloatsInString(numbers)
        try:
            res = self._sendCommand(GLSCommands.CO_WAYPOINT + wpStr + "," + waypoint.getName()) 
        except Exception, e:
            if isinstance(e, GLSException.GLSException):
                raise e
            raise GLSException.GLSException("Could not send waypoint to server.", GLSException.EC_UNKNOWN_ERROR, "Underlaying error: " + str(e))
        
    def requestPositions(self):
        """
        Requests positions of others from the server.
        
        @return: List of position of others received from the server in dictionary format. The key is the name of the "other", the value is the position.
        @rtype: C{Dict} of C{String} | L{PythonGLS.Position}
        """
        try:
            res = self._sendCommand(GLSCommands.CO_POSITION)    
            ret = {}
            for item in res:
                if item[0]!= GLSCommands.RE_FINISHED:
                    line = item[1:]
                    tokens = self._extractFloatsFromString(line)
                    ret[tokens[0]] = Position(tokens[1],tokens[2],tokens[3],tokens[4],tokens[5])
            return ret
        except Exception, e:
            if isinstance(e, GLSException.GLSException):
                raise e
            raise GLSException.GLSException("Could not request positions of others from server.", GLSException.EC_UNKNOWN_ERROR, "Underlaying error: " + str(e))
        
    def requestWaypoints(self):
        """
        Requests waypoints of others from the server.

        @return: List of waypoints of others received from the server in dictionary format. The key is the name of the "other", the value is the waypoint.
        @rtype: C{Dict} of C{String} | L{PythonGLS.Waypoint}
        """
        try:
            res = self._sendCommand(GLSCommands.CO_WAYPOINT)    
            ret = {}
            for item in res:
                if item[0]!= GLSCommands.RE_FINISHED:
                    line = item[1:]
                    tokens = self._extractFloatsFromString(line)
                    ret[tokens[0]] = Waypoint(tokens[1],tokens[2],tokens[3],tokens[4])
            return ret
        except Exception, e:
            if isinstance(e, GLSException.GLSException):
                raise e
            raise GLSException.GLSException("Could not request positions of others from server.", GLSException.EC_UNKNOWN_ERROR, "Underlaying error: " + str(e))
        
        
