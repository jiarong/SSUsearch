SSUsearch
=========

A quick start
-----------------

SSUsearch is pipeline for identify SSU rRNA gene and use them for diversity analysis. THe pipeline requires HMMER3.1, mothur, RDP mcclust, and python pandas, scipy, matplotlib, and screed package. The ssusearch_pe_qc method also need FLASH for PE merging. The pipeline is implemented in Makefile.

###
This tutorial assumes HMMER3.1, mothur, and python pandas, scipy, matplotlib, and screed package have been installed. First, set variables in Makefile (Hmmsearch and Mothur) to paths of the binary paths of their tools. If tools are installed system wide, just use hmmsearch and mothur for the values of these two variables. Alternatively variables can also be set in command line arguments. e.g. Make -f Makefile Hmmsearch=path_to_hmmsearch_binary Mothur=path_to_mothur_binary


To check if tools are installed correctly, run:

	git clone https://github.com/jiarong/SSUsearch.git
	cd SSUsearch
	Make -f Makefile tool_check

Then several databases and hidden markov models are needed: 

	wget http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch_db.tgz
	tar -xzvf SSUsearch_db.tgz

Parameters related to databases are Ali_template, Copy_db, Gene_db_cc, Gene_db, Gene_model_org, Gene_tax_cc, Gene_tax, Hmm. First part of each database files its variable in Makefile. e.g. Ali_template.silva_lsu.fasta is for Ali_template. Set values of these parameters to paths of their database in Makefile. Again, we can also set variables as commandline arguments. The default value should be OK if you follow the above steps.

Other than wgs data files, a design file is also needed for diversity analysis in mothur. [Some description](http://www.mothur.org/wiki/Design_header_file) can be found in mothur wiki. Use the first column as sample tag and second as treatment. Sample tag is the first part of wgs data file names. e.g. For M1.fa.gz, the tag is M1.

	#Download a test dataset and its design file
	wget -r -np -nH --cut-dir=4 --reject="index.html*" http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/
	make -f Makefile Seqfiles="test/data/*.fa" Design=test/SS.design Method=ssusearch_no_qc

Taxonomy results are here:

	ls test/data/*.fa.ssu.out/*.taxonomy

The diversity analysis can be found at:

	# no copy correction
	ls diversity.ssu
	# copy correction
	ls diverstiy_cc.ssu

This pipeline includes PCoA, beta-diversity indces, weighted UNIFRAC and AMOVA. With SS.shared, SS.names, SS.groups, SS.design, most analysis in mothur can be done.
