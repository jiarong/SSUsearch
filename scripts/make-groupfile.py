#! /usr/bin/ python
# make group file for mcclust (called sample file)  and mothur
# mcclust does not take muti seq files when seqs in aligned fasta format
# by gjr; Jan 30, 12

import sys
import os

import screed

def main():
    '''
    usage: python <thisFile><sampleFile><seqFile1><seqFile2>...
    '''
    if len(sys.argv) < 3:
        mes = 'Usage: python {} <seq1> <seq2> ..'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    fw = open(sys.argv[1], 'wb')
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
            fname = os.path.basename(f)
            group = fname.split('.',1)[0]
            fw.write('{}\t{}\n'.format(name, group))

if __name__ == '__main__':
    main()
