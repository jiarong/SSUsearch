#! /usr/bin python
# plot for PCoA or NMDS
# by gjr; Feb 22, 12

import sys
import matplotlib
#matplotlib.use('Agg')
#matplotlib.use('Pdf')
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt

'''
usage: python<thisFile><.axes><.loading>
'''

cnt = 0
labels=[]
xLis = []
yLis = []
zLis = []
for line in open(sys.argv[1]):
    line = line.strip()
    if not line:
        continue
    if (cnt == 0 and line.split('\t') == ['axis1', 'axis2']):
        print 'reading NMDS output..'
        print 'make sure using 3 dimention when run nMDS..'
        continue
    elif (cnt==0 and line.startswith('group')):
        print 'pcoa output..'
        continue

    lis = line.split('\t')
    sample, x, y, z = lis[0], lis[1], lis[2], lis[3]

    labels.append(sample)
    x = float(x)
    y = float(y)
    z = float(z)
    xLis.append(x)
    yLis.append(y)
    zLis.append(z)
    cnt += 1

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(xLis, yLis, zLis, marker='o', 
               c=[i/float(cnt) for i in range(cnt)],
               s = 50,
               cmap=plt.get_cmap('Spectral'))

# 3d annotation
for label, x, y, z in zip(labels, xLis, yLis, zLis):
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    plt.annotate(
        label,
        xy = (x2, y2))

# parse .loading for variation explained by axis 
pctVars = []
for n, line in enumerate(open(sys.argv[2])):
    if n == 0:
        assert line.startswith('axis'), 'check format..'
        continue
    if not line:
        continue
    items = line.rstrip().split('\t')
    assert len(items) == 2
    var = float(items[1])
    pctVars.append(var)

ax.set_xlabel('%s (%.f%%)' %('PC1', pctVars[0]))
ax.set_ylabel('%s (%.f%%)' %('PC2', pctVars[1]))
ax.set_zlabel('%s (%.f%%)' %('PC3', pctVars[2]))
plt.title(sys.argv[1])
plt.savefig('%s.3d.pdf' %(sys.argv[1]))
#plt.savefig('%s.3d.png' %(sys.argv[1]))
plt.show()
