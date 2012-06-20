#! /usr/bin/env python
# add reverse complement to DNA seq fasta file, just for hmmer DNA search
# Jul 13, 11; by gjr

import sys
import string
import time
import os

#insert the path of screed
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed

transTable=string.maketrans('ATGC','TACG')

def reverseComp(seq):
    temp = seq.translate(transTable)
    rc = temp[::-1]
    return rc 

if __name__ == '__main__':
    '''
    make sure the seq files are in scratch
    '''
    start = time.time()
    f = sys.argv[1]
    fName = os.path.basename(f)
    fw = open(fName+'.RCaddedForHmmer', 'w')
    for n, record in enumerate(screed.open(f)):
        name = record['name']
        seq = record['sequence']
        seq_rc = reverseComp(seq)
        print >> fw, '>%s\n%s\n>%s\n%s' %(name, seq, name+'-RC-', seq_rc)
        if n%10000 == 0:
            print n+1, 'seqs processed..'

    end = time.time()
    print n, 'sequences processed in total'
    print 'took %d seconds' %(end-start)
