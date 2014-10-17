#! /usr/bin/env python
# add reverse complement to DNA seq fasta file, just for hmmer DNA search
# Jul 13, 11; by gjr

import sys
import string
import time
import os
import fileinput

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
    if len(sys.argv) != 3:
        mes = 'Usage: python {} <seqfile> <seqfile-with-rc>'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    start = time.time()
    infile = sys.argv[1]
    outfile = sys.argv[2]

    if outfile == '-':
        fw = sys.stdout
    else:
        fw = open(outfile, 'wb')

    for n, record in enumerate(screed.open(infile)):
        name = record['name']
        seq = record['sequence']
        seq_rc = reverseComp(seq)
        print >> fw, '>%s\n%s\n>%s\n%s' %(name, seq, name+'-RC-', seq_rc)

    end = time.time()
    mes = '{} Million sequences took {} hours to add reverse complement'
    print >> sys.stderr, mes.format((n+1)/1.0e6, (end-start)/3600.0)
