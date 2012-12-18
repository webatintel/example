import os
import re
import util
import time
import random
import sys

category = ''
build = 0

def updateStatus():
    file = open('status.txt')
    lines = file.readlines()
    file.close()
    
    categoryPattern = re.compile("category=(.*)")
    queuePattern = re.compile("queue=(.*)")

    for lineIndex in range(0, len(lines)):
        line = lines[lineIndex]
        if categoryPattern.search(line):
            m = categoryPattern.search(line)
            categoryCurrent = m.group(1)
        elif queuePattern.search(line):
            if categoryCurrent != category:
                continue
            m = queuePattern.search(line)
            queue = str.strip(m.group(1))
            builds = queue.split(',')
            for buildIndex in range(0, len(builds)):
                if re.match(str(build) + '\(r\)', builds[buildIndex]):
                    builds[buildIndex] = str(build) + '(f)'
                    break
            lines[lineIndex] = util.queuePrefix + ','.join(builds) + '\n'
            break
    
    util.writeStatus(lines)

def runTest():
    util.dlog('runTest begins. category=' + category + ' build=' + str(build))
    time.sleep(random.uniform(5, 15))
    util.dlog('runTest ends.   category=' + category + ' build=' + str(build))
    

def getAvailable():
    global category
    global build

    file = open('status.txt')
    lines = file.readlines()
    file.close()
    
    categoryPattern = re.compile("category=(.*)")
    queuePattern = re.compile("queue=(.*)")

    for lineIndex in range(0, len(lines)):
        line = lines[lineIndex]
        if categoryPattern.search(line):
            m = categoryPattern.search(line)
            category = m.group(1)
        elif queuePattern.search(line):
            m = queuePattern.search(line)
            queue = str.strip(m.group(1))

            if not queue:
                category = ""
                continue

            builds = queue.split(',')
            for buildIndex in range(0, len(builds)):
                if re.match('^\d+$', builds[buildIndex]):
                    build = builds[buildIndex]
                    builds[buildIndex] += '(r)'
                    lines[lineIndex] = util.queuePrefix + ','.join(builds) + '\n'
                    util.writeStatus(lines)
                    return True

    return False
                    
if __name__ == '__main__':
    os.chdir(sys.path[0])
    util.dlog('Start to run test')
    
    lockRunName = 'lock-run'
    if util.hasLock(lockRunName):
        util.dlog("It's already running")
        quit()

    util.lock(lockRunName)

    hasUpdate = False
    while util.atomOp(getAvailable):
        hasUpdate = True
        runTest()
        util.atomOp(updateStatus)
    
    if not hasUpdate:
        util.dlog("Has no test to run")
        
    util.unlock(lockRunName)
        
        
