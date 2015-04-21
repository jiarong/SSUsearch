
set another directory for unsupervised analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    mkdir -p /usr/local/notebooks/workdir/clust

.. code:: python

    cd /usr/local/notebooks/workdir/clust


.. parsed-literal::

    /usr/local/notebooks/workdir/clust


.. code:: python

    Prefix='SS'    # name for the analysis run
    Script_dir='/usr/local/notebooks/external_tools/SSUsearch/scripts'
    Wkdir='/usr/local/notebooks/workdir'
    Mcclust_jar='/usr/local/notebooks/external_tools/Clustering/dist/Clustering.jar'
    Java_xmx='10g'
    Java_gc_threads='2'
    Otu_dist_cutoff='0.03'
    Design='/usr/local/notebooks/data/test/SS.design'


.. code:: python

    import os
    os.environ.update(
        {'Prefix':Prefix, 
         'Script_dir':Script_dir, 
         'Wkdir':Wkdir, 
         'Mcclust_jar':Mcclust_jar, 
         'Java_xmx':Java_xmx, 
         'Java_gc_threads':Java_gc_threads, 
         'Otu_dist_cutoff':Otu_dist_cutoff, 
         'Design':Design})

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
        $Prefix.names temp.txt combined_seqs.afa
        
    !rm temp.txt


.. parsed-literal::

    *** Starting mcclust derep
    Processing combined_seqs.afa
    Total sequences: 199
    Unique sequences: 174
    Dereplication complete: 368
    0.57user 0.12system 0:00.47elapsed 147%CPU (0avgtext+0avgdata 355728maxresident)k
    0inputs+192outputs (0major+22898minor)pagefaults 0swaps


.. code:: python

    !time java -Xmx$Java_xmx -XX:+UseParallelOldGC -XX:ParallelGCThreads=$Java_gc_threads \
        -jar $Mcclust_jar dmatrix \
        -l 25 -o matrix.bin -i $Prefix.names -I derep.fasta


.. parsed-literal::

    Reading sequences(memratio=1.2895267219085598E-4)...
    Using distance model edu.msu.cme.rdp.alignment.pairwise.rna.UncorrectedDistanceModel
    Read 174 Nucleotide sequences (memratio=3.869057932748428E-4)
    Reading ID Mapping from file /usr/local/notebooks/workdir/clust/SS.names
    Read mapping for 199 sequences (memratio=3.869057932748428E-4)
    Starting distance computations, predicted max edges=30276, at=Sat Apr 18 06:38:13 UTC 2015
    Dumping 15051 edges to partial_matrix0 FINAL EDGES (memory ratio=0.001979570661990768)
    Matrix edges computed: 163
    Maximum distance: 0.5238095238095238
    Splits: 1
    Partition files merged: 6
    0.62user 0.12system 0:00.37elapsed 203%CPU (0avgtext+0avgdata 239424maxresident)k
    0inputs+424outputs (0major+17364minor)pagefaults 0swaps


.. code:: python

    !time java -Xmx$Java_xmx -XX:+UseParallelOldGC -XX:ParallelGCThreads=$Java_gc_threads \
        -jar $Mcclust_jar cluster \
        -i $Prefix.names -s $Prefix.groups -o complete.clust -d matrix.bin
    
    !python $Script_dir/mcclust2mothur-list-cutoff.py complete.clust $Prefix.list $Otu_dist_cutoff
    !sed -i 's/:/_/g' $Prefix.names $Prefix.groups $Prefix.list
    !echo "*** Replace ':' with '_' in seq names (original illumina name has ':' in them)"


.. parsed-literal::

    Doing complete linkage clustering with step 0.009999999776482582 (realstep=100)
    Clustering complete: 341
    0.82user 0.16system 0:00.48elapsed 201%CPU (0avgtext+0avgdata 329744maxresident)k
    0inputs+1088outputs (0major+24243minor)pagefaults 0swaps
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
    
    
    
    mothur > make.shared(list=SS.list, group=SS.groups, label=0.03)
    0.03
    
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
    
    
    
    mothur > classify.otu(list=SS.list, taxonomy=SS.taxonomy, label=0.03)
    reftaxonomy is not required, but if given will keep the rankIDs in the summary file static.
    0.03	147
    
    Output File Names: 
    SS.0.03.cons.taxonomy
    SS.0.03.cons.tax.summary
    
    
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
    
    
    
    mothur > make.biom(shared=SS.shared, constaxonomy=SS.0.03.cons.taxonomy)
    0.03
    
    Output File Names: 
    SS.0.03.biom
    
    
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
    Rsq 1 axis: 0.718058
    Rsq 2 axis: 0.827489
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
    Lowest stress :	0.152534
    R-squared for configuration:	0.377017
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.lt.nmds.iters
    SS.userLabel.subsample.braycurtis.userLabel.lt.nmds.stress
    SS.userLabel.subsample.braycurtis.userLabel.lt.nmds.axes
    
    
    mothur > amova(phylip=SS.userLabel.subsample.braycurtis.userLabel.lt.dist, design=/usr/local/notebooks/data/test/SS.design)
    c-d	Among	Within	Total
    SS	0.409934	0.722407	1.13234
    df	1	2	3
    MS	0.409934	0.361203
    
    Fs:	1.13491
    p-value: 0.304
    
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
    1	c-d	0.963687	<0.0010
    It took 0 secs to run unifrac.weighted.
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.trewsummary
    SS.userLabel.subsample.braycurtis.userLabel.tre1.weighted
    
    
    mothur > quit()


.. code:: python

    !echo "This part of pipeline finishes successfully :)"


.. parsed-literal::

    This part of pipeline finishes successfully :)


