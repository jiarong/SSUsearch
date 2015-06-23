
Copy corrections is based on `copyrighter <http://www.ncbi.nlm.nih.gov/pubmed/24708850>`_. One copy database for each Greengene taxon at each level is provided by the tool. We will use that database for correcting our Greengene taxonomy abundance and OTU abundance.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    pwd



.. parsed-literal::

    u'/home/guojiaro/SSUsearch/notebooks'



.. code:: python

    ### set up directory
    !mkdir -p ./workdir/copy_correction
.. code:: python

    cd ./workdir/copy_correction

.. parsed-literal::

    /home/guojiaro/SSUsearch/notebooks/workdir/copy_correction


.. code:: python

    Prefix='SS'    # name for the analysis run
    Script_dir='./external_tools/SSUsearch/scripts'
    Wkdir='./workdir'
    Design='./data/test/SS.design'
    Otu_dist_cutoff='0.05'
    Copy_db='./data/SSUsearch_db/Copy_db.copyrighter.txt'
.. code:: python

    import os
    os.environ.update(
        {'Prefix':Prefix,
         'Script_dir': os.path.abspath(Script_dir), 
         'Wkdir': os.path.abspath(Wkdir), 
         'Otu_dist_cutoff':Otu_dist_cutoff,
         'Design': os.path.abspath(Design), 
         'Copy_db': os.path.abspath(Copy_db)})
.. code:: python

    # get input files from '/usr/local/notebooks/workdir/clust'
    !ln -sf $Wkdir/clust/$Prefix.biom
    !ln -sf $Wkdir/clust/$Prefix.list

.. code:: python

    # get Greengene taxonomy
    !cat $Wkdir/*.ssu.out/*.gg.taxonomy > $Prefix.taxonomy
    !mothur "#classify.otu(list=$Prefix.list, taxonomy=$Prefix.taxonomy, label=$Otu_dist_cutoff)"

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
    
    
    
    mothur > classify.otu(list=SS.list, taxonomy=SS.taxonomy, label=0.03)
    reftaxonomy is not required, but if given will keep the rankIDs in the summary file static.
    0.03	147
    
    Output File Names: 
    SS.0.03.cons.taxonomy
    SS.0.03.cons.tax.summary
    
    
    mothur > quit()


.. code:: python

    !mothur "#make.shared(biom=$Prefix.biom)"
    
    # do copy correction and even sampling
    !python $Script_dir/copyrighter-otutable.py $Copy_db \
        $Prefix.$Otu_dist_cutoff.cons.taxonomy \
        $Prefix.shared $Prefix.cc.shared
        
    !mv $Prefix.cc.shared $Prefix.shared
    !mothur "#make.biom(shared=$Prefix.shared, constaxonomy=$Prefix.$Otu_dist_cutoff.cons.taxonomy);"
    !mv $Prefix.userLabel.biom $Prefix.biom
    !rm -f mothur.*.logfile

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
    userLabel
    
    Output File Names: 
    SS.userLabel.biom
    
    
    mothur > quit()


SS.biom can be further used for diversity analysis, important but focus of this tutorial (details see `mothur wiki <http://www.mothur.org/wiki/454_SOP>`_).
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

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
    Sampling 7 from each group.
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
    Rsq 1 axis: 0.749418
    Rsq 2 axis: 0.926937
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
    Lowest stress :	0.115236
    R-squared for configuration:	0.8053
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.lt.nmds.iters
    SS.userLabel.subsample.braycurtis.userLabel.lt.nmds.stress
    SS.userLabel.subsample.braycurtis.userLabel.lt.nmds.axes
    
    
    mothur > amova(phylip=SS.userLabel.subsample.braycurtis.userLabel.lt.dist, design=/usr/local/notebooks/data/test/SS.design)
    c-d	Among	Within	Total
    SS	0.433674	0.867347	1.30102
    df	1	2	3
    MS	0.433674	0.433674
    
    Fs:	1
    p-value: 0.656
    
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
    1	c-d	0.981481	<0.0010
    It took 0 secs to run unifrac.weighted.
    
    Output File Names: 
    SS.userLabel.subsample.braycurtis.userLabel.trewsummary
    SS.userLabel.subsample.braycurtis.userLabel.tre1.weighted
    
    
    mothur > quit()


