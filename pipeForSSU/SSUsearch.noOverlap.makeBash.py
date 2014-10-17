#! /usr/bin/env python
# make the bash files to ssu search pipe
# by gjr; Jan 26, 12

import sys
import os

'''
usage: python <thisFile><sampleDir>
'''

sampleDir = sys.argv[1]
sampleList = os.listdir(sampleDir)

for fName in sampleList:
    # bash files saved in the current dir
    f = sampleDir.rstrip('/')+'/'+fName 
    sample = fName.rstrip('.bz2').rstrip('.gz').rstrip('.fq').rstrip('.fastq')
    outDir = f+'.out'
    fw = open('%s.sh' %sample, 'w')

    # make bash file
    print >> fw, '#! /bin/bash'
    print >> fw, '#PBS -q main'
    print >> fw, '#PBS -l nodes=1:ppn=1,walltime=48:00:00'
    print >> fw, '#PBS -l mem=6gb'

    print >> fw, 'TERM=linux'
    print >> fw, 'export TERM'
    print >> fw, 'mkdir %s' %(outDir)
    print >> fw, 'cd %s' %(outDir)
    print >> fw, 'cleanup_script()'
    print >> fw, '{'
    print >> fw, "  echo 'Error, cleaning up..'"
    print >> fw, '  cd ..'
    print >> fw, '  rm -rf %s.out' %(f) 
    print >> fw, '}'
    print >> fw, "#trap 'cleanup_script' ERR"
    print >> fw, 'set -e'
    print >> fw, '# turn -x on if DEBUG is set to a non-empty string'
    print >> fw, '[ -n "$DEBUG" ] && set -x'

    print >> fw, "echo 'data filter..'"
    print >> fw, 'time('
    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/quality-trim-noSep.py %s' %(f)
    print >> fw, "echo 'separate pair-ends done..'"
    print >> fw, ')'

    print >> fw, "echo 'filter done..'"

    print >> fw, 'time python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/makeFastaForDNAHmmer.py %s/%s.filtered' %(outDir, fName)
    print >> fw, "echo 'reverse complement added for hmmsearch..'"


    print >> fw, "echo 'start hmmsearch'"
    print >> fw, 'time /mnt/home/guojiaro/Documents/software/hmmer3.0b3/./hmmsearch --incE 10 --incdomE 10 -A %s/%s.SSU.sto -o %s/%s.SSU.hmmout --tblout %s/%s.SSU.hmmtblout --domtblout %s/%s.SSU.hmmdomtblout /mnt/scratch/gjr/data/hmms/SSU.hmm %s/%s.filtered.RCaddedForHmmer' %(outDir, sample, outDir, sample, outDir, sample, outDir, sample, outDir, fName)
    print >> fw, "echo 'hmmsearch done'"

    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/parseHMMgetSeq.py %s/%s.SSU.hmmdomtblout %s/%s.SSU.sto' %(outDir, sample, outDir, sample)
    #print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/parseHMMgetSeq2.py %s/%s.SSU.hmmdomtblout %s/%s.filtered.RCaddedForHmmer %s/%s.SSU.fa' %(outDir, sample, outDir, sample, outDir, fName)
    print >> fw, 'rm  %s/%s.filtered.RCaddedForHmmer' %(outDir, fName)
    print >> fw, "echo 'hmm filter and MSA conversion done..'"

    print >> fw, "echo 'start mothur align'"
    print >> fw, 'time /mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#align.seqs(candidate=%s/%s.SSU.fa, template=/mnt/home/guojiaro/Documents/data/RefDB/silva.ssu.fasta, search=suffix, threshold=0.5, flip=t, processors=1)"' %(outDir, sample)
    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/mothurAlignReportParser.py  %s/%s.SSU.align.report  %s/%s.SSU.align' %(outDir, sample, outDir, sample)

    print >> fw, 'cat /mnt/home/guojiaro/Documents/data/16s_ecoli_J01695.afa  %s/%s.SSU.align.badSeqsFiltered > %s/%s.SSU.align.badSeqsFiltered.RFadded' %(outDir, sample, outDir, sample)
    #
    # pay att to the ave read len: 75, 100 , 125; minLen are 2/3 of ave len;
    #
    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/regionCut.py  %s/%s.SSU.align.badSeqsFiltered.RFadded 971 1046 50' %(outDir, sample)
    print >> fw, 'mv  %s/%s.SSU.align.badSeqsFiltered.RFadded.971to1046.cut.lenScreened.afa %s' %(outDir, sample, sample)
    print >> fw, "echo 'ready for clustering ..'"


print 'pay att to the ave read len: 75, 100 , 125; minLen are 2/3 of ave len'
print 'do not forget to change files name in next mv command line'
