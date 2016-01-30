# Makefile for  ssusearch, clust , and mothur analysis
# key parameters

Method:=ssusearch_no_qc
Seqfiles:=$(wildcard ./test/data/*.fa)
Design:=./test/SS.design
Script_dir:=./scripts

Name=SS
Gene=ssu
Otu_dist_cutoff=0.05
Start=550
#Start=1200
#End=1350
End=700
Len_cutoff=100
Phred=64            #64 or 33
Cpu=1
Java_xmx=10g
Java_gc_threads=4

SSUsearch_db=./SSUsearch_db

Clust_dir=./clust.$(Gene)
Diversity_dir=./diversity.$(Gene)
Diversity_cc_dir=./diversity_cc.$(Gene)

# tools, dirs, etc

Flash=/mnt/home/guojiaro/Documents/software/QC/FLASH/flash
Flash_flags=-m 10 -M 120 -x 0.08 -r 140 -f 250 -s 25 -d . -t 1 -p $(Phred)
Hmmsearch=hmmsearch
Mothur=/mnt/home/guojiaro/Documents/software/mothur/Mothur.source/./mothur
Mcclust_jar=/mnt/home/guojiaro/Documents/software/mcclust/Clustering.jar
TERM?=linux

override Method:=$(realpath $(Method))
override Seqfiles:=$(realpath $(Seqfiles))
override Design:=$(realpath $(Design))
override Script_dir:=$(realpath $(Script_dir))

override SSUsearch_db:=$(realpath $(SSUsearch_db))

Hmm=$(SSUsearch_db)/Hmm.ssu.hmm
Gene_db=$(SSUsearch_db)/Gene_db.silva_108_rep_set.fasta
Gene_tax=$(SSUsearch_db)/Gene_tax.silva_taxa_family.tax
Ali_template=$(SSUsearch_db)/Ali_template.silva_ssu.fasta
#Ali_template=$(SSUsearch_db)/Ali_template.test.fasta
Gene_model_org=$(SSUsearch_db)/Gene_model_org.16s_ecoli_J01695.fasta
Gene_db_cc=$(SSUsearch_db)/Gene_db_cc.greengene_97_otus.fasta
Gene_tax_cc=$(SSUsearch_db)/Gene_tax_cc.greengene_97_otus.tax
Copy_db=$(SSUsearch_db)/Copy_db.copyrighter.txt

override Seqfiles:=$(realpath $(Seqfiles))
Seqfile_names=$(notdir $(Seqfiles))
Tags=$(foreach name, $(Seqfile_names), $(word 1,$(subst ., ,$(name))))
Outdirs=$(foreach name, $(Seqfiles), $(name).$(Gene).out/)

Dummy_tag=dummy
Dummyfiles_filter=$(foreach outdir, $(Outdirs), $(outdir)$(Dummy_tag).qc.$(Gene).align.filter)
Dummyfiles_filter_nogap=$(foreach outdir, $(Outdirs), $(outdir)$(Dummy_tag).qc.$(Gene).align.filter.fa)
Dummyfiles_filter_cut=$(foreach outdir, $(Outdirs), $(outdir)$(Dummy_tag))
Dummyfiles_filter_silva_taxonomy=$(foreach outdir, $(Outdirs), $(outdir)$(Dummy_tag).qc.$(Gene).align.filter.wang.silva.taxonomy.count)
Dummyfiles_filter_cc_taxonomy=$(foreach outdir, $(Outdirs), $(outdir)$(Dummy_tag).qc.$(Gene).align.filter.wang.gg.taxonomy.cc.count)

Tagfiles=$(join $(Outdirs),$(Tags))

MAKEOVERRIDES= 
export

#TARGETS
all: tool_check diversity diversity_cc taxonomy_silva taxonomy_cc

.PHONY: ssusearch region_cut clust \
	make_biom diversity make_biom_cc diversity_cc \
	taxonomy_silva taxonomy_cc \
	clean very_clean setup tool_check help

.SECONDEXPANSION:

ssusearch: $(Dummyfiles_filter)

# static pattern match to run ssusearch_makefile on all seqfiles
# can not figure out static pattern match using $(Tagfiles)
# use dummy as a hack
$(Dummyfiles_filter): %.$(Gene).out/$(Dummy_tag).qc.$(Gene).align.filter: %
	mkdir -p $(dir $@)
	make -f $(Script_dir)/ssusearch.Makefile $(Method) \
	  Seqfile=$< -C $(dir $@) Tag=$(Dummy_tag) Cpu=$(Cpu)

degap: $(Dummyfiles_filter_nogap)

$(Dummyfiles_filter_nogap): %.fa: %
	python $(Script_dir)/remove-gap.py $< $@

taxonomy_silva: $(Dummyfiles_filter_silva_taxonomy)

$(Dummyfiles_filter_silva_taxonomy): %.wang.silva.taxonomy.count: %.fa
	rm -f $(basename $<).*.wang.taxonomy \
	&& $(Mothur) "#classify.seqs(fasta=$<, \
	  template=$(Gene_db), taxonomy=$(Gene_tax), cutoff=50, \
	  processors=$(Cpu))" \
	&& mv $(basename $<).*.wang.taxonomy \
	  $(basename $<).wang.silva.taxonomy \
	&& python $(Script_dir)/count-taxon.py \
	  $(basename $<).wang.silva.taxonomy \
	  $(basename $<).wang.silva.taxonomy.count \
	&& rm -f mothur.*.logfile \
	|| { rm -f $@; exit 1; }

taxonomy_cc: $(Dummyfiles_filter_cc_taxonomy)

$(Dummyfiles_filter_cc_taxonomy): %.wang.gg.taxonomy.cc.count: %.fa
	rm -f $(basename $<).*.wang.taxonomy \
	&& $(Mothur) "#classify.seqs(fasta=$<, \
	  template=$(Gene_db_cc), taxonomy=$(Gene_tax_cc), cutoff=50, \
	  processors=$(Cpu))" \
	&& mv $(basename $<).*.wang.taxonomy $(basename $<).wang.gg.taxonomy \
	&& python $(Script_dir)/count-taxon.py \
	  $(basename $<).wang.gg.taxonomy \
	  $(basename $<).wang.gg.taxonomy.count \
	&& python $(Script_dir)/copyrighter.py $(Copy_db) \
	  $(basename $<).wang.gg.taxonomy \
	  $(basename $<).wang.gg.taxonomy.cc.count \
	&& rm -f mothur.*.logfile \
	|| { rm -f $@; exit 1; }

region_cut: $(Dummyfiles_filter_cut)

$(Dummyfiles_filter_cut): %: %.qc.$(Gene).align.filter
	@echo
	@echo "*** Starting region cut"
	@echo
	### pay att to the average read length: 75, 100 , 125
	### minLen are 2/3 of ave length
	###
	python $(Script_dir)/region-cut.py $< $(Start) $(End) $(Len_cutoff)
	mv $<.$(Start)to$(End).cut.lenscreen $@
	-(rm -f $(dir $@)mothur.*.logfile)

$(Tagfiles): $$(dir $$@)$(Dummy_tag)
	cp $< $@
	@echo "*** $(notdir $@) ready for clustering.."
	@echo
	@echo

clust: $(Clust_dir).sub.clu/$(Name).list

$(Clust_dir).sub.clu/$(Name).list: $(Tagfiles)
	#collect seqs in another directory
	rm -f $(Clust_dir)/* $(Clust_dir).sub/* $(Clust_dir).sub.clu/*
	mkdir -p $(Clust_dir) \
	&& cp $(Tagfiles) $(Clust_dir) \
	|| { rm -rf $(Clust_dir) && exit 1; }

	# even sampling
	Mincount=$$(python $(Script_dir)/count-min.py $(Clust_dir)) \
	&& python $(Script_dir)/subsample.py $(Clust_dir) $$Mincount \
	  $(Clust_dir).sub \
	&& sed -i 's/:/_/g' $(Clust_dir).sub/* \
	&& echo "*** Replace ':' with '_' in seq names (original illumina name has ':' in them)" \
	|| { rm -rf $(Clust_dir).sub && exit 1; }

	mkdir -p $(Clust_dir).sub.clu
	cp $(Design) $(Clust_dir).sub.clu
	cat $(Clust_dir).sub/* > $(Clust_dir).sub.clu/combined_seqs.afa
	python $(Script_dir)/make-groupfile.py \
	  $(Clust_dir).sub.clu/$(Name).groups $(Clust_dir).sub

	@echo "*** Starting mcclust"
	{ cd $(Clust_dir).sub.clu \
	&& time java -Xmx$(Java_xmx) -XX:+UseParallelOldGC \
	  -XX:ParallelGCThreads=$(Java_gc_threads) \
	  -jar $(Mcclust_jar) derep -a -o derep.fasta \
	  temp.mcclust.names temp.txt combined_seqs.afa \
	&& rm temp.txt \
	&& python $(Script_dir)/mcclust2mothur_names_file.py \
	  temp.mcclust.names temp.mothur.names \
	&& $(Mothur) "#pre.cluster(fasta=derep.fasta, diffs=1, \
	  name=temp.mothur.names)" \
	&& python $(Script_dir)/mothur2mcclust_names_file.py \
	  derep.precluster.names $(Name).names \
	&& time java -Xmx$(Java_xmx) -XX:+UseParallelOldGC \
	  -XX:ParallelGCThreads=$(Java_gc_threads) \
	  -jar $(Mcclust_jar) dmatrix -l 25 \
          -o matrix.bin -i $(Name).names -I derep.precluster.fasta \
	&& time java -Xmx$(Java_xmx) -XX:+UseParallelOldGC \
	  -XX:ParallelGCThreads=$(Java_gc_threads) \
	  -jar $(Mcclust_jar) cluster \
          -i $(Name).names -s $(Name).groups -o complete.clust -d matrix.bin \
	&& python $(Script_dir)/mcclust2mothur-list-cutoff.py complete.clust \
	  $(Name).list $(Otu_dist_cutoff); \
	}

make_biom: $(Diversity_dir)/$(Name).biom

$(Diversity_dir)/$(Name).biom: $(Clust_dir).sub.clu/$(Name).list
	{ mkdir -p $(Diversity_dir) \
	&& cp $< $(Diversity_dir) \
	&& cp $(dir $<)$(Name).groups $(dir $@) \
	&& cd $(Diversity_dir) \
	&& $(Mothur) "#make.shared(list=$(Name).list, group=$(Name).groups,\
	  label=$(Otu_dist_cutoff));" \
	&& $(Mothur) "#make.biom(shared=$(Name).shared)" \
	&& mv $(Name).$(Otu_dist_cutoff).biom $(Name).biom \
	&& rm -f mothur.*.logfile; \
	} || { rm -f $(Diversity_cc_dir)/$(Name).biom && exit 1; }

diversity: $(Diversity_dir)/$(Name).biom
	{ cd $(Diversity_dir) \
	&& $(Mothur) "#make.shared(biom=$(Name).biom); \
	  summary.single(calc=nseqs-coverage-sobs-chao-shannon-invsimpson); \
	  dist.shared(calc=thetayc-braycurtis); \
	  pcoa(phylip=$(Name).thetayc.dummy.lt.dist); \
	  pcoa(phylip=$(Name).braycurtis.dummy.lt.dist); \
	  nmds(phylip=$(Name).thetayc.dummy.lt.dist); \
	  nmds(phylip=$(Name).braycurtis.dummy.lt.dist); \
	  amova(phylip=$(Name).braycurtis.dummy.lt.dist, design=$(Design)); \
	  tree.shared(calc=braycurtis); \
	  unifrac.weighted(tree=$(Name).braycurtis.dummy.tre, \
	    group=$(Design), random=T)" \
	&& rm -f mothur.*.logfile; \
	}

$(Diversity_cc_dir)/$(Name).list: $(Clust_dir).sub.clu/$(Name).list
	mkdir -p $(Diversity_cc_dir)
	cp $^ $(Diversity_cc_dir)
	cp $(dir $<)$(Name).groups $(dir $@)

# make taxonomy file for copy correction
$(Diversity_cc_dir)/$(Name).$(Otu_dist_cutoff).cons.taxonomy: \
	$(Diversity_cc_dir)/$(Name).list \
	$(Clust_dir).sub.clu/combined_seqs.afa

	python $(Script_dir)/remove-gap.py \
	  $(Clust_dir).sub.clu/combined_seqs.afa \
	  $(Diversity_cc_dir)/combined_seqs.fa
	{ cd $(Diversity_cc_dir) \
	&& $(Mothur) "#classify.seqs(fasta=combined_seqs.fa, \
	  template=$(Gene_db_cc), taxonomy=$(Gene_tax_cc), cutoff=50, \
	  processors=$(Cpu)); \
	  classify.otu(list=$(Name).list, label=$(Otu_dist_cutoff))" \
	&& rm -f mothur.*.logfile; \
	}

# make biom file after copy correction
make_biom_cc: $(Diversity_cc_dir)/$(Name).biom

$(Diversity_cc_dir)/$(Name).biom: $(Diversity_cc_dir)/$(Name).list \
	$(Diversity_cc_dir)/$(Name).$(Otu_dist_cutoff).cons.taxonomy

	{ cd $(Diversity_cc_dir) \
	&& $(Mothur) "#make.shared(list=$(Name).list, group=$(Name).groups, \
	  label=$(Otu_dist_cutoff));" \
	&& python $(Script_dir)/copyrighter-otutable.py $(Copy_db) \
	  $(Name).$(Otu_dist_cutoff).cons.taxonomy \
	  $(Name).shared $(Name).cc.shared \
	&& mv $(Name).cc.shared $(Name).shared \
	&& $(Mothur) "#make.biom(shared=$(Name).shared, \
	  constaxonomy=$(Name).$(Otu_dist_cutoff).cons.taxonomy)" \
	&& mv $(Name).$(Otu_dist_cutoff).biom $(Name).biom \
	&& rm -f mothur.*.logfile; \
	} || { rm -f $(Diversity_cc_dir)/$(Name).biom && exit 1; }

# diversity analysis with copy correction
diversity_cc: $(Diversity_cc_dir)/$(Name).biom
	{ cd $(Diversity_cc_dir) \
	&& $(Mothur) "#make.shared(biom=$(Name).biom); \
	  summary.single(calc=nseqs-coverage-sobs-chao-shannon-invsimpson); \
	  dist.shared(calc=thetayc-braycurtis); \
	  pcoa(phylip=$(Name).thetayc.dummy.lt.dist); \
	  pcoa(phylip=$(Name).braycurtis.dummy.lt.dist); \
	  nmds(phylip=$(Name).thetayc.dummy.lt.dist); \
	  nmds(phylip=$(Name).braycurtis.dummy.lt.dist); \
	  amova(phylip=$(Name).braycurtis.dummy.lt.dist, design=$(Design)); \
	  tree.shared(calc=braycurtis); \
	  unifrac.weighted(tree=$(Name).braycurtis.dummy.tre, \
	    group=$(Design),random=T)" \
	&& rm -f mothur.*.logfile; \
	}

clean:
	-@(rm -f $(filter-out $(foreach dir, $(Outdirs), $(wildcard $(dir)*.filter) $(wildcard $(dir)*.filter.fa) $(wildcard $(dir)*.count)),$(foreach dir, $(Outdirs), $(wildcard $(dir)*))))
	-@(rm -rf $(Clust_dir) $(Clust_dir).sub $(Clust_dir).sub.clu)
	-@(rm -f $(Diversity_dir)/mothur.*.logfile $(Diversity_cc_dir)/mothur.*.logfile)

very_clean:
	-@(rm -rf $(Clust_dir) $(Clust_dir).sub $(Clust_dir).sub.clu $(Diversity_dir) $(Diversity_cc_dir) $(Outdirs))

setup:
	virtualenv --no-site-packages --python python2.7 $(Py_virtenv) && source $(Py_virtenv)/bin/activate && pip install numpy && pip install matplotlib && pip install screed
	# add mothur, hmmer, flash installation

tool_check:
	@$(foreach cmd, $(Hmmsearch) $(Mothur), hash $(cmd) 2>/dev/null || { echo "$(cmd) not found. Please place $(cmd) in PATH or update variable in this script"; exit 1; };)
	@(java -jar $(Mcclust_jar) &> /dev/null); if [ ! $$? -eq 0 ]; then echo "$(Mcclust_jar) is not valid jar file." && exit 1; fi
	@python -c 'import numpy' &> /dev/null || { echo "numpy is not installed" && exit 1; }
	@python -c 'import scipy' &> /dev/null || { echo "scipy is not installed" && exit 1; }
	@python -c 'import pandas' &> /dev/null || { echo "pandas is not installed" && exit 1; }
	@python -c 'import matplotlib' &> /dev/null || { echo "matplotlib is not installed" && exit 1; }
	@python -c 'import screed' &> /dev/null || { echo "screed is not installed" && exit 1; }
	@echo "*** Dependencies are installed"

help:
	# ***This is a pipeline combining several tool. Thus there are many parameters, which can be changed in this Makefile or run as flag in command line (e.g. Make Method=ssusearch_no_qc Seqfiles=Path_to_sequence_files)
	#
	# Parameters
	# Method: Method to use in ssusearch.Makefile, three options: 
	#         ssusearch_no_qc: search gene without read quality control
	#         ssusearch_pe_qc: search gene with PE read quality control
	#         ssusearch_se_qc: search gene with SE read quality control
	# Seqfiles: Sequence files for searching ssu
	# Design: Tab delimited file with 1 col as sample name and 2 col as
	#         treatment
	# Script_dir: directory for scripts 
	# Name: Prefix of file names in diveristy analysis (default: SS)
	# Gene: name of gene for search (default: ssu)

	# Hmm: path to hmm file
	# Gene_db: fasta sequence database of interest gene for classification
	# Gene_tax: tab delimited file with 1st col as sequence name and 2nd as
	#           taxonomy
	# Ali_template: aligned fasta file of interest gene
	# Gene_model_org: gene sequence of a organism as standard for
	#                 gene position
 
	# Otu_dist_cutoff: distance cutoff for OTU definition (default: 0.05)
	# Start: start position of region selected for clustering 
	#        (default: 550)
	# End: end position of region selected for clustering (default: 700)
	# Len_cutoff: minimum lenght required for reads selected for 
	#             clustering (default: 100)
	# Phred: phred score system used in raw read (64 or 33)
	# Cpu: maximum threads for each job; Maximum number for parallel jobs 
	#      can be controled with  -j flag within make itself.
	#      Cpu * (-j) should be less than available threads in machine
	# Java_xmx: heap size for mcclust (e.g. 10000m or 10g; default: 10g)
	# Java_gc_threads: threads number for Garbage Collector (should be
	#                  maxium threas minus one (default: 1)

	# Gene_db_cc: fasta sequence database of interest gene for copy
	#             correction (greengene database)
	# Gene_tax_cc: tab delimited file with 1st col as sequence name 
	#              and 2nd as taxonomy for copy correction 
	#              (greengene database)
	# Copy_db: tab deliminated file with 1st col as taxonmy in greengene
	#          and 2nd col as copy number for taxonomy (compiled by
	#          copyrighter)

	# Clust_dir: directory for sequence files for clustering 
	#            (default: ./clust.$(Gene) )
	# Diversity_dir: output directory for diversity analysis
	#                (default: ./diversity.$(Gene) )
	# Diversity_cc_dir: output directory for copy corrected diversity 
	#                   analysis (default: ./diversity_cc.$(Gene) )
	#

	# Flash: path of Flash binary 
	# Flash_flags: flags for Flash (default: -m 10 -M 120 -x 0.08 
	#              -r 140 -f 250 -s 25 -d . -t 1 -p $(Phred) )
	# Hmmsearch: path of hmmsearch binary
	# Mothur: path of Mothur binary
	# Mcclust_jar: path of mcclust jar file
	# Py_virtenv: path of virtualenv directory (default: ./py_vertenv)

	# Dummy_tag: prefix as file names in ssusearch.Makefile
	# Tags
