"""
Setup module for PythonGLS

Python library for GPS Location Sharing.

This module should be started for installation of pygls as a python site package. This way
it may used used easily with any application afterwards.

http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

@author: Michael Pilgermann
@contact: mailto:michael.pilgermann@gmx.de
@contact: http://www.kichkasch.de
@license: GPL (General Public License)

@var version: Current version of PythonGLS
@type version: C{String}
"""


from distutils.core import setup

global version
version = "0.1.3"

if __name__ == "__main__":
    setup (
        name = "pygls",
        version = version,
        description = "pygls - linking gps devices together",
        author = "Michael Pilgermann",
        author_email = "michael.pilgermann@gmx.de",
        url = "http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG",
        package_dir = {'pygls': '.'},
        packages = ["pygls"]
        )
