
Overview
~~~~~~~~

SSUsearch is pipeline for identify SSU rRNA gene and use them for
diversity analysis. THe pipeline requires HMMER3.1, mothur, RDP mcclust,
and python numpy, pandas, scipy, matplotlib, and screed package.
Following are step by step tutorial for this pipeline:

1. Update the notebooks by running this notebook (click "Cell" then "Run
   All").

2. `Install dependencies <./pipeline-dependency-installation.ipynb>`_.
   If running amazon EC2 with ami "**ami-d87571b0**\ ", skip this step.

3. `Database and dataset preparation <./data-preparation.ipynb>`_

4. `SSU rRNA gene fragment search and
   classification <./ssu-search.ipynb>`_. ssu-search-Copy1.ipynb,
   ssu-search-Copy2.ipynb, ssu-search-Copy3.ipynb, and
   ssu-search-Copy4.ipynb are the ones to run for test data

5. `Unsupervised analysis <./unsupervised-analysis.ipynb>`_

6. `Copy correction <./copy-correction.ipynb>`_

.. code:: python

    # update the notebooks
    !rm -rf SSUsearch
    !git clone https://github.com/jiarong/SSUsearch.git
    !cp SSUsearch/notebooks/*.ipynb .

.. parsed-literal::

    Cloning into SSUsearch...
    remote: Counting objects: 323, done.[K
    remote: Compressing objects: 100% (28/28), done.[K
    remote: Total 323 (delta 14), reused 0 (delta 0), pack-reused 295[K
    Receiving objects: 100% (323/323), 197.67 KiB, done.
    Resolving deltas: 100% (147/147), done.


