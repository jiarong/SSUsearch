#! /bin/bash
# script for mcclust and mothur analysis
# by gjr; Feb 22, 2012

set -e
TERM=linux
export TERM

##change outdir here
outdir=MS.out
cd "$outdir"
# commands for mothur diversity analysis

/u/gjr/software/Mothur/./mothur "#make.shared(list=SS.list, group=SS.groups, label=0.03); rarefaction.single(freq=0.01); heatmap.bin(scale=log2, numotu=2000); heatmap.sim(); venn(); tree.shared(calc=thetayc-jclass-braycurtis); dist.shared(calc=thetayc-jclass-braycurtis); pcoa(phylip=SS.thetayc.0.03.lt.dist); pcoa(phylip=SS.jclass.0.03.lt.dist); pcoa(phylip=SS.braycurtis.0.03.lt.dist); nmds(phylip=SS.thetayc.0.03.lt.dist); nmds(phylip=SS.jclass.0.03.lt.dist); nmds(phylip=SS.braycurtis.0.03.lt.dist);"
