#! /usr/bin/env python
# plot for PCoA for qiime
# sample name format "T1M7"
# by gjr; 021514

import sys, os
import matplotlib
#matplotlib.use('Agg')
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import numpy as np
import brewer2mpl
import pandas

# Get "Set2" colors from ColorBrewer (all colorbrewer scales: http://bl.ocks.org/mbostock/5577023)
paired = brewer2mpl.get_map('Paired', 'qualitative', 8).mpl_colors
almost_black='#262626'

shapeLis = ['o', 's', 'v', 'd']
colorLis = paired    # color
colorBooLis = [True, False]

def main():
    if len(sys.argv) != 5:
        print >> sys.stderr, \
               'Usage: python %s "file1.pcoa,file2.pcoa.." "tag1,tag2,.." '\
                  '"KW1,KW2,.." <outfile>\n'\
                 %(os.path.basename(sys.argv[0]))
        sys.exit(1)

    fLis = [f.strip() for f in sys.argv[1].split(',')]
    tagLis = [tag.strip() for tag in sys.argv[2].split(',')]
    fTagLis = zip(fLis, tagLis)
    KWLis = [kw.strip() for kw in sys.argv[3].split(',')]
    outfile = sys.argv[4]
    if outfile.lower().endswith('.pdf'):
        outfile = outfile[:-4]

    if len(fLis) > len(shapeLis):
        print >> sys.stderr, 'more shapes are needed in shapeLis'
        sys.exit(1)

    dShape = dict(zip(fLis, shapeLis))
    dColorBoo=dict(zip(KWLis, colorBooLis))
    xvars = []
    yvars = []
    
    fig, ax = plt.subplots(1)
    dLeg = {}  # for collecting one shape for keyword
    repSt = set()

    for f, tag in fTagLis:
        df = pandas.read_csv(f, sep='\t', index_col='pc vector number')
        df = df.dropna(how='all')
        # only first two dimensions
        dfx = df[[0,1]]
        # % variation explained
        xvar, yvar = dfx.ix[-1]
        xvars.append(xvar)
        yvars.append(yvar)
        # skip last two: eigvals and variation explained
        dfx = dfx.ix[:-2]

        for idx in dfx.index:
            # use hard coding due to bad name format
            # use facecolor to diff loc variable


            kw = idx[0]  # hardCode, index should be the position of kw in name
            key = idx[0]
            key2 = int(idx[1]) - 1
            repSt.add(key2)
            eColor = colorLis[key2]
            if dColorBoo[kw]:
                fColor = eColor
            else:
                fColor = 'none'

            legKey = '%s_%s' %(tag, key)
            assert kw in KWLis, '%s is not in %s' %(kw, sys.argv[3])
            

            x, y = dfx.ix[idx]
            tempP = ax.scatter(x, y, marker=dShape[f], 
                                s = 50, lw = 1,
                                edgecolor=eColor,
                                facecolor=fColor)

            ### treatment info in leg
            #if not dLeg.has_key(legKey):
            if key2 == 0:  # rep 1
                dLeg[legKey] = tempP
            

            #ax.annotate(idx, (x,y), (x,y), fontsize='x-small')
            #ax.annotate(key, (x,y), (x,y), fontsize='x-small')


    # put on lengend for three shapes
    pairs = sorted(dLeg.items())
    kws, ps = zip(*pairs)

    box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width*0.75, box.height*0.75])
    ax.set_position([box.x0, box.y0, box.width, box.height*0.8])

    #legend = ax.legend(ps, kws, frameon=True, scatterpoints=1)
    legend = ax.legend(ps, kws, frameon=False, scatterpoints=1, ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.2))

    # set up the lengend using another artist
    legendProxies = []
    repLis = list(repSt)
    repLis = sorted(repLis)
    repTagLis = ['Rep{}'.format(i) for i in repLis]
    for i in repLis:
        c = colorLis[i]
        legendProxies.append(plt.Rectangle((0,0), 0.25, 0.25, fc=c, ec='None'))

    #legend2 = ax.legend(legendProxies, repTagLis, frameon=False, scatterpoints=1, ncol=1, loc='center right', bbox_to_anchor=(1.2, 0.5), prop={'size':'small'})

    #plt.gca().add_artist(legend)

    # Remove top and right axes lines ("spines")
    spines_to_remove = ['top', 'right']
    for spine in spines_to_remove:
        ax.spines[spine].set_visible(False)

    # Get rid of ticks. The position of the numbers is informative enough of
    # the position of the value.
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # For remaining spines, thin out their line and change the black to a slightly off-black dark grey
    spines_to_keep = ['bottom', 'left']
    for spine in spines_to_keep:
        ax.spines[spine].set_linewidth(0.5)
        ax.spines[spine].set_color(almost_black)

    ax.set_xlabel('%s (%.f%%)' %('PC1', np.average(xvars)))
    ax.set_ylabel('%s (%.f%%)' %('PC2', np.average(yvars)))


    # Remove the line around the legend box, and instead fill it with a light grey
    # Also only use one point for the scatterplot legend because the user will 
    # get the idea after just one, they don't need three.
    light_grey = np.array([float(248)/float(255)]*3)
    #rect = legend.get_frame()
    #rect.set_facecolor(light_grey)
    #rect.set_linewidth(0.0)


    # Change the legend label colors to almost black, too
    texts = legend.texts
    for t in texts:
        t.set_color(almost_black)
        t.set_fontsize('small')
        t.set_weight('bold')

    #plt.title(sys.argv[1])
    plt.savefig('%s.pdf' %(outfile))
    #plt.savefig('%s.pdf' %('+'.join(tagLis)))
    #plt.savefig('%s.png' %(sys.argv[1]), dpi=300)

if __name__ == '__main__':
    main()
