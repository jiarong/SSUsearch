#! /usr/bin/env python
# get minimum seq number in a dir

"""
Get minimum seq number among sequence files in a directory

% python count-min.py <seqdir>
"""

import sys
import os
import glob

import screed

def main():
    # Usage: python <thisfile> <seqdir>
    if len(sys.argv) != 2:
        mes = 'python {} <seqdir>'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    seqdir = sys.argv[1].rstrip()
    mes = '{} should a directory with seqfiles'
    assert os.path.isdir(seqdir), mes.format(seqdir)
    seqfiles = glob.glob('{}/*'.format(seqdir))
    min_cnt = 1e9
    for n, file in enumerate(seqfiles):
        if os.path.isdir(file):
            continue
        cnt = 0
        for record in screed.open(file):
            cnt += 1
        if n == 0 or cnt < min_cnt:
            min_cnt = cnt

    print min_cnt

if __name__ == '__main__':
    main()
