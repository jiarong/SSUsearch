#! /usr/bin/env python
# make rarefaction plot for version 1.32.1
# by gjr

import sys, os

import numpy
import matplotlib
matplotlib.use('Agg')
#matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

def readData(f):
    for n, line in enumerate(open(f)):
        if n==0 and line.startswith('numsampled'):
            print >> sys.stderr, 'row header detected: %s' %line
            continue
        x, sample, _, y, up, low = line.rstrip().split('\t')
        x = float(x)
        y = float(y)
        yield sample, x, y

def main():
    if len(sys.argv) != 7:
        print >> sys.stderr, \
           'usage: python %s '\
           'cutoff "divInd1,divInd2.." "kw1,kw2.." ' \
           '"<V2.groups.summary>,<V4.groups.summary>.." '\
           '"V2,V4.." '\
           '<outfile> '\
            %(os.path.basename(sys.argv[0]))

        print >> sys.stderr, 'divInd: chao, ace, shannon, invsimpson'
        print >> sys.stderr, 'summary file group can have more than 2 files'
        print >> sys.stderr, 'argv[4] and argv[5] should have same lenght \n'
        sys.exit(1)

    cutoff = sys.argv[1]
    divInds = [ind.strip() for ind in sys.argv[2].split(',')]
    if not set(divInds).issubset(set(['chao', 'ace',
                                        'shannon', 'invsimpson'])):
        print >> sys.stderr, 'divInd: chao, ace, shannon, invsimpson'
        sys.exit(1)

    Kws = sys.argv[3].split(',')
    f_lis = sys.argv[4].split(',')
    f_labels = sys.argv[5].split(',')
    outfile = sys.argv[6]
    if outfile.lower().endswith('.pdf'):
        outfile = outfile[:-4]

    Kws = [kw.strip() for kw in Kws]
    f_lis = [f.strip() for f in f_lis]
    f_labels = [f.strip() for f in f_labels]

    numInd = len(divInds)
    fig = plt.figure()
    subPlotNum = 1

    for divInd in divInds:
        ax = fig.add_subplot(1, numInd, subPlotNum)
        subPlotNum += 1
        f_container = []
        for f in f_lis:
            arr = numpy.genfromtxt(f,
                    dtype=None, delimiter='\t', names=True)
            keys = arr.dtype.names

            container = []
            lis = zip(arr['label'], arr['group'], arr[divInd])

            for Kw in Kws:
                dataLis = []
                for row in lis:
                    if row[0] != cutoff:
                        continue
                    if Kw not in row[1]:
                        continue
                    dataLis.append(row[2])
                    #print >> sys.stderr, '%s collected' %(row[1])

                sampNum = len(dataLis)
                print >> sys.stderr, '%d samples collect for Kw %s' %(sampNum, Kw)
                mean = numpy.mean(dataLis)
                std = numpy.std(dataLis)
                ste = std/numpy.sqrt(sampNum)
                container.append((Kw, mean, ste))

            f_container.append(container) 


        f_num = len(f_labels)
        samp_num = len(Kws)
        margin = 0.1
        width = (1.-2.*margin)/samp_num * (2.0/3)
        xs = numpy.arange(f_num)
        xs = xs + margin


        almost_black = '#262626'
        color = 0.2
        step = (0.8- color)/(samp_num-1)

        # f_container
        #[[(V2_lable1,V2_mean1,V2_ste1),(V2_label2,V2_mean2,V2_ste2)],
        #       [(V4_lable1,V4_mean1,V4_ste1),(V4_label2,V4_mean2,V4_ste2)]]

        lis_per_label = zip(*f_container)
        #[[(V2_lable1,V2_mean1,V2_ste1),(V4_label1,V4_mean1,V4_ste1)],
        #       [(V2_lable2,V2_mean2,V2_ste2),(V4_label2,V4_mean2,V4_ste2)]]
        for lis in lis_per_label:
            labels, means, stes = zip(*lis)
            assert len(set(labels)) == 1, \
                  'labels: %s should be the same label' %(','.join(labels))

            label = labels[0]
            rects = ax.bar(xs, means, width, yerr=stes, ecolor='k', color='%.2f' %color, label=label)
            color +=  step
            xs += width

        ax.set_ylabel('%s' %(divInd), fontsize='large')
        xticks = (xs+xs-samp_num*width)/2
        ax.set_xticks(xticks)
        ax.set_xticklabels(f_labels, fontsize='large')

        # Remove top and right axes lines ("spines")
        spines_to_remove = ['top', 'right']
        for spine in spines_to_remove:
            ax.spines[spine].set_visible(False)

        # Get rid of ticks. The position of the numbers is informative enough of
        # the position of the value.
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')

        # Change the labels to the off-black
        ax.xaxis.label.set_color(almost_black)
        ax.yaxis.label.set_color(almost_black)

        # Change the axis title to off-black
        ax.title.set_color(almost_black)

        # For remaining spines, thin out their line and change the black to a slightly off-black dark grey
        spines_to_keep = ['bottom', 'left']
        for spine in spines_to_keep:
            ax.spines[spine].set_linewidth(0.5)
            ax.spines[spine].set_color(almost_black)

        light_grey = numpy.array([float(248)/float(255)]*3)
        #legend = plt.figlegend(rects, keyWords, loc='upper right', frameon=True) 
        legend = ax.legend(loc = 'upper right')
        rect = legend.get_frame()
        #rect.set_facecolor(light_grey)
        rect.set_linewidth(0.0)


    fig.set_tight_layout(True)
    #plt.savefig('%s.png' %(sys.argv[1]))
    #plt.savefig('%s.div_index.pdf' %('+'.join(f_labels)))
    #plt.savefig('%s.pdf' %(outfile))
    plt.savefig('%s.png' %(outfile))

if __name__ == '__main__':
    main()
