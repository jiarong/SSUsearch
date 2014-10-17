#! /usr/bin/env python
# parse output of mc clust
# by gjr; May 5, 11


import sys
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed

#-----------------------------
CUTOFF = 0.15
#SAMPLE = 'iowa_native_prairie'
SAMPLE = 'iowa_cont_corn'
#-----------------------------

def parse_fp(fp, ):
    triger = False
    cnt = 0
    d = {}
    for line in fp:
        if 'File' in line:
            print line
            continue
        if 'Sequences:' in line:
            print line
            continue
        if 'distance cutoff:' in line and str(CUTOFF) in line:
            triger = True
            continue
        if not triger:
            continue
        line = line.strip()
        if 'Total Clusters:' in line:
            total = line.split(':', 1)[1].strip()
            total = int(total)
        if SAMPLE in line:
            _, s, num, names = line.split('\t')
            print 'clu%d\t%s' %(cnt, num)
            names = names.split()
            assert s == SAMPLE, s
            for name in names:
                d[name] = cnt
            cnt += 1

        if not line:
            break

    return d

def getNum(f, cutoff, tag=None):
    '''
    get dict (OTU#, [names, totalSeq#inOTU])
    '''
    fp = open(f)
    triger = False
    d = {}
    for line in fp:
        if 'File' in line:
            print line
            continue
        if 'Sequences:' in line:
            print line
            continue
        line = line.strip()
        if 'distance cutoff:' in line:
            assert triger == False, 'check format ..'
            cutoffTemp = line.split(':',1)[1].strip()
            #cutoffTemp = float(cutoffTemp)
            if cutoffTemp == cutoff:
                triger = True
                print >> sys.stderr, 'reading %s' %(line)
            continue

        if not triger:
            continue

        if 'Total Clusters:' in line:
            total = line.split(':', 1)[1].strip()
            total = int(total)
            print >> sys.stderr, line
            continue

        if not line:
            triger = False
            continue

        # parsing the useful lines
        assert len(line.split('\t')) == 4, 'parsing wrong ..'
        cluNum, s, num, names = line.split('\t')
        cluNum = int(cluNum)
        num = int(num)
        print 'clu%d\t%s\t%d' %(cluNum, s, num)
        names = names.split()
        tagCnt = 0
        for name in names:
            if tag in name:
                tagCnt+=1
        #Sname = ','.join(names)
        try:
            d[cluNum][0]+=tagCnt
            d[cluNum][1]+=num
            #Sname = d[cluNum][0]+','+Sname
            #num = d[cluNum][1]+num
            #d[cluNum] = Sname, num
        except KeyError:
            d[cluNum] = tagCnt, num

    return d

def getOTUAbun(f, cutoff, tags):
    '''
    get dict (tag, listOfOTUAbun)
    listOfOTUAbun is not sorted
    '''
    fp = open(f)
    triger = False
    d = {}
    for line in fp:
        if 'File' in line:
            print line
            continue
        if 'Sequences:' in line:
            print line
            continue
        line = line.strip()
        if 'distance cutoff:' in line:
            assert triger == False, 'check format ..'
            cutoffTemp = line.split(':',1)[1].strip()
            #cutoffTemp = float(cutoffTemp)
            if cutoffTemp == cutoff:
                triger = True
                print >> sys.stderr, 'reading %s' %(line)
            continue

        if not triger:
            continue

        if 'Total Clusters:' in line:
            total = line.split(':', 1)[1].strip()
            total = int(total)
            print >> sys.stderr, line
            continue

        if not line:
            triger = False
            continue

        # parsing the useful lines
        assert len(line.split('\t')) == 4, 'parsing wrong ..'
        cluNum, s, num, names = line.split('\t')
        if not s in tags:
            continue
        cluNum = int(cluNum)
        num = int(num)
        #print 'clu%d\t%s\t%d' %(cluNum, s, num)
        names = names.split()
        assert num == len(names)
        try:
            d[s].append(num)
        except KeyError:
            d[s] = [num,]

    return d

def makeMothurListFile(f,listFile):
    fp = open(f)
    fw = open(listFile, 'w')
    triger = False
    d = {}
    for line in fp:
        if 'File' in line:
            print line
            continue
        if 'Sequences:' in line:
            print line
            continue
        line = line.strip()
        if 'distance cutoff:' in line:
            assert triger == False, 'check the file format..'
            cutoff = line.split(':',1)[1].strip()
            cutoff = float(cutoff)
            continue
        if 'Total Clusters:' in line:
            total = line.split(':', 1)[1].strip()
            total = int(total)
            triger = True
            continue

        if triger:
            if not line:
                str = '\t'.join(d.values())
                print >> fw, '%.2f\t%d\t%s' %(cutoff, total, str)
                d = {}
                triger = False
                continue

            assert len(line.split('\t')) == 4, 'parsing wrong ..'
            cluNum, s, num, names = line.split('\t')
            cluNum = float(cluNum)
            #print 'clu%d\t%s\t%s' %(cluNum, s, num)
            Sname = ','.join(names.split())
            if d.has_key(cluNum):
                d[cluNum] = '%s,%s' %(d[cluNum],Sname)
            else:
                d[cluNum] = Sname

def getVenn(f, cutoff, n, tags):
    '''
    get Venn showing (n)tons removed
    by gjr, May 20, 2012
    '''
    assert len(tags) == 2, 'This script do venn of 2 samples'
    fp = open(f)
    n = int(n)
    triger = False
    d1 = {}
    d2 = {} # dict with (n)tons filtered
    dd = {} # dict (sample, dict(cluNum, num))
    for sample in tags:
        dd[sample] = {}

    for line in fp:
        if 'File' in line:
            print line
            continue
        if 'Sequences:' in line:
            print line
            continue
        line = line.strip()
        if 'distance cutoff:' in line:
            assert triger == False, 'check format ..'
            cutoffTemp = line.split(':',1)[1].strip()
            #cutoffTemp = float(cutoffTemp)
            if cutoffTemp == cutoff:
                triger = True
                print >> sys.stderr, 'reading %s' %(line)
            continue

        if not triger:
            continue

        if 'Total Clusters:' in line:
            total = line.split(':', 1)[1].strip()
            total = int(total)
            print >> sys.stderr, line
            continue

        if not line:
            triger = False
            continue

        # parsing the useful lines
        assert len(line.split('\t')) == 4, 'parsing wrong ..'
        cluNum, s, num, names = line.split('\t')
        if not s in tags:
            continue
        cluNum = int(cluNum)
        num = int(num)
        #print 'clu%d\t%s\t%d' %(cluNum, s, num)
        names = names.split()
        assert num == len(names)
        try:
            d1[s].append(cluNum)

        except KeyError:
            d1[s] = [cluNum,]

        if num > n:
            try:
                d2[s].append(cluNum)
            except KeyError:
                d2[s] = [cluNum,]

        dd[s][cluNum] = num

    sample1 = tags[0]
    sample2 = tags[1]

    print '(%s)tons not filtered:'
    print 'description\tOTUs\tSeqs'

    tempSet = set(d1[sample1]).difference(set(d1[sample2]))
    tempSum = sum((dd[sample1][key] for key in tempSet))
    print '%s only:\t%d\t%d' %(sample1, len(tempSet), tempSum)

    tempSet = set(d1[sample1]).intersection(set(d1[sample2]))
    tempSum1 = sum((dd[sample1][key] for key in tempSet))
    tempSum2 = sum((dd[sample2][key] for key in tempSet))
    print 'shared   :\t%d\t%d(%s)|%d(%s)' %(len(tempSet), tempSum1, sample1, tempSum2, sample2)

    tempSet = set(d1[sample2]).difference(set(d1[sample1]))
    tempSum = sum((dd[sample2][key] for key in tempSet))
    print '%s only:\t%d\t%d' %(sample2, len(tempSet), tempSum)

    # filtered:
    print '(%s)tons filtered:'
    print 'description\tOTUs\tSeqs'

    tempSet = set(d2[sample1]).difference(set(d2[sample2]))
    tempSum = sum((dd[sample1][key] for key in tempSet))
    print '%s only:\t%d\t%d' %(sample1, len(tempSet), tempSum)

    tempSet = set(d2[sample1]).intersection(set(d2[sample2]))
    tempSum1 = sum((dd[sample1][key] for key in tempSet))
    tempSum2 = sum((dd[sample2][key] for key in tempSet))
    print 'shared   :\t%d\t%d(%s)|%d(%s)' %(len(tempSet), tempSum1, sample1, tempSum2, sample2)

    tempSet = set(d2[sample2]).difference(set(d2[sample1]))
    tempSum = sum((dd[sample2][key] for key in tempSet))
    print '%s only:\t%d\t%d' %(sample2, len(tempSet), tempSum)

if __name__ == '__main__':

    if 0:
        '''
        usage: python <thisFile><MCclustOut><seqFile>
        change seq names to clusters
        '''
        fp = open(sys.argv[1])
        d = parse_fp(fp)
        fw = open('%s.%s.clusterNamed' %(sys.argv[2], CUTOFF), 'w')
        for n, record in enumerate(screed.open(sys.argv[2])):
            name = record['name']
            seq = record['sequence']
            cluster = d[name]
            print >> fw, '>clu%d_%d\n%s' %(cluster, n, seq)


    if 0:
        '''
        usage: python <thisFile><mcclust.file><mothur.list>
        convert mcclust.clust to mothur.list
        '''
        f = sys.argv[1]
        listFile = sys.argv[2]
        makeMothurListFile(f,listFile)

    if 0:
        '''
        usage: python <thisFile><complete.clust><cutoff><tag>
        purpose: make tab dilimited file of "cluterIndex, seqNumInClu, tagSeqNum"
        Apr 10, 12
        '''
        import math

        f = sys.argv[1]
        cutoff = sys.argv[2]
        tag = sys.argv[3]
        fw = open('%s.iTolData' %(sys.argv[1]), 'wb')
        fw2 = open('%s.1or2ersFiltered.iTolData' %(sys.argv[1]), 'wb')
        d = getNum(f, cutoff, tag)
        # dict(cluNum = [tagNum, seqNum])
        '''
        vals = d.values()
        tagNums, seqNums = zip(*vals)
        totalTag = sum(tagNums)
        totalSeq = sum(seqNums)
        '''
        for key in d:
            tagNum = d[key][0]
            seqNum = d[key][1]
            print >> fw, 'OTU%d,%f,%f' %(key, math.log(tagNum+1), math.log(seqNum))
            # filter singletons and doubletons
            if seqNum < 3:
                continue
            print >> fw2, 'OTU%d,%f,%f' %(key, math.log(tagNum+1), math.log(seqNum))

    if 0:
        '''
        usage: python<thisFile><mcClust.out><cutoff><listOfsamples>
        purpose: plot the ranked relative abudance of OTUs
        '''
        import math
        import matplotlib
        matplotlib.use('Pdf')
        import matplotlib.pyplot as plt
        f = sys.argv[1]
        cutoff = sys.argv[2]
        tags = sys.argv[3:]
        d = getOTUAbun(f, cutoff, tags)
        # sort the OTUAbun list of each sample
        for sample in d:
            OTUAbunLis = d[sample]
            total = sum(OTUAbunLis)
            RelAbunLis = [math.log(i/float(total),2) for i in OTUAbunLis]
            #remove singletons
            #RelAbunLis = [math.log(i/float(total),2) for i in OTUAbunLis if i>2]
            RelAbunLis.sort(reverse=True)
            xs = range(1, (len(RelAbunLis)+1))
            #Plot
            plt.plot(xs, RelAbunLis, '-x', label=sample)

        leg = plt.legend(loc='upper right')
        plt.xlim(xmin=-100)
        plt.savefig('%s.pdf' %(sys.argv[1]))
        plt.clf()

    if 1:
        '''
        usage: python<thisFile><complete.clust><cutoff><N><tags>
        OTUs with <= N seqs are removed
        '''
        f = sys.argv[1]
        cutoff = sys.argv[2] # no need to convert to float
        n = int(sys.argv[3])
        tags = sys.argv[4:]
        
        getVenn(f, cutoff, n, tags)
