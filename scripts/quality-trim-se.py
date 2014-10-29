#!/usr/bin python

import sys
import os

import screed

#python quality-trim.py phred <input fastq file> basename
#MINLENGTH is the minimum lenth of read desired.
MINLENGTH = 30

def main():
    if len(sys.argv) != 4:
        mes = 'Usage: python {} phred <input fastq file> <outfile>'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    print >> sys.stderr, ('This quality trimming script does not handle fasta'
                          'seqs as input (requiring quality score)')

    phred = int(sys.argv[1])
    filein = sys.argv[2]
    fileout = sys.argv[3]

    assert phred in [33, 64], '*** phred score should be either 33 or 64'
    if phred == 33:
        bad_q = '#'
    else:
        bad_q = 'B'


    count = 0
    with open(fileout, 'wb') as fw:
        for n, record in enumerate(screed.open(filein)):
            name = record['name']
            sequence = record['sequence']
            accuracy = record['accuracy']

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

            fw.write('@%s\n%s\n+\n%s\n' % (name, sequence, accuracy))
            count += 1

    print >> sys.stderr, 'Original Number of Reads: %d'  %(n + 1)
    print >> sys.stderr, 'Final Number of Reads: %d' %(count)
    print >> sys.stderr, 'Total Filtered: %d'  %(n + 1 - count)

if __name__ == '__main__':
    main()
