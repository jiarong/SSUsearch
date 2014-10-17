#! /usr/bin/env python
# extract the domain and phylum info from classify.seqs summary
# Jul 18, 11; by gjr

import sys

fp = open(sys.argv[1])

for line in fp:
    lis = line.split()
    if lis[0] == '1':
        print lis[2],'\t','\t',lis[4]
    if lis[0] == '2':
        print '\t',lis[2],'\t',lis[4]
