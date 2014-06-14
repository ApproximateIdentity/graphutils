# simple makefile to simplify repetetive build env management tasks under posix

# caution: testing won't work on windows, see README

PYTHON ?= python
UNITTEST ?= unittest

TESTDIR=graphutils/tests

all: install

# First install with pip
install: clean
	$(PYTHON) setup.py sdist
	pip install dist/*

# Reinstall with pip
reinstall: clean
	pip uninstall graphutils
	$(PYTHON) setup.py sdist
	pip install dist/*

uninstall:
	pip uninstall graphutils

clean:
	$(PYTHON) setup.py clean --all
	rm -rf dist

test:
	$(PYTHON) -m $(UNITTEST) discover -s $(TESTDIR) -v

code-analysis:
	flake8 graphutils | grep -v __init__ | grep -v external
	pylint -E -i y graphutils/ -d E1103,E0611,E1101
