import os
import re
from httplib import BadStatusLine
import urllib2
import time
import util
import sys

lines = ""
hasUpdate = False

def updateStatus():
    if not hasUpdate:
        util.dlog('Has no update')
        return

    util.writeStatus(lines)

def checkUpdate():
    global lines
    global hasUpdate

    urlPrefix = "http://wrt-buildbot.bj.intel.com/snapshots/"

    file = open('status.txt')
    lines = file.readlines()
    file.close()
    
    categoryPattern = re.compile("category=(.*)")
    startPattern = re.compile("start=(.*)")
    queuePattern = re.compile("queue=(.*)")

    for lineIndex in range(0, len(lines)):
        line = lines[lineIndex]
        if categoryPattern.search(line):
            m = categoryPattern.search(line)
            category = m.group(1)
        elif startPattern.search(line):
            m = startPattern.search(line)
            start = m.group(1)
            startDate = time.strptime(start, '%Y-%m-%d')
        elif queuePattern.search(line):
            m = queuePattern.search(line)
            queue = str.strip(m.group(1))
            
            # Get the previous max build number
            if not queue:
                maxBuildNumber = 0
            else:
                oldBuilds = queue.split(',')
                numberPattern = re.compile("(\d+)")
                m = numberPattern.search(oldBuilds[0])
                maxBuildNumber = m.group(1)

            # Ensure startDate is valid
            if not start:
                startDate = time.strptime('20120101', '%d-%b-%Y')
                
            # Get the new queue needs to be updated
            url = urlPrefix + category
            try:
                u = urllib2.urlopen(url)
            except BadStatusLine:
                start = ""
                continue
            html = u.read()
            
            buildPattern = re.compile('href="(\d+).*(\d\d-.*-\d+ \d+:\d+)')
            builds = buildPattern.findall(html)
            newQueue = ""
            for build in reversed(builds):
                buildNumber = build[0]
                if buildNumber <= maxBuildNumber:
                    break
                
                buildDate = time.strptime(build[1], '%d-%b-%Y %H:%M')
                if buildDate <= startDate:
                    break
                
                if not newQueue:
                    newQueue = str(buildNumber)   
                else:
                    newQueue = newQueue + "," + str(buildNumber)
            
            # Update the queue
            if not newQueue:
                continue
            hasUpdate = True
            if not queue:
                line = "queue=" + newQueue
            else:
                line = "queue=" + newQueue + "," + queue
            lines[lineIndex] = line + '\n'
            util.dlog('Has an update: category=' + category + ' ' + line)
    
            
if __name__ == '__main__':  
    os.chdir(sys.path[0])
    util.dlog('Start to check update')
    checkUpdate()
    util.atomOp(updateStatus)