# Makefile for  ssusearch, clust , and mothur analysis
# key parameters

Name=SS
Seqfiles:=$(wildcard /mnt/scratch/tg/g/dataForPaper/RNA/jobs/cluster/ssusearch/test/data/*.fa)
Design=/mnt/lustre_scratch_2012/tg/g/dataForPaper/RNA/jobs/cluster/ssusearch/test/SS.design
Clust_dir=./clust.$(Gene)
Diversity_dir=./diversity.$(Gene)
Diversity_cc_dir=./diversity_cc.$(Gene)

Gene=ssu
Hmm=/mnt/home/guojiaro/Documents/db/qiimeDB/Silva_108/hmm3.1/ssu.hmm
Gene_db=/mnt/home/guojiaro/Documents/data/RefDB/qiimeSilva/Silva_108_rep_set.fna
Gene_tax=/mnt/home/guojiaro/Documents/data/RefDB/qiimeSilva/Silva_RDP_taxa_mapping_family.tax
Ali_template=/mnt/home/guojiaro/Documents/data/RefDB/silva.ssu.fasta
Gene_model_org=/mnt/home/guojiaro/Documents/data/16s_ecoli_J01695_oneline.fa
Start=550
#Start=1200
#End=1350
End=700
Len_cutoff=100
Phred=64            #64 or 33

Gene_db_cc=/mnt/home/guojiaro/Documents/db/qiimeDB/gg_12_10_otus/rep_set/97_otus.fasta
Gene_tax_cc=/mnt/home/guojiaro/Documents/db/qiimeDB/gg_12_10_otus/taxonomy/97_otu_taxonomy.mothurtax
Copy_db=/mnt/home/guojiaro/Documents/db/copyrighter/tax_string_ssu_img40_gg201210.txt

# tools, dirs, etc
Script_dir=/mnt/scratch/tg/g/dataForPaper/RNA/jobs/cluster/ssusearch/scripts
#Flash=./external_tools/FLASH/.flash
Flash=/mnt/home/guojiaro/Documents/software/QC/FLASH/flash
Flash_flags=-m 10 -M 120 -x 0.08 -r 140 -f 250 -s 25 -d . -t 1 -p $(Phred)
Hmmsearch=hmmsearch
Mothur=/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur
Clustering_jar=/mnt/home/guojiaro/Documents/software/mcclust/Clustering.jar
TERM?=linux

Seqfiles:=$(realpath $(Seqfiles))
Seqfile_names=$(notdir $(Seqfiles))
Tags=$(foreach name, $(Seqfile_names), $(word 1,$(subst ., ,$(name))))
Outdirs=$(foreach name, $(Seqfiles), $(name).$(Gene).out/)

Dummy_tag=dummy
Dummyfiles=$(foreach outdir, $(Outdirs), $(outdir)$(Dummy_tag))
Tagfiles=$(join $(Outdirs),$(Tags))

export

#TARGETS
all: diversity diversity_cc

.PHONY: ssusearch clust diversity diversity_cc clean very_clean setup

.SECONDEXPANSION:

ssusearch: $(Tagfiles)

.SECONDEXPANSION:

# static pattern match to run ssusearch_makefile on all seqfiles
# can not figure out static pattern match using $(Tagfiles)
# use dummy as a hack
$(Dummyfiles): %.$(Gene).out/dummy: %
	mkdir -p $(dir $@)
	make -f $(Script_dir)/ssusearch.Makefile ssusearch_no_qc Seqfile=$< -C $(dir $@)

$(Tagfiles): $$(dir $$@)dummy
	cp $< $@

collect: $(Clust_dir)

$(Clust_dir): $(Tagfiles)
	mkdir -p $(Clust_dir) \
	&& cp $(Tagfiles) $(Clust_dir) \
	|| (rm -rf $(Clust_dir) && false)

subsample: $(Clust_dir).sub

$(Clust_dir).sub: $(Clust_dir)
	# even sampling
	(Mincount=$$(python $(Script_dir)/count-min.py $(Clust_dir)) \
	&& python $(Script_dir)/subsample.py $(Clust_dir) $$Mincount \
	  $(Clust_dir).sub) \
	|| (rm -rf $(Clust_dir).sub && false)

clust: $(Clust_dir).sub.clu/$(Name).list

$(Clust_dir).sub.clu/$(Name).list: $(Clust_dir).sub
	mkdir -p $(Clust_dir).sub.clu
	cp $(Design) $(Clust_dir).sub.clu
	cat $(Clust_dir).sub/* > $(Clust_dir).sub.clu/combined_seqs.afa
	python $(Script_dir)/make-groupfile.py \
	  $(Clust_dir).sub.clu/$(Name).groups $(Clust_dir).sub

	@echo "*** Starting mcclust"
	(cd $(Clust_dir).sub.clu \
	&& time java -jar $(Clustering_jar) derep -a -o derep.fasta \
	  $(Name).names x combined_seqs.afa \
	&& time java -jar $(Clustering_jar) dmatrix -l 25 -o matrix.bin \
	  -i $(Name).names -I derep.fasta \
	&& time java -jar $(Clustering_jar) cluster -i $(Name).names \
	  -s $(Name).groups -o complete.clust -d matrix.bin \
	&& python $(Script_dir)/mcclust2mothur-list.py complete.clust \
	  $(Name).list \
	&& sed -i 's/:/_/g' $(Name).names $(Name).groups $(Name).list \
	)
	@echo "*** Replace ':' with '_' in seq names\
	  (original illumina name has ':' in them)"

diversity: $(Diversity_dir)/$(Name).biom

$(Diversity_dir)/$(Name).biom: $(Clust_dir).sub.clu/$(Name).list
	(mkdir -p $(Diversity_dir) \
	&& cp $< $(Diversity_dir) \
	&& cp $(dir $<)$(Name).groups $(dir $@) \
	&& cd $(Diversity_dir) \
	&& $(Mothur) "#make.shared(list=$(Name).list, group=$(Name).groups, \
	  label=0.03);" \
	&& $(Mothur) "#make.biom(shared=$(Name).shared)" \
	&& mv $(Name).0.03.biom $(Name).biom \
	&& $(Mothur) "#make.shared(biom=$(Name).biom); dist.shared(calc=thetayc-braycurtis); pcoa(phylip=$(Name).thetayc.dummy.lt.dist); pcoa(phylip=$(Name).braycurtis.dummy.lt.dist); nmds(phylip=$(Name).thetayc.dummy.lt.dist); nmds(phylip=$(Name).braycurtis.dummy.lt.dist);unifrac.weighted(tree=$(Name).braycurtis.dummy.tre, group=$(Design), random=T); amova(phylip=$(Name).braycurtis.dummy.lt.dist, design=$(Design)); metastats(design=$(Design))" \
	) || (rm -f $(Diversity_cc_dir)/$(Name).biom && false)


$(Diversity_cc_dir)/$(Name).list: $(Clust_dir).sub.clu/$(Name).list
	mkdir -p $(Diversity_cc_dir)
	cp $^ $(Diversity_cc_dir)
	cp $(dir $<)$(Name).groups $(dir $@)


diversity_cc: $(Diversity_cc_dir)/$(Name).biom


$(Diversity_cc_dir)/$(Name).biom: $(Diversity_cc_dir)/$(Name).list \
	$(Diversity_cc_dir)/$(Name).0.03.cons.taxonomy

	(cd $(Diversity_cc_dir) \
	&& $(Mothur) "#make.shared(list=$(Name).list, group=$(Name).groups, \
	  label=0.03);" \
	&& python $(Script_dir)/copyrighter-otutable.py $(Copy_db) \
	  $(Name).0.03.cons.taxonomy $(Name).shared $(Name).cc.shared \
	&& $(Mothur) "#make.biom(shared=$(Name).shared, \
	  constaxonomy=$(Name).0.03.cons.taxonomy)" \
	&& mv $(Name).0.03.biom $(Name).biom \
	&& $(Mothur) "#make.shared(biom=$(Name).biom); dist.shared(calc=thetayc-braycurtis); pcoa(phylip=$(Name).thetayc.dummy.lt.dist); pcoa(phylip=$(Name).braycurtis.dummy.lt.dist); nmds(phylip=$(Name).thetayc.dummy.lt.dist); nmds(phylip=$(Name).braycurtis.dummy.lt.dist);unifrac.weighted(tree=$(Name).braycurtis.dummy.tre, group=$(Design), random=T); amova(phylip=$(Name).braycurtis.dummy.lt.dist, design=$(Design)); metastats(design=$(Design))" \
	) || (rm -f $(Diversity_cc_dir)/$(Name).biom && false)


$(Diversity_cc_dir)/$(Name).0.03.cons.taxonomy: $(Diversity_cc_dir)/$(Name).list

	python $(Script_dir)/remove-gap.py \
	  $(Clust_dir).sub.clu/combined_seqs.afa \
	  $(Diversity_cc_dir)/combined_seqs.fa
	(cd $(Diversity_cc_dir) \
	&& $(Mothur) "#classify.seqs(fasta=combined_seqs.fa, \
	  template=$(Gene_db_cc), taxonomy=$(Gene_tax_cc), cutoff=50, \
	  processors=1); \
	  classify.otu(list=$(Name).list, label=0.03)" \
	)


clean:
	-@(rm -f $(filter-out $(Clust_dir)/$(Name).list $(foreach dir, $(Outdirs), $(wildcard $(dir)*.filter)),$(wildcard $(Clust_dir)/*) $(foreach dir, $(Outdirs), $(wildcard $(dir)*))))


very_clean:
	-@(rm -rf $(Clust_dir) $(Diversity_dir) $(Diversity_cc_dir) $(Outdirs))

setup:
	module load NumPy
	source /mnt/home/guojiaro/Documents/vEnv/qiime_pip/bin/activate
