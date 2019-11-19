SSUsearch
=========
[![Snakemake](https://img.shields.io/badge/snakemake-≥5.2.0-brightgreen.svg)](https://snakemake.bitbucket.io)
[![Build Status](https://travis-ci.org/jiarong/SSUsearch.svg?branch=master)](https://travis-ci.org/jiarong/SSUsearch)

SSUsearch is pipeline for identify SSU rRNA gene and use them for diversity analysis. THe pipeline requires HMMER3.1, mothur, RDP mcclust, and python numpy, pandas, scipy, matplotlib, and screed package. The pipeline has two key features:

1. unsupervised (OTU based) community analysis with shotgun data

2. Scalibility: 5 Gb peak mem and 5 CPU hours on about 40 Gb data.

**The manuscript has been published in AEM (doi: 10.1128/AEM.02772-15). It is also available on [research gate](https://www.researchgate.net/publication/282945621_Microbial_community_analysis_with_ribosomal_gene_fragments_from_shotgun_metagenomes).**


Pipeline tutorial
------------------

## New! SSUsearch (1.0) is now powered by Snakemake and much easier to install and run.

### Step 1: Install dependencies

Install conda: (skip if you have `conda` ready)
```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh              # Make sure to "yes" to add the conda to your PATH
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
```

Install snakemake: (skip if you have `snakemake` version 5.2.0 or later ready)
```bash
conda install -c bioconda -c conda-forge snakemake
```

### Step 2: clone this repo and setp up `metadata.tsv` and `config.yaml`:
```bash
git clone https://github.com/jiarong/SSUsearch.git
cd SSUsearch
```

You just need to prepare two files: `metadata.tsv` and `config.yaml` following the templates in the repo:

The `metadata.tsv` file is metadata about samples with the following headers:
- ID: sample name
- GROUP: treatment that a sample belongs to
- R1: path of unmerged R1 of paired ends
- R2: path of unmerged R2 of paired ends
- merged: path of merged paired ends
- **Try to use absolute paths to avoid troulbe; If relative paths are used, they should be relative to working direcory (WORKDIR in config.yaml file)**
- ssusearch internally only pick one read from paired ends for clustering and taxonomy summary; it is very flexible on input formats: merged, unmerged, single ends are all allowed. Single end data can be put under R1. use NA or empty string ("") if no such a file.

The `config.yaml` file has parameter setting for tools in the pipeline. It is YAML format. The `metadata.tsv` path is also set in `config.yaml`.

### Step 3: When the above two files are ready, you just need to run the following command.

```bash
./ssusearch --configfile config.yaml
```

It will run ssusearch with test dataset included in the repo. All output are in a directory name by "Project" parameter in `config.yaml` (**test** in this case); `test/test.biom` and `test_cc.biom` (copy # corrected) can be used as input to mothur, QIIME and phyloseq for common community diversity analyses. If you want conventional OTU table, use `test/clust/test.shared` (A.K.A shared file in mothur). Taxonomy classifications are in `test/taxa_summary/` directory.

All snakemake make options are also allowed, e.g.
```bash
./ssusearch --configfile config.yaml --core 4
```
The above limit the maximum # of processes or threads to 4. See more workflow managemnt options in snakemake help (`snakemake -h`).

### Run on HPC

SSUsearch can also easily run in computer clusters. The search step in the pipeline, most computationally instensive step, can be run parallelly for each sample. There is a convenient script in `hpc/slurm/submit.sub` for SLURM (used in MSU HPCC). You just need to modify the following vaviables in the script (using absolute paths):

```bash
Workdir=.                                   # a working directory    
SSUsearch=ssusearch                         # ssusearch file
Configfile=config.yaml                      # config.yaml file
Clust_config=hpc/slurm/cluster.yaml         # hpc/slurm/cluster.yaml file
Jobscript=hpc/slurm/jobscript.sh            # hpc/slurm/jobscript.sh file
```

Then submit the job:
```bash
sbatch hpc/slurm/submit.sub
```

Results will be in `Workdir`.

### Notes

Installing dependencies is a part of the pipeline, done by conda. It only need to be done once for each working directory but it might be slow (>10 mins) depending on the network connection. If installation is interupted somehow, you need to delete the `.snakemake` directory in your working directory before running again.

The soil datasets used in the paper are pair end merged long reads (longest is ~300 bp) and the default Start, End, and Len\_cutoff are set for those datasets. For datasets have 100bp reads, Start=577, End=657, Len\_cutoff=75 is recommended. Rule of thumb is to pick a region with more reads with larger overlap. Details are in "Testing  the  effect  of  target  region  size  and  variable  region  on clustering" of the paper.

--------------------

If you prefer to run the pipeline step by step in linux command line, please go to http://microbial-ecology-protocols.readthedocs.org/en/latest/SSUsearch/overview.html

---------------------


### Run on EC2 (all platform)

The tutorials are written in ipython notebook. The **easiest way to run it** is using amazon EC2 instances with ami **ami-7c82af16** and **add security groups https**. Add more storage according to your data size (the default is 20 Gb). [Here](http://ged.msu.edu/angus/tutorials-2012/start-up-an-ec2-instance.html) is tutorial on how to setup EC2 instances. Notebooks could be accessed through https using browser (**chrome or firefox NOT safari**). Briefly, connect into your machine by using "https://" plus your machine name or IP address, and accept the “broken certificate” message. Password to access https is **openscience**. There are some introduction [here](http://ged.msu.edu/angus/tutorials-2012/introducing-ipython-notebook.html).

### Run on your computer (linux only)

If you want to run the notebooks on your computer, ipython (v4) with notebook dependencies are needed.

If you already have Python:

	pip install "ipython[notebook]"

If you are new to Python, go to http://continuum.io/downloads and copy the link for Linux installer (pay attention to 64 or 32 bit version based on your cpu type). This tutorial use 64 bit version. At the time of this writing the 64 bit installer is [here](https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.2.0-Linux-x86_64.sh).

	wget -c https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.2.0-Linux-x86_64.sh

	bash Anaconda-2.2.0-Linux-x86_64.sh 

Accept the license.
Choose an installation directory (default is fine). 
Add to default path at the end of installation. 

Then 

	source ~/.bashrc

Ipython is ready to go :)

Download SSUsearch:

	cd ~/Desktop
	git clone https://github.com/jiarong/SSUsearch

Go to notebook directory:

	cd SSUsearch/notebooks-pc-linux

Start ipython notebook: 

	ipython notebook

In your default web browser, you will see a page showing several \*.ipynb links.

First open overview.ipynb, and follow the instructions there. **You will need to change the data directory settings for your own data**.
