
Set up working directory
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    cd /usr/local/notebooks

.. parsed-literal::

    /usr/local/notebooks


.. code:: python

    mkdir -p ./workdir
.. code:: python

    #check seqfile files to process in data directory (make sure you still remember the data directory)
    !ls ./data/test/data

.. parsed-literal::

    1c.fa  1d.fa  2c.fa  2d.fa


README
======

This part of pipeline search for the SSU rRNA gene fragments, classify them, and extract reads aligned specific region. It is also heavy lifting part of the whole pipeline (more cpu will help).
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

This part works with one seqfile a time. You just need to change the "Seqfile" and maybe other parameters in the two cells bellow.
----------------------------------------------------------------------------------------------------------------------------------

To run commands, click "Cell" then "Run All". After it finishes, you will see "\*\*\* pipeline runs successsfully :)" at bottom of this pape.
---------------------------------------------------------------------------------------------------------------------------------------------

If your computer has many processors, there are two ways to make use of the resource:
-------------------------------------------------------------------------------------

1. Set "Cpu" higher number.

2. make more copies of this notebook (click "File" then "Make a copy" in
   menu bar), so you can run the step on multiple files at the same
   time.

(Again we assume the "Seqfile" is quality trimmed.)

Here we will process one file at a time; set the "Seqfile" variable to the seqfile name to be be processed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First part of seqfile basename (separated by ".") will be the label of this sample, so named it properly.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

e.g. for "/usr/local/notebooks/data/test/data/1c.fa", "1c" will the
label of this sample.

.. code:: python

    Seqfile='./data/test/data/2d.fa'
Other parameters to set
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    Cpu='2'   # number of maxixum threads for search and alignment
    Hmm='./data/SSUsearch_db/Hmm.ssu.hmm'   # hmm model for ssu
    Gene='ssu'
    Script_dir='./SSUsearch/scripts'
    Gene_model_org='./data/SSUsearch_db/Gene_model_org.16s_ecoli_J01695.fasta'
    Ali_template='./data/SSUsearch_db/Ali_template.silva_ssu.fasta'
    
    Start='577'  #pick regions for de novo clustering
    End='727'
    Len_cutoff='100' # min length for reads picked for the region
    
    Gene_tax='./data/SSUsearch_db/Gene_tax.silva_taxa_family.tax' # silva 108 ref
    Gene_db='./data/SSUsearch_db/Gene_db.silva_108_rep_set.fasta'
    
    Gene_tax_cc='./data/SSUsearch_db/Gene_tax_cc.greengene_97_otus.tax' # greengene 2012.10 ref for copy correction
    Gene_db_cc='./data/SSUsearch_db/Gene_db_cc.greengene_97_otus.fasta'
.. code:: python

    # first part of file basename will the label of this sample
    import os
    Filename=os.path.basename(Seqfile)
    Tag=Filename.split('.')[0]
.. code:: python

    import os
    Hmm=os.path.abspath(Hmm)
    Seqfile=os.path.abspath(Seqfile)
    Script_dir=os.path.abspath(Script_dir)
    Gene_model_org=os.path.abspath(Gene_model_org)
    Ali_template=os.path.abspath(Ali_template)
    Gene_tax=os.path.abspath(Gene_tax)
    Gene_db=os.path.abspath(Gene_db)
    Gene_tax_cc=os.path.abspath(Gene_tax_cc)
    Gene_db_cc=os.path.abspath(Gene_db_cc)
    
    os.environ.update(
        {'Cpu':Cpu, 
         'Hmm':os.path.abspath(Hmm), 
         'Gene':Gene, 
         'Seqfile':os.path.abspath(Seqfile), 
         'Filename':Filename, 
         'Tag':Tag, 
         'Script_dir':os.path.abspath(Script_dir), 
         'Gene_model_org':os.path.abspath(Gene_model_org), 
         'Ali_template':os.path.abspath(Ali_template), 
         'Start':Start, 
         'End':End,
         'Len_cutoff':Len_cutoff,
         'Gene_tax':os.path.abspath(Gene_tax), 
         'Gene_db':os.path.abspath(Gene_db), 
         'Gene_tax_cc':os.path.abspath(Gene_tax_cc), 
         'Gene_db_cc':os.path.abspath(Gene_db_cc)})
.. code:: python

    !echo "*** make sure: parameters are right"
    !echo "Seqfile: $Seqfile\nCpu: $Cpu\nFilename: $Filename\nTag: $Tag"

.. parsed-literal::

    *** make sure: parameters are right
    Seqfile: /usr/local/notebooks/data/test/data/1c.fa
    Cpu: 2
    Filename: 1c.fa
    Tag: 1c


.. code:: python

    cd workdir

.. parsed-literal::

    /usr/local/notebooks/workdir


.. code:: python

    mkdir -p $Tag.ssu.out
.. code:: python

    ### start hmmsearch
.. code:: python

    !echo "*** hmmsearch starting"
    !time hmmsearch --incE 10 --incdomE 10 --cpu $Cpu \
      --domtblout $Tag.ssu.out/$Tag.qc.$Gene.hmmdomtblout \
      -o /dev/null -A $Tag.ssu.out/$Tag.qc.$Gene.sto \
      $Hmm $Seqfile
    !echo "*** hmmsearch finished"

.. parsed-literal::

    *** hmmsearch starting
    0.95user 0.04system 0:00.99elapsed 99%CPU (0avgtext+0avgdata 65712maxresident)k
    0inputs+1080outputs (0major+7774minor)pagefaults 0swaps
    *** hmmsearch finished


.. code:: python

    !python $Script_dir/get-seq-from-hmmout.py \
        $Tag.ssu.out/$Tag.qc.$Gene.hmmdomtblout \
        $Tag.ssu.out/$Tag.qc.$Gene.sto \
        $Tag.ssu.out/$Tag.qc.$Gene

.. parsed-literal::

    parsing hmmdotblout done..
    50 of 114 seqs are kept after hmm parser


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
    
    
    
    mothur > align.seqs(candidate=1c.ssu.out/1c.qc.ssu.RFadded, template=/usr/local/notebooks/data/SSUsearch_db/Ali_template.silva_ssu.fasta, threshold=0.5, flip=t, processors=2)
    
    Using 2 processors.
    
    Reading in the /usr/local/notebooks/data/SSUsearch_db/Ali_template.silva_ssu.fasta template sequences...	DONE.
    It took 25 to read  18491 sequences.
    Aligning sequences from 1c.ssu.out/1c.qc.ssu.RFadded ...
    23
    28
    It took 1 secs to align 51 sequences.
    
    
    Output File Names: 
    1c.ssu.out/1c.qc.ssu.align
    1c.ssu.out/1c.qc.ssu.align.report
    
    [WARNING]: your sequence names contained ':'.  I changed them to '_' to avoid problems in your downstream analysis.
    
    mothur > quit()
    26.96user 2.61system 0:29.14elapsed 101%CPU (0avgtext+0avgdata 4881984maxresident)k
    0inputs+7792outputs (0major+399013minor)pagefaults 0swaps


Get aligned seqs that have > 50% matched to references
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !python $Script_dir/mothur-align-report-parser-cutoff.py \
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

    28 sequences are matched to 577-727 region


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
    
    
    
    mothur > classify.seqs(fasta=1c.ssu.out/1c.qc.ssu.align.filter.fa, template=/usr/local/notebooks/data/SSUsearch_db/Gene_db.silva_108_rep_set.fasta, taxonomy=/usr/local/notebooks/data/SSUsearch_db/Gene_tax.silva_taxa_family.tax, cutoff=50, processors=2)
    
    Using 2 processors.
    Reading template taxonomy...     DONE.
    Reading template probabilities...     DONE.
    It took 20 seconds get probabilities. 
    Classifying sequences from 1c.ssu.out/1c.qc.ssu.align.filter.fa ...
    Processing sequence: 25
    Processing sequence: 25
    
    It took 0 secs to classify 50 sequences.
    
    
    It took 1 secs to create the summary file for 50 sequences.
    
    
    Output File Names: 
    1c.ssu.out/1c.qc.ssu.align.filter.silva_taxa_family.wang.taxonomy
    1c.ssu.out/1c.qc.ssu.align.filter.silva_taxa_family.wang.tax.summary
    
    
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
    
    
    
    mothur > classify.seqs(fasta=1c.ssu.out/1c.qc.ssu.align.filter.fa, template=/usr/local/notebooks/data/SSUsearch_db/Gene_db_cc.greengene_97_otus.fasta, taxonomy=/usr/local/notebooks/data/SSUsearch_db/Gene_tax_cc.greengene_97_otus.tax, cutoff=50, processors=2)
    
    Using 2 processors.
    Reading template taxonomy...     DONE.
    Reading template probabilities...     DONE.
    It took 14 seconds get probabilities. 
    Classifying sequences from 1c.ssu.out/1c.qc.ssu.align.filter.fa ...
    Processing sequence: 25
    Processing sequence: 25
    
    It took 1 secs to classify 50 sequences.
    
    
    It took 0 secs to create the summary file for 50 sequences.
    
    
    Output File Names: 
    1c.ssu.out/1c.qc.ssu.align.filter.greengene_97_otus.wang.taxonomy
    1c.ssu.out/1c.qc.ssu.align.filter.greengene_97_otus.wang.tax.summary
    
    
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

    1c.577to727
    1c.cut
    1c.forclust
    1c.qc.ssu
    1c.qc.ssu.align
    1c.qc.ssu.align.filter
    1c.qc.ssu.align.filter.577to727.cut
    1c.qc.ssu.align.filter.577to727.cut.lenscreen.fa
    1c.qc.ssu.align.filter.fa
    1c.qc.ssu.align.filter.greengene_97_otus.wang.tax.summary
    1c.qc.ssu.align.filter.silva_taxa_family.wang.tax.summary
    1c.qc.ssu.align.filter.wang.gg.taxonomy
    1c.qc.ssu.align.filter.wang.gg.taxonomy.count
    1c.qc.ssu.align.filter.wang.silva.taxonomy
    1c.qc.ssu.align.filter.wang.silva.taxonomy.count
    1c.qc.ssu.align.report
    1c.qc.ssu.hmmdomtblout
    1c.qc.ssu.hmmdomtblout.parsedToDictWithScore.pickle
    1c.qc.ssu.hmmtblout
    1c.qc.ssu.RFadded
    1c.qc.ssu.sto


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

.. code:: python

    !echo "*** pipeline runs successsfully :)"

.. parsed-literal::

    *** pipeline runs successsfully :)


