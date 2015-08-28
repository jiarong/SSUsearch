#! /usr/bin/env python
# combine .axes and .loading file from mothur pcoa analysis for Qiime Procrustes
# by gjr; May 28, 12

"""
Combine .axes and .loading file from mothur pcoa analysis 
for Qiime Procrustes analysis

% python merge-pcoa-axes-loading.py <file.axes> <file.loading> <file.out>
"""

import sys, os

def main():

    if len(sys.argv) != 4:
        print >> sys.stderr, \
               'Usage: python %s <file.axes> <file.loading> <file.out>'\
                  %(os.path.basename(sys.argv[0]))
        sys.exit(1)
    fw = open(sys.argv[3], 'wb')
    for n, line in enumerate(open(sys.argv[1])):
        if n == 0:
            assert line.startswith('group'), 'check mothur pcoa format'
            num_pc = len(line.rstrip().split('\t')) - 1
            newline = 'pc vector number\t%s\n' %('\t'.join([str(i) for i in range(1, num_pc + 1)]))
            fw.write(newline)
            continue
        line = line.rstrip()
        fw.write('%s\n' %line)
    fw.write('\n')
    fw.write('\n')

    pct_var = []
    for n, line in enumerate(open(sys.argv[2])):
        if n == 0:
            assert line.startswith('axis'), 'check format..'
            continue
        if not line:
            continue
        items = line.rstrip().split('\t')
        assert len(items) == 2
        var = items[1]
        pct_var.append(var)

    eigvals = ['0']*len(pct_var)
    print >> sys.stderr, 'eigValues are hacked as 0s'
    print >> fw, '%s\t%s' %('eigvals','\t'.join(eigvals))
    print >> fw, '%s\t%s' %('% variation explained','\t'.join(pct_var))

if __name__ == '__main__':
    main()
