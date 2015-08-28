#! /usr/bin/python
# remove gaps - or . in aligned fasta file
# by gjr; Aug 12, 11 

"""
Remove gaps in aligned sequence file

% python remove-gap.py <gaped.file> <nogap.file>

"""
import sys
import screed
from screed import fasta

def main():

    if len(sys.argv) != 3:
        print >> sys.stderr, 'Usage: python %s <gaped.file> <nogap.file>' \
                                 %sys.argv[0]
        sys.exit(1)

    input_file = sys.argv[1]
    fw = open(sys.argv[2], 'wb')

    for record in screed.open(input_file):
        name = record['name']
        if name == 'ReFeReNcE':
            continue
        seq = record['sequence']
        desc = record['description']

        seq1 = seq.replace('-','').replace('.','')
        lis = seq1.split()
        seq1 = ''.join(lis)
        print >> fw, '>%s  %s\n%s' %(name, desc, seq1)

if __name__ == '__main__':
    main()
