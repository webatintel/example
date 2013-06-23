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

### Mouse Simulation ###
import win32api, win32con
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


