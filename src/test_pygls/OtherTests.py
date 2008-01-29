"""
Test program for
Python library for GPS Location Sharing.
http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

Simple atomic tests (conntectivity and so on).

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""

#host_testserver = "home.schuring.eu"
host_testserver = "localhost"
port_testserver = 47757

def testServerConnectivity(host, port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Connection attempt for %s." %host
    s.connect((host, port))
    print "Connected to %s " %host
    data, tmp = s.recvfrom(1024)
    print 'Received', repr(data)
    s.send('V2\n')
    data, tmp = s.recvfrom(1024)
    print 'Received', repr(data)
    s.close()
    
testServerConnectivity(host_testserver, port_testserver)
