README for PythonGLS

Michael Pilgermann
Email to: michael.pilgermann@gmx.de
Licensed under the Genreal Public License (GPL) 

http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG


Content
1. Introduction
2. Installation
3. Usage
...


1. Introduction
---------------
...



2. Installation
---------------
Requirements
- Python (>=2.5) must be installed.

Step by step
- Unpack the archive
    * tar xzvf pygls-0.1.tar.gz
- Change into directory pygls
    * cd pygls
- Run Makefile with option install
    * make install  (you must have root privileges: e.g. sudo make install)

Off you go. The library is installed.


3. Usage
--------
PythonGLS is a library. You may use it from within your Python code to access functionality
from the GPS Location Sharing project. You have to import the moduel (pygls); afterwards you
have access to members of this package.

Here an example:

import pygls
