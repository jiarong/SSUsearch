
set another directory for unsupervised analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    cd /usr/local/notebooks

.. parsed-literal::

    /usr/local/notebooks


.. code:: python

    mkdir -p ./workdir/clust
.. code:: python

    Prefix='SS'    # name for the analysis run
    Script_dir='./SSUsearch/scripts'
    Wkdir='./workdir'
    Mcclust_jar='./external_tools/Clustering/dist/Clustering.jar'
    Java_xmx='10g'
    Java_gc_threads='2'
    Otu_dist_cutoff='0.05'
    Design='./data/test/SS.design'

.. code:: python

    # get absolute path
    import os
    Script_dir=os.path.abspath(Script_dir)
    Wkdir=os.path.abspath(Wkdir)
    Mcclust_jar=os.path.abspath(Mcclust_jar)
    Design=os.path.abspath(Design)
    
    os.environ.update(
        {'Prefix':Prefix, 
         'Script_dir': Script_dir, 
         'Wkdir': Wkdir, 
         'Mcclust_jar': Mcclust_jar, 
         'Java_xmx':Java_xmx, 
         'Java_gc_threads':Java_gc_threads, 
         'Otu_dist_cutoff':Otu_dist_cutoff, 
         'Design': Design})
.. code:: python

    cd ./workdir/clust

.. parsed-literal::

    /usr/local/notebooks/workdir/clust


.. code:: python

    cat $Wkdir/*.ssu.out/*.forclust > combined_seqs.afa
.. code:: python

    # make group file for mcclust and mothur. 
    # first part of the file basename will be the group label, e.g. file "aa.bb.cc" will have "aa" as group label.
    !python $Script_dir/make-groupfile.py $Prefix.groups $Wkdir/*.ssu.out/*.forclust

.. parsed-literal::

    input is list of files..


.. code:: python

    !echo "*** Starting mcclust derep"
    !time java -Xmx$Java_xmx -XX:+UseParallelOldGC -XX:ParallelGCThreads=$Java_gc_threads \
        -jar $Mcclust_jar derep -a -o derep.fasta \
        temp.mcclust.names temp.txt combined_seqs.afa
        
    !rm temp.txt

.. parsed-literal::

    *** Starting mcclust derep
    Processing combined_seqs.afa
    Total sequences: 199
    Unique sequences: 174
    Dereplication complete: 499
    0.62user 0.14system 0:00.84elapsed 90%CPU (0avgtext+0avgdata 354992maxresident)k
    1936inputs+192outputs (1major+23117minor)pagefaults 0swaps


.. code:: python

    # convert mcclust names to mothur names
    !python $Script_dir/mcclust2mothur_names_file.py temp.mcclust.names temp.mothur.names
.. code:: python

    !echo "starting preclust.."
    ### output: derep.precluster.fasta, derep.precluster.names
    !mothur "#pre.cluster(fasta=derep.fasta, diffs=1, name=temp.mothur.names)"

.. parsed-literal::

    starting preclust..
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
    
    
    
    mothur > pre.cluster(fasta=derep.fasta, diffs=1, name=temp.mothur.names)
    
    Using 1 processors.
    0	174	0
    100	165	9
    174	163	11
    Total number of sequences before precluster was 174.
    pre.cluster removed 11 sequences.
    
    It took 0 secs to cluster 174 sequences.
    
    Output File Names: 
    derep.precluster.fasta
    derep.precluster.names
    derep.precluster.map
    
    
    mothur > quit()


.. code:: python

    !python $Script_dir/mothur2mcclust_names_file.py derep.precluster.names $Prefix.names
.. code:: python

    !time java -Xmx$Java_xmx -XX:+UseParallelOldGC -XX:ParallelGCThreads=$Java_gc_threads \
        -jar $Mcclust_jar dmatrix \
        -l 25 -o matrix.bin -i $Prefix.names -I derep.precluster.fasta

.. parsed-literal::

    Reading sequences(memratio=1.2895267219085598E-4)...
    Using distance model edu.msu.cme.rdp.alignment.pairwise.rna.UncorrectedDistanceModel
    Read 163 Nucleotide sequences (memratio=2.579355191410434E-4)
    Reading ID Mapping from file /usr/local/notebooks/SS.names
    Read mapping for 199 sequences (memratio=3.8690076414828753E-4)
    Starting distance computations, predicted max edges=26569, at=Mon Jun 22 21:42:46 UTC 2015
    Dumping 13203 edges to partial_matrix0 FINAL EDGES (memory ratio=0.001850005274547931)
    Matrix edges computed: 129
    Maximum distance: 0.5238095238095238
    Splits: 1
    Partition files merged: 102
    0.60user 0.08system 0:00.55elapsed 124%CPU (0avgtext+0avgdata 201776maxresident)k
    1872inputs+376outputs (0major+14881minor)pagefaults 0swaps


.. code:: python

    !time java -Xmx$Java_xmx -XX:+UseParallelOldGC -XX:ParallelGCThreads=$Java_gc_threads \
        -jar $Mcclust_jar cluster -m upgma \
        -i $Prefix.names -s $Prefix.groups -o complete.clust -d matrix.bin
    
    !python $Script_dir/mcclust2mothur-list-cutoff.py complete.clust $Prefix.list $Otu_dist_cutoff
    !sed -i 's/:/_/g' $Prefix.names $Prefix.groups $Prefix.list
    !echo "*** Replace ':' with '_' in seq names (original illumina name has ':' in them)"

.. parsed-literal::

    lambda=0
    Clustering complete: 619
    Lookaheads performed: 0
    Time spent Looking ahead: 0
    1.33user 0.15system 0:00.79elapsed 188%CPU (0avgtext+0avgdata 284992maxresident)k
    368inputs+744outputs (0major+20127minor)pagefaults 0swaps
    File(s):	1c 1d 2c 2d 
    
    Sequences:	50 49 50 50 
    
    *** Replace ':' with '_' in seq names (original illumina name has ':' in them)


.. code:: python

    !java -jar $Mcclust_jar rep-seqs -c -l -s complete.clust $Otu_dist_cutoff combined_seqs.afa
    !mv complete.clust_rep_seqs.fasta otu_rep_align.fa
.. code:: python

    !mothur "#make.shared(list=$Prefix.list, group=$Prefix.groups, label=$Otu_dist_cutoff);"
    !cat $Wkdir/*.ssu.out/*.silva.taxonomy > $Prefix.taxonomy
    !mothur "#classify.otu(list=$Prefix.list, taxonomy=$Prefix.taxonomy, label=$Otu_dist_cutoff)"
    !mothur "#make.biom(shared=$Prefix.shared, constaxonomy=$Prefix.$Otu_dist_cutoff.cons.taxonomy)"
    !mv $Prefix.$Otu_dist_cutoff.biom $Prefix.biom

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
    
    
    
    mothur > make.shared(list=SS.list, group=SS.groups, label=0.05)
    0.05
    
    Output File Names: 
    SS.shared
    SS.1c.rabund
    SS.1d.rabund
    SS.2c.rabund
    SS.2d.rabund
    
    
    mothur > quit()
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
    
    
    
    mothur > classify.otu(list=SS.list, taxonomy=SS.taxonomy, label=0.05)
    reftaxonomy is not required, but if given will keep the rankIDs in the summary file static.
    0.05	130
    
    Output File Names: 
    SS.0.05.cons.taxonomy
    SS.0.05.cons.tax.summary
    
    
    mothur > quit()
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
    
    
    
    mothur > make.biom(shared=SS.shared, constaxonomy=SS.0.05.cons.taxonomy)
    0.05
    
    Output File Names: 
    SS.0.05.biom
    
    
    mothur > quit()


.. code:: python

    # clean up tempfiles
    !rm -f mothur.*.logfile *rabund complete* derep.fasta matrix.bin nonoverlapping.bin temp.*
With SS.groups, SS.names and SS.list, most diversity analysis can be done by mothur. You can look at `mothur wiki <http://www.mothur.org/wiki/454_SOP>`_ for details (Do not forgot to do even sampling before beta-diversity analysis).
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SS.biom file can used in most tools. (qiime and rdp)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    #since The purpose of this tutorial is to show our new pipeline, we will skip details of community analysis with mothur
    #following are some common commands in mothur
    
    !mothur "#make.shared(biom=$Prefix.biom); sub.sample(shared=$Prefix.shared); summary.single(calc=nseqs-coverage-sobs-chao-shannon-invsimpson); dist.shared(calc=braycurtis); pcoa(phylip=$Prefix.userLabel.subsample.braycurtis.userLabel.lt.dist); nmds(phylip=$Prefix.userLabel.subsample.braycurtis.userLabel.lt.dist); amova(phylip=$Prefix.userLabel.subsample.braycurtis.userLabel.lt.dist, design=$Design); tree.shared(calc=braycurtis); unifrac.weighted(tree=$Prefix.userLabel.subsample.braycurtis.userLabel.tre, group=$Design, random=T)"
    !rm -f mothur.*.logfile; 
    !rm -f *.rabund

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
    
    
    
    mothur > make.shared(biom=SS.biom)
    
    userLabel
    
    Output File Names: 
    SS.shared
    SS.1c.rabund
    SS.1d.rabund
    SS.2c.rabund
    SS.2d.rabund
    
    
    mothur > sub.sample(shared=SS.shared)
    Sampling 49 from each group.
    userLabel
    
    Output File Names: 
    SS.userLabel.subsample.shared
    
    
    mothur > summary.single(calc=nseqs-coverage-sobs-chao-shannon-invsimpson)
    Using SS.userLabel.subsample.shared as input file for the shared parameter.
    
    Processing group 1c
    
    userLabel
    
    Processing group 1d
    
    userLabel
    
    Processing group 2c
    
    userLabel
    
    Processing group 2d
    
    userLabel
    
    Output File Names: 
    SS.userLabel.subsample.groups.summary
    
    
    mothur > dist.shared(calc=braycurtis)
    Using SS.userLabel.subsample.shared as input file for the shared parameter.
    
    Using 1 processors.
    userLabel
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.lt.dist
    
    
    mothur > pcoa(phylip=SS.userLabel.subsample.braycurtis.userLabel.lt.dist)
    
    Processing...
    Rsq 1 axis: 0.91053
    Rsq 2 axis: 0.726899
    Rsq 3 axis: 1
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.lt.pcoa.axes
    SS.userLabel.subsample.braycurtis.userLabel.lt.pcoa.loadings
    
    
    mothur > nmds(phylip=SS.userLabel.subsample.braycurtis.userLabel.lt.dist)
    Processing Dimension: 2
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    
    Number of dimensions:	2
    Lowest stress :	0.15928
    R-squared for configuration:	0.314006
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.lt.nmds.iters
    SS.userLabel.subsample.braycurtis.userLabel.lt.nmds.stress
    SS.userLabel.subsample.braycurtis.userLabel.lt.nmds.axes
    
    
    mothur > amova(phylip=SS.userLabel.subsample.braycurtis.userLabel.lt.dist, design=/usr/local/notebooks/data/test/SS.design)
    c-d	Among	Within	Total
    SS	0.357247	0.673053	1.0303
    df	1	2	3
    MS	0.357247	0.336526
    
    Fs:	1.06157
    p-value: 0.349
    
    Experiment-wise error rate: 0.05
    If you have borderline P-values, you should try increasing the number of iterations
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.lt.amova
    
    
    mothur > tree.shared(calc=braycurtis)
    Using SS.userLabel.subsample.shared as input file for the shared parameter.
    
    Using 1 processors.
    userLabel
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.tre
    
    
    mothur > unifrac.weighted(tree=SS.userLabel.subsample.braycurtis.userLabel.tre, group=/usr/local/notebooks/data/test/SS.design, random=T)
    
    Using 1 processors.
    Tree#	Groups	WScore	WSig
    1	c-d	0.942529	<0.0010
    It took 0 secs to run unifrac.weighted.
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.trewsummary
    SS.userLabel.subsample.braycurtis.userLabel.tre1.weighted
    
    
    mothur > quit()


.. code:: python

    !echo "This part of pipeline finishes successfully :)"

.. parsed-literal::

    This part of pipeline finishes successfully :)



.. code:: python

    ### some simple visualization
.. code:: python

    # alpha diveristy index
    !python $Script_dir/plot-diversity-index.py "userLabel" "chao,shannon,invsimpson" "c,d" "SS.userLabel.subsample.groups.summary" "test" "test.alpha" 

.. parsed-literal::

    2 samples collect for Kw c
    2 samples collect for Kw d
    2 samples collect for Kw c
    2 samples collect for Kw d
    2 samples collect for Kw c
    2 samples collect for Kw d


.. code:: python

    from IPython.display import Image
    Image('test.alpha.png')



.. image:: unsupervised-analysis_files/unsupervised-analysis_23_0.png



.. code:: python

    # taxon distribution
    !python $Script_dir/plot-taxa-count.py 2 test.taxa.dist ../*.ssu.out/*.silva.taxonomy.count
.. code:: python

    from IPython.display import Image
    Image('test.taxa.dist.png')



.. image:: unsupervised-analysis_files/unsupervised-analysis_25_0.png



.. code:: python

    # ordination
    !python $Script_dir/plot-pcoa.py  SS.userLabel.subsample.braycurtis.userLabel.lt.pcoa.axes  SS.userLabel.subsample.braycurtis.userLabel.lt.pcoa.loadings  test.beta.pcoa
.. code:: python

    from IPython.display import Image
    Image('test.beta.pcoa.png')



.. image:: unsupervised-analysis_files/unsupervised-analysis_27_0.png



