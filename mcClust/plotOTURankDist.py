#! /usr/bin/env python
# parse output of mc clust
# by gjr; May 5, 11


import sys
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed


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

if __name__ == '__main__':

    if 1:
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
