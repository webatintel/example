# -*- coding: utf-8 -*- 
import os
import sys


### Path of script ###
'''
Directory structure:
D:
©À©¤gytemp
©¦  ©¦  main.py
©¦  ©À©¤test
©¦  ©¦  ©¦  path.py 

Execute d:\gytemp\main.py, and it will call test/path.py that includes following commands
'''
os.getcwd() # D:\
sys.path[0] # D:\gytemp
sys.argv[0] # D:\gytemp\main.py
os.path.split(os.path.realpath(__file__))[0] # D:\gytemp\test

### Press enter, then exit ###
raw_input("Press <enter>")



