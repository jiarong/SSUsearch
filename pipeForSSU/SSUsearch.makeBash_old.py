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

    print >> fw, "echo 'data filter and pair ends assembly:'"
    print >> fw, 'time('
    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/quality-trim-sepPairEnds.py %s' %(f)
    print >> fw, "echo 'separate pair-ends done..'"

    print >> fw, '/mnt/home/guojiaro/Documents/software/flash_v1.0.2/./flash %s %s -m 10 -M 120 -x 0.20 -p 33 -o %s -r 140 -f 250 -s 25 -d %s' %(outDir+'/'+fName+'.1', outDir+'/'+fName+'.2', sample, outDir)

    print >> fw, 'rm %s %s' % (outDir+'/'+fName+'.1', outDir+'/'+fName+'.2')

    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/sumFlashOut.py %s %s > %s/flashOut.sum' %(sample, outDir, outDir)
    print >> fw, "echo 'merge by flash done..'"

    print >> fw, 'cat %s/%s.extendedFrags.fastq %s/%s.notCombined_1.fastq %s/%s.notCombined_2.fastq > %s/%s.afterMerge.fastq' %(outDir, sample, outDir, sample, outDir, sample, outDir, sample) 
    print >> fw, 'rm %s/%s.extendedFrags.fastq %s/%s.notCombined_1.fastq %s/%s.notCombined_2.fastq' %(outDir, sample, outDir, sample, outDir, sample) 
    print >> fw, "echo 'combine assembled and unassembled done..'"

    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/makeFastaForDNAHmmer.py %s/%s.afterMerge.fastq' %(outDir, sample)
    print >> fw, "echo 'reverse complement added for hmmsearch..'"
    print >> fw, ')'

    print >> fw, "echo 'start hmmsearch'"
    print >> fw, 'time /mnt/home/guojiaro/Documents/software/hmmer3.0b3/./hmmsearch --incE 10 --incdomE 10 -A %s/%s.afterMerge.SSU.sto -o %s/%s.afterMerge.SSU.hmmout --tblout %s/%s.afterMerge.SSU.hmmtblout --domtblout %s/%s.afterMerge.SSU.hmmdomtblout /mnt/scratch/gjr/data/hmms/SSU.hmm %s/%s.afterMerge.fastq.RCaddedForHmmer' %(outDir, sample, outDir, sample, outDir, sample, outDir, sample, outDir, sample)
    print >> fw, "echo 'hmmsearch done'"

    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/parseHMMgetSeq.py %s/%s.afterMerge.SSU.hmmdomtblout %s/%s.afterMerge.SSU.sto' %(outDir, sample, outDir, sample)
    #print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/parseHMMgetSeq2.py %s/%s.afterMerge.SSU.hmmdomtblout %s/%s.afterMerge.fastq.RCaddedForHmmer %s/%s.afterMerge.SSU.fa' %(outDir, sample, outDir, sample, outDir, sample)
    print >> fw, 'rm %s/%s.afterMerge.fastq %s/%s.afterMerge.fastq.RCaddedForHmmer' %(outDir, sample, outDir, sample)
    print >> fw, "echo 'hmm filter and MSA conversion done..'"

    print >> fw, 'cat /mnt/home/guojiaro/Documents/data/16s_ecoli_J01695_online.fa  %s/%s.afterMerge.SSU.fa > %s/%s.afterMerge.SSU.RFadded.fa' %(outDir, sample, outDir, sample)

    print >> fw, "#echo 'start mothur align'"
    print >> fw, '#time /mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#align.seqs(candidate=%s/%s.afterMerge.SSU.RFadded.fa, template=/mnt/home/guojiaro/Documents/data/RefDB/silva.ssu.fasta, search=suffix, threshold=0.5, flip=t, processors=1)"' %(outDir, sample)

    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/mothurAlignReportParser.py  %s/%s.afterMerge.SSU.RFadded.align.report  %s/%s.afterMerge.SSU.RFadded.align' %(outDir, sample, outDir, sample)

    print >> fw, 'python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/MSA_manip.py  %s/%s.afterMerge.SSU.RFadded.align.badSeqsFiltered 971 1118' %(outDir, sample)
    print >> fw, 'mv  %s/%s.afterMerge.SSU.RFadded.align.badSeqsFiltered.971to1118.cut.lenScreened.afa %s' %(outDir, sample, sample)
    print >> fw, "echo 'ready for clustering ..'"
