#! /usr/bin/env python
# parse tabular output from HMMER
# by gjr; May 5, 11

'''
usage: python <thisFile><hmm.out><db><seq.fa>
'''

import sys
import os
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed
from screed import fasta

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

if __name__ == '__main__':
    if 0:
        fp = open(sys.argv[1])
        N = 1e-10
        d = getDict(fp)
        print '%d hits got at %s cutoff' %(len(d), str(N))
        names = d.keys()
        fw = open(sys.argv[3], 'w')
        for record in fasta.fasta_iter(open(sys.argv[2])):
            name = record['name']
            if name not in names:
                continue
            seq = record['sequence']
            print >> fw, '>%s\n%s' %(name, seq)

    if 0:
        '''
        funGenes hmmHits on multiple samples
        python <thisFile><hmmtbloutDir><table.txt>
        '''
        #N = 1e-6
        hmmOutList = os.listdir(sys.argv[1])
        outFile = open(sys.argv[2], 'w')
        fields = set() #samples
        names = set()  #genes
        d2 = {}
        for f in hmmOutList:
            sample, _, gene, _ = f.split('.')
            fields.add(gene)
            names.add(sample)

        fields = list(fields)
        names = list(names)
        fields.sort()
        names.sort()
        dd = {}
        for sample in names:
            dd[sample] = {}
            
        for f in hmmOutList:
            fp = open(sys.argv[1].rstrip('/')+'/'+f)
            sample, _, gene, _ = f.split('.')
            d = getDict_wholeSeq(fp)
            print '%s-%s: %d hits got at %s cutoff' %(sample, gene, len(d), str(N))
            dd[sample][gene] = len(d)

        header = 'name\t'+ '\t'.join(fields)
        print >> outFile, header
        for sample in names:
            lis = [sample]
            for gene in fields:
                n = str(dd[sample][gene])
                lis.append(n)
            print >> outFile, '\t'.join(lis)


    if 0:
        '''
        extract funGenes hmmHit seqs on muliple genes and multiple samples
        python <thisFile><hmmtbloutDir><seqDir><outDir>
        ###
        NOT useful, too slow
        Need to extract seqs separately
        '''
        #N = 1e-6

        hmmOutList = os.listdir(sys.argv[1])
        fields = set() #gene
        names = set()  #samples
        d2 = {}
        for f in hmmOutList:
            sample, _, gene, _ = f.split('.')
            fields.add(gene)
            names.add(sample)

        fields = list(fields)
        names = list(names)
        fields.sort()
        names.sort()
        dd = {}
        for sample in names:
            # dict in dict
            dd[sample] = {}
            
        for f in hmmOutList:
            fp = open(sys.argv[1].rstrip('/')+'/'+f)
            sample, _, gene, _ = f.split('.')
            d = getDict_wholeSeq(fp)
            print '%s-%s: %d hits got at %s cutoff' %(sample, gene, len(d), str(N))
            dd[sample][gene] = d.keys()

        os.mkdir(sys.argv[3])
        path = os.path.abspath(sys.argv[3])
        for sample in names:
            print 'working on %s' %(sample)
            proteinFiles = os.listdir(sys.argv[2])
            for file in proteinFiles:
                if sample in file:
                    sample_proteinFile = file

            for n, record in enumerate(screed.open('%s/%s' %(os.path.abspath(sys.argv[2]), sample_proteinFile))):
                name = record['name']
                seq = record['sequence']
                for gene in fields:
                    if len(dd[sample][gene]) == 0:
                        break
                    fw = open('%s/%s.%s.hmmout.fa' %(path, sample, gene), 'w')
                    if name in dd[sample][gene]:
                        print >> fw, '>%s\n%s' %(name, seq)
                        # remove name in list to speed search next round
                        dd[sample][gene].remove(name)

                if (n+1)%1000 == 0:
                    print (n+1), 'seqs scanned..' 


    if 0:
        '''
        split hmmtblout 
        python <thisFile><hmmtbloutDir><newOutDir>
        '''

        N = 100

        hmmOutList = os.listdir(sys.argv[1])

        os.mkdir(sys.argv[2])
        path = os.path.abspath(sys.argv[2])
        for f in hmmOutList:
            fp = open(sys.argv[1].rstrip('/')+'/'+f)
            sample, _, gene, _ = f.split('.')
            d = getDict_wholeSeq(fp)
            print '%s-%s: %d hits got at %s cutoff' %(sample, gene, len(d), str(N))
            dd[sample][gene] = d.keys()


    if 1:
        '''
        python <thisFile><hmmtblout><seqDB><targetGene.fa>
        extract the hmm hits seq from shotgun data
        '''
        import time

        verbose = 0
        if verbose:
            start = time.time()

        fp = open(sys.argv[1])
        fw = open(sys.argv[3], 'w')
        d = getDict_wholeSeq(fp)
        print '%d hits got at %s cutoff' %(len(d), str(N))
        if len(d) == 0:
            print 'no hmmhits for ', sys.argv[1]
            sys.exit(1)

        for n, record in enumerate(screed.open(sys.argv[2])):
            name = record['name']
            if name in d:
                seq = record['sequence']
                l = d.pop(name)
                print >> fw, '>%s\n%s' %(name, seq)
                if verbose:
                    print name, 'detected..'

            '''
            if ((n+1)%10000 == 0 and verbose):
                end = time.time()
                print '%d mins are took for %d seqs' %((end-start)/60, (n+1)) 
            '''

        fw.close()
