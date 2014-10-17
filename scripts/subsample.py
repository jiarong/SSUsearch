# by gjr; May 2, 12

import sys
import os
import random
import glob

import screed

def getRseqsFromBigFile6(fastaFile, newF, N):
    # NOT using indexed screeDB, using fasta.fasta_iter

    ### can get len(db) by count '>' in fastaFile, db not necessary
    lengthDB = 0
    for line in open(fastaFile):
        if line.startswith('>'):
            lengthDB += 1

    #assert lengthDB > N, 'too few sequences in file'
    if lengthDB < N:
        print >> sys.stderr, 'too few sequences in %s' %fastaFile
        return
    outFp = open('%s' %(newF), 'wb')
    l = random.sample(xrange(lengthDB), N)
    ###sort
    l.sort()

    #print 'writing the sampled seqs'
    count = 0
    triger = False
    for n, record in enumerate(screed.open(fastaFile)):
        if len(l) == 0:
            break
        if n == l[0]:
            l.remove(n)
            count += 1
            triger = True
            print >> outFp, '>%s\n%s' %(record['name'],
                                         record['sequence'])
        
        '''
        if n%100 == 0:
            print '%d seqs scanned..' %(n)
        if count%100 == 0 and triger:
            print '%d sequences sampled' %(count)
            triger = False
        '''

def getRseqsFromBigFile5(fastaFile, N):
    # NOT using indexed screeDB, using fasta.fasta_iter
    outFp = open('%s.subSampled' %(fastaFile), 'wb')
    ### can get len(db) by count '>' in fastaFile, db not necessary
    lengthDB = 0
    for line in open(fastaFile):
        if line.startswith('>'):
            lengthDB += 1

    if lengthDB < N:
        print >> sys.stderr, 'too few sequences in %s' %fastaFile
        return
    l = random.sample(xrange(lengthDB), N)
    ###sort
    l.sort()

    print 'writing the sampled seqs'
    count = 0
    triger = False
    for n, record in enumerate(screed.open(fastaFile)):
        if len(l) == 0:
            break
        if n == l[0]:
            l.remove(n)
            count += 1
            triger = True
            print >> outFp, '>%s\n%s' %(record['name'],
                                       record['sequence'])
        '''
        if n%1000 == 0:
            print '%d seqs scanned..' %(n)
        if count%1000 == 0 and triger:
            print '%d sequences sampled' %(count)
            triger = False
        '''

def main():
    if len(sys.argv) != 4:
        mes = 'Usage: python %s <fastaFileDir> N <outdir>'
        print >> sys.stderr,  mes %(sys.argv[0])
        sys.exit(1)
    dir = sys.argv[1].rstrip('/')
    if not os.path.isdir(dir):
        print >> sys.stderr, '%s does not exist' %(dir)

    N = int(sys.argv[2])
    newDir = sys.argv[3]
    lisDir = glob.glob('%s/*' %dir)
    print lisDir

    if not os.path.exists(newDir):
        os.mkdir(newDir)

    for f in lisDir:
        fName = os.path.basename(f)
        newF = '%s/%s' %(newDir, fName)
        getRseqsFromBigFile6(f, newF, N)
        print >> sys.stderr, '%d seqs sampled from %s' %(N, f)

if __name__ == '__main__':
    main()
