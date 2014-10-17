#! /usr/bin python
# split fasta seqs (after deunique.seqs) base on group file (.groups file from mothur)
#   in case of split.groups does not work, cutRegion.py will delete some seqs \
#     so the number seqs in .fasta and .groups are not the same
# by gjr; Feb 22, 11

import sys
import os
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed
from screed import fasta
import re

'''
usage: python <thisFile><file.fasta><file.groups>
'''

fSeq = sys.argv[1]
fGroup = sys.argv[2]

d = {}
for line in open(fGroup):
    line = line.rstrip()
    key, value = line.split('\t')
    d[key] = value

samples = set(d.values())
d2 = {}
d3 = {}
for s in samples:
    sw = open(s, 'w')
    d2[s] = sw
    d3[s] = 0          # for counting seqs in samples
for n, record in enumerate(screed.open(fSeq)):
    name = record['name']
    seq = record['sequence']
    s = d[name]
    fw = d2[s] 
    d3[s] += 1
    print >> fw, '>%s\n%s' %(name, seq)
    if n%10000 == 0:
        print '%d seqs scanned ..' %(n+1)

print 'sample\tseqNumber'
for s in d3:
    print '%s\t%d' %(s, d3[s])

print 'splitGroup done..'
