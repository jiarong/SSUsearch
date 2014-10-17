#! /usr/bin python
# parse output of mc clust, convert to mothurList file
# by gjr; Feb 22, 12


import sys
import os

import screed

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
                d[cluNum] = d[cluNum]+','+Sname
            else:
                d[cluNum] = Sname

def main():
    '''
    Usage: python <thisFile><mcclust.file><mothur.list>
    convert mcclust.clust to mothur.list
    '''
    if len(sys.argv) != 3:
        mes = 'Usage: python {} <mcclust.file> <mothur.list>'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    clust_listfile = sys.argv[1]
    mothur_listfile = sys.argv[2]
    makeMothurListFile(clust_listfile,mothur_listfile)

if __name__ == '__main__':
    main()
