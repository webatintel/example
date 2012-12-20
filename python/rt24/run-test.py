import os
import re
import util
import time
import random
import sys
import urllib2
import shutil

category = ''
build = 0
testMethod = 'qa'

def downloadBinary():
    os.chdir('binary/' + category)
    
    # Download zip file
    zipFile = build + '.zip'
    if not os.path.exists(build + '.zip'):
        util.dlog('Downloading ' + category + '/' + build)
        url = util.urlPrefix + category + '/' + build + '/chrome-win32.zip'
        f = urllib2.urlopen(url);
        data = f.read()
        with open(zipFile, 'wb') as code:
            code.write(data)
        util.dlog('Download ' + category + '/' + build + ' finished.')  

    if not os.path.exists(zipFile):
        util.dlog("Download failed")
        os.chdir(sys.path[0])
        return
        
    # Extract zip file
    if os.path.exists(build):
        shutil.rmtree(build)
        
    os.system('unzip ' + build + '.zip')
    os.rename('chrome-win32', build)
    
    # Handle webmark config file
    if testMethod != 'webmark':
        os.chdir(sys.path[0])
        return
        
    configFile = build + '.json'    
    if os.path.exists(configFile):
        os.remove(configFile)
    
    shutil.copyfile(sys.path[0] + '/webmark.json', configFile)
    f = open(configFile)
    lines = f.readlines()
    f.close()
    
    placeHolder = 'placeholder'
    for lineIndex in range(0, len(lines)):
        if re.search(placeHolder, lines[lineIndex]):
            line = lines[lineIndex]
            line = line.replace(placeHolder, os.getcwd() + '/' + build + '/chrome.exe')
            line = line.replace('\\', '/')
            lines[lineIndex] = line
            break
    
    f = open(configFile, "w")
    for line in lines:
        f.write(line)
    f.close() 
    
    os.chdir(sys.path[0])

def updateStatus():
    f = open('status.txt')
    lines = f.readlines()
    f.close()
    
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
    if testMethod == 'webmark':
        os.system('python WebMark/webmark.py binary/' + category + '/' + build + '.json')
    
    command = "python qa/ts-rt24/ts-rt24-testtools/run_qatest/run_qatest.py --type=QATEST-RUN-SLAVE --test-properties={'buildername':'" + category + "-builder','buildnumber':'" + build + "','mastername':'rt24','scheduler':'','slavename':'" + category + "','testcfg':'','restcfg_uri_default':'','testcfg_uri_temp':''}"
    print command
    os.system(command)
    #time.sleep(random.uniform(5, 15))
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
        if testMethod == 'webmark':
            downloadBinary()
        runTest()
        util.atomOp(updateStatus)
    
    if not hasUpdate:
        util.dlog("Has no test to run")
        
    util.unlock(lockRunName)
        
        
