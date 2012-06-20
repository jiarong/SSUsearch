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

fw1 = open(fileout+'.1', 'w')
fw2 = open(fileout+'.2', 'w')
fw3 = open(fileout+'.singleton', 'w')

count=0
count2=0
tempName=''
tempCount=None
tempSeq = None
tempAcc = None
trigger = False

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

    if tempName.rsplit('/',1)[0] == name.rsplit('/',1)[0]:
        # better to keep original name
        ##tag = name.split(':',1)[0]
        count2 += 1
        trigger = False
        #fw2.write('>%d:%s/2\n%s\n' % (tempCount,tag, sequence)) #fasta output
        #fw1.write('>%d:%s/1\n%s\n' % (tempCount,tag, tempSeq)) #fasta output
        #fw2.write('@%d:%s/2\n%s\n+\n%s\n' % (tempCount, tag, sequence, accuracy)) #fastq output
        fw2.write('@%s\n%s\n+\n%s\n' % (name, sequence, accuracy)) #fastq output
        #fw1.write('@%d:%s/1\n%s\n+\n%s\n' % (tempCount, tag, tempSeq, tempAcc)) #fastq output
        fw1.write('@%s\n%s\n+\n%s\n' % (tempName, tempSeq, tempAcc)) #fastq output

    else:
        #trigger == False
        if not trigger:
            trigger = True

        #trigger == True, write the singleton (end with /3)
        else:
            #tag = tempName.split(':',1)[0]
            #fw3.write('>%d:%s/3\n%s\n' %(tempCount, tag, tempSeq)) #fasta output
            #fw3.write('@%d:%s/3\n%s\n+\n%s\n' % (tempCount, tag, tempSeq, tempAcc)) #fastq output
            fw3.write('@%s/3\n%s\n+\n%s\n' % (tempName.rsplit('/',1)[0], tempSeq, tempAcc)) #fastq output

        tempSeq = sequence
        tempAcc = accuracy
        tempName=name
        tempCount=count

    count += 1

    if n % 10000 == 0:
        print 'scanning', n


fw1.close()
fw2.close()
fw3.close()
print 'Original Number of Reads', n + 1
print 'Final Number of Reads', count
print 'Total Filtered', n + 1  - int(count)
print 'Number of pairs of pairedEndRead', count2
print 'Number of singletons', int(count)-2*count2
