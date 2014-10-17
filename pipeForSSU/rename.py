#! /bin/python
# rename file names

import sys
import os

cnt = 0
for line in sys.stdin:
    old = line.rstrip()
    new = old.replace('-','')
    os.rename(old, new)
    cnt += 1

print 'done ..'
print '%d files changed' %(cnt)
