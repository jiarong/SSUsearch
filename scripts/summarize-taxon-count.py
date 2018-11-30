#! /usr/bin/env python
# make plot of copyrighter.py output table
# by gjr
from __future__ import print_function
import sys, os, itertools, collections
from operator import itemgetter, attrgetter
import numpy

"""
Summmary from taxon count table (from count-taxon.py)


% python summarize-taxa-count.py level <outdir> \
                                    <file1.taxonomy> [ <file2.taxonomy> ... ]

"""

EXCLUDE = ['Archaea', 'Eukaryota', 'unknown']
#EXCLUDE = []
TOP=10
ORDER=True  # Most abundant to least abundant
def readData(f):
    """
    Parse taxon count table (from count-taxon.py)

    Parameters:
    -----------
    f : str
        file name of taxon count table

    Returns:
    --------
    tuple
        a list of taxons and a list of their counts

    """
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
    #usage: python <thisFile> level <outfile> <file.taxonomy> ..
    if len(sys.argv) < 4:
        mes = '*** Usage: python {} level <outfile> <file.taxonomy>..\n'
        sys.stderr.write(mes.format(os.path.basename(sys.argv[0])))
        sys.stderr.write("*** ATT: filename.split('.')[0] will "\
                                 'be the sample label\n')
        sys.exit(1)

    level = int(sys.argv[1])
    outfile = sys.argv[2]
    d = {}
    dCombined = {}
    lisSampOrder = []
    for f in sys.argv[3:]:
        samp = os.path.basename(f).split('.')[0]    # sample name
        container, num_lis = readData(f)
        tranLis = itertools.izip_longest(*container, fillvalue='Unclassified')
        levelLis = list(tranLis)[:level]
        levelLis = [';'.join(i) for i in zip(*levelLis)]
        countD = {}
        for tax, num in zip(levelLis, num_lis):
            countD[tax] = countD.get(tax, 0) + num

        total = sum(countD.values())
        d[samp] = dict((taxa, countD[taxa]*1.0/total) for taxa in countD)
        for key in d[samp]:
            dCombined[key] = dCombined.get(key, 0) + d[samp][key]

        lisSampOrder.append(samp)

    items = sorted(dCombined.items(), key= itemgetter(1), reverse=ORDER)
    #items =  items[:TOP]
    taxas, nums = zip(*items)

    d2 = {}
    with open(outfile, 'w') as fw:
        fw.write('Sample\t{}\n'.format('\t'.join(taxas)))
        for key in lisSampOrder:
            lis = []
            for word, count in items[:TOP]:
                pct = d[key].get(word, 0)
                lis.append(pct*100)
            fw.write('{}\t{}\n'.format(
                key, 
                '\t'.join(('{:.1f}'.format(x) for x in lis)
                    )
                )
            )
            d2[key] = lis

if __name__ == '__main__':
    main()
