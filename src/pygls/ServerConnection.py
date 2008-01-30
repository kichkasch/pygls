"""
Python library for GPS Location Sharing - responsible for the connection to the GLS Server.
http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""
import socket

class ServerConnection:
    """
    An instance of this class maintains one connection to the GLS server.
    
    It may be reused for several commands.
    """
    
    def __init__(self, hostName, port, version, clientName, password, deviceName, groupName):
        """
        Constructor
        
        Only stores the given parameters in instance variables. No connection is being established here.
        
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
        
    def _sendComamnd(self, s, command):
        """
        Sends exactly one command to the GLS server.
        
        The command is extended by a line feed before sending. The line feed from the line(s) in the reply
        is / are removed before the value is returned.
        
        @param s: Socket, which shall be used for sending commands
        @type s: L{socket.socket}
        @param command: Command to be sent to the server
        @type command: C{String}
        @return: Received reply from the server. A String in case of a single line reply; an array of strings in case of multi line reply.
        @rtype: C{String} or C{List} of C{String}
        """
        s.send(c +'\n')
        data, tmp = s.recvfrom(1024)
        data = data[:len(data)-1]   # remove line feed
        return data
    
    def _sendCommands(self, commands):
        """
        Sends an array of commands to the GLS server (line by line).
        
        Each item in the lists is sent to the GLS server. Before sending, a line feed is appended.
        
        Received results are stored in a dictionary - the list of commands makes up the keys in the dictionary,
        the received results are the values. (Values might either be a simple string or a list of strings in case of
        several lines are sent back by the server for a command.
        
        @param commands: Commands to be send to the GLS server. They must not contain the line feed.
        @type commands: C{List}
        @return: Received results for all command
        @rtype: C{Dict} of C{String} and C{String} | C{List}
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "Connection attempt for %s." %host
        s.connect((host, port))
        print "Connected to %s " %host
        data, tmp = s.recvfrom(1024)
        self._serverVersion = data

        results = {}
        for item in commands:
            result = self._sendCommand(s, item)
            results[item] = result
        s.close()
        return results
        
    def testConnection(self):
        """
        Tests connectivity to the GLS server using the parameters stored for the instance.
        
        Sends a sequence of commands V, N, D and Q to the server and evaluates the replies. If a password
        is available for this connection, it is used - if no password is available, the connection is being established
        without providing one.
        
        An exception is raised if the connection cannot be established.
        """
        commands =  []
        commands.append("V" +self._version)
        if self._password:
            commands.append("N" + self._clientName + "," + self._password)
        else:
            commands.append("N" + self._clientName)
        commands.append("D" + self._deviceName)
        commands.append("Q")

        results = self._sendCommands(commands)
    
