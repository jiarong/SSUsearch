#! /usr/bin/env python
# make rarefaction plot
# by gjr, May 15, 2012

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

def readData(f):
    for n, line in enumerate(open(f)):
        if n==0 and line.startswith('numsampled'):
            print >> sys.stderr, 'row header detected: %s' %line
            continue
        # there is hiden '\t' between sampel and y
        x, sample, _, y, up, low = line.rstrip().split('\t')
        x = float(x)
        y = float(y)
        yield sample, x, y

if __name__ == '__main__':

    import matplotlib.colors as colors
    import matplotlib.cm as cm

    gen = readData(sys.argv[1])
    d = {}
    for sample, x, y in gen:
        try:
            d[sample].append((x,y))
        except KeyError:
            d[sample] = [(x,y),]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    sampleNum = len(d)
    # setting up an array of smapleNum colors
    jet_cm = plt.get_cmap('jet')
    cNorm = colors.Normalize(vmin=0, vmax=range(sampleNum)[-1])
    scalarMap = cm.ScalarMappable(norm=cNorm, cmap=jet_cm)
    print scalarMap.get_clim()

    lis = d.items()
    lis.sort()
    cnt = 0
    lines = []
    for key, value in lis:
        value.sort()
        xs, ys = zip(*value)
        colorVal = scalarMap.to_rgba(range(sampleNum)[cnt])
        retLine, = ax.plot(xs, ys, marker='2', color=colorVal, 
                                     markersize=5,
                                     label = key)
        cnt += 1

        lines.append(retLine)

    ax.set_xlabel('Number of sequences')
    ax.set_ylabel('Number of OTUs')
    # shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.8, box.height*0.8])
    keys = d.keys()
    keys.sort()
    leg = ax.legend(lines, keys, loc = 'center left', bbox_to_anchor=(1,0.5))
    for t in leg.get_texts():
        t.set_fontsize('small')
    plt.savefig('%s.png' %(sys.argv[1]))
