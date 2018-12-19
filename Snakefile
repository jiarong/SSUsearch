# The main entry point of your workflow.
# After configuring, running snakemake -n in a clone of this repository should successfully execute a dry-run of the workflow.

import os
import sys
import pandas as pd
from snakemake.utils import min_version, validate

### pipeline version
VERSION = '1.0.0'
### set minimum snakemake version ###
min_version('4.8.0')

if config['Workdir']:
    workdir: config['Workdir']

Df = pd.read_table(config['Metadata']).set_index('ID', drop=False)
Df = Df.astype(str)
validate(Df, 'schemas/metadata.schema.yaml')

Srcdir = srcdir('.') # directory where snakefile is
### check wether SSUsearch_db has been downloaded
if config['Refdir']:
    Refdir = config['Refdir']
else:
    Refdir = '{}'.format(Srcdir)

Refdir = os.path.abspath(Refdir)
Downdir = Refdir
Refdir = '{}/SSUsearch_db'.format(Refdir)
if not os.path.exists(Refdir):
    mes = (
        '*** SSUsearch_db has not been downloaded yet..\n'
        '*** Downloading to {} ..\n'
        '*** Make sure you have write permission..\n'
        '***   or else change "Refdir" in config file..\n'
    ).format(Downdir)
    print(mes)
    shell(
        """
        cd {Downdir} && curl https://zenodo.org/record/1492910/files/SSUsearch_db.tgz?download=1 -o SSUsearch_db.tgz && tar -xzvf SSUsearch_db.tgz
        """
    )


Gene = config['Gene']
Hmm = '{}/Hmm.{}.hmm'.format(Refdir, Gene)   # hmm model for ssu
Gene_model_org = '{}/Gene_model_org.{}.fasta'.format(Refdir, Gene)
Ali_template = '{}/Ali_template.{}.silva.fasta'.format(Refdir, Gene)
Gene_tax = '{}/Gene_tax.{}.silva_108_rep_family.tax'.format(Refdir, Gene) # silva ref
Gene_db = '{}/Gene_db.{}.silva_108_rep.fasta'.format(Refdir, Gene)
Gene_tax_cc = '{}/Gene_tax_cc.{}.greengene_rep.tax'.format(Refdir, Gene) # greengene 2012.10 ref for copy correction
Gene_db_cc = '{}/Gene_db_cc.{}.greengene_rep.fasta'.format(Refdir, Gene)
Copy_db_cc = '{}/Copy_db_cc.{}.copyrighter.txt'.format(Refdir, Gene)


Samples = Df.index
Start = config['Start']
End = config['End']
Len_cutoff = config['Len_cutoff']
Java_xmx = config['Java_xmx']  # increase this if your machine has more memory
Otu_dist_cutoff = config['Otu_dist_cutoff']
Project = config['Project']

print('Please double check the metadata info:')
print(Df.to_string(index=False, justify='right'))

localrules: taxa_summary, make_biom, copy_correction, all

include: 'rules/convert_seqname.smk'

### search step
include: 'rules/hmmsearch.smk'
include: 'rules/region_cut.smk'

### classification
include: 'rules/classify.smk'
include: 'rules/taxa_summary.smk'

### clustering
include: 'rules/clust.smk'
include: 'rules/make_biom.smk'

### copy correction
include: 'rules/copy_correction.smk'



rule all:
    input:
        # The first rule should define the default target files
        # Subsequent target rules can be specified below. They should start with all_*.
        #
        expand('{project}/seqname_convert/{sample}.fa', project=Project, sample=Samples),
        expand('{project}/search/{sample}/{sample}.forclust', project=Project, sample=Samples),
        expand('{project}/search/{sample}/{sample}.align.filter.wang.gg.taxonomy.count', project=Project, sample=Samples),
        expand('{project}/search/{sample}/{sample}.align.filter.wang.silva.taxonomy.count', project=Project, sample=Samples),
        expand('{project}/taxa_summary/level.{i}.tsv', project=Project, i=[1,2,3,4,5]),
        expand('{project}/{project}.biom', project=Project),
        expand('{project}/{project}.cc.biom', project=Project),


##### singularity #####

# this container defines the underlying OS for each job when using the workflow
# with --use-conda --use-singularity
#singularity: "docker://continuumio/miniconda3"

##### report #####

report: "report/workflow.rst"

onstart: 
    print('----------------------------------')
    print('Welcome to the SSUsearch pipeline.')
    print('----------------------------------')

onsuccess:
    print("\n--- SSUsearch Workflow executed successfully! ---\n")
