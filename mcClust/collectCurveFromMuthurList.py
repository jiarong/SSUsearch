#! /usr/bin/env python
# make collector's curve from mothur list
# by gjr; Apr 9, 12

import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

'''
usage: python <thisFile><file.list><cutoff><tag>
'tag' is the prefix or suffix of interested seq names, like (like RL1_ISO)
'''

cutoff = sys.argv[2]
tag = sys.argv[3]
for line in open(sys.argv[1]):
    # look for cuoff line
    if line.startswith(cutoff):
        line = line.rstrip()

        lis = line.split('\t')
        cutoff, otuNum, otus = lis[0], lis[1], lis[2:]
        
        assert len(otus) == int(otuNum)
        lisTemp = [(len(otu.split(',')), set(otu.split(','))) for otu in otus]
        # sort based on the otu size from large to small
        lisTemp.sort(reverse=True)
        sizeLis, otuLis = zip(*lisTemp)

        # get the list of number of seqs with tag
        # cnt = 0
        # cumulative: tagSeqLis = [(cnt++ for i in otu if tag in i) for otu in otuLis]
        tagSeqLis = []
        for otu in otuLis:
            cnt = 0
            for i in otu:
                if tag not in i:
                    continue
                cnt+=1
            tagSeqLis.append(cnt)

        totalSeqs = sum(sizeLis)
        totalTags = sum(tagSeqLis)
        print totalSeqs
        print totalTags, '<--------------'
        sizeLisRelAbun = [float(i)/totalSeqs for i in sizeLis]
        tagSeqLisRelAbun = [float(i)/totalTags for i in tagSeqLis]
        sizeLisRelAbun_acum = []
        tempTotal = 0
        for i in sizeLisRelAbun:
            tempTotal+=i
            sizeLisRelAbun_acum.append(tempTotal)
        
        tagSeqLisRelAbun_acum = []
        tempTotal = 0
        for i in tagSeqLisRelAbun:
            tempTotal+=i
            tagSeqLisRelAbun_acum.append(tempTotal)

        #plt.scatter((range(1, int(otuNum)+1, 1)), sizeLisRelAbun, c='green', label='PT', linestyle='solid')
        plt.scatter((range(1, int(otuNum)+1, 1)), sizeLisRelAbun_acum, c='green', label='PT', linestyle='solid')
        plt.scatter((range(1, int(otuNum)+1, 1)), tagSeqLisRelAbun, c='red', label='ISO', linestyle='solid')
        #plt.scatter((range(1, int(otuNum)+1, 1)), tagSeqLisRelAbun_acum, c='red', label='ISO', linestyle='solid')
        
        plt.title(sys.argv[1])
        #plt.ylim(ymin=0, ymax=50000)
        #plt.ylim(ymin=0, ymax=0.05)
        leg = plt.legend(loc = 'upper left', shadow = True, borderpad = 0.1)
        for t in leg.get_texts():
            t.set_fontsize('small')
        for l in leg.get_lines():
            l.set_linewidth(5) 

        #plt.show()
        plt.savefig('%s.png' %(sys.argv[1]))
        plt.clf()

