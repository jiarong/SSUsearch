#! /usr/bin python
# parse output of mc clust, convert to mothurList file
# by gjr; Feb 22, 12

"""
Convert mcclust.clust to mothur.list

% python mcclust2mothur-list-cutoff.py <mcclust.file> <mothur.list> cutoff

"""

import sys
import os

import screed

def makeMothurListFile(f,listFile,target_cutoff):
    """
    Convert mcclust.clust to mothur.list

    Parameters:
    -----------
    f : str
        clustering result (.clust file) from mcclust
    listFile : str
        mothur list file name
    target_cutoff: str
        distance cutoff used for OTU (e.g., 0.03)

    Returns:
    --------
    None
    """
    
    fp = open(f)
    fw = open(listFile, 'w')
    target_cutoff = float(target_cutoff)
    assert 0 <= target_cutoff <= 1
    triger = False

    d = {}
    temp_cutoff = None
    temp_total = None
    temp_str = None
    for line in fp:
        if 'File' in line:
            print line
            continue
        if 'Sequences:' in line:
            print line
            continue
        line = line.strip()
        if 'distance cutoff:' in line:
            _cutoff = line.split(':',1)[1].strip()
            continue
        if 'Total Clusters:' in line:
            total = line.split(':', 1)[1].strip()
            total = int(total)
            triger = True
            continue

        if triger:
            if not line:
                str = '\t'.join(d.values())
                _cutoff = float(_cutoff)

                if _cutoff == target_cutoff:
                    print >> fw, '%.2f\t%d\t%s' %(target_cutoff, total, str)
                    break
                elif _cutoff > target_cutoff:
                    print >> fw, '%.2f\t%d\t%s' \
                                   %(target_cutoff, temp_total, temp_str)
                    break

                d = {}
                triger = False
                temp_cutoff = _cutoff
                temp_total = total
                temp_str = str
                continue

            assert len(line.split('\t')) == 4, 'parsing wrong ..'
            cluNum, s, num, names = line.split('\t')
            cluNum = float(cluNum)
            Sname = ','.join(names.split())
            if d.has_key(cluNum):
                d[cluNum] = d[cluNum]+','+Sname
            else:
                d[cluNum] = Sname

def main():

    if len(sys.argv) != 4:
        mes = 'Usage: python {} <mcclust.file> <mothur.list> cutoff'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    clust_listfile = sys.argv[1]
    mothur_listfile = sys.argv[2]
    target_cutoff = sys.argv[3]
    makeMothurListFile(clust_listfile,mothur_listfile,target_cutoff)

if __name__ == '__main__':
    main()
