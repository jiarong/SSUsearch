#!/usr/bin python

"""
Quality trimming for paired end reads: 
    1) remove read segment quality control indicator 
    2) discard reads with "N"

% python quality-trim-se.py phred <input_fastq_file> basename

phred is either 33 or 64

Output files are basename.1 and basename.2

"""

import sys
import os

import screed

#python quality-trim.py phred <input fastq file> basename
#MINLENGTH is the minimum lenth of read desired.
MINLENGTH = 30

def main():
    if len(sys.argv) != 4:
        mes = 'Usage: python {} phred <input fastq file> basename'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    print >> sys.stderr, ('This quality trimming script does not handle fasta'
                          'seqs as input (requiring quality score)')
    print >> sys.stderr, ('Output two files in current directory: fileout.1'
                          ' and fileout.2')

    phred = int(sys.argv[1])
    filein = sys.argv[2]
    fileout = sys.argv[3]

    assert phred in [33, 64], '*** phred score should be either 33 or 64'
    if phred == 33:
        bad_q = '#'
    else:
        bad_q = 'B'

    fw1 = open(fileout+'.1', 'wb')
    fw2 = open(fileout+'.2', 'wb')
    fw3 = open(fileout+'.singleton', 'wb')

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

        ### trim 'B's or '#'s at end
        trim = accuracy.find(bad_q)
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
            count2 += 1
            trigger = False
            fw2.write('@%s\n%s\n+\n%s\n' % (name, sequence, accuracy)) #fastq output
            fw1.write('@%s\n%s\n+\n%s\n' % (tempName, tempSeq, tempAcc)) #fastq output

        else:
            if not trigger:
                trigger = True

            else:
                fw3.write('@%s/3\n%s\n+\n%s\n' % (tempName.rsplit('/',1)[0], tempSeq, tempAcc)) #fastq output

            tempSeq = sequence
            tempAcc = accuracy
            tempName=name
            tempCount=count

        count += 1

    fw1.close()
    fw2.close()
    fw3.close()

    print 'Original Number of Reads', n + 1
    print 'Final Number of Reads', count
    print 'Total Filtered', n + 1  - int(count)
    print 'Number of pairs of pairedEndRead', count2
    print 'Number of singletons', int(count)-2*count2

if __name__ == '__main__':
    main()
