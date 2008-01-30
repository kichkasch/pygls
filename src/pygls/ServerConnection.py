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
        
        @param command: Command to be sent to the server
        @type command: C{String}
        @param initMode: When sending this command the connection is in initialisation mode; meaning, it shall no be checked, whether a connection is establised already
        @type initMode: C{int}
        @return: Received reply from the server. A String in case of a single line reply; an array of strings in case of multi line reply.
        @rtype: C{String} or C{List} of C{String}
        """
        print "Sending %s" %command
        if not self._connected and not initMode:
            self._establishConnection()
        self._s.send(command +'\n')
        data, tmp = self._s.recvfrom(1024)
        data = data[:len(data)-1]   # remove line feed
        print "\tReceived %s" %data
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
        print "Connection attempt for %s." %self._hostName
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((self._hostName, self._port))
        data, tmp = self._s.recvfrom(1024)
        self._serverVersion = data[:len(data)-1]
        
        res = self._sendCommand(GLSCommands.CO_VERSION +self._version, 1)
        if res != GLSCommands.RE_OK:
            raise GLSException.GLSException("Requested version of GLS specification not supported by server.", GLSException.EC_VERSION_NOT_SUPPORTED, "Version mismatch - server understands %s; client wants to speak %s" % (self._serverVersion, self._version))
        
        
        if self._password:
            comm = GLSCommands.CO_LOGIN + self._clientName + "," + self._password
        else:
            comm = GLSCommands.CO_LOGIN + self._clientName
        res = self._sendCommand(comm, 1)
        if res != GLSCommands.RE_OK:
            raise GLSException.GLSException("Authentication error when connecting to GLS server.", GLSException.EC_AUTHENTICATION_ERROR, "The client (%s) could not be authenticated on the server." %(self._clientName))
        
        res = self._sendCommand(GLSCommands.CO_DEVICE + self._deviceName, 1)  
        if res != GLSCommands.RE_OK:
            raise GLSException.GLSException("Device not accepted by server.", GLSException.EC_UNKNOWN_ERROR, "The server did not accept the device (%s) for the connection establishment." %(self._deviceName))

        self._connected = 1
        print "Connected to %s " %self._hostName
        
        
    def _closeConnection(self):
        """
        Closes down the socket to the server.
        """
        if not self._connected:
            return
        print "Closing connection to GLS server"
        self._sendCommand(GLSCommands.CO_QUIT)
        self._s.close()
        print "\tConnection closed"

        
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

