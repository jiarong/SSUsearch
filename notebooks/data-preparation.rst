
Setup data directory
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    mkdir -p /usr/local/notebooks/data

.. code:: python

    cd /usr/local/notebooks/data


.. parsed-literal::

    /usr/local/notebooks/data


Download database files
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !wget http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch_db.tgz


.. parsed-literal::

    --2015-04-16 17:45:45--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch_db.tgz
    Resolving lyorn.idyll.org... 35.9.124.246
    Connecting to lyorn.idyll.org|35.9.124.246|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 122862729 (117M) [application/x-gzip]
    Saving to: `SSUsearch_db.tgz.1'
    
    100%[======================================>] 122,862,729  497K/s   in 4m 12s  
    
    2015-04-16 17:49:56 (476 KB/s) - `SSUsearch_db.tgz.1' saved [122862729/122862729]
    


.. code:: python

    !tar -xzvf SSUsearch_db.tgz


.. parsed-literal::

    SSUsearch_db/
    SSUsearch_db/Gene_db.silva_108_rep_set.fasta
    SSUsearch_db/Gene_tax.silva_taxa_family.tax
    SSUsearch_db/Gene_model_org.16s_ecoli_J01695.fasta
    SSUsearch_db/Gene_db_cc.greengene_97_otus.fasta
    SSUsearch_db/Gene_tax_cc.greengene_97_otus.tax
    SSUsearch_db/Copy_db.copyrighter.txt
    SSUsearch_db/Ali_template.silva_ssu.fasta
    SSUsearch_db/readme
    SSUsearch_db/Ali_template.silva_lsu.fasta
    SSUsearch_db/Ali_template.test.fasta
    SSUsearch_db/Ali_template.test_lsu.fasta
    SSUsearch_db/Gene_db.lsu_silva_rep.fasta
    SSUsearch_db/Gene_db.ssu_rdp_rep.fasta
    SSUsearch_db/Gene_tax.lsu_silva_rep.tax
    SSUsearch_db/Gene_tax.ssu_rdp_rep.tax
    SSUsearch_db/Hmm.lsu.hmm
    SSUsearch_db/clean.sh
    SSUsearch_db/Hmm.ssu.hmm


download a small test dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ATT: for real (larger) dataset, make sure there is enough disk space.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !wget -r -np -nH --cut-dir=4 --reject="index.html*" http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/


.. parsed-literal::

    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/
    Resolving lyorn.idyll.org... 35.9.124.246
    Connecting to lyorn.idyll.org|35.9.124.246|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 1212 (1.2K) [text/html]
    Saving to: `test/index.html'
    
    100%[======================================>] 1,212       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (120 MB/s) - `test/index.html' saved [1212/1212]
    
    Loading robots.txt; please ignore errors.
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/robots.txt
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 404 Not Found
    2015-04-16 17:50:05 ERROR 404: Not Found.
    
    Removing test/index.html since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/?C=N;O=D
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1212 (1.2K) [text/html]
    Saving to: `test/index.html?C=N;O=D'
    
    100%[======================================>] 1,212       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (134 MB/s) - `test/index.html?C=N;O=D' saved [1212/1212]
    
    Removing test/index.html?C=N;O=D since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/?C=M;O=A
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1212 (1.2K) [text/html]
    Saving to: `test/index.html?C=M;O=A'
    
    100%[======================================>] 1,212       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (137 MB/s) - `test/index.html?C=M;O=A' saved [1212/1212]
    
    Removing test/index.html?C=M;O=A since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/?C=S;O=A
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1212 (1.2K) [text/html]
    Saving to: `test/index.html?C=S;O=A'
    
    100%[======================================>] 1,212       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (136 MB/s) - `test/index.html?C=S;O=A' saved [1212/1212]
    
    Removing test/index.html?C=S;O=A since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/?C=D;O=A
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1212 (1.2K) [text/html]
    Saving to: `test/index.html?C=D;O=A'
    
    100%[======================================>] 1,212       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (135 MB/s) - `test/index.html?C=D;O=A' saved [1212/1212]
    
    Removing test/index.html?C=D;O=A since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/SS.design
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 20
    Saving to: `test/SS.design'
    
    100%[======================================>] 20          --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (2.26 MB/s) - `test/SS.design' saved [20/20]
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1602 (1.6K) [text/html]
    Saving to: `test/data/index.html'
    
    100%[======================================>] 1,602       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (131 MB/s) - `test/data/index.html' saved [1602/1602]
    
    Removing test/data/index.html since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/?C=N;O=A
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1212 (1.2K) [text/html]
    Saving to: `test/index.html?C=N;O=A'
    
    100%[======================================>] 1,212       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (137 MB/s) - `test/index.html?C=N;O=A' saved [1212/1212]
    
    Removing test/index.html?C=N;O=A since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/?C=M;O=D
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1212 (1.2K) [text/html]
    Saving to: `test/index.html?C=M;O=D'
    
    100%[======================================>] 1,212       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (140 MB/s) - `test/index.html?C=M;O=D' saved [1212/1212]
    
    Removing test/index.html?C=M;O=D since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/?C=S;O=D
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1212 (1.2K) [text/html]
    Saving to: `test/index.html?C=S;O=D'
    
    100%[======================================>] 1,212       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (137 MB/s) - `test/index.html?C=S;O=D' saved [1212/1212]
    
    Removing test/index.html?C=S;O=D since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/?C=D;O=D
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1212 (1.2K) [text/html]
    Saving to: `test/index.html?C=D;O=D'
    
    100%[======================================>] 1,212       --.-K/s   in 0s      
    
    2015-04-16 17:50:05 (145 MB/s) - `test/index.html?C=D;O=D' saved [1212/1212]
    
    Removing test/index.html?C=D;O=D since it should be rejected.
    
    --2015-04-16 17:50:05--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/?C=N;O=D
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1602 (1.6K) [text/html]
    Saving to: `test/data/index.html?C=N;O=D'
    
    100%[======================================>] 1,602       --.-K/s   in 0s      
    
    2015-04-16 17:50:06 (131 MB/s) - `test/data/index.html?C=N;O=D' saved [1602/1602]
    
    Removing test/data/index.html?C=N;O=D since it should be rejected.
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/?C=M;O=A
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1602 (1.6K) [text/html]
    Saving to: `test/data/index.html?C=M;O=A'
    
    100%[======================================>] 1,602       --.-K/s   in 0s      
    
    2015-04-16 17:50:06 (163 MB/s) - `test/data/index.html?C=M;O=A' saved [1602/1602]
    
    Removing test/data/index.html?C=M;O=A since it should be rejected.
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/?C=S;O=A
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1602 (1.6K) [text/html]
    Saving to: `test/data/index.html?C=S;O=A'
    
    100%[======================================>] 1,602       --.-K/s   in 0s      
    
    2015-04-16 17:50:06 (97.9 MB/s) - `test/data/index.html?C=S;O=A' saved [1602/1602]
    
    Removing test/data/index.html?C=S;O=A since it should be rejected.
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/?C=D;O=A
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1602 (1.6K) [text/html]
    Saving to: `test/data/index.html?C=D;O=A'
    
    100%[======================================>] 1,602       --.-K/s   in 0s      
    
    2015-04-16 17:50:06 (91.8 MB/s) - `test/data/index.html?C=D;O=A' saved [1602/1602]
    
    Removing test/data/index.html?C=D;O=A since it should be rejected.
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/1c.fa
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 14992 (15K)
    Saving to: `test/data/1c.fa'
    
    100%[======================================>] 14,992      --.-K/s   in 0.03s   
    
    2015-04-16 17:50:06 (584 KB/s) - `test/data/1c.fa' saved [14992/14992]
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/1d.fa
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 14974 (15K)
    Saving to: `test/data/1d.fa'
    
    100%[======================================>] 14,974      --.-K/s   in 0.02s   
    
    2015-04-16 17:50:06 (590 KB/s) - `test/data/1d.fa' saved [14974/14974]
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/2c.fa
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 14991 (15K)
    Saving to: `test/data/2c.fa'
    
    100%[======================================>] 14,991      --.-K/s   in 0.02s   
    
    2015-04-16 17:50:06 (590 KB/s) - `test/data/2c.fa' saved [14991/14991]
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/2d.fa
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 14994 (15K)
    Saving to: `test/data/2d.fa'
    
    100%[======================================>] 14,994      --.-K/s   in 0.02s   
    
    2015-04-16 17:50:06 (589 KB/s) - `test/data/2d.fa' saved [14994/14994]
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/?C=N;O=A
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1602 (1.6K) [text/html]
    Saving to: `test/data/index.html?C=N;O=A'
    
    100%[======================================>] 1,602       --.-K/s   in 0s      
    
    2015-04-16 17:50:06 (95.1 MB/s) - `test/data/index.html?C=N;O=A' saved [1602/1602]
    
    Removing test/data/index.html?C=N;O=A since it should be rejected.
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/?C=M;O=D
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1602 (1.6K) [text/html]
    Saving to: `test/data/index.html?C=M;O=D'
    
    100%[======================================>] 1,602       --.-K/s   in 0s      
    
    2015-04-16 17:50:06 (76.0 MB/s) - `test/data/index.html?C=M;O=D' saved [1602/1602]
    
    Removing test/data/index.html?C=M;O=D since it should be rejected.
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/?C=S;O=D
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1602 (1.6K) [text/html]
    Saving to: `test/data/index.html?C=S;O=D'
    
    100%[======================================>] 1,602       --.-K/s   in 0s      
    
    2015-04-16 17:50:06 (90.9 MB/s) - `test/data/index.html?C=S;O=D' saved [1602/1602]
    
    Removing test/data/index.html?C=S;O=D since it should be rejected.
    
    --2015-04-16 17:50:06--  http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch/test/data/?C=D;O=D
    Reusing existing connection to lyorn.idyll.org:80.
    HTTP request sent, awaiting response... 200 OK
    Length: 1602 (1.6K) [text/html]
    Saving to: `test/data/index.html?C=D;O=D'
    
    100%[======================================>] 1,602       --.-K/s   in 0s      
    
    2015-04-16 17:50:06 (159 MB/s) - `test/data/index.html?C=D;O=D' saved [1602/1602]
    
    Removing test/data/index.html?C=D;O=D since it should be rejected.
    
    FINISHED --2015-04-16 17:50:06--
    Downloaded: 23 files, 83K in 0.1s (835 KB/s)


.. code:: python

    ls test/data/


.. parsed-literal::

    1c.fa  1d.fa  2c.fa  2d.fa


**This tutorial assumes that you ready finished quality trimming, and
also paired end merge, if you paired end reads overlap.**

For quality trimming, we recommend
`trimmomatic <http://www.usadellab.org/cms/?page=trimmomatic>`_ written
in java, or
`fastq-mcf <https://code.google.com/p/ea-utils/wiki/FastqMcf>`_ written
in C.

For paired end reads merging, we recommend
`pandseq <https://github.com/neufeld/pandaseq>`_ or
`flash <http://ccb.jhu.edu/software/FLASH/>`_
