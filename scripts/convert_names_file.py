#! /usr/bin/env python
# convert between mothur and mcclust names file
# by gjr; 042215

import sys
import os

def main():
    if len(sys.argv) != 3:
        mes = 'Usage: python {} <infile.names> <outfile.names>'
        print >> sys.stderr, mes.format(sys.argv[0])
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2]

    with open(outfile, 'wb') as fw:
        trigger = True
        for n, line in enumerate(open(infile)):
            line = line.rstrip()
            id, temp_str = line.split()
            rep = temp_str.split(',',1)[0]
            if id == rep:
                if trigger:
                    print >> sys.stderr, '*** Mothur names file found..'
                    print >> sys.stderr, ('*** Converting to mcClust '
                                           'names file ..')
                    trigger = False

                print >> fw, '{} {}'.format(n, temp_string)

            else:
                assert id.isalnum(), ('*** McClust names file use '
                                        'number for cluster name')
                if trigger:
                    print >> sys.stderr, '*** McClust names file found..'
                    print >> sys.stderr, ('*** Converting to mothur '
                                           'names file ..')
                    trigger = False

                print >> fw, '{}\t{}'.format(rep, temp_str)

if __name__ == '__main__':
    main()
