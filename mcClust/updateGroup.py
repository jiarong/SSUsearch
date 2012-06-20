#! /usr/bin python
#  cutRegion.py will delete some seqs \
#     so the number seqs in .fasta and .groups are not the same
# by gjr; Feb 22, 11

import sys
import os
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed
from screed import fasta
import re

'''
usage: python <thisFile><file.fasta><file.groups><newFile.groups>
'''

fSeq = sys.argv[1]
fGroup = sys.argv[2]
fw = open(sys.argv[3], 'wb')

d = {}
st =set()
cnt = 0
for n, record in enumerate(screed.open(fSeq)):
    name = record['name']
    seq = record['sequence']
    st.add(name)
    if n%10000 == 0:
        print '%d seqs scanned ..' %(n+1)

for line in open(fGroup):
    line = line.rstrip()
    key, value = line.split('\t')
    if key not in st:
        cnt += 1
        continue
    print >> fw, line

print '%d seqs do not pass len cutoff by regionCut.py' %(cnt)
print 'Group file updated in %s' %(sys.argv[3])
