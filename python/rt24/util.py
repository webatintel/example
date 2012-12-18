import os
import re
import time

queuePrefix = 'queue='

debugMode = 0

def dlog(str):
    if not debugMode:
        return
        
    logFile = open('log.txt', 'a')
    logFile.write(time.strftime('%Y-%m-%d %X', time.localtime(time.time())) + '    ' + str + '\n')
    logFile.close()

def writeStatus(lines):
    f = open("status.txt", "w")
    for line in lines:
        f.write(line)
    f.close()     

def hasLock(pattern):
    lockPattern = re.compile(pattern)
    files = os.listdir(os.getcwd())
    for file in files:
        if lockPattern.search(file):
            return True

    return False
    
def lock(name):
    f = open(name, 'w')
    f.close()
    
def unlock(name):
    os.remove(name)
    
def atomOp(function, *args):
    lockName = 'lock-status'
    for i in range(3):
        if hasLock(lockName):
            print("A lock exists!")
            time.sleep(10)
        else:
            lock(lockName)
            ret = function(*args)
            unlock(lockName)
            return ret
    
    return False