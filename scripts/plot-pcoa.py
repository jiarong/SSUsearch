#! /usr/bin/env python
# plot for PCoA for qiime
# sample name format "T1M7"
# by gjr; 021514

import sys, os
import matplotlib
matplotlib.use('Agg')
#matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import numpy as np
import brewer2mpl
import pandas

almost_black = '#262626'
def main():
    if len(sys.argv) != 4:
        print >> sys.stderr, \
       'Usage: python %s <file.pcoa.axis> <file.pcoa.loadings> <outfile>'\
                         %(os.path.basename(sys.argv[0]))
        sys.exit(1)

    outfile = sys.argv[3]
    if outfile.lower().endswith('.png'):
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

    for idx in dfx.index:
        x, y = dfx.ix[idx]
        tempP = ax.scatter(x, y, s = 50, lw = 1, facecolor='none')

        ax.annotate(idx, (x,y), (x,y), fontsize='small')


    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height*0.8])


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

    #plt.title(sys.argv[1])
    plt.savefig('%s.png' %(outfile))
    #plt.savefig('%s.pdf' %(sys.argv[1]))
    #plt.savefig('%s.png' %(sys.argv[1]), dpi=300)

if __name__ == '__main__':
    main()
