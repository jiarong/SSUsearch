
Set up working directory
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    mkdir -p /usr/local/notebooks/workdir

.. code:: python

    cd /usr/local/notebooks/workdir


.. parsed-literal::

    /usr/local/notebooks/workdir


.. code:: python

    #check seqfile files to process in data directory
    !ls /usr/local/notebooks/data/test/data


.. parsed-literal::

    1c.fa  1d.fa  2c.fa  2d.fa


README
======

This part of pipeline works with one seqfile a time. You just need to change the "Seqfile" and maybe other parameters in the two cells bellow.
----------------------------------------------------------------------------------------------------------------------------------------------

If your computer has many processors, there are two ways to make use of the resource:
-------------------------------------------------------------------------------------

1. Set "Cpu" higher number.

2. make more copies of this notebook (click "file" then "Make a copy" in
   menu bar), so you can run the step on multiple files at the same
   time.

(Again we assume the "Seqfile" is quality trimmed.)

Here we will process one file at a time; set the "Seqfile" variable to the seqfile name to be be processed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Seqfile='/usr/local/notebooks/data/test/data/2c.fa'

Other parameters to set
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Cpu='2'   # number of maxixum threads for search and alignment
    Hmm='/usr/local/notebooks/data/SSUsearch_db/Hmm.ssu.hmm'   # hmm model for ssu
    Gene='ssu'
    Script_dir='/usr/local/notebooks/external_tools/SSUsearch/scripts'
    Gene_model_org='/usr/local/notebooks/data/SSUsearch_db/Gene_model_org.16s_ecoli_J01695.fasta'
    Ali_template='/usr/local/notebooks/data/SSUsearch_db/Ali_template.silva_ssu.fasta'
    
    Start='577'  #pick regions for de novo clustering
    End='727'
    Len_cutoff='100' # min length for reads picked for the region
    
    Gene_tax='/usr/local/notebooks/data/SSUsearch_db/Gene_tax.silva_taxa_family.tax' # silva 108 ref
    Gene_db='/usr/local/notebooks/data/SSUsearch_db/Gene_db.silva_108_rep_set.fasta'
    
    Gene_tax_cc='/usr/local/notebooks/data/SSUsearch_db/Gene_tax_cc.greengene_97_otus.tax' # greengene 2012.10 ref for copy correction
    Gene_db_cc='/usr/local/notebooks/data/SSUsearch_db/Gene_db_cc.greengene_97_otus.fasta'

.. code:: python

    import os
    Filename=os.path.basename(Seqfile)
    Tag=Filename.split('.')[0]

.. code:: python

    import os
    os.environ.update(
        {'Cpu':Cpu, 
         'Hmm':Hmm, 
         'Gene':Gene, 
         'Seqfile':Seqfile, 
         'Filename':Filename, 
         'Tag':Tag, 
         'Script_dir':Script_dir, 
         'Gene_model_org':Gene_model_org, 
         'Ali_template':Ali_template, 
         'Start':Start, 
         'End':End,
         'Len_cutoff':Len_cutoff,
         'Gene_tax':Gene_tax, 
         'Gene_db':Gene_db, 
         'Gene_tax_cc':Gene_tax_cc, 
         'Gene_db_cc':Gene_db_cc})

.. code:: python

    !echo "*** make sure: parameters are right"
    !echo "Seqfile: $Seqfile\nCpu: $Cpu\nFilename: $Filename\nTag: $Tag"


.. parsed-literal::

    *** make sure: parameters are right
    Seqfile: /usr/local/notebooks/data/test/data/2c.fa
    Cpu: 2
    Filename: 2c.fa
    Tag: 2c


.. code:: python

    mkdir -p $Tag.ssu.out

.. code:: python

    ### start hmmsearch

.. code:: python

    !echo "*** hmmsearch starting"
    !time hmmsearch --incE 10 --incdomE 10 --cpu $Cpu \
      --tblout $Tag.ssu.out/$Tag.qc.$Gene.hmmtblout \
      -o /dev/null \
      $Hmm $Seqfile
    !echo "*** hmmsearch finished"


.. parsed-literal::

    *** hmmsearch starting
    0.91user 0.04system 0:00.95elapsed 99%CPU (0avgtext+0avgdata 64880maxresident)k
    32inputs+40outputs (0major+7574minor)pagefaults 0swaps
    *** hmmsearch finished


.. code:: python

    !python $Script_dir/get-seq-from-hmmtblout.py \
        $Tag.ssu.out/$Tag.qc.$Gene.hmmtblout \
        $Seqfile \
        $Tag.ssu.out/$Tag.qc.$Gene


.. parsed-literal::

    50 hits at 10 cutoff


Pass hits to mothur aligner
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !echo "*** Starting mothur align"
    !cat  $Gene_model_org $Tag.ssu.out/$Tag.qc.$Gene > $Tag.ssu.out/$Tag.qc.$Gene.RFadded
    
    # mothur does not allow tab between its flags, thus no indents here
    !time mothur "#align.seqs(candidate=$Tag.ssu.out/$Tag.qc.$Gene.RFadded, template=$Ali_template, threshold=0.5, flip=t, processors=$Cpu)"
    
    !rm -f mothur.*.logfile


.. parsed-literal::

    *** Starting mothur align
    [H[2J
    
    
    
    
    
    mothur v.1.34.4
    Last updated: 12/22/2014
    
    by
    Patrick D. Schloss
    
    Department of Microbiology & Immunology
    University of Michigan
    pschloss@umich.edu
    http://www.mothur.org
    
    When using, please cite:
    Schloss, P.D., et al., Introducing mothur: Open-source, platform-independent, community-supported software for describing and comparing microbial communities. Appl Environ Microbiol, 2009. 75(23):7537-41.
    
    Distributed under the GNU General Public License
    
    Type 'help()' for information on the commands that are available
    
    Type 'quit()' to exit program
    
    
    
    mothur > align.seqs(candidate=2c.ssu.out/2c.qc.ssu.RFadded, template=/usr/local/notebooks/data/SSUsearch_db/Ali_template.silva_ssu.fasta, threshold=0.5, flip=t, processors=2)
    
    Using 2 processors.
    
    Reading in the /usr/local/notebooks/data/SSUsearch_db/Ali_template.silva_ssu.fasta template sequences...	DONE.
    It took 25 to read  18491 sequences.
    Aligning sequences from 2c.ssu.out/2c.qc.ssu.RFadded ...
    24
    27
    It took 1 secs to align 51 sequences.
    
    
    Output File Names: 
    2c.ssu.out/2c.qc.ssu.align
    2c.ssu.out/2c.qc.ssu.align.report
    
    [WARNING]: your sequence names contained ':'.  I changed them to '_' to avoid problems in your downstream analysis.
    
    mothur > quit()
    26.95user 2.68system 0:29.41elapsed 100%CPU (0avgtext+0avgdata 4881696maxresident)k
    2087696inputs+7672outputs (0major+398990minor)pagefaults 0swaps


Get aligned seqs that have > 50% matched to references
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !python $Script_dir/mothur-align-report-parser.py \
        $Tag.ssu.out/$Tag.qc.$Gene.align.report \
        $Tag.ssu.out/$Tag.qc.$Gene.align \
        $Tag.ssu.out/$Tag.qc.$Gene.align.filter \
        0.5
        


.. parsed-literal::

    0 bad seqs out of 51 total are removed from alignment


.. code:: python

    !python $Script_dir/remove-gap.py $Tag.ssu.out/$Tag.qc.$Gene.align.filter $Tag.ssu.out/$Tag.qc.$Gene.align.filter.fa

Search is done here (the computational intensive part). Hooray!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  $Tag.ssu.out/$Tag.qc.$Gene.align.filter:
    aligned SSU rRNA gene fragments

-  $Tag.ssu.out/$Tag.qc.$Gene.align.filter.fa:
    unaligned SSU rRNA gene fragments

Extract the reads mapped 150bp region in V4 (577-727 in *E.coli* SSU rRNA gene position) for unsupervised clustering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !python $Script_dir/region-cut.py $Tag.ssu.out/$Tag.qc.$Gene.align.filter $Start $End $Len_cutoff
    
    !mv $Tag.ssu.out/$Tag.qc.$Gene.align.filter."$Start"to"$End".cut.lenscreen $Tag.ssu.out/$Tag.forclust


.. parsed-literal::

    50 sequences are matched to 577-727 region


Classify SSU rRNA gene seqs using SILVA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !rm -f $Tag.ssu.out/$Tag.qc.$Gene.align.filter.*.wang.taxonomy
    !mothur "#classify.seqs(fasta=$Tag.ssu.out/$Tag.qc.$Gene.align.filter.fa, template=$Gene_db, taxonomy=$Gene_tax, cutoff=50, processors=$Cpu)"
    !mv $Tag.ssu.out/$Tag.qc.$Gene.align.filter.*.wang.taxonomy \
        $Tag.ssu.out/$Tag.qc.$Gene.align.filter.wang.silva.taxonomy


.. parsed-literal::

    [H[2J
    
    
    
    
    
    mothur v.1.34.4
    Last updated: 12/22/2014
    
    by
    Patrick D. Schloss
    
    Department of Microbiology & Immunology
    University of Michigan
    pschloss@umich.edu
    http://www.mothur.org
    
    When using, please cite:
    Schloss, P.D., et al., Introducing mothur: Open-source, platform-independent, community-supported software for describing and comparing microbial communities. Appl Environ Microbiol, 2009. 75(23):7537-41.
    
    Distributed under the GNU General Public License
    
    Type 'help()' for information on the commands that are available
    
    Type 'quit()' to exit program
    
    
    
    mothur > classify.seqs(fasta=2c.ssu.out/2c.qc.ssu.align.filter.fa, template=/usr/local/notebooks/data/SSUsearch_db/Gene_db.silva_108_rep_set.fasta, taxonomy=/usr/local/notebooks/data/SSUsearch_db/Gene_tax.silva_taxa_family.tax, cutoff=50, processors=2)
    
    Using 2 processors.
    Reading template taxonomy...     DONE.
    Reading template probabilities...     DONE.
    It took 20 seconds get probabilities. 
    Classifying sequences from 2c.ssu.out/2c.qc.ssu.align.filter.fa ...
    Processing sequence: 25
    Processing sequence: 25
    
    It took 1 secs to classify 50 sequences.
    
    
    It took 0 secs to create the summary file for 50 sequences.
    
    
    Output File Names: 
    2c.ssu.out/2c.qc.ssu.align.filter.silva_taxa_family.wang.taxonomy
    2c.ssu.out/2c.qc.ssu.align.filter.silva_taxa_family.wang.tax.summary
    
    
    mothur > quit()


.. code:: python

    !python $Script_dir/count-taxon.py \
        $Tag.ssu.out/$Tag.qc.$Gene.align.filter.wang.silva.taxonomy \
        $Tag.ssu.out/$Tag.qc.$Gene.align.filter.wang.silva.taxonomy.count
    !rm -f mothur.*.logfile

Classify SSU rRNA gene seqs with Greengene for copy correction later
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !rm -f $Tag.ssu.out/$Tag.qc.$Gene.align.filter.*.wang.taxonomy
    !mothur "#classify.seqs(fasta=$Tag.ssu.out/$Tag.qc.$Gene.align.filter.fa, template=$Gene_db_cc, taxonomy=$Gene_tax_cc, cutoff=50, processors=$Cpu)"
    !mv $Tag.ssu.out/$Tag.qc.$Gene.align.filter.*.wang.taxonomy \
        $Tag.ssu.out/$Tag.qc.$Gene.align.filter.wang.gg.taxonomy


.. parsed-literal::

    [H[2J
    
    
    
    
    
    mothur v.1.34.4
    Last updated: 12/22/2014
    
    by
    Patrick D. Schloss
    
    Department of Microbiology & Immunology
    University of Michigan
    pschloss@umich.edu
    http://www.mothur.org
    
    When using, please cite:
    Schloss, P.D., et al., Introducing mothur: Open-source, platform-independent, community-supported software for describing and comparing microbial communities. Appl Environ Microbiol, 2009. 75(23):7537-41.
    
    Distributed under the GNU General Public License
    
    Type 'help()' for information on the commands that are available
    
    Type 'quit()' to exit program
    
    
    
    mothur > classify.seqs(fasta=2c.ssu.out/2c.qc.ssu.align.filter.fa, template=/usr/local/notebooks/data/SSUsearch_db/Gene_db_cc.greengene_97_otus.fasta, taxonomy=/usr/local/notebooks/data/SSUsearch_db/Gene_tax_cc.greengene_97_otus.tax, cutoff=50, processors=2)
    
    Using 2 processors.
    Reading template taxonomy...     DONE.
    Reading template probabilities...     DONE.
    It took 14 seconds get probabilities. 
    Classifying sequences from 2c.ssu.out/2c.qc.ssu.align.filter.fa ...
    Processing sequence: 25
    Processing sequence: 25
    
    It took 2 secs to classify 50 sequences.
    
    
    It took 0 secs to create the summary file for 50 sequences.
    
    
    Output File Names: 
    2c.ssu.out/2c.qc.ssu.align.filter.greengene_97_otus.wang.taxonomy
    2c.ssu.out/2c.qc.ssu.align.filter.greengene_97_otus.wang.tax.summary
    
    
    mothur > quit()


.. code:: python

    !python $Script_dir/count-taxon.py \
        $Tag.ssu.out/$Tag.qc.$Gene.align.filter.wang.gg.taxonomy \
        $Tag.ssu.out/$Tag.qc.$Gene.align.filter.wang.gg.taxonomy.count
    !rm -f mothur.*.logfile

.. code:: python

    # check the output directory
    !ls $Tag.ssu.out


.. parsed-literal::

    2c.577to727
    2c.qc.ssu
    2c.qc.ssu.align
    2c.qc.ssu.align.filter
    2c.qc.ssu.align.filter.577to727.cut
    2c.qc.ssu.align.filter.577to727.cut.lenscreen.fa
    2c.qc.ssu.align.filter.fa
    2c.qc.ssu.align.filter.greengene_97_otus.wang.tax.summary
    2c.qc.ssu.align.filter.silva_taxa_family.wang.tax.summary
    2c.qc.ssu.align.filter.wang.gg.taxonomy
    2c.qc.ssu.align.filter.wang.gg.taxonomy.count
    2c.qc.ssu.align.filter.wang.silva.taxonomy
    2c.qc.ssu.align.filter.wang.silva.taxonomy.count
    2c.qc.ssu.align.report
    2c.qc.ssu.hmmtblout
    2c.qc.ssu.RFadded


This part of pipeline (working with one sequence file) finishes here. Next we will combine samples for community analysis (see unsupervised analysis).
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following are files useful for community analysis:

-  1c.577to727: aligned fasta file of seqs mapped to target region for
   de novo clustering
-  1c.qc.ssu.align.filter: aligned fasta file of all SSU rRNA gene
   fragments
-  1c.qc.ssu.align.filter.wang.gg.taxonomy: Greengene taxonomy (for copy
   correction)
-  1c.qc.ssu.align.filter.wang.silva.taxonomy: SILVA taxonomy

