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
NA='Unclassified'


def read_mothur_taxonomy(f):
    """
    Parse mothur classify.seqs output

    Parameters:
    -----------
    f : str
        file name of .taxonomy file from classify.seqs

    Returns:
    --------
    dictionary
        an dictionary of read name and tuples (each level of taxonomy)

    """
    na_lis = ['', 'unknown', 'Unclassified', 
            'unclassified', 'other', 'unassigned']
    d = {}
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

            if item in na_lis:
                item = NA

            item = item.capitalize()
            lis2.append(item)

        t = tuple(lis2)
        if name.endswith('/1'):
            other = '{}/2'.format(name[:-2])
            if other in d:
                other_taxon = d[other]
                if other_taxon.count(NA) > lis2.count(NA):
                    _ = d.pop(other)
                    d[name] = t
            
        elif name.endswith('/2'):
            other = '{}/1'.format(name[:-2])
            if other in d:
                other_taxon = d[other]
                if other_taxon.count(NA) > lis2.count(NA):
                    _ = d.pop(other)
                    d[name] = t

        else:
            d[name] = t

    return d


def main():
    if len(sys.argv) != 3:
        mes = ('Usage: python {} <sample.gg.taxonomy> <outfile.table>')
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    taxonfile = sys.argv[1]
    outfile = sys.argv[2]


    d = read_mothur_taxonomy(taxonfile)
    g_taxonomy = d.values()
    d_count = collections.Counter(g_taxonomy)

    with open(outfile, 'wb') as fw:
        for key, cnt in sorted(d_count.items()):
            taxon_string = ';'.join(key)
            print >> fw, '{}\t{}'.format(taxon_string, cnt)

if __name__ == '__main__':
    main()
