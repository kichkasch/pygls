# Makefile
#
# PythonGLS
# Michael Pilgermann
# michael.pilgermann@gmx.de

#
# global parameters
TITLE=  "PythonGLS"
URL=    "http://www.assembla.com/wiki/show/dZdDzazrmr3k7AabIlDkbG"
API_DOC_DIR=apidoc/

# program names
EPYDOC=/usr/bin/epydoc 
MKDIR=mkdir
RM=rm
PYTHON=python

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

distribution:	
	$(PYTHON) setup.py sdist --formats=gztar,zip
