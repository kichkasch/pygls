"""
Python library for GPS Location Sharing - collection of constants for commands and replies for the GLS server.

All constants starting with "co" are commands sent from the client to the server. All constants starting with
"re" are replies, which are sent back from the server to the client in reply to a request.

http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)

@var CO_VERSION: Command string of protocol - request version.
@type CO_VERSION: C{String}
@var CO_LOGIN: Command string of protocol - login attempt.
@type CO_LOGIN: C{String}
@var CO_DEVICE: Command string of protocol - submit device information.
@type CO_DEVICE: C{String}
@var CO_POSITION: Command string of protocol - submit or request position information.
@type CO_POSITION: C{String}
@var CO_WAYPOINT: Command string of protocol - submit or request waypoint information.
@type CO_WAYPOINT: C{String}
@var CO_GROUP: Command string of protocol - enter group or request group information.
@type CO_GROUP: C{String}
@var CO_QUIT: Command string of protocol - shut down connection.
@type CO_QUIT: C{String}

@var RE_OK: Command reply from server of protocol - OK, sucessful processed last request.
@type RE_OK: C{String}
@var RE_CHANGE: Command reply from server of protocol - processing not sucessful because of business rules.
@type RE_CHANGE: C{String}
@var RE_ERROR: Command reply from server of protocol - error, due to validation rules.
@type RE_ERROR: C{String}
@var RE_GROUP: Command reply from server of protocol - sending of a group.
@type RE_GROUP: C{String}
@var RE_POSITION: Command reply from server of protocol - sending position of a client.
@type RE_POSITION: C{String}
@var RE_WAYPOINT: Command reply from server of protocol - sending a waypoint of a client.
@type RE_WAYPOINT: C{String}
@var RE_FINISHED: Command reply from server of protocol - a sequence was finished.
@type RE_FINISHED: C{String}
@var RE_QUIT: Command reply from server of protocol - server is closing connection.
@type RE_QUIT: C{String}
"""

# Commands
CO_VERSION = "V"
CO_LOGIN = "N"
CO_DEVICE = "D"
CO_POSITION = "P"
CO_WAYPOINT = "W"
CO_GROUP = "G"
CO_QUIT = "Q"


# Replies
RE_OK = "K"
RE_CHANGE = "C"
RE_ERROR = "E"
RE_GROUP = "G"
RE_POSITION = "P"
RE_WAYPOINT = "W"
RE_FINISHED = "F"
RE_QUIT = "Q"
