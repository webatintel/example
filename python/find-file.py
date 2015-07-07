# /usr/bin/python

import os

files = os.popen('find /workspace/project/BWS/img -type f -printf "%f\n"').readlines()

for file in files:
    name = file.rstrip('\n')
    ret = os.system('grep -r ' + name + ' /workspace/project/BWS/* >/dev/null')
    if ret != 0:
        print name + " has no reference"
        os.system("git rm /workspace/project/BWS/img/" + name)
