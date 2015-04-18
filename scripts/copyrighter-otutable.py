#! /usr/bin/env python
# corrent ssu rRNA gene copy number based on the taxon copy number table from
#   copyrigter.
# by gjr; 080614

# Usage: python <thisFile> <copy.table> <SS.cons.taxonomy> <SS.shared> 
#   <outfile.table>

import sys
import os
import collections
import pandas

#EXCLUDE = ['Archaea', 'Eukaryota', 'unknown']
EXCLUDE = []
LEVELS = 7


def read_refcopy(f):
    # This function can read copyrighter # tax_string table

    d_refcopy = {}
    for n, line in enumerate(open(f)):
        if line.startswith('#'):
            continue

        line = line.rstrip()
        if line == '':
            continue

        _lis = line.split('\t')
        taxa, num, = _lis[:2]
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
            if item in ['', 'unknown', 'other', 'unassigned']:
                item = 'Unclassifed'

            item = item.capitalize()
            lis2.append(item)

        length = len(lis2)
        assert length <= LEVELS, '> {} levels found ({})'.format(
            LEVELS, length)
        if length != LEVELS:
            lis2 = lis2 + ['Unclassified']*(LEVELS - length)

        tu = tuple(lis2)
        d_refcopy[tu] = float(num)

    return d_refcopy


def read_mothur_taxonomy(f):
    # read in mothur classify.seqs output
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
            if item in ['', 'unknown', 'other', 'unassigned']:
                item = 'Unclassifed'

            item = item.capitalize()
            lis2.append(item)

        length = len(lis2)
        assert length == LEVELS, 'levels ({}) is not ({})'.format(
            length, LEVELS)
        yield tuple(lis2)


def read_mothur_cons_taxonomy(f):
    # read in mothur classify.seqs output
    d_otu2tax = {}
    for n, line in enumerate(open(f)):
        # the first header line does not startswith "#" in v1.33
        if line.startswith('OTU\tSize\tTaxonomy'):
            continue

        if line.startswith('#'):
            continue

        line = line.rstrip()
        otu, num, taxa = line.rstrip().split('\t')
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
            if item in ['unknown', 'unclassified', 'other', 'unassigned']:
                item = 'Unclassifed'

            item = item.capitalize()
            lis2.append(item)

        length = len(lis2)
        mes = 'levels number ({}) is not ({}): {}'
        assert length == LEVELS, mes.format(
            length, LEVELS, repr(lis2))
        d_otu2tax[otu] =  tuple(lis2)

    return d_otu2tax


def main():
    if len(sys.argv) != 5:
        mes = ('Usage: python {} <copy.table> <SS.cons.taxonomy>'
               '<SS.shared> <outfile.table>')
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    copytable = sys.argv[1]
    constaxfile = sys.argv[2]
    sharedfile = sys.argv[3]
    outfile = sys.argv[4]

    d_refcopy = read_refcopy(copytable)
    d_otu2tax = read_mothur_cons_taxonomy(constaxfile)

    sum_copy = 0
    cnt_otu_with_copy = 0
    for otu in d_otu2tax:
        _tax = d_otu2tax[otu]
        if _tax in d_refcopy:
            sum_copy += d_refcopy[_tax]
            cnt_otu_with_copy += 1

    average_copy = sum_copy/cnt_otu_with_copy

    d_otucopy = dict(
      (otu, d_refcopy.get(d_otu2tax[otu], average_copy)) for otu in d_otu2tax)

    df_shared = pandas.read_csv(sharedfile, sep='\t', index_col=False)
    df_shared = df_shared.ix[:,:-1]     # remove last column due trailing tab

    subsample_size_list_before = df_shared.iloc[:,3:].sum(axis=1)

    # even the sample depth to original
    sample_depth = int(min(subsample_size_list_before))

    for key in df_shared.columns[3:]:
        copy = d_otucopy[key]
        df_shared[key] = df_shared[key]/copy

    subsample_size_list_after = df_shared.iloc[:,3:].sum(axis=1)
    # even the sample depth to max after correction
    #sample_depth = int(max(subsample_size_list_after))

    for i in df_shared.index:
        abund_series = df_shared.iloc[i,3:]
        row_total = float(sum(abund_series))
        assert row_total != 0, 'samples size is 0 after correction'
        ratio = sample_depth*1.0/row_total

        abund_series = abund_series*ratio
        df_shared.iloc[i,3:] = abund_series


    df_shared.iloc[:,3:] = df_shared.iloc[:,3:].astype(int)
    df_shared.to_csv(outfile, sep='\t', index=False, line_terminator='\t\n')


if __name__ == '__main__':
    main()
