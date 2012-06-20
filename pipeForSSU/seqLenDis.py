#! /usr/bin/ python
# make seq length distribution
# by gjr; Dec 21, 11

import sys
import screed

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if 1:
    '''
    #can deal with seqs with gaps
    '''
    liss = []
    for record in screed.open(sys.argv[1]):
        name = record['name']
        seq = record['sequence']

        seq1 = seq.strip('.').strip('-').replace('-','')
        lis = seq1.split()
        seq1 = ''.join(lis)
        length = len(seq1)
        liss.append(length)

    mi = min(liss)
    ma = max(liss)
    print mi, ma
    #n, bins, batches = plt.hist(liss, (ma-mi)/10, cumulative = False, histtype = 'step')
    n, bins, batches = plt.hist(liss, (ma-mi)/5, cumulative = False)
    plt.xlabel ('Length')
    plt.ylabel ('Number of sequences')
    #plt.grid(1)
    plt.gca().xaxis.grid(False)
    plt.gca().yaxis.grid(True)
    plt.savefig(sys.argv[1]+'.lenDist.png')
    plt.clf()
