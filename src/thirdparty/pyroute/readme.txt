README for pygls extension module for pyroute
---------------------------------------------

pyroute_pygls.py is a Python module, intended to be used as an extension for the pyroute gps program
based on OpenSreetMap.

GLS Website:
http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG

Pyroute Website:
http://wiki.openstreetmap.org/index.php/Pyroute

It is running as a thread in the background of pyroute. Updates of gps locations (from the GLS server) are
pulled periodically. Update intervalls and connection data has to be provided in a configuration file. For
visualisation of locations from GLS the already in pyroute implemented mechanism of poi (point of interest)
is used. The class has been derived from the corresponding class and, this way, integrates easily in the
infrastructure.

Notes for activation:
- Place the module (pyroute_pygls.py) in the pyroute program folder
- Place the settings file for pyroute_pygles named "glssettings.txt" in the subfolder "Setup" of the pyroute program folder and apply your settings
- Apply changes to the GUI-module for pyroute in order to make this extension running
    * import the new module by inserting the following line at around line 70
        - from pyroute_pygls import pyglsPoiModule
    * Activate the module by inserting a new line inside the function loadModules (line 102)
        - self.modules['poi']['gls'] = pyglsPoiModule(self.modules)
    * just before the line with the command gtk.main() (around line 360) enable proper threading for GTK by inserting the following line
        - gtk.gdk.threads_init()
    Alternatively, you can use the modified gui.py coming with this module and place it in the pyroute program folder
