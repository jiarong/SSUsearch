#! /usr/bin/ python
# make group file for mcclust and mothur \
#   mcclust does not take muti seq files when \
#     seqs in aligned fasta format \
#by gjr; Jan 30, 12

import sys
import os
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed

'''
usage: python <thisFile><sampleFile><seqFile1><seqFile2>...
'''

fw = open(sys.argv[1], 'w')
lis = []
if os.path.isdir(sys.argv[2]):
    print >> sys.stderr, 'input is dir..'
    assert len(sys.argv) == 3, 'use the seq file dir'
    dir = sys.argv[2]
    fNames = os.listdir(sys.argv[2]) 
    for fName in fNames:
        f = dir.rstrip('/')+'/'+fName
        lis.append(f)

else:
    print >> sys.stderr, 'input is list of files..'
    lis = sys.argv[2:]


for f in lis:
    for n, record in enumerate(screed.open(f)):
        name = record['name']
        fw.write('%s\t%s\n' %(name, os.path.basename(f)))
