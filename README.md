SSUsearch
=========

SSUsearch is pipeline for identify SSU rRNA gene and use them for diversity analysis. THe pipeline requires HMMER3.1, mothur, RDP mcclust, and python numpy, pandas, scipy, matplotlib, and screed package. The ssusearch_pe_qc method also need FLASH for PE merging. The pipeline is implemented in Makefile.

Install dependencies
--------------------

This pipeline requires: HMMER3.1, mothur, RDP mcclust, FLASH and python pandas, scipy, matplotlib, and screed package. Following steps should work for linux machines.

	git clone https://github.com/jiarong/SSUsearch.git
	cd SSUsearch
	mkdir -p external_tools; cd external_tools

	wget http://selab.janelia.org/software/hmmer3/3.1b1/hmmer-3.1b1-linux-intel-x86_64.tar.gz -O hmmer-3.1b1-linux-intel-x86_64.tar.gz
	tar -xzvf hmmer-3.1b1-linux-intel-x86_64.tar.gz
	HMMSEARCH_BIN=$(readlink -f hmmer-3.1b1-linux-intel-x86_64/binaries/hmmsearch)

	wget http://www.mothur.org/w/images/8/88/Mothur.cen_64.zip -O mothur.zip
	unzip mothur.zip
	MOTHUR_BIN=$(readlink -f mothur/mothur)

	# add FLASH
	wget http://sourceforge.net/projects/flashpage/files/FLASH-1.2.11.tar.gz/download -O FLASH-1.2.11.tar.gz
	tar -xzvf FLASH-1.2.11.tar.gz
	(cd FLASH-1.2.11/ && make)
	FLASH_BIN=$(readlink -f FLASH-1.2.11/flash)

	# RDP mcClust
	# Updated version can be found github:  https://github.com/rdpstaff/RDPTools.git
	# Here an older version is used
	wget http://lyorn.idyll.org/~gjr/public2/misc/mcclust_20120119.tar.gz
	tar -xzvf mcclust_20120119.tar.gz
	MCCLUST_JAR=$(readlink -f mcclust/Clustering.jar)

	# python packages, assuming virtualenv installed
	# virtualenv installation guide: https://virtualenv.pypa.io/en/latest/virtualenv.html#installation
	virtualenv ssusearch_pyenv
	source ssusearch_pyenv/bin/activate
	pip install numpy pandas scipy screed matplotlib

	# test if tools are properly installed
	cd ..
	Make -f Makefile tool_check Hmmsearch=$HMMSEARCH_BIN Mothur=$MOTHUR_BIN Flash=$FLASH_BIN Mcclust_jar=$MCCLUST_JAR

In the above, variables are set in command line arguments. It is better to modify the value of these variables to absolute path of binaries in Makefile, so there is no need to put them in argument in future. If tools are installed system wide, just use **hmmsearch**, **mothur** and **flash** for the values of these three variables. 

An example:
-----------------

Several databases and hidden markov models are needed: 

	wget http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch_db.tgz
	tar -xzvf SSUsearch_db.tgz

Parameters related to databases are **Ali_template, Copy_db, Gene_db_cc, Gene_db, Gene_model_org, Gene_tax_cc, Gene_tax, and Hmm**. First part of each database files its variable in Makefile. e.g. Ali_template.silva_lsu.fasta is for Ali_template. Set values of these parameters to *absolute paths** of their database in Makefile. Again, we can also set variables as commandline arguments. The default value should be OK for this tutorial if you follow the above steps.

Other than wgs data files, **a design file** is also needed for diversity analysis in mothur. [Some description](http://www.mothur.org/wiki/Design_header_file) can be found in mothur wiki. Use the first column as sample tag and second as treatment. Sample tag is the first part of wgs data file names. e.g. For M1.fa.gz, the tag is M1.

	# download a test dataset and its design file
	wget -r -np -nH --cut-dir=4 --reject="index.html*" http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/
	# check wgs data files
	ls test/data/*.fa
	# check design file
	cat test/SS.design
	# run the pipeline
	make -f Makefile Seqfiles="test/data/1c.fa test/data/1d.fa test/data/2c.fa test/data/2d.fa" Design=test/SS.design Script_dir=./scripts Method=ssusearch_no_qc Method=ssusearch_no_qc Hmmsearch=$HMMSEARCH_BIN Mothur=$MOTHUR_BIN Flash=$FLASH_BIN Mcclust_jar=$MCCLUST_JAR 

Taxonomy results are here:

	ls test/data/*.fa.ssu.out/*.taxonomy

By default, V4 will be used for OTU based analysis. The diversity analysis can be found at:

	# no copy correction
	ls diversity.ssu
	# copy correction
	ls diversity_cc.ssu

This pipeline includes PCoA, beta-diversity indces, weighted UNIFRAC and AMOVA. With SS.shared, SS.names, SS.groups, SS.design, most analysis in mothur can be done.

Makefile includes many variables for steps in pipeline. To see a full list of variables in Makefile:

	make -f Makefile help


