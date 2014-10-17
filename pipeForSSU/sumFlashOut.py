#! /usr/bin python
# summarize the merged result of flash 
# by gjr; Oct 1, 11

'''
usage: python <thisFile><prefix><fileDir>
'''
import sys
import os
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed

prefix = sys.argv[1]
dir = os.path.abspath(sys.argv[2])
merged = prefix+'.extendedFrags.fastq'
notCombined = prefix+'.notCombined_1.fastq'

mergedCnt = 0
for record in screed.open(dir+'/'+merged):
    mergedCnt += 1

notCombinedCnt = 0
for record in screed.open(dir+'/'+notCombined):
    notCombinedCnt += 1

print 'In sample %s:' %(prefix)
print '%d pairs are merged' %(mergedCnt)
print '%d pairs are notCombined' %(notCombinedCnt)
