#! /usr/bin python
# 3d plot for 
# by gjr; Feb 22, 12

import sys
import matplotlib
#matplotlib.use('Agg')
#matplotlib.use('Pdf')
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt

'''
usage: python<thisFile><pc1><pc2>
'''

labelLists=[]
xLists = []
yLists = []
zLists = []
pctVars = [] # percent variation explained by axis
for f in sys.argv[1:]:
    lis = [line.rstrip().split('\t') for line in open(f) if line.rstrip()]
    assert len(lis[0]) == 4, 'check format..'
    assert lis[0][0] == 'pc vector number', 'check format..'
    assert lis[-1][0] == '% variation explained', 'check format..'
    labels, xs, ys, zs = zip(*lis[1:-2])
    xs = [float(i) for i in xs]
    ys = [float(i) for i in ys]
    zs = [float(i) for i in zs]
    vars = [float(i) for i in lis[-1][1:]]
    xLists.append(xs)
    yLists.append(ys)
    zLists.append(zs)
    labelLists.append(labels)
    pctVars.append(vars)

assert pctVars[0] == pctVars[1], 'variation explained diff in two files'

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for xs, ys, zs, lables, color in zip(xLists,yLists,zLists,labelLists,['r','b']):

    '''
    # same color for dots from same file
    ax.scatter(xs, ys, zs, marker='o', 
               c=color,
               s = 50,)
    '''
    # different color for diff samples, same sample from two files sampe color
    cnt = len(xs)
    ax.scatter(xs, ys, zs, marker='o', 
                   c=[i/float(cnt) for i in range(cnt)],
                   s = 50,
                   cmap=plt.get_cmap('Spectral'))

    # annoations
    for label, x, y, z in zip(labels, xs, ys, zs):
        x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
        annot = plt.annotate(
                    label,
                    xy = (x2, y2))

# draw line between same sample in two files
xxs = zip(*xLists)
yys = zip(*yLists)
zzs = zip(*zLists)
edges = zip(xxs, yys, zzs)
for xx, yy, zz in edges:
    ax.plot(xx, yy, zz, '-g', )

ax.set_xlabel('%s (%.f%%)' %('PC1', pctVars[0][0]))
ax.set_ylabel('%s (%.f%%)' %('PC2', pctVars[0][1]))
ax.set_zlabel('%s (%.f%%)' %('PC3', pctVars[0][2]))
#plt.title(sys.argv[1])
plt.savefig('%s.pdf' %(sys.argv[1]))
plt.show()
#plt.savefig('%s.png' %(sys.argv[1]))