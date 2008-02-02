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
        
    def __str__(self):
        """
        Computes a string representation of the content of this position instance.
        
        This representation is made up by the latitude, the longitude and the altitude.
        
        @return: String representation of object content
        @rtype: C{String}        
        """
        return "Position: " + str(self._latitude) + "," + str(self._longitude) + "," + str(self._altitude)
        
    def getLatitude(self):
        """
        GETTER
        """
        return self._latitude

    def getLongitude(self):
        """
        GETTER
        """
        return self._longitude

    def getAltitude(self):
        """
        GETTER
        """
        return self._altitude

    def getSpeed(self):
        """
        GETTER
        """
        return self._speed

    def getBearing(self):
        """
        GETTER
        """
        return self._bearing

    
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

    def __str__(self):
        """
        Computes a string representation of the content of this waypoint instance.
        
        This representation is made up by the name, the latitude, the longitude and the altitude.
        
        @return: String representation of object content
        @rtype: C{String}        
        """
        return "Waypoint "  + self._name + ": " + str(self._latitude) + "," + str(self._longitude) + "," + str(self._altitude)
        
    def getLatitude(self):
        """
        GETTER
        """
        return self._latitude

    def getLongitude(self):
        """
        GETTER
        """
        return self._longitude

    def getAltitude(self):
        """
        GETTER
        """
        return self._altitude

    def getName(self):
        """
        GETTER
        """
        return self._name
