#! /usr/bin/env python
# make plot of copyrighter.py output table
# by gjr

import sys, os, itertools, collections
from operator import itemgetter, attrgetter

import numpy

import matplotlib
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, LinearLocator,\
  LogLocator, MaxNLocator, AutoLocator, AutoMinorLocator, FormatStrFormatter
from pylab import LogFormatter
import matplotlib.colors as colors
import matplotlib.cm as cm

import brewer2mpl


EXCLUDE = ['Archaea', 'Eukaryota', 'unknown']
#EXCLUDE = []
TOP=10
#ORDER=True  #reverse the order
ORDER=False  #normal order
def readData(f):
    taxa_lis = []
    num_lis = []
    for n, line in enumerate(open(f)):
        if line.startswith('#'):
            continue

        line = line.rstrip()
        if line == '':
            continue

        taxa, num = line.split('\t')
        skip = False
        for word in EXCLUDE:
            if word in taxa:
                skip = True
                break

        if skip:
            continue 

        taxa = taxa.rstrip(';')
        lis = taxa.split(';')
        lis2 = []
        for item in lis:
            item = item.strip()
            if item.endswith(')'):
                item = item.split('(')[0].strip()

            # remove taxon level prefix, e.g. 'p__Firmicutes'
            if '__' in item:
                item = item.split('__', 1)[1]

            #item = item.strip('"')

            item = item.lower()
            if 'unclassified' in item:
                item = 'Unclassifed'
            elif 'unknown' in item:
                item = 'Unclassifed'
            elif 'other' in item:
                item = 'Unclassifed'
            elif 'unassigned' in item:
                item = 'Unclassifed'

            item = item.capitalize()
            lis2.append(item)

        taxa_lis.append(lis2)
        num_lis.append(float(num))

    return taxa_lis, num_lis


def main():
    #usage: python <thisFile> level <outfile> <file.taxonomy> ..
    if len(sys.argv) < 3:
        mes = 'usage: python {} level <outfile> <file.taxonomy>..'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        print >> sys.stderr, "*** filename.split('.')[0] will "\
                                 'be the sample label'
        sys.exit(1)

    level = int(sys.argv[1])
    level = level - 1
    outfile = sys.argv[2]
    d = {}
    dCombined = {}
    lisSampOrder = []
    for f in sys.argv[3:]:
        samp = os.path.basename(f).split('.')[0]    # sample name
        container, num_lis = readData(f)
        tranLis = itertools.izip_longest(*container, fillvalue='Unclassified')
        levelLis = list(tranLis)[level]
        countD = {}
        for tax, num in zip(levelLis, num_lis):
            countD[tax] = countD.get(tax, 0) + num

        total = sum(countD.values())
        d[samp] = dict((taxa, countD[taxa]*1.0/total) for taxa in countD)
        for key in d[samp]:
            dCombined[key] = dCombined.get(key, 0) + d[samp][key]

        lisSampOrder.append(samp)

    items = sorted(dCombined.items(), key= itemgetter(1), reverse=True)
    items =  items[:TOP]
    if ORDER:
        items.reverse()
    taxas, nums = zip(*items)

    d2 = {}
    with open('{}.taxa.plot.summary'.format(outfile), 'wb') as fw2:
        print >> fw2, 'Sample\t{}'.format('\t'.join(taxas))
        for key in lisSampOrder:
            lis = []
            for word, count in items[:TOP]:
                pct = d[key].get(word, 0)
                lis.append(pct*100)
            print >> fw2, '{}\t{}'.format(key, '\t'.join(('{:.1f}'.format(x) for x in lis)))
            d2[key] = lis
    
    sampNum = len(d2)
    #color = brewer2mpl.get_map('Set3', 'qualitative', TOP).mpl_colors
    color = brewer2mpl.get_map('Paired', 'qualitative', TOP).mpl_colors
    almost_black = '#262626'

    fig = plt.figure()
    ax = fig.add_subplot(111)


    margin = 0.1
    #width = (1.-2.*margin)/sampNum
    width = 0.25
    xs = numpy.arange(sampNum)
    xs = xs + margin
    rects = []
    labels = []
    liss = []
    for samp in lisSampOrder:
        labels.append(samp)
        liss.append(d2[samp])
    #labels, liss = zip(*d2.items())

    taxaLiss = zip(*liss)
    taxaNum = len(taxaLiss)
    assert taxaNum <= TOP

    rect = ax.bar(xs, taxaLiss[0], width, color=color[0], linewidth=0)
    #rect = ax.bar(xs, taxaLiss[0], width, color=color[0], edgecolor='none')
    rects.append(rect)

    bottom = numpy.cumsum(taxaLiss, axis=0)
    for i in range(1,taxaNum):
        rect = ax.bar(xs, taxaLiss[i], width, bottom=bottom[i-1], color=color[i], linewidth=0)
        #rect = ax.bar(xs, taxaLiss[i], width, bottom=bottom[i-1], color=color[i], edgecolor='none')
        rects.append(rect)



    ax.set_ylabel('Percent of total community')
    ax.set_xticks(xs+width/2)
    ax.set_xticklabels(labels)

    # Remove top and right axes lines ("spines")
    spines_to_remove = ['top', 'right']
    for spine in spines_to_remove:
        ax.spines[spine].set_visible(False)

    # Get rid of ticks. The position of the numbers is informative enough of
    # the position of the value.
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.xaxis.set_ticks_position('none')
    #ax.yaxis.set_ticks_position('none')

    # For remaining spines, thin out their line and change the black to a slightly off-black dark grey
    spines_to_keep = ['bottom', 'left']
    for spine in spines_to_keep:
        ax.spines[spine].set_linewidth(0.5)
        ax.spines[spine].set_color(almost_black)

    # shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.6, box.height])

    # Change the labels to the off-black
    ax.xaxis.label.set_color(almost_black)
    ax.yaxis.label.set_color(almost_black)

    # Change the axis title to off-black
    ax.title.set_color(almost_black)

    # Remove the line around the legend box, and instead fill it with a light grey
    # Also only use one point for the scatterplot legend because the user will 
    # get the idea after just one, they don't need three.
    #light_grey = np.array([float(248)/float(255)]*3)
    legend = ax.legend(rects[::-1], taxas[::-1], frameon=True, loc='center left', bbox_to_anchor=(1,0.5)) 
    #legend = ax.legend(lines, keys, loc = 'center left', bbox_to_anchor=(1,0.5))
    #legend = ax.legend(frameon=True)
    rect = legend.get_frame()
    #rect.set_facecolor(light_grey)
    rect.set_linewidth(0.0)


    # Change the legend label colors to almost black, too
    texts = legend.texts
    for t in texts:
        t.set_color(almost_black)
        t.set_fontsize('medium')
        t.set_weight('bold')

    ax.set_ylim((0,100.8))
    ### stuff for log scale
    #ax.set_yscale('symlog', linthreshy=0.1)
    #yticks = (0.1, 1, 10, 100)
    #yticks_str = [str(i) for i in yticks]
    #ax.set_yticks(yticks)
    #ax.set_yticklabels(yticks_str)

    # handling the ticks
    #majorLocator = AutoLocator()
    #minorLocator = MultipleLocator(10)
    #minorLocator = LogLocator(subs=[2,4,6,8])
    #minorLocator = AutoMinorLocator()
    #minorLocator = LinearLocator()
    #minorLocator = MaxNLocator(nbins=9)
    #ax.yaxis.set_major_locator(majorLocator)
    #ax.yaxis.set_minor_locator(minorLocator)

    #plt.savefig('{}.png'.format(outfile))
    plt.savefig('{}.pdf'.format(outfile))

if __name__ == '__main__':
    main()
