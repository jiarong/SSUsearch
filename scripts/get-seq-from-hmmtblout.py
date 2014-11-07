#! /usr/bin/env python
# parse tabular output from HMMER
# by gjr; May 5, 11

import sys
import os
import screed

N = 10
M = None

def getDict_domain(fp):
    '''
    still need to verify the position of item in list
    '''
    d = {}
    for line in fp:
        if line.startswith('#'):
            continue
        line = line.strip()
        lis = line.split()
        name = lis[2]
        e_val = float(lis[5])
        bit = float(lis[6])
        if M:
            if bit > M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit

    return d

def getDict_wholeSeq(fp):
    d = {}
    for line in fp:
        if line.startswith('#'):
            continue
        line = line.strip()
        lis = line.split()
        name = lis[0]
        e_val = float(lis[4])
        bit = float(lis[5])
        if M:
            if bit > M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit

    return d

def main():
    '''
    python <thisFile><hmmtblout><seqDB><targetGene.fa>
    extract the hmm hits seq from shotgun data
    '''
    if len(sys.argv) != 4:
        mes = 'Usage: python %s <hmmtblout><seqdb><target_gene.fa>'
        print >> sys.stderr, mes %(os.path.basename(sys.argv[0]))
        sys.exit(1)

    fp = open(sys.argv[1])
    fw = open(sys.argv[3], 'wb')
    d = getDict_wholeSeq(fp)
    print >> sys.stderr, '%d hits at %s cutoff' %(len(d), str(N))
    if len(d) == 0:
        print >> sys.stderr,'no hmmhits for %s' %(sys.argv[1])
        sys.exit(1)
    
    for n, record in enumerate(screed.open(sys.argv[2])):
        name = record['name']
        if name in d:
            seq = record['sequence']
            l = d.pop(name)
            print >> fw, '>%s\n%s' %(name, seq)
    
    fw.close()

if __name__ == '__main__':
    main()

