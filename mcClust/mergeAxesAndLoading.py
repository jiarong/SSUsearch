#! /usr/bin/env python
# combine .axes and .loading file from mothur pcoa analysis for Qiime Procrustes
# by gjr; May 28, 12


'''
usage: python<thisFile><.axes><.loading>
'''
import sys

fw = open('%sprocrustes' %(sys.argv[1].rstrip('axes')), 'wr')
for line in open(sys.argv[1]):
    fw.write(line)
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
print >> sys.stderr, 'eigValues are faked as 0s'
print >> fw, '%s\t%s' %('eigvals','\t'.join(eigvals))
print >> fw, '%s\t%s' %('% variation explained','\t'.join(pct_var))
