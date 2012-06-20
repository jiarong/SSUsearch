#! /usr/bin python
# plot for PCoA or NMDS
# by gjr; Feb 22, 12

import sys
import matplotlib
matplotlib.use('Agg')
#matplotlib.use('Pdf')
import matplotlib.pyplot as plt

cnt = 0
for line in open(sys.argv[1]):
    line = line.strip()
    if not line:
        continue
    if (cnt == 0 and line.split('\t') == ['axis1', 'axis2']):
        print 'reading NMDS output..'
        continue

    sample, x, y = line.split('\t')
    global coo
    global mm
    coo = 'blue'
    mm = 'o'
    #if 'Wheat' or 'Corn' in sample:
    if 'MSB' in sample:
        #coo = 'blue'
        pass
    #if 'Prairie' in sample:
    if 'MSR' in sample:
        coo = 'green'

    #if 'corn' in sample:
    if 'SG' in sample:
        mm = '+'
    '''
    if 'pra' in sample:
        mm = 'x'
        coo = 'green'
    '''

    x = float(x)
    y = float(y)
    plt.scatter(x, y, label=sample, marker=mm, color=coo, linestyle='solid')
    cnt += 1

'''
leg = plt.legend(loc='center left', bbox_to_anchor=(1,0.5), shadow = True, borderpad = 0.1)
for t in leg.get_texts():
    t.set_fontsize('small')
for l in leg.get_lines():
    l.set_linewidth(5) 
'''
plt.title(sys.argv[1])
#plt.savefig('%s.pdf' %(sys.argv[1]))
plt.savefig('%s.png' %(sys.argv[1]))
