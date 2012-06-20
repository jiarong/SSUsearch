#! /usr/bin/env bash
# purpose: recording commands for making a tree from SS.names, complete.clust and
#            derep.fasta
# by gjr, Apr 10, 12

java -jar ../Clustering.jar rep-seqs -I SS.names complete.clust 0.12 derep.fasta

python makeiTolData.py /mnt/research/tiedjelab/temp/PT/MSRandISO.out/complete.clust 0.12 _ISO
# add headlines output manully
python renameRepOTU.mcclust.py ISOandMSR_representatives_0.12.fasta ISOandMSR_representatives_0.12.renamed.fasta
#or
python ~/Documents/scripts/mcClust/renameRepOTU.mcclust.py ISOandMSR_representatives_0.12.fasta complete.clust.1or2ersFiltered.iTolData

~/Documents/software/./FastTree -nt -gamma /mnt/research/tiedjelab/temp/PT/MSRandISO.out/ISOandMSR_representatives_0.12.renamed.fasta > /mnt/research/tiedjelab/temp/PT/MSRandISO.out/ISOandMSR_representatives_0.12.renamed.ftree

