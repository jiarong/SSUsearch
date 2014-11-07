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
set2 = brewer2mpl.get_map('Set2', 'qualitative', 4).mpl_colors
almost_black='#262626'

shapeLis = ['o', 's', 'v']
colorLis = set2

treatLis = ['PT', '']               ### use list with 2 elements for 2 treats
#treatLis = []                        ### use empty list for b & w figure
dColor=dict(zip(treatLis, colorLis))

def main():
    if len(sys.argv) != 5:
        print >> sys.stderr, \
       'Usage: python %s <file.pcoa.axis> <file.pcoa.loadings> '\
                        '"KW1,KW2,.." <outfile>'\
                         %(os.path.basename(sys.argv[0]))
        sys.exit(1)

    KWLis = [kw.strip() for kw in sys.argv[3].split(',')]
    # 3, C, 22
    if len(KWLis) > len(shapeLis):
        print >> sys.stderr, 'more shapes are needed in shapeLis'
        sys.exit(1)

    dShape = dict(zip(KWLis, shapeLis))
    
    outfile = sys.argv[4]
    if outfile.lower().endswith('.pdf'):
        outfile = outfile[:-4]

    df = pandas.read_csv(sys.argv[1], sep='\t', index_col=False)
    #df = pandas.read_csv(sys.argv[1], sep='\t')

    df = df.set_index('group', drop=True, append=False)
    df = df.dropna(how='all')
    # only first two dimensions
    dfx = df[[0,1]]
    # % variation explained
    df2 = pandas.read_csv(sys.argv[2], sep='\t', index_col='axis')
    xvar = df2.loc[1]
    yvar = df2.loc[2]


    # plot
    fig, ax = plt.subplots(1)
    dLeg = {}  # for collecting one shape for keyword

    for idx in dfx.index:
        # use hard coding due to bad name format
        # use facecolor to diff loc variable
        fColor = 'none'
        kw = idx[0]  # hardCode, index should be the position of kw in name
        key = idx[0]

        # if there are treatments, e.g. Oct and Jul, or SG and PT
        checkS = False
        if treatLis:
            if treatLis[0] in idx:
                loc=treatLis[0]
                checkS = True
            else:
                assert treatLis[1] in idx
                loc=treatLis[1]
            eColor = dColor[loc]
            if loc:  # not empty string
                legKey = '%s_%s' %(key, loc)
            else:
                legKey = key

        else:
            checkS = True
            eColor = almost_black
            legKey = idx[0] + idx[2:]   # hard coded take C_PT  from C1_PT

        assert kw in KWLis, '%s is not in %s' %(kw, sys.argv[3])
        x, y = dfx.ix[idx]
        tempP = ax.scatter(x, y, marker=dShape[kw], 
                            s = 50, lw = 1,
                            edgecolor=eColor,
                            facecolor=fColor)

        ### not treatment info in leg
        #if not dLeg.has_key(kw):
        #    if checkS:
        #        dLeg[kw] = tempP

        ### treatment info in leg
        if not dLeg.has_key(legKey):
            dLeg[legKey] = tempP
        

        #ax.annotate(idx, (x,y), (x,y), fontsize='x-small')
        #ax.annotate(key, (x,y), (x,y), fontsize='x-small')


    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height*0.8])

    # put on lengend for three shapes
    pairs = sorted(dLeg.items())
    kws, ps = zip(*pairs)
    #legend = ax.legend(ps, kws, frameon=True, scatterpoints=1)
    legend = ax.legend(ps, kws, frameon=True, scatterpoints=1, ncol=4, loc='upper center', bbox_to_anchor=(0.5,1.2))

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

    ax.set_xlabel('%s (%.f%%)' %('PC1', xvar))
    ax.set_ylabel('%s (%.f%%)' %('PC2', yvar))


    # Remove the line around the legend box, and instead fill it with a light grey
    # Also only use one point for the scatterplot legend because the user will 
    # get the idea after just one, they don't need three.
    light_grey = np.array([float(248)/float(255)]*3)
    rect = legend.get_frame()
    rect.set_facecolor(light_grey)
    rect.set_linewidth(0.0)


    # Change the legend label colors to almost black, too
    texts = legend.texts
    for t in texts:
        t.set_color(almost_black)
        t.set_fontsize('small')
        t.set_weight('bold')


    #plt.title(sys.argv[1])
    plt.savefig('%s.pdf' %(outfile))
    #plt.savefig('%s.pdf' %(sys.argv[1]))
    #plt.savefig('%s.png' %(sys.argv[1]), dpi=300)

if __name__ == '__main__':
    main()
