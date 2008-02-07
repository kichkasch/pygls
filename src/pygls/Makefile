# Makefile
#
# PythonGLS
# Michael Pilgermann
# michael.pilgermann@gmx.de

#
# Special feature - this Makefile can create a IPKG package (special format for embedded devices)
# you have to download the "ipkg-build.sh" beforehand (website http://www.oesf.org/index.php?title=IPKG_Howto)
# and place it in any folder, which is in your PATH environment

#
# global parameters
TITLE=  "PythonGLS"
URL=    "http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG"
API_DOC_DIR=apidoc/
IPKG_DIR = binPackage
IPKG_CONTROL_FILE = control
IPKG_CONTROL_DIR = $(IPKG_DIR)/CONTROL
DIST_DIR = dist

# program names
EPYDOC=/usr/bin/epydoc 
MKDIR=mkdir
RM=rm
PYTHON=python
IPKG_BUILD=ipkg-build.sh

all: docs

$(API_DOC_DIR):
	$(MKDIR) $(API_DOC_DIR)

api-docs:	$(API_DOC_DIR)
	$(EPYDOC) --html --inheritance listed -o $(API_DOC_DIR) --name $(TITLE) --url $(URL) --css blue *.py
#	$(EPYDOC) --html --inheritance listed -o $(API_DOC_DIR) --name $(TITLE) --url $(URL) --css blue --no-private *.py

docs:   api-docs

install:
	$(PYTHON) setup.py install

clean:
	$(RM) *.pyc pygls/*.pyc

$(IPKG_DIR):
	$(MKDIR) $(IPKG_DIR)

$(IPKG_CONTROL_DIR): $(IPKG_DIR)
	$(MKDIR) $(IPKG_CONTROL_DIR)
	
distribution:	
	$(PYTHON) setup.py sdist --formats=gztar,zip
	
bindistribution: $(IPKG_DIR) $(IPKG_CONTROL_FILE) $(IPKG_CONTROL_DIR)
	$(RM) -f $(DIST_DIR)/*linux*
	$(PYTHON) setup.py bdist
	tar --directory $(IPKG_DIR) -xzvf  $(DIST_DIR)/*linux* 
	cp $(IPKG_CONTROL_FILE) $(IPKG_CONTROL_DIR)
	$(IPKG_BUILD) "$(IPKG_DIR)" "$(DIST_DIR)"
	$(RM) -rf $(IPKG_DIR)
