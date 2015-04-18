SSUsearch
=========

SSUsearch is pipeline for identify SSU rRNA gene and use them for diversity analysis. THe pipeline requires HMMER3.1, mothur, RDP mcclust, and python numpy, pandas, scipy, matplotlib, and screed package. The pipeline is implemented in Makefile. Two key features:

1. unsupervised community analysis with shotgun data

2. Scalibility: 5 Gb peak mem and 30 CPU hours on 60 Gb data.


Pipeline tutorial
------------------

The tutorials are written in ipython notebook. The **easiest way to run it** is using amazon EC2 instances with ami **ami-947f7bfc** and add more storage according to your data size (the default is 20 Gb).

If you want to run the notebooks on your computer, ipython (v4) with notebook dependencies are needed.

If you already have Python:

	pip install "ipython[notebook]"

If you are new to Python, go to http://continuum.io/downloads and copy the link for Linux 64-bits installer. At the time of this writing it is https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.2.0-Linux-x86_64.sh 

	wget -c https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.2.0-Linux-x86_64.sh

	bash Anaconda-2.2.0-Linux-x86_64.sh 

Accept the license
Choose an installation directory (default is fine)
Add to default path at the end of installation
Then 

	source ~/.bashrc

Ipython is ready to go :)

Download SSUsearch:

	git clone https://github.com/jiarong/SSUsearch

Go to notebook directory:

	cd SSUsearch/notebooks

Start ipython notebook: 

	ipython notebook

In your default web browser, you will see a page showing several *.ipynb links.

First open overview.ipynb, and follow the instructions there. **You will need to change the data directory setting** (those on the notebooks are for running on amazon EC2 instances).


Makefile implementation 
-----------------------
There is also a Makefile implemention shown below. It is great for automation but not as easy to read and modify. (I am not interested in maintaining api or wrapers.) Thus the above notebooks are recommended to run the pipeline.


Install dependencies
--------------------

This pipeline requires: HMMER3.1, mothur, RDP mcclust, FLASH and python pandas, scipy, matplotlib, and screed package. Following steps should work for **linux** machines.

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
	make -f Makefile tool_check Hmmsearch=$HMMSEARCH_BIN Mothur=$MOTHUR_BIN Flash=$FLASH_BIN Mcclust_jar=$MCCLUST_JAR

In the above, variables are set in command line arguments. It is better to modify the value of these variables to absolute path of binaries in Makefile, so there is no need to put them in argument in future. If tools are installed system wide, just use **hmmsearch**, **mothur** and **flash** for the values of these three variables. 

An example:
-----------------

Several databases and hidden markov models are needed: 

	wget http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch_db.tgz
	tar -xzvf SSUsearch_db.tgz

Parameters related to databases are **Ali_template, Copy_db, Gene_db_cc, Gene_db, Gene_model_org, Gene_tax_cc, Gene_tax, and Hmm**. First part of each database files its variable in Makefile. e.g. Ali_template.silva_lsu.fasta is for Ali_template. Set values of these parameters to **absolute paths** of their database in Makefile. Again, we can also set variables as commandline arguments. The default value should be OK for this tutorial if you follow the above steps.

Other than wgs data files, **a design file** is also needed for diversity analysis in mothur. [Some description](http://www.mothur.org/wiki/Design_header_file) can be found in mothur wiki. Use the first column as sample tag and second as treatment. Sample tag is the first part of wgs data file names. e.g. For M1.fa.gz, the tag is M1.

	# download a test dataset and its design file
	wget -r -np -nH --cut-dir=4 --reject="index.html*" http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/
	# check wgs data files
	ls test/data/*.fa
	# check design file
	cat test/SS.design
	# run the pipeline
	make -f Makefile Seqfiles="test/data/1c.fa test/data/1d.fa test/data/2c.fa test/data/2d.fa" Design=test/SS.design Script_dir=./scripts SSUsearch_db=./SSUsearch_db Method=ssusearch_no_qc Method=ssusearch_no_qc Hmmsearch=$HMMSEARCH_BIN Mothur=$MOTHUR_BIN Flash=$FLASH_BIN Mcclust_jar=$MCCLUST_JAR 

Taxonomy results are here:

	ls test/data/*.fa.ssu.out/*.taxonomy

By default, V4 will be used for OTU based analysis. The diversity analysis can be found at:

	# no copy correction
	ls diversity.ssu
	# copy correction
	ls diversity_cc.ssu

This pipeline includes PCoA, beta-diversity indces, weighted UNIFRAC and AMOVA. Familiarity with [mothur](http://www.mothur.org/wiki/Schloss_SOP) are needed to find and plot the specific results. With SS.shared, SS.names, SS.groups, SS.design, most analysis in mothur can be done.

Makefile includes many variables for steps in pipeline. To see a full list of variables in Makefile:

	make -f Makefile help


