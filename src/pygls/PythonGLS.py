"""
Python library for GPS Location Sharing - entry point to library.

http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)
"""

class Position:
    """
    GPS Position
    
    @ivar _latitude: Latitude of the GPS position
    @type _latitude: C{float}
    @ivar _longitude: Longitude of the GPS position
    @type _longitude: C{float}
    @ivar _altitude: Altitude of the GPS position
    @type _altitude: C{float}
    @ivar _speed: Speed of the GPS position
    @type _speed: C{float}
    @ivar _bearing: Bearing of the GPS position
    @type _bearing: C{float}
    """

    def __init__(self, latitude, longitude, altitude, speed, bearing):
        """
        Constructor
        """
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._speed = speed
        self._bearing = bearing

    
class Waypoint:
    """
    GPS Waypoint
    
    @ivar _latitude: Latitude of the waypoint
    @type _latitude: C{float}
    @ivar _longitude: Longitude of the waypoint
    @type _longitude: C{float}
    @ivar _altitude: Altitude of the waypoint
    @type _altitude: C{float}
    @ivar _name: Name of the waypoint
    @type _name: C{String}
    """

    def __init__(self, latitude, longitude, altitude, name):
        """
        Constructor
        """
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._name = name
