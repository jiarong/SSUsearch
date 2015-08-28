#! /usr/bin/env python
# plot for OTU scatter plot for two samples
# by gjr; 04/06/14

"""
Plot for OTU scatter plot for two samples using OTU table (.shared file)

% python plot-otu-corr-scatter.py <file.shared> <outfile> "KW1,KW2"

Only two KeyWords allowed: "KW1,KW2"
"""

import sys, os
from collections import Counter
import numpy as np
import matplotlib
#matplotlib.use('Agg')
matplotlib.use('Pdf')
import matplotlib.pyplot as plt


almost_black='#262626'

def readData(f):
    """
    Parse OTU table (.shared file)

    Parameters:
    -----------
    f : str
        file name of .shared file

    Returns:
    --------
    dict
        a dictionary with sample label as key (str)
        and a list of abundance for each OTU as value (list)
    """
    container = {}
    for n, line in enumerate(open(f)):
        if line.startswith('#'):
            print >> sys.stderr, 'row header detected: %s' %line
            continue
        lis = line.rstrip().split('\t')
        container[lis[1]] = lis[3:]
    return container

def main():
    if len(sys.argv) != 4:
        mes = ('Usage: python {} <file.shared> <outfile> "KW1,KW2" \n'
               'Only two KeyWords allowed: "KW1,KW2" \n')
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    kw1, kw2 = [kw.strip() for kw in sys.argv[3].split(',')]
    outfile = sys.argv[2]
    if outfile.lower().endswith('.pdf'):
        outfile = outfile[-4:]

    d_temp = readData(sys.argv[1])
    arr1 = np.array(d_temp[kw1], dtype=int)
    arr2 = np.array(d_temp[kw2], dtype=int)

    arr_sum = arr1 + arr2
    pairs = np.column_stack((arr1, arr2))

    #remove the pair both number are 0
    pairs = pairs[arr_sum > 0]

    # convert to tuple for Counter
    pairs_tup = [tuple(i) for i in pairs]
    uniq_pairs_d = Counter((pairs_tup))
    _items = uniq_pairs_d.items()
    uniq_pairs, marker_sizes = zip(*_items)

    marker_sizes = np.array(marker_sizes) * 2

    _lis1, _lis2 = zip(*uniq_pairs)
    arr1 = np.array(_lis1)
    arr2 = np.array(_lis2)
    
    # replace 0 with 1 for log scale
    #arr1[arr1 == 0] = 1
    #arr2[arr2 == 0] = 1

    # increase each OTU abundance in each sample by one
    arr1 = arr1 + 1
    arr2 = arr2 + 1

    # scatter plot
    fig, ax = plt.subplots(1)

    rect_main = ax.scatter(arr1, arr2, marker = 'o',
                               s = marker_sizes, lw = 1, 
                               edgecolor=almost_black, facecolor='none')

    ax.set_ylim(ymin=0.8)
    ax.set_xlim(xmin=0.8)
    ax.loglog()
    # Remove top and right axes lines ("spines")
    spines_to_remove = ['top', 'right']
    for spine in spines_to_remove:
        ax.spines[spine].set_visible(False)

    # Get rid of ticks. The position of the numbers is informative enough of
    # the position of the value.
    #ax.xaxis.set_ticks_position('none')
    #ax.yaxis.set_ticks_position('none')
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # For remaining spines, thin out their line and change the black to a slightly off-black dark grey
    spines_to_keep = ['bottom', 'left']
    for spine in spines_to_keep:
        ax.spines[spine].set_linewidth(0.5)
        ax.spines[spine].set_color(almost_black)

    ax.set_xlabel(kw1)
    ax.set_ylabel(kw2)


    # Remove the line around the legend box, and instead fill it with a light grey
    # Also only use one point for the scatterplot legend because the user will 
    # get the idea after just one, they don't need three.
    #light_grey = np.array([float(248)/float(255)]*3)
    #legend = ax.legend(frameon=True, scatterpoints=1)
    #legend = ax.legend(frameon=True, scatterpoints=1, ncol=2, loc='lower center')
    #rect = legend.get_frame()
    #rect.set_facecolor(light_grey)
    #rect.set_linewidth(0.0)


    # Change the legend label colors to almost black, too
    #texts = legend.texts
    #for t in texts:
    #    t.set_color(almost_black)
    #    t.set_fontsize('small')
    #    t.set_weight('bold')


    #plt.title(sys.argv[1])
    #plt.savefig('{}.{}vs{}.otu_corr.pdf'.format(outfile, kw1, kw2))
    plt.savefig('{}.pdf'.format(outfile))
    #plt.savefig('%s.OTUscat.png' %(sys.argv[1]), dpi=300)

if __name__ == '__main__':
    main()
