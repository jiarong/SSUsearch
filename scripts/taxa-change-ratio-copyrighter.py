#! /usr/bin/env python
# make plot of copyrighter.py output table
# by gjr

"""
Get the taxon relative abudance change ratio after copy correction

% python taxa-change-ratio-copyrighter.py \
                                    level <outfile> \
                                    <file.before.cc.taxonomy> \
                                    <file.after.cc.taxonomy>

"""
import sys, os, itertools, collections
from operator import itemgetter, attrgetter

import numpy
import pandas

EXCLUDE = ['Archaea', 'Eukaryota', 'unknown']
#EXCLUDE = []
TOP=20
#ORDER=True  #reverse the order
ORDER=False  #normal order
def readData(f):
    taxa_lis = []
    num_lis = []
    for n, line in enumerate(open(f)):
        if line.startswith('#'):
            continue

        line = line.rstrip()
        if line == '':
            continue

        taxa, num = line.split('\t')
        skip = False
        for word in EXCLUDE:
            if word in taxa:
                skip = True
                break

        if skip:
            continue 

        taxa = taxa.rstrip(';')
        lis = taxa.split(';')
        lis2 = []
        for item in lis:
            item = item.strip()
            if item.endswith(')'):
                item = item.split('(')[0].strip()

            # remove taxon level prefix, e.g. 'p__Firmicutes'
            if '__' in item:
                item = item.split('__', 1)[1]

            #item = item.strip('"')

            item = item.lower()
            if 'unclassified' in item:
                item = 'Unclassifed'
            elif 'unknown' in item:
                item = 'Unclassifed'
            elif 'other' in item:
                item = 'Unclassifed'
            elif 'unassigned' in item:
                item = 'Unclassifed'

            item = item.capitalize()
            lis2.append(item)

        taxa_lis.append(lis2)
        num_lis.append(float(num))

    return taxa_lis, num_lis

def main():
    #Usage: python <thisFile> level <outfile> <file.taxonomy> ..
    if len(sys.argv) < 3:
        mes = 'Usage: python {} level <outfile> <file.taxonomy>..'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        print >> sys.stderr, "*** filename.split('.')[0] will "\
                                 "be the sample label"
        sys.exit(1)

    level = int(sys.argv[1])
    level = level - 1
    outfile = sys.argv[2]
    d = {}
    dCombined = {}
    lisSampOrder = []
    for f in sys.argv[3:]:
        samp = os.path.basename(f).split('.')[0]    # sample name
        container, num_lis = readData(f)
        tranLis = itertools.izip_longest(*container, fillvalue='Unclassified')
        levelLis = list(tranLis)[level]
        countD = {}
        for tax, num in zip(levelLis, num_lis):
            countD[tax] = countD.get(tax, 0) + num

        total = sum(countD.values())
        d[samp] = dict((taxa, countD[taxa]*1.0/total) for taxa in countD)
        for key in d[samp]:
            dCombined[key] = dCombined.get(key, 0) + d[samp][key]

        lisSampOrder.append(samp)

    df = pandas.DataFrame(d)
    # only take members > 0.1% before copy correction
    df2 = df[df.iloc[:,0] > 0.001]
    df2['ratio'] = df2.iloc[:,0]/df2.iloc[:,1]
    df2 = df2.sort(columns=['ratio'], ascending=[0])
    df2.to_csv('{}.tsv'.format(outfile), sep='\t', index=False)

if __name__ == '__main__':
    main()

