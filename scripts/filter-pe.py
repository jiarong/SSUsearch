#!/usr/bin/env python

import sys
import os
import screed
from collections import OrderedDict

def main():
    if len(sys.argv) < 2:
        sys.stderr.write('*** Usage: python {} <seqfile>\n'.format(
            os.path.basename(sys.argv[0])))

        sys.exit(1)

    seqfile = sys.argv[1]
    d = OrderedDict()
    for rec in screed.open(seqfile):
        name = rec.name.split(None, 1)[0]
        seq = rec.sequence
        if name.endswith('/1') or name.endswith('/2'):
            name2 = name[:-2]
            if name2 in d:
                if d[name2][0] > len(seq):
                    continue

            d[name2] = len(seq), name
        else:
            d[name] = len(seq), name

    st = set([d[name][-1] for name in d])
    for rec in screed.open(seqfile):
        name = rec.name.split(None, 1)[0]
        if name in st:
            sys.stdout.write('>{}\n{}\n'.format(name, rec.sequence))

if __name__ == '__main__':
    main()

