#!/usr/bin python

import sys
import os
#insert the path of screed
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed

# python quality-trim.py <input fastq file> <output filtered fastq or fasta file>
# MINLENGTH is the minimum lenth of read desired.
MINLENGTH = 30

print >> sys.stderr, 'This quality trimming script does not handle fasta seqs as input'
filein = sys.argv[1]
# output two files in current directory: fileout.1 and fileout.2
fileout = os.path.basename(filein)
# to implement: assert sys.argv[3] in ['fasta','fastq'], 'select fasta or fastq'

fw = open(fileout+'.filtered', 'w')

count=0

for n, record in enumerate(screed.open(filein)):
    name = record['name']
    sequence = record['sequence']
    accuracy = record['accuracy']

    ###remove chunks of Ns at the beginning(not common)
    #sequence = sequence.lstrip('N')
    ### do not need accuracy info further
    #accuracy = accuracy[-len(sequence):]

    ### trim 'B's at end
    trim = accuracy.find('B')
    if (trim+1) > MINLENGTH:
        sequence = sequence[:trim]
        accuracy = accuracy[:trim]
    elif (trim+1) == 0:
        if len(sequence) < MINLENGTH:
            continue
        else:
            pass
    else:
        continue

    #remove reads with Ns in middle
    if 'N' in sequence:
        continue

    fw.write('@%s\n%s\n+\n%s\n' % (name, sequence, accuracy)) #fastq output

    count += 1

    if n % 10000 == 0:
        print 'scanning', n


fw.close()
print 'Original Number of Reads', n + 1
print 'Final Number of Reads', count
print 'Total Filtered', n + 1  - int(count)
