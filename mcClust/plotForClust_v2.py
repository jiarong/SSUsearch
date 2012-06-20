#! /usr/bin python
# plot for PCoA or NMDS
# by gjr; Feb 22, 12

import sys
import matplotlib
matplotlib.use('Agg')
#matplotlib.use('Pdf')
import matplotlib.pyplot as plt

cnt = 0
labels=[]
xLis = []
yLis = []
for line in open(sys.argv[1]):
    line = line.strip()
    if not line:
        continue
    if (cnt == 0 and line.split('\t') == ['axis1', 'axis2']):
        print 'reading NMDS output..'
        continue
    elif (cnt==0 and line.startswith('group')):
        print 'pcoa output..'
        continue

    lis = line.split('\t')
    sample, x, y = lis[0], lis[1], lis[2]

    labels.append(sample)
    x = float(x)
    y = float(y)
    xLis.append(x)
    yLis.append(y)
    cnt += 1

plt.scatter(xLis, yLis, marker='o', 
               c=[i/float(cnt) for i in range(cnt)],
               s = 50,
               cmap=plt.get_cmap('Spectral'))

'''
plt.scatter(xLis, yLis, marker='o', 
               color='g',
               s = 20,)
'''

for label, x, y in zip(labels, xLis, yLis):
    plt.annotate(
        label,
        xy = (x, y))

plt.title(sys.argv[1])
#plt.savefig('%s.pdf' %(sys.argv[1]))
plt.savefig('%s.png' %(sys.argv[1]))
