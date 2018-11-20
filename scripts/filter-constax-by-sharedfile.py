#! /usr/bin/env python
# by gjr; 080614

import sys
import os

def main():
    if len(sys.argv) != 3:
        mes = ('Usage: python {} <SS.cons.taxonomy>'
               '<SS.shared>\n')
        sys.stderr.write(mes.format(os.path.basename(sys.argv[0])))
        sys.exit(1)

    constaxfile = sys.argv[1]
    sharedfile = sys.argv[2]

    st = None
    with open(sharedfile) as fp:
        l1 = fp.readline()
        assert l1.startswith('label'), \
                '*** make sure {} is shared file'.format(
                        os.path.basename(sharedfilea))
        l1 = l1.rstrip()
        otus = l1.split('\t')[3:]
        st = set(otus)

    with open(constaxfile) as fp:
        for n, line in enumerate(fp):
            if n == 0:
                sys.stdout.write(line)
                continue
            otu = line.split('\t', 1)[0]
            if not otu in st:
                pass
            else:
                sys.stdout.write(line)
                
if __name__ == '__main__':
    main()
