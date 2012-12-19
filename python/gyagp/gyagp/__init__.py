#!/usr/bin/env python

__version__ = "0.1.0"

def check():
	try:
		import win32api
		print('Module pywin32 has been installed')
	except ImportError:
		print('Module pywin32 has not been installed')