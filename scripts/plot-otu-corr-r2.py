#! /usr/bin/env python
# plot for R2 for OTU abundance of two samples
# by gjr; 04/07/14

"""
Plot for R2 for OTU abundance of two samples using OTU table (.shared file)

% python plot-otu-corr-r2.py \ 
                OTUabunCutoff \ 
                <file.shared> \ 
                <outfile> \ 
                "KW1,KW2" \ 
                "KW1,KW3"

Only two KeyWords "KW1,KW2" allowed for each pair 
"""

import sys, os
from collections import Counter
import numpy
from scipy import stats
import matplotlib
#matplotlib.use('Agg')
matplotlib.use('Pdf')
import matplotlib.pyplot as plt


almost_black='#262626'
shape_list = ['+', '.', 'x', 'v', 's']

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

def get_r2(xs, ys):
    """
    Get the R2 of xs and ys fitting to y = x
    defined here

    Parameters:
    -----------
    xs : list
        a list of abundance for each OTU
    ys : list
        a list of abundance for each OTU

    Returns:
    --------
    float
        R^2 of xs and ys
    """
    y_bar = numpy.average(ys)
    y_hat = xs  # fiting to y = x
    ss_reg = numpy.sum((y_hat - y_bar)**2)
    ss_tot = numpy.sum((ys - y_bar)**2)
    assert ss_reg <= ss_tot

    return ss_reg*1.0/ss_tot

def get_r2_scipy(xs, ys):
    """
    Get the R2 of xs and ys fitting to y = x
    using scipy

    Parameters:
    -----------
    xs : list
        a list of abundance for each OTU
    ys : list
        a list of abundance for each OTU

    Returns:
    --------
    float
        R^2 of xs and ys
    """

    slope, intercept, r_value, p_value, std_err = stats.linregress(xs, ys)
    return r_value**2

def main():
    if len(sys.argv) < 5:
        mes = ('Usage: python {} OTUabunCutoff <file.shared> <outfile> '
                 '"KW1,KW2" "KW1,KW3"\n'
                 'Only two KeyWords "KW1,KW2" allowed for each pair \n')
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    cnt = 0
    cutoff = int(sys.argv[1])
    fig, ax = plt.subplots(1)
    d_temp = readData(sys.argv[2])
    outfile = sys.argv[3]
    if outfile.lower().endswith('.pdf'):
        outfile = outfile[:-4]
    for kws in sys.argv[4:]:
        kw1, kw2 = kws.split(',')
        kw1 = kw1.strip()
        kw2 = kw2.strip()

        arr1 = numpy.array(d_temp[kw1], dtype=int)
        arr2 = numpy.array(d_temp[kw2], dtype=int)

        arr_sum = arr1 + arr2
        pairs = numpy.column_stack((arr1, arr2))

        #remove the pair both number are 0
        lis = []
        xrange = range(1, 50)
        for i in xrange:
            _pairs = pairs[arr_sum >= i]
            arr1, arr2 = _pairs.T
            if i == cutoff:
                # get corelation efficient
                label = '{}-{}'.format(kw1, kw2)
                #cor, p_val = stats.spearmanr(arr1, arr2)
                cor, p_val = stats.pearsonr(arr1, arr2)
                mes = '*** Normal scale: {} {:.3f} {:.3f}'
                print >> sys.stderr, mes.format(label, cor, p_val)

            # increase abundance by 1
            arr1 += 1
            arr2 += 1
            arr1 = numpy.log10(arr1)
            arr2 = numpy.log10(arr2)
            if i == cutoff:
                # get corelation efficient
                label = '{}-{}'.format(kw1, kw2)
                #cor, p_val = stats.spearmanr(arr1, arr2)
                cor, p_val = stats.pearsonr(arr1, arr2)
                mes = '*** Log scale: {} {:.3f} {:.3f}'
                print >> sys.stderr, mes.format(label, cor, p_val)

            r2 = get_r2_scipy(arr1, arr2)
            if i == 25:
                print >> sys.stderr, 'Cutoff: {} --> R2: {:.3f}'.format(i, r2)
                r2_25 = r2

            lis.append(r2)

        # scatter plot

        ax.scatter(xrange, lis, marker = shape_list[cnt],
                                   s = 25, lw = 1, 
                                   edgecolor=almost_black, facecolor='none',
                                 )

        cnt += 1

        idx = r'$R^2 = {:.2f}$'.format(r2_25)
        ax.annotate(idx, (25,r2_25), (25+2,r2_25-0.1), fontsize='medium')
        ax.axvline(x=25, color=almost_black)

    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
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

    ax.set_xlabel('OTU abundance threshold')
    ax.set_ylabel('R2')

    #plt.title(sys.argv[1])

    #plt.savefig('{}.otu_corr_r2.pdf'.format(outfile))
    plt.savefig('{}.pdf'.format(outfile))
    #plt.savefig('{}.OTUscat.png'.format(sys.argv[1]), dpi=300)

if __name__ == '__main__':
    main()
