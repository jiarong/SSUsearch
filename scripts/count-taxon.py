#! /usr/bin/env python
# count the taxon number from mothur taxonomy file
# by gjr; 080614

"""
Count the taxon number for each taxon in mothur taxonomy file

% python <thisFile> <sample.gg.taxonomy> <outfile.table>
"""

import sys
import os
import collections

#EXCLUDE = ['Archaea', 'Eukaryota', 'unknown']
EXCLUDE = []
LEVELS = 7


def read_mothur_taxonomy(f):
    """
    Parse mothur classify.seqs output

    Parameters:
    -----------
    f : str
        file name of .taxonomy file from classify.seqs

    Returns:
    --------
    generator
        an iterable (generator) of tuples (each level of taxonomy)

    """
    for n, line in enumerate(open(f)):
        if line.startswith('#'):
            continue

        line = line.rstrip()
        name, taxa = line.rstrip().split('\t')
        skip = False
        for word in EXCLUDE:
            if word in taxa:
                skip = True
                break

        if skip:
            continue 

        # the parsing of taxa works for both mothur output and this
        taxa = taxa.rstrip(';')    # for mothur classfy.seqs output
        lis = taxa.split(';')
        lis2 = []
        for item in lis:
            item = item.strip()    # for copyrigher copy table ' ;' separater
            if item.endswith(')'):
                item = item.rsplit('(', 1)[0].strip()

            # remove taxon level prefix, e.g. 'p__Firmicutes'
            if '__' in item:
                item = item.split('__', 1)[1]

            #item = item.strip('"')

            # green gene taxonomy has sapce
            item = item.replace(' ', '_')

            item = item.lower()
            if item == '':
                item = 'Unclassifed'
            elif item == 'unknown':
                item = 'Unclassifed'
            elif item == 'unclassified':
                item = 'Unclassifed'
            elif item == 'other':
                item = 'Unclassifed'
            elif item == 'unassigned':
                item = 'Unclassifed'

            item = item.capitalize()
            lis2.append(item)

        yield tuple(lis2)


def main():
    if len(sys.argv) != 3:
        mes = ('Usage: python {} <sample.gg.taxonomy> <outfile.table>')
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    taxonfile = sys.argv[1]
    outfile = sys.argv[2]

    g_taxonomy = read_mothur_taxonomy(taxonfile)
    d_count = collections.Counter(g_taxonomy)

    with open(outfile, 'wb') as fw:
        for key, cnt in sorted(d_count.items()):
            taxon_string = ';'.join(key)
            print >> fw, '{}\t{}'.format(taxon_string, cnt)

if __name__ == '__main__':
    main()
