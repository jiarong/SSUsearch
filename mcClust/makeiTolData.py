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
    #
    # for tracking tags purpose
    #
    tracking = True
    if tracking:
        dTag = {}
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
        #print 'clu%d\t%s\t%d' %(cluNum, s, num)
        names = names.split()
        #collecting name with "tag"
        stTag = set()
        tagCnt = 0
        for name in names:
            if tag in name:
                tagCnt+=1
                stTag.add(name)

        #Sname = ','.join(names)
        try:
            d[cluNum][0]+=tagCnt
            d[cluNum][1]+=num
            #Sname = d[cluNum][0]+','+Sname
            #num = d[cluNum][1]+num
            #d[cluNum] = Sname, num
        except KeyError:
            d[cluNum] = tagCnt, num

        if tracking:
            try:
                dTag[cluNum].update(stTag)
            except KeyError:
                dTag[cluNum] = stTag

    if tracking:
        for key in dTag:
            if not dTag[key]:
                #empty set
                continue
            lisTag = list(dTag[key])
            print 'OTU%d\t%s' %(key, ','.join(lisTag))

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

    if 1:
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
            print >> fw, 'OTU%d\t%f\t%f' %(key, math.log(tagNum+1), math.log(seqNum))
            # filter singletons and doubletons
            if seqNum < 3 and tagNum == 0:
                continue
            print >> fw2, 'OTU%d\t%f\t%f' %(key, math.log(tagNum+1), math.log(seqNum))

