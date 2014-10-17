#! /bin/bash
# script for mcclust and mothur analysis
# by gjr; Feb 22, 2012

#
# USAGE: bash <thisFile><fastaFileDir>
#
set -e
TERM=linux
export TERM

echo "ATT: make sure all aligned fasta files are cut for the same region"
echo "take 10 seconds to confirm .."

for ((i=0;i<10;i+=2))
do
    echo -ne "${i}..  "
    sleep 2
done
echo

#sample dir from argv
samples=$1
#samples=`echo "$samples"|sed 's/[/]//g'`
samples=`readlink -f "$samples"`

#
##change outdir here
#
outdir="$samples.out"
if [ ! -d "$outdir" ]; then
    echo "output dir does not exsit, mkdir '$outdir'.."
    mkdir "$outdir"
else
    echo "output dir: '$outdir' exsits .."
fi

cd "$outdir"
#
# make samples.txt file mcclust
python /mnt/home/guojiaro/Documents/scripts/mcClust/makeSampleFile.py SS.groups "$samples"
cat "$samples"/* > combinedSeqs.afa
#
# x is not useful
time java -jar /mnt/home/guojiaro/Documents/software/mcclust/Clustering.jar derep -a -o derep.fasta SS.names x combinedSeqs.afa
time java -jar /mnt/home/guojiaro/Documents/software/mcclust/Clustering.jar dmatrix -l 25 -o matrix.bin -i SS.names -I derep.fasta
time java -jar /mnt/home/guojiaro/Documents/software/mcclust/Clustering.jar cluster -i SS.names -s SS.groups -o complete.clust -d matrix.bin
python /mnt/home/guojiaro/Documents/scripts/mcClust/mcclustToMothurList.py complete.clust SS.list

# commands for mothur diversity analysis

/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#make.shared(list=SS.list, group=SS.groups, label=0.03); rarefaction.single(freq=0.01); heatmap.bin(scale=log2, numotu=2000); heatmap.sim(); venn(); tree.shared(calc=thetayc-jclass-braycurtis); dist.shared(calc=thetayc-jclass-braycurtis); pcoa(phylip=SS.thetayc.0.03.lt.dist); pcoa(phylip=SS.jclass.0.03.lt.dist); pcoa(phylip=SS.braycurtis.0.03.lt.dist); nmds(phylip=SS.thetayc.0.03.lt.dist); nmds(phylip=SS.jclass.0.03.lt.dist); nmds(phylip=SS.braycurtis.0.03.lt.dist);"
