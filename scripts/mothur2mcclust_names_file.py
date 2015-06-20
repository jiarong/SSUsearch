#! /usr/bin/env python
# convert between mothur and mcclust names file
# by gjr; 042215

import sys
import os

def main():
    if len(sys.argv) != 3:
        mes = 'Usage: python {} <mothur.names> <mcclust.names>'
        print >> sys.stderr, mes.format(sys.argv[0])
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2]

    with open(outfile, 'wb') as fw:
        for n, line in enumerate(open(infile)):
            line = line.rstrip()
            id, temp_str = line.split()
            rep = temp_str.split(',',1)[0]
            assert id == rep, '*** Input is not mothur names file format..'
            print >> fw, '{} {}'.format(n, temp_str)

if __name__ == '__main__':
    main()
