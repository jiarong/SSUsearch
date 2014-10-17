#! /usr/bin/env bash
# to realign the seqs from diff sample in case that the alignment in diff sample
#     are diff due to diff run by preprocess.mothurCommand or 
#     SSUsearch.makeBash.py, so that they can be ready for the mcclust
# by gjr; Apr 5, 12

set -e
TERM=linux
export TERM

echo "ATT: START and END position in "regionCut.py" should be changed in diff cases"
echo "take 10 seconds to confirm .."

for ((i=0;i<10;i+=2))
do
    echo -ne "${i}..  "
    sleep 2
done
echo

#
##change sample dir or samples here
#
#samples=/u/gjr/glbrc/SSU_after060111/silvaAlign/bigD/sep/10M

#sample dir from argv
samples=$1
#samples=`echo "$samples"|sed 's/[/]//g'`
samples=`readlink -f "$samples"`

#
##change outdir here
#
outdir="$samples.out"
if [ ! -d "$outdir" ]; then
    echo "output dir does not exsit.."
    echo "making dir '$outdir'"
    mkdir "$outdir"
else
    echo "output dir: '$outdir' exsits .."
fi

cd "$outdir"

#
# make group file for mothur
# it should be same as samples.txt file mcclust
python /mnt/home/guojiaro/Documents/scripts/mcClust/makeSampleFile.py SS.groups "$samples"

cat "$samples"/* > combinedSeqsForMothurAlign.fasta

# realign
/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#summary.seqs(fasta=combinedSeqsForMothurAlign.fasta)"

/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#unique.seqs(fasta=combinedSeqsForMothurAlign.fasta)"
#name file is produced by unique.seqs
/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#summary.seqs(fasta=combinedSeqsForMothurAlign.unique.fasta, name=combinedSeqsForMothurAlign.names)"

/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#align.seqs(candidate=combinedSeqsForMothurAlign.unique.fasta, template=/mnt/home/guojiaro/Documents/data/RefDB/temp/silva.ssu.Namechanged.fasta, flip=t, threshold=0.50, processors=1)"
/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#summary.seqs(fasta=combinedSeqsForMothurAlign.unique.align, name=combinedSeqsForMothurAlign.names)"
echo 'aligning done..'

#add ReFeReNcE
cat /mnt/home/guojiaro/Documents/data/16s_ecoli_J01695.afa combinedSeqsForMothurAlign.unique.align > combinedSeqsForMothurAlign.unique.align.RFadded
#cut region, (899to1365 in silva), minLen=200(all seqs>200bp should pass)
python /mnt/home/guojiaro/Documents/scripts/pipeForSSU/regionCut.py combinedSeqsForMothurAlign.unique.align.RFadded 899 1365 200
mv combinedSeqsForMothurAlign.unique.align.RFadded.899to1365.cut.lenScreened.afa combinedSeqsForMothurAlign.unique.align
python /mnt/home/guojiaro/Documents/scripts/mcClust/updateNamePlusGroup.py combinedSeqsForMothurAlign.unique.align combinedSeqsForMothurAlign.names SS.groups combinedSeqsForMothurAlign.updated.names SS.updated.groups
mv combinedSeqsForMothurAlign.updated.names combinedSeqsForMothurAlign.names
mv SS.updated.groups SS.groups

/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#filter.seqs(fasta=combinedSeqsForMothurAlign.unique.align, vertical=T, trump=, processors=1)"
#remove columns with only gaps, MSA is not 50000 cols
#need realign if compare with other data
/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#summary.seqs(fasta=combinedSeqsForMothurAlign.unique.filter.fasta, name=combinedSeqsForMothurAlign.names)"
echo 'filter.seqs done..'

/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#deunique.seqs(fasta=combinedSeqsForMothurAlign.unique.filter.fasta, name=combinedSeqsForMothurAlign.names)"
echo 'deunique.seqs done..'
#
# combinedSeqsForMothurAlign.redundant.fasta produced
#
mv combinedSeqsForMothurAlign.redundant.fasta combinedSeqs.afa

#------------------------------------------------------
#above is the realign
#if shotgun reads need to do regionCut

#
# .names files in mothur and .names file in mcClust are DIFF
#
# SS.groups already produced
echo "ready for mcClust.."
time java -jar  /mnt/home/guojiaro/Documents/software/mcclust/Clustering.jar derep -a -o derep.fasta SS.names x combinedSeqs.afa
time java -jar /mnt/home/guojiaro/Documents/software/mcclust/Clustering.jar dmatrix -l 25 -o matrix.bin -i SS.names -I derep.fasta
time java -jar /mnt/home/guojiaro/Documents/software/mcclust/Clustering.jar cluster -i SS.names -s SS.groups -o complete.clust -d matrix.bin
python /mnt/home/guojiaro/Documents/scripts/mcClust/mcclustToMothurList.py complete.clust SS.list

# commands for mothur diversity analysis

/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#make.shared(list=SS.list, group=SS.groups, label=0.03); rarefaction.single(list=SS.list, freq=0.01); heatmap.bin(shared=SS.shared, scale=log2, numotu=2000); heatmap.sim(); venn(); tree.shared(calc=thetayc-jclass-braycurtis); dist.shared(calc=thetayc-jclass-braycurtis); pcoa(phylip=SS.thetayc.0.03.lt.dist); pcoa(phylip=SS.jclass.0.03.lt.dist); pcoa(phylip=SS.braycurtis.0.03.lt.dist); nmds(phylip=SS.thetayc.0.03.lt.dist); nmds(phylip=SS.jclass.0.03.lt.dist); nmds(phylip=SS.braycurtis.0.03.lt.dist);"

cat *.logfile > mothur.log
rm *.logfile
