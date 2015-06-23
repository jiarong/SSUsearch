
Setup data directory
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    cd /usr/local/notebooks

.. parsed-literal::

    /usr/local/notebooks


.. code:: python

    mkdir -p ./data
.. code:: python

    cd ./data

.. parsed-literal::

    /usr/local/notebooks/data


Download database files
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !curl -O http://lyorn.idyll.org/~gjr/public2/misc/SSUsearch_db.tgz

.. parsed-literal::

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  117M  100  117M    0     0   9.9M      0  0:00:11  0:00:11 --:--:-- 10.4M


.. code:: python

    !tar -xzvf SSUsearch_db.tgz

.. parsed-literal::

    x SSUsearch_db/
    x SSUsearch_db/Gene_db.silva_108_rep_set.fasta
    x SSUsearch_db/Gene_tax.silva_taxa_family.tax
    x SSUsearch_db/Gene_model_org.16s_ecoli_J01695.fasta
    x SSUsearch_db/Gene_db_cc.greengene_97_otus.fasta
    x SSUsearch_db/Gene_tax_cc.greengene_97_otus.tax
    x SSUsearch_db/Copy_db.copyrighter.txt
    x SSUsearch_db/Ali_template.silva_ssu.fasta
    x SSUsearch_db/readme
    x SSUsearch_db/Ali_template.silva_lsu.fasta
    x SSUsearch_db/Ali_template.test.fasta
    x SSUsearch_db/Ali_template.test_lsu.fasta
    x SSUsearch_db/Gene_db.lsu_silva_rep.fasta
    x SSUsearch_db/Gene_db.ssu_rdp_rep.fasta
    x SSUsearch_db/Gene_tax.lsu_silva_rep.tax
    x SSUsearch_db/Gene_tax.ssu_rdp_rep.tax
    x SSUsearch_db/Hmm.lsu.hmm
    x SSUsearch_db/clean.sh
    x SSUsearch_db/Hmm.ssu.hmm


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

    ls: test/data/: No such file or directory


This tutorial assumes that you ready finished quality trimming, and also paired end merge, if you paired end reads overlap.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For quality trimming, we recommend
`trimmomatic <http://www.usadellab.org/cms/?page=trimmomatic>`_ written
in java, or
`fastq-mcf <https://code.google.com/p/ea-utils/wiki/FastqMcf>`_ written
in C.

For paired end reads merging, we recommend
`pandseq <https://github.com/neufeld/pandaseq>`_ or
`flash <http://ccb.jhu.edu/software/FLASH/>`_

