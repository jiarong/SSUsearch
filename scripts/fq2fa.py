#! /usr/bin/python
# convert fastq to fasta
# by gjr; Oct 4, 11

"""
Convert fastq to fasta

% python fq2fa.py <file.fastq> <file.fasta> 
"""

import sys, os
import screed

def main():
    if len(sys.argv) != 3:
        print >> sys.stderr, 'Usage: python %s <file.fastq> <file.fasta>'\
                               %(os.path.basename(sys.argv[0]))
        sys.exit(1)

    f = sys.argv[1]
    fout = sys.argv[2]
    fw = open(fout, 'wb')

    for n, record in enumerate(screed.open(f)):
        name = record['name']
        seq = record['sequence']
        print >> fw, '>%s\n%s' %(name, seq)

    #print (n+1), 'fasta seqs written'
    fw.close()

if __name__ == '__main__':
    main()
