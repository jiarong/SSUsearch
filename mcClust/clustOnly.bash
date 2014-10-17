set -e
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

/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur "#make.shared(list=SS.list, group=SS.groups, label=0.03); rarefaction.single(freq=0.01); heatmap.bin(scale=log2, numotu=2000); heatmap.sim(); venn(); tree.shared(calc=thetayc-jclass-braycurtis); dist.shared(calc=thetayc-jclass-braycurtis); pcoa(phylip=SS.thetayc.0.03.lt.dist); pcoa(phylip=SS.jclass.0.03.lt.dist); pcoa(phylip=SS.braycurtis.0.03.lt.dist); nmds(phylip=SS.thetayc.0.03.lt.dist); nmds(phylip=SS.jclass.0.03.lt.dist); nmds(phylip=SS.braycurtis.0.03.lt.dist);"
