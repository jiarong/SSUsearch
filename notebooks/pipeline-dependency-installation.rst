
Install dependencies
====================

**If you are running this tutorial using Amazon EC2 instance loaded with
the recommended AMI, you can skip this part.**

This pipeline requires:

-  HMMER3.1
-  mothur
-  RDP mcclust
-  python pandas, numpy, scipy, matplotlib, and screed package.

Following steps should work for linux machines. If you are running this
tutorial using Amazon EC2 instance loaded with the recommended AMI, you
can skip this part.

setup installation directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    cd /usr/local/notebooks

.. parsed-literal::

    /usr/local/notebooks


.. code:: python

    mkdir -p ./external_tools
.. code:: python

    cd ./external_tools

.. parsed-literal::

    /usr/local/notebooks/external_tools


.. code:: python

    mkdir -p ./bin
Install HMMER
~~~~~~~~~~~~~

.. code:: python

    !wget -c http://selab.janelia.org/software/hmmer3/3.1b1/hmmer-3.1b1-linux-intel-x86_64.tar.gz -O hmmer-3.1b1-linux-intel-x86_64.tar.gz

.. parsed-literal::

    --2015-04-14 21:38:23--  http://selab.janelia.org/software/hmmer3/3.1b1/hmmer-3.1b1-linux-intel-x86_64.tar.gz
    Resolving selab.janelia.org... 206.241.0.22
    Connecting to selab.janelia.org|206.241.0.22|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 20174637 (19M) [application/x-gzip]
    Saving to: `hmmer-3.1b1-linux-intel-x86_64.tar.gz'
    
    100%[======================================>] 20,174,637  38.9M/s   in 0.5s    
    
    2015-04-14 21:38:24 (38.9 MB/s) - `hmmer-3.1b1-linux-intel-x86_64.tar.gz' saved [20174637/20174637]
    


.. code:: python

    !tar -xzvf hmmer-3.1b1-linux-intel-x86_64.tar.gz

.. parsed-literal::

    hmmer-3.1b1-linux-intel-x86_64/
    hmmer-3.1b1-linux-intel-x86_64/lib/
    hmmer-3.1b1-linux-intel-x86_64/lib/libhmmer.a
    hmmer-3.1b1-linux-intel-x86_64/install-sh
    hmmer-3.1b1-linux-intel-x86_64/documentation/
    hmmer-3.1b1-linux-intel-x86_64/documentation/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmbuild.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/boilerplate-tail
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmer.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/phmmer.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmpgmd.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmalign.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmconvert.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/nhmmer.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmscan.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmpress.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmemit.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmfetch.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/nhmmscan.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmstat.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmsearch.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/jackhmmer.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/hmmsim.man
    hmmer-3.1b1-linux-intel-x86_64/documentation/man/alimask.man
    hmmer-3.1b1-linux-intel-x86_64/config.sub
    hmmer-3.1b1-linux-intel-x86_64/binaries/
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-ssdraw
    hmmer-3.1b1-linux-intel-x86_64/binaries/nhmmscan
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-alipid
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmpress
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-construct
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-compalign
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmsim
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-sfetch
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmsearch
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-mask
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-compstruct
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-histplot
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmfetch
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmstat
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-selectn
    hmmer-3.1b1-linux-intel-x86_64/binaries/nhmmer
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-cluster
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmscan
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-alistat
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmbuild
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmalign
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-reformat
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-alimap
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-seqrange
    hmmer-3.1b1-linux-intel-x86_64/binaries/alimask
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmc2
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmlogo
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-alimask
    hmmer-3.1b1-linux-intel-x86_64/binaries/jackhmmer
    hmmer-3.1b1-linux-intel-x86_64/binaries/phmmer
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-alimanip
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-shuffle
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmconvert
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-afetch
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmemit
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-alimerge
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-weight
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-seqstat
    hmmer-3.1b1-linux-intel-x86_64/binaries/esl-stranslate
    hmmer-3.1b1-linux-intel-x86_64/binaries/hmmpgmd
    hmmer-3.1b1-linux-intel-x86_64/LICENSE
    hmmer-3.1b1-linux-intel-x86_64/configure
    hmmer-3.1b1-linux-intel-x86_64/INSTALL
    hmmer-3.1b1-linux-intel-x86_64/configure.ac
    hmmer-3.1b1-linux-intel-x86_64/include/
    hmmer-3.1b1-linux-intel-x86_64/include/p7_gmxb.h
    hmmer-3.1b1-linux-intel-x86_64/include/p7_hmmcache.h
    hmmer-3.1b1-linux-intel-x86_64/include/p7_gbands.h
    hmmer-3.1b1-linux-intel-x86_64/include/impl_sse.h
    hmmer-3.1b1-linux-intel-x86_64/include/cachedb.h
    hmmer-3.1b1-linux-intel-x86_64/include/p7_gmxchk.h
    hmmer-3.1b1-linux-intel-x86_64/include/p7_config.h
    hmmer-3.1b1-linux-intel-x86_64/include/hmmer.h
    hmmer-3.1b1-linux-intel-x86_64/RELEASE-NOTES
    hmmer-3.1b1-linux-intel-x86_64/Userguide.pdf
    hmmer-3.1b1-linux-intel-x86_64/README
    hmmer-3.1b1-linux-intel-x86_64/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/profmark/
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-fps-ncbiblast+
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-hmmsearch-max
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-fps-ncbiblast
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-phmmer-consensus
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-fps-ssearch
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-h2-ls
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-single-ssearch
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-iterate-psiblast
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-single-phmmer
    hmmer-3.1b1-linux-intel-x86_64/profmark/pmark.param
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-fps-wublast
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-single-ncbiblast
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-fps-fasta
    hmmer-3.1b1-linux-intel-x86_64/profmark/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/profmark/pmark-master.pl
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-hmmsearch
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-fps-phmmer
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-psiblast
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-psiblast+
    hmmer-3.1b1-linux-intel-x86_64/profmark/rocplot.pl
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-sam
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-h2-fs
    hmmer-3.1b1-linux-intel-x86_64/profmark/create-profmark.c
    hmmer-3.1b1-linux-intel-x86_64/profmark/rocplot.c
    hmmer-3.1b1-linux-intel-x86_64/profmark/00README
    hmmer-3.1b1-linux-intel-x86_64/profmark/x-iterate-jackhmmer
    hmmer-3.1b1-linux-intel-x86_64/aclocal.m4
    hmmer-3.1b1-linux-intel-x86_64/src/
    hmmer-3.1b1-linux-intel-x86_64/src/p7_hmmwindow.c
    hmmer-3.1b1-linux-intel-x86_64/src/evalues.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_decoding.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_optacc.c
    hmmer-3.1b1-linux-intel-x86_64/src/mpisupport.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_prior.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_tophits.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_gmxb.h
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/mpi.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/00MANIFEST
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/msvfilter.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/optacc.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/impl_sse.h
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/decoding.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/vitfilter.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/fwdback.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/null2.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/ssvfilter.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/stotrace.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/vitscore.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/p7_oprofile.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/fbparsers.tex
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/io.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/p7_omx.ai
    hmmer-3.1b1-linux-intel-x86_64/src/impl_sse/p7_omx.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_vtrace.c
    hmmer-3.1b1-linux-intel-x86_64/src/nhmmer.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_spensemble.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_builder.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_viterbi.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_hmmcache.h
    hmmer-3.1b1-linux-intel-x86_64/src/hmmalign.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_gbands.h
    hmmer-3.1b1-linux-intel-x86_64/src/modelconfig.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_scoredata.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmdmstr.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_fwdback_rescaled.c
    hmmer-3.1b1-linux-intel-x86_64/src/jackhmmer.c
    hmmer-3.1b1-linux-intel-x86_64/src/phmmer.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_alidisplay.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_null2.c
    hmmer-3.1b1-linux-intel-x86_64/src/logsum.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_hmmcache.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_gmxchk.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/mpi.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/00MANIFEST
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/impl_vmx.h
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/msvfilter.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/optacc.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/decoding.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/vitfilter.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/fwdback.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/null2.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/stotrace.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/vitscore.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/p7_oprofile.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/io.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_vmx/p7_omx.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_hmm.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmscan.c
    hmmer-3.1b1-linux-intel-x86_64/src/cachedb.h
    hmmer-3.1b1-linux-intel-x86_64/src/hmmdutils.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_gmxchk.h
    hmmer-3.1b1-linux-intel-x86_64/src/seqmodel.c
    hmmer-3.1b1-linux-intel-x86_64/src/itest_brute.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmer.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_null3.c
    hmmer-3.1b1-linux-intel-x86_64/src/nhmmscan.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_fwdback.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_fwdback_banded.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_gmx.c
    hmmer-3.1b1-linux-intel-x86_64/src/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/src/hmmsim.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmpress.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/src/hmmconvert.c
    hmmer-3.1b1-linux-intel-x86_64/src/modelstats.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmstat.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_domaindef.c
    hmmer-3.1b1-linux-intel-x86_64/src/errors.c
    hmmer-3.1b1-linux-intel-x86_64/src/eweight.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmbuild.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_msv.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_gbands.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmc2.c
    hmmer-3.1b1-linux-intel-x86_64/src/alimask.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_profile.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_fwdback_chk.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmsearch.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_gmxb.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/mpi.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/impl_dummy.h
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/msvfilter.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/optacc.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/decoding.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/vitfilter.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/fwdback.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/null2.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/stotrace.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/vitscore.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/p7_oprofile.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/io.c
    hmmer-3.1b1-linux-intel-x86_64/src/impl_dummy/p7_omx.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmpgmd_client_example.pl
    hmmer-3.1b1-linux-intel-x86_64/src/hmmlogo.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_pipeline.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmpress.c
    hmmer-3.1b1-linux-intel-x86_64/src/tracealign.c
    hmmer-3.1b1-linux-intel-x86_64/src/h2_io.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmfetch.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmdwrkr.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmpgmd.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_trace.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_config.h.in
    hmmer-3.1b1-linux-intel-x86_64/src/heatmap.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_bg.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmemit.c
    hmmer-3.1b1-linux-intel-x86_64/src/generic_stotrace.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmpgmd.h
    hmmer-3.1b1-linux-intel-x86_64/src/cachedb.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmer.h
    hmmer-3.1b1-linux-intel-x86_64/src/build.c
    hmmer-3.1b1-linux-intel-x86_64/src/emit.c
    hmmer-3.1b1-linux-intel-x86_64/src/hmmpgmd2msa.c
    hmmer-3.1b1-linux-intel-x86_64/src/p7_hmmfile.c
    hmmer-3.1b1-linux-intel-x86_64/share/
    hmmer-3.1b1-linux-intel-x86_64/share/doc/
    hmmer-3.1b1-linux-intel-x86_64/share/doc/hmmer/
    hmmer-3.1b1-linux-intel-x86_64/share/man/
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/phmmer.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/jackhmmer.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmsim.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmemit.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmscan.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmalign.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmfetch.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmer.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmpgmd.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmconvert.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/nhmmscan.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmsearch.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmpress.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/alimask.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmbuild.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/nhmmer.1
    hmmer-3.1b1-linux-intel-x86_64/share/man/man1/hmmstat.1
    hmmer-3.1b1-linux-intel-x86_64/testsuite/
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i17-stdin.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/ecori.fa
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i15-hmmconvert.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i6-hmmalign-mapali.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/20aa-alitest.fa
    hmmer-3.1b1-linux-intel-x86_64/testsuite/Patched.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i5-hmmbuild-naming.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/Patched.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/RRM_1.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/Caudal_act.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/M1.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/Caudal_act.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/RRM_1.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/h3.pm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/minifam
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i14-hmmemit-consensus.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/XYPPX.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/PSE.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/XYPPX.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i16-build-allins.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i2-search-variation.sh
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i11-hmmalign-mapali.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i1-build-variation.sh
    hmmer-3.1b1-linux-intel-x86_64/testsuite/test-make.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i20-fmindex-core.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i3-seqsearch-variation.sh
    hmmer-3.1b1-linux-intel-x86_64/testsuite/PSE.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i9-optional-annotation.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i4-zerolength-seqs.sh
    hmmer-3.1b1-linux-intel-x86_64/testsuite/testsuite.sqc
    hmmer-3.1b1-linux-intel-x86_64/testsuite/SMC_N.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i12-delete-corruption.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/rndseq400-10.fa
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i18-nhmmer-generic.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/PAX8_HUMAN
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i19-hmmpgmd-ga.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/3box.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/20aa.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/M1.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/ecori.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i8-nonresidues.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/20aa.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/SMC_N.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i10-duplicate-names.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/LuxC.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/ecori.sto
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i7-hmmbuild-fragments.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/LuxC.hmm
    hmmer-3.1b1-linux-intel-x86_64/testsuite/i13-msa-integrity.pl
    hmmer-3.1b1-linux-intel-x86_64/testsuite/3box.sto
    hmmer-3.1b1-linux-intel-x86_64/easel/
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stretchexp.c
    hmmer-3.1b1-linux-intel-x86_64/easel/install-sh
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_mpi.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stats.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msacluster.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_cluster.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_paml.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_tree.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_selex.h
    hmmer-3.1b1-linux-intel-x86_64/easel/config.sub
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_selex.c
    hmmer-3.1b1-linux-intel-x86_64/easel/interface_gsl.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_stockholm.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_gumbel.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_rootfinder.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_config.h.in
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sqio_ascii.h
    hmmer-3.1b1-linux-intel-x86_64/easel/interface_lapack.h
    hmmer-3.1b1-linux-intel-x86_64/easel/LICENSE
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sqio.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stack.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_normal.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_gumbel.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stats.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_translate.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_ssi.h
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-weight.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-reformat.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-stranslate.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-seqstat.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimask.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-seqrange.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-mask.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimap.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-seqrange.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-cluster.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-compstruct.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-afetch.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-compalign.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimap.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alipid.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-seqrange.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alipid.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimanip.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-construct.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-seqstat.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimask.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimanip.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimerge.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-selectn.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-shuffle.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-shuffle.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-histplot.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-mask.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-compalign.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-afetch.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-sfetch.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-sfetch.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-ssdraw.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-ssdraw.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-construct.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-construct.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-histplot.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-compstruct.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-reformat.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-mask.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimap.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-shuffle.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alistat.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alistat.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimerge.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimask.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-weight.c
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alistat.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-afetch.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-compalign.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-selectn.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-ssdraw.man
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimerge.itest.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/miniapps/esl-alimanip.man
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_scorematrix.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sqio.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_keyhash.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_mpi.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_composition.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_minimizer.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_getopts.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_recorder.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stopwatch.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stack.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msacluster.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_random.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_cluster.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_buffer.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msashuffle.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_regexp.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/LICENSE.sh.in
    hmmer-3.1b1-linux-intel-x86_64/easel/configure
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/man2optlist
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/sedition
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/cexcerpt.man
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/ctags-fix
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/rmanprocess.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/esl-dependencies
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/sqc
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/cexcerpt
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/c2optlist
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/sedition-pp
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/autodoc
    hmmer-3.1b1-linux-intel-x86_64/easel/devkit/00README
    hmmer-3.1b1-linux-intel-x86_64/easel/INSTALL
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stretchexp.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_getopts.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_minimizer.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stopwatch.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msaweight.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_hyperexp.h
    hmmer-3.1b1-linux-intel-x86_64/easel/configure.ac
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_random.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_alphabet.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_randomseq.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_mem.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_tree.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_random.c
    hmmer-3.1b1-linux-intel-x86_64/easel/BUGTRAX
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_afa.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_vectorops.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_randomseq.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_buffer.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_fileparser.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_psiblast.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_paml.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_histogram.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_dirichlet.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sq.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_histogram.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_stockholm.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_psiblast.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_threads.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_vmx.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_distance.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_weibull.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_workqueue.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_gev.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_buffer.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_translate.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_swat.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_hmm.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile2.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_recorder.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_getopts.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_regexp.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stats.c
    hmmer-3.1b1-linux-intel-x86_64/easel/interface_gsl.c
    hmmer-3.1b1-linux-intel-x86_64/easel/easel.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_hyperexp.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_dmatrix.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_wuss.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msaweight.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_a2m.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_randomseq.c
    hmmer-3.1b1-linux-intel-x86_64/easel/aclocal.m4
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_vectorops.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_gumbel.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_fileparser.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_workqueue.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_phylip.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sse.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_hyperexp.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msacluster.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_phylip.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_normal.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sq.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_afa.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_gamma.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_cluster.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_paml.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_dmatrix.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sq.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_wuss.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sqio.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_distance.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sqio_ncbi.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_swat.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_dirichlet.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_gamma.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_exponential.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msashuffle.c
    hmmer-3.1b1-linux-intel-x86_64/easel/easel.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_wuss.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_alphabet.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_a2m.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_mixgev.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_regexp.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_fileparser.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stack.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_scorematrix.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_gamma.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile2.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_alphabet.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_exponential.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.11
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/00MANIFEST
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.12
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.good.1
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.14
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.10
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.2
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.good.2
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.9
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.5
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.6
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.7
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.1
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.3
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.good.3
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.4
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.8
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa_testfiles/selex/selex.bad.13
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_rootfinder.h
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/driver_report.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/e2.sh
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/valgrind_report.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/coverage_report.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/trna-5.stk
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/i3-blank-gf.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/i1-degen-residues.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/testsuite.sqc
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/i2-ncbi-indices.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/testsuite/trna-ssdraw.ps
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_ssi.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sse.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_normal.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_rootfinder.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_ratematrix.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/config.guess
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_gev.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sqio_ascii.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_distance.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_histogram.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_dmatrix.h
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/blast2profmark
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/demotic_blast.pm
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/fasta2profmark
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/ncbi-blastp-tbl.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/wu-blastp-tbl.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/ssearch-profmark.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/ncbi-blastp-profmark.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/hmmsearch-tbl.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/psiblast-tbl.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/fasta-tbl.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/h2-tbl.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/psiblast-profmark.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/phmmer-profmark.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/hmmsearch-profmark.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/fasta-profmark.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/phmmer-tbl.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/wu-blastp-profmark.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/h2-profmark.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/regress/ssearch-tbl.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/h22tbl
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/h22profmark
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/hmmer2tbl
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/test.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/hmmer2profmark
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.wu-blastp.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.psiblast.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.phmmer.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example-single.fa.pin
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example-single.fa.psq
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example-single.asnt
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example-single.sto
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.h2.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example-single.pbl
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.sto
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.ncbi-blastp.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example-single.fa.phr
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example-single.fa
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.ssearch.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.fa
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example-single-psiquery.fa
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.hmm2
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.hmmsearch.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.fasta.out
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/examples/example.hmm
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/infernal_tab2gff.pl
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/demotic_h2.pm
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/demotic_hmmer.pm
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/fasta2tbl
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/blast2tbl
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/demotic_infernal_tab.pm
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/demotic_fasta.pm
    hmmer-3.1b1-linux-intel-x86_64/easel/demotic/00README
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sqio_ncbi.c
    hmmer-3.1b1-linux-intel-x86_64/easel/easel.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_threads.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_ratematrix.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_gev.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_sse.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stretchexp.h
    hmmer-3.1b1-linux-intel-x86_64/easel/COPYRIGHT
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_clustal.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_keyhash.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_exponential.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_composition.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_vectorops.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile_clustal.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_scorematrix.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_keyhash.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/interface_lapack.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_hmm.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msafile.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_stopwatch.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_weibull.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_ssi.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_mixgev.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_tree.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_vmx.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msa.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_mem.c
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_dirichlet.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_msaweight.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_minimizer.tex
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_mpi.h
    hmmer-3.1b1-linux-intel-x86_64/easel/00README
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/genbank.bad.1
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/stockholm.1
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/fasta.odd.1
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/fasta.bad.1
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/uniprot
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/genbank.2
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/fasta
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/wag.dat
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/embl
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/fasta.bad.3
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/genbank
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/fasta.2
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/fasta.bad.2
    hmmer-3.1b1-linux-intel-x86_64/easel/formats/BLOSUM62
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_weibull.h
    hmmer-3.1b1-linux-intel-x86_64/easel/esl_ratematrix.c
    hmmer-3.1b1-linux-intel-x86_64/libdivsufsort/
    hmmer-3.1b1-linux-intel-x86_64/libdivsufsort/divsufsort.c
    hmmer-3.1b1-linux-intel-x86_64/libdivsufsort/divsufsort.h.in
    hmmer-3.1b1-linux-intel-x86_64/libdivsufsort/COPYING
    hmmer-3.1b1-linux-intel-x86_64/libdivsufsort/VERSION
    hmmer-3.1b1-linux-intel-x86_64/libdivsufsort/README
    hmmer-3.1b1-linux-intel-x86_64/libdivsufsort/Makefile.in
    hmmer-3.1b1-linux-intel-x86_64/libdivsufsort/AUTHORS
    hmmer-3.1b1-linux-intel-x86_64/config.guess
    hmmer-3.1b1-linux-intel-x86_64/COPYRIGHT
    hmmer-3.1b1-linux-intel-x86_64/tutorial/
    hmmer-3.1b1-linux-intel-x86_64/tutorial/Pkinase.sto
    hmmer-3.1b1-linux-intel-x86_64/tutorial/minifam.h3f
    hmmer-3.1b1-linux-intel-x86_64/tutorial/MADE1.sto
    hmmer-3.1b1-linux-intel-x86_64/tutorial/7LESS_DROME
    hmmer-3.1b1-linux-intel-x86_64/tutorial/fn3.sto
    hmmer-3.1b1-linux-intel-x86_64/tutorial/globins45.fa
    hmmer-3.1b1-linux-intel-x86_64/tutorial/HBB_HUMAN
    hmmer-3.1b1-linux-intel-x86_64/tutorial/MADE1.hmm.h3i
    hmmer-3.1b1-linux-intel-x86_64/tutorial/MADE1.hmm.h3p
    hmmer-3.1b1-linux-intel-x86_64/tutorial/minifam
    hmmer-3.1b1-linux-intel-x86_64/tutorial/Pkinase.hmm
    hmmer-3.1b1-linux-intel-x86_64/tutorial/fn3.hmm
    hmmer-3.1b1-linux-intel-x86_64/tutorial/globins4.out
    hmmer-3.1b1-linux-intel-x86_64/tutorial/MADE1.hmm
    hmmer-3.1b1-linux-intel-x86_64/tutorial/minifam.h3p
    hmmer-3.1b1-linux-intel-x86_64/tutorial/globins4.sto
    hmmer-3.1b1-linux-intel-x86_64/tutorial/MADE1.hmm.h3f
    hmmer-3.1b1-linux-intel-x86_64/tutorial/minifam.h3i
    hmmer-3.1b1-linux-intel-x86_64/tutorial/fn3.out
    hmmer-3.1b1-linux-intel-x86_64/tutorial/MADE1.out
    hmmer-3.1b1-linux-intel-x86_64/tutorial/minifam.h3m
    hmmer-3.1b1-linux-intel-x86_64/tutorial/MADE1.hmm.h3m
    hmmer-3.1b1-linux-intel-x86_64/tutorial/dna_target.fa
    hmmer-3.1b1-linux-intel-x86_64/tutorial/globins4.hmm


.. code:: python

    cp hmmer-3.1b1-linux-intel-x86_64/binaries/hmmsearch /usr/local/bin
.. code:: python

    cp hmmer-3.1b1-linux-intel-x86_64/binaries/hmmsearch ./bin
Install mothur
~~~~~~~~~~~~~~

.. code:: python

    !wget http://www.mothur.org/w/images/8/88/Mothur.cen_64.zip -O mothur.zip

.. parsed-literal::

    --2015-04-11 19:39:44--  http://www.mothur.org/w/images/8/88/Mothur.cen_64.zip
    Resolving www.mothur.org... 141.214.31.125
    Connecting to www.mothur.org|141.214.31.125|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 44310761 (42M) [application/zip]
    Saving to: `mothur.zip'
    
    100%[======================================>] 44,310,761  4.89M/s   in 8.8s    
    
    2015-04-11 19:39:53 (4.82 MB/s) - `mothur.zip' saved [44310761/44310761]
    


.. code:: python

    !unzip mothur.zip

.. parsed-literal::

    Archive:  mothur.zip
       creating: mothur/
      inflating: mothur/.DS_Store        
       creating: __MACOSX/
       creating: __MACOSX/mothur/
      inflating: __MACOSX/mothur/._.DS_Store  
       creating: mothur/blast/
      inflating: mothur/blast/.DS_Store  
       creating: __MACOSX/mothur/blast/
      inflating: __MACOSX/mothur/blast/._.DS_Store  
       creating: mothur/blast/bin/
      inflating: mothur/blast/bin/bl2seq  
       creating: __MACOSX/mothur/blast/bin/
      inflating: __MACOSX/mothur/blast/bin/._bl2seq  
      inflating: mothur/blast/bin/blastall  
      inflating: __MACOSX/mothur/blast/bin/._blastall  
      inflating: mothur/blast/bin/blastclust  
      inflating: __MACOSX/mothur/blast/bin/._blastclust  
      inflating: mothur/blast/bin/blastpgp  
      inflating: __MACOSX/mothur/blast/bin/._blastpgp  
      inflating: mothur/blast/bin/copymat  
      inflating: __MACOSX/mothur/blast/bin/._copymat  
      inflating: mothur/blast/bin/fastacmd  
      inflating: __MACOSX/mothur/blast/bin/._fastacmd  
      inflating: mothur/blast/bin/formatdb  
      inflating: __MACOSX/mothur/blast/bin/._formatdb  
      inflating: mothur/blast/bin/formatrpsdb  
      inflating: __MACOSX/mothur/blast/bin/._formatrpsdb  
      inflating: mothur/blast/bin/impala  
      inflating: __MACOSX/mothur/blast/bin/._impala  
      inflating: mothur/blast/bin/makemat  
      inflating: __MACOSX/mothur/blast/bin/._makemat  
      inflating: mothur/blast/bin/megablast  
      inflating: __MACOSX/mothur/blast/bin/._megablast  
      inflating: mothur/blast/bin/rpsblast  
      inflating: __MACOSX/mothur/blast/bin/._rpsblast  
      inflating: mothur/blast/bin/seedtop  
      inflating: __MACOSX/mothur/blast/bin/._seedtop  
      inflating: __MACOSX/mothur/blast/._bin  
      inflating: __MACOSX/mothur/._blast  
      inflating: mothur/CatchAllCmdL.exe  
      inflating: __MACOSX/mothur/._CatchAllCmdL.exe  
      inflating: mothur/mothur           
      inflating: mothur/uchime           


.. code:: python

    cp mothur/mothur /usr/local/bin
.. code:: python

    cp mothur/mothur ./bin
Install RDP mcclust tool
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !wget http://lyorn.idyll.org/~gjr/public2/misc/Clustering.tar.gz

.. parsed-literal::

    --2015-04-11 20:06:29--  http://lyorn.idyll.org/~gjr/public2/misc/Clustering.tar.gz
    Resolving lyorn.idyll.org... 35.9.124.246
    Connecting to lyorn.idyll.org|35.9.124.246|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 28617228 (27M) [application/x-gzip]
    Saving to: `Clustering.tar.gz'
    
    100%[======================================>] 28,617,228  9.26M/s   in 2.9s    
    
    2015-04-11 20:06:33 (9.26 MB/s) - `Clustering.tar.gz' saved [28617228/28617228]
    


.. code:: python

    !tar -xzvf Clustering.tar.gz

.. parsed-literal::

    Clustering/
    Clustering/hadoop/
    Clustering/hadoop/hadoop-0.18.3-core.jar
    Clustering/nbproject/
    Clustering/nbproject/project.properties
    Clustering/nbproject/project.xml
    Clustering/nbproject/genfiles.properties
    Clustering/nbproject/build-impl.xml
    Clustering/nbproject/configs/
    Clustering/nbproject/configs/MCUPGMA.properties
    Clustering/nbproject/configs/Pairwise.properties
    Clustering/nbproject/configs/Create_Matrix.properties
    Clustering/nbproject/configs/Main.properties
    Clustering/nbproject/configs/TestCluster.properties
    Clustering/nbproject/configs/GridwareTest.properties
    Clustering/lib/
    Clustering/lib/junit-4.8.2.jar
    Clustering/lib/jaxb-impl-2.2.7.jar
    Clustering/lib/commons-codec-1.8-sources.jar
    Clustering/lib/jaxb-impl-2.2.7-sources.jar
    Clustering/lib/jaxb-api-2.2.7.jar
    Clustering/lib/junit-4.8.2-sources.jar
    Clustering/lib/jsr173_api-1.0.jar
    Clustering/lib/commons-cli-1.2-sources.jar
    Clustering/lib/jaxb-core-2.2.7.jar
    Clustering/lib/commons-io-2.4-sources.jar
    Clustering/lib/istack-commons-runtime-2.16.jar
    Clustering/lib/commons-cli-1.2-javadoc.jar
    Clustering/lib/FastInfoset-1.2.12.jar
    Clustering/lib/commons-codec-1.8.jar
    Clustering/lib/junit-4.8.2-javadoc.jar
    Clustering/lib/commons-cli-1.2.jar
    Clustering/lib/commons-io-2.4.jar
    Clustering/lib/commons-io-2.4-javadoc.jar
    Clustering/lib/jaxb-impl-2.2.7-javadoc.jar
    Clustering/lib/commons-codec-1.8-javadoc.jar
    Clustering/.gitignore
    Clustering/ivy.xml
    Clustering/dist/
    Clustering/dist/Clustering.jar
    Clustering/dist/lib/
    Clustering/dist/lib/ReadSeq.jar
    Clustering/dist/lib/TaxonomyTree.jar
    Clustering/dist/lib/SeqFilters.jar
    Clustering/dist/lib/jaxb-api-2.2.7.jar
    Clustering/dist/lib/jsr173_api-1.0.jar
    Clustering/dist/lib/commons-codec-1.8.jar
    Clustering/dist/lib/commons-cli-1.2.jar
    Clustering/dist/lib/commons-io-2.4.jar
    Clustering/dist/lib/jaxb-core-2.2.7.jar
    Clustering/dist/lib/hadoop-0.18.3-core.jar
    Clustering/dist/lib/AlignmentTools.jar
    Clustering/dist/lib/jaxb-impl-2.2.7.jar
    Clustering/dist/lib/junit-4.8.2.jar
    Clustering/src/
    Clustering/src/org/
    Clustering/src/org/apache/
    Clustering/src/org/apache/hadoop/
    Clustering/src/org/apache/hadoop/mapred/
    Clustering/src/org/apache/hadoop/mapred/ResortPartialResub.java
    Clustering/src/org/apache/hadoop/mapred/ReadPartialResultFile.java
    Clustering/src/org/apache/hadoop/mapred/CombinedIntermediateSortedReader.java
    Clustering/src/org/apache/hadoop/mapred/ResortPartialResult.java
    Clustering/src/org/apache/hadoop/mapred/SummarizeAttempts.java
    Clustering/src/org/apache/hadoop/mapred/SortPartialResults.java
    Clustering/src/edu/
    Clustering/src/edu/msu/
    Clustering/src/edu/msu/cme/
    Clustering/src/edu/msu/cme/rdp/
    Clustering/src/edu/msu/cme/rdp/taxatree/
    Clustering/src/edu/msu/cme/rdp/taxatree/TreeBuilder.java
    Clustering/src/edu/msu/cme/rdp/hadoop/
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/ByteSeqInputFormat.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/DistancePartitioner.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/DistanceReducer.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/keys/
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/keys/MatrixRange.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/keys/Comparison.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/keys/IntDistance.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/keys/DistanceAndComparison.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/mapred/DistanceAndComparisonMapper.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/sampler/
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/sampler/SamplerMain.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/sampler/SamplerInputFormat.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/sampler/SamplerReducer.java
    Clustering/src/edu/msu/cme/rdp/hadoop/distance/DistancesMain.java
    Clustering/src/edu/msu/cme/rdp/hadoop/oneoff/
    Clustering/src/edu/msu/cme/rdp/hadoop/oneoff/DistancesMainOneOff.java
    Clustering/src/edu/msu/cme/rdp/hadoop/oneoff/DistancePartitionerOneOff.java
    Clustering/src/edu/msu/cme/rdp/hadoop/oneoff/HDFSEdgeReaderOneOff.java
    Clustering/src/edu/msu/cme/rdp/hadoop/oneoff/ByteSeqInputFormatOneOff.java
    Clustering/src/edu/msu/cme/rdp/hadoop/utils/
    Clustering/src/edu/msu/cme/rdp/hadoop/utils/IntSeq.java
    Clustering/src/edu/msu/cme/rdp/hadoop/utils/HDFSEdgeReader.java
    Clustering/src/edu/msu/cme/rdp/hadoop/utils/HadoopClustering.java
    Clustering/src/edu/msu/cme/rdp/hadoop/utils/AlignedIntSeqStore.java
    Clustering/src/edu/msu/cme/rdp/hadoop/HadoopMain.java
    Clustering/src/edu/msu/cme/pyro/
    Clustering/src/edu/msu/cme/pyro/derep/
    Clustering/src/edu/msu/cme/pyro/derep/SampleMapping.java
    Clustering/src/edu/msu/cme/pyro/derep/Dereplicator.java
    Clustering/src/edu/msu/cme/pyro/derep/RefreshMappings.java
    Clustering/src/edu/msu/cme/pyro/derep/IdMapping.java
    Clustering/src/edu/msu/cme/pyro/derep/ExplodeMappings.java
    Clustering/src/edu/msu/cme/pyro/cluster/
    Clustering/src/edu/msu/cme/pyro/cluster/Clustering.java
    Clustering/src/edu/msu/cme/pyro/cluster/ClusterReplay.java
    Clustering/src/edu/msu/cme/pyro/cluster/dist/
    Clustering/src/edu/msu/cme/pyro/cluster/dist/MergeSortTest.java
    Clustering/src/edu/msu/cme/pyro/cluster/dist/ThinEdge.java
    Clustering/src/edu/msu/cme/pyro/cluster/dist/MergeDistsJob.java
    Clustering/src/edu/msu/cme/pyro/cluster/dist/DistanceCalculator.java
    Clustering/src/edu/msu/cme/pyro/cluster/dist/SlimDistMatrixSeq.java
    Clustering/src/edu/msu/cme/pyro/cluster/dist/ThickEdge.java
    Clustering/src/edu/msu/cme/pyro/cluster/dist/PairwiseDistance.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/UPGMAClusterFactory.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/UPGMAState.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/CannotLoadMoreEdgesException.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/UPGMAReaderTest.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/EdgeComparator.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/ClusterMinEdge.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/BufferedRandomAccessFile.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/RandomAccessEdgeFile.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/UPGMAEdgeReader.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/UPGMAClusterEdges.java
    Clustering/src/edu/msu/cme/pyro/cluster/upgma/Heap.java
    Clustering/src/edu/msu/cme/pyro/cluster/ClusterMain.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/
    Clustering/src/edu/msu/cme/pyro/cluster/utils/RepresenativeSeqs.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/Cluster.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/CDHitToOTUTable.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/ClusterFactory.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/CDHitToRDP.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/ClusterUtils.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/ClusterEdges.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/MergeSampleMapping.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/AlignSeqMatch.java
    Clustering/src/edu/msu/cme/pyro/cluster/utils/AbstractClusterFactory.java
    Clustering/src/edu/msu/cme/pyro/cluster/io/
    Clustering/src/edu/msu/cme/pyro/cluster/io/LocalEdgeReader.java
    Clustering/src/edu/msu/cme/pyro/cluster/io/ClusterOutput.java
    Clustering/src/edu/msu/cme/pyro/cluster/io/RFormatter.java
    Clustering/src/edu/msu/cme/pyro/cluster/io/EdgeReader.java
    Clustering/src/edu/msu/cme/pyro/cluster/io/ClusterToBiom.java
    Clustering/src/edu/msu/cme/pyro/cluster/io/EdgeWriter.java
    Clustering/src/edu/msu/cme/pyro/cluster/io/RDPClustParser.java
    Clustering/src/edu/msu/cme/pyro/cluster/io/ClusterFileOutput.java
    Clustering/build/
    Clustering/build/empty/
    Clustering/build/classes/
    Clustering/build/classes/edu/
    Clustering/build/classes/edu/msu/
    Clustering/build/classes/edu/msu/cme/
    Clustering/build/classes/edu/msu/cme/pyro/
    Clustering/build/classes/edu/msu/cme/pyro/derep/
    Clustering/build/classes/edu/msu/cme/pyro/derep/Dereplicator$DerepMode.class
    Clustering/build/classes/edu/msu/cme/pyro/derep/Dereplicator.class
    Clustering/build/classes/edu/msu/cme/pyro/derep/Dereplicator$DerepSeq.class
    Clustering/build/classes/edu/msu/cme/pyro/derep/IdMapping.class
    Clustering/build/classes/edu/msu/cme/pyro/derep/SampleMapping.class
    Clustering/build/classes/edu/msu/cme/pyro/derep/RefreshMappings.class
    Clustering/build/classes/edu/msu/cme/pyro/derep/ExplodeMappings.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/
    Clustering/build/classes/edu/msu/cme/pyro/cluster/Clustering$1.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/ThinEdge.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/DistanceCalculator$PartialMatrixResult.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/MergeSortTest$1.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/DistanceCalculator$SequenceFile.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/MergeDistsJob.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/PairwiseDistance$SequenceFile.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/ThickEdge.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/DistanceCalculator$1.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/PairwiseDistance.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/MergeSortTest.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/DistanceCalculator.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/dist/SlimDistMatrixSeq.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/ClusterMain.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/Clustering.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/ClusterToBiom.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/ClusterFileOutput.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/RDPClustParser$Cutoff.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/EdgeWriter.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/ClusterOutput.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/RFormatter.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/RDPClustParser.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/LocalEdgeReader.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/EdgeReader.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/io/RDPClustParser$ClusterSample.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/UPGMAState$UPGMAStateHolder.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/RandomAccessEdgeFile.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/UPGMAEdgeReader.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/UPGMAClusterFactory.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/BufferedRandomAccessFile.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/UPGMAState.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/ClusterMinEdge.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/EdgeComparator.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/Heap.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/UPGMAReaderTest.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/CannotLoadMoreEdgesException.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/upgma/UPGMAClusterEdges.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/AbstractClusterFactory.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/CDHitToRDP$EasyClustFactory.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/ClusterFactory.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/Cluster.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/CDHitToRDP.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/ClusterUtils.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/AlignSeqMatch$AlignSeqMatchResult.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/AlignSeqMatch.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/MergeSampleMapping.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/ClusterUtils$ClusterParams.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/ClusterEdges.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/CDHitToOTUTable.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/CDHitToOTUTable$EasyClustFactory.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/utils/RepresenativeSeqs.class
    Clustering/build/classes/edu/msu/cme/pyro/cluster/ClusterReplay.class
    Clustering/build/classes/edu/msu/cme/rdp/
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/HadoopMain.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/utils/
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/utils/HDFSEdgeReader.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/utils/HadoopClustering.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/utils/HadoopClustering$1.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/utils/IntSeq.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/utils/AlignedIntSeqStore.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/DistancesMain.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/ByteSeqInputFormat$SeqInputSplit.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/DistanceAndComparisonMapper.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/ByteSeqInputFormat.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/keys/
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/keys/Comparison.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/keys/DistanceAndComparison.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/keys/IntDistance.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/keys/MatrixRange.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/keys/DistanceAndComparison$GroupingComparator.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/DistancePartitioner.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/DistanceReducer.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/mapred/ByteSeqInputFormat$SeqRecordReader.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/sampler/
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/sampler/SamplerMain.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/sampler/SamplerInputFormat.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/distance/sampler/SamplerReducer.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/oneoff/
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/oneoff/DistancesMainOneOff.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/oneoff/HDFSEdgeReaderOneOff.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/oneoff/ByteSeqInputFormatOneOff.class
    Clustering/build/classes/edu/msu/cme/rdp/hadoop/oneoff/DistancePartitionerOneOff.class
    Clustering/build/classes/edu/msu/cme/rdp/taxatree/
    Clustering/build/classes/edu/msu/cme/rdp/taxatree/TreeBuilder$1.class
    Clustering/build/classes/edu/msu/cme/rdp/taxatree/TreeBuilder.class
    Clustering/build/classes/org/
    Clustering/build/classes/org/apache/
    Clustering/build/classes/org/apache/hadoop/
    Clustering/build/classes/org/apache/hadoop/mapred/
    Clustering/build/classes/org/apache/hadoop/mapred/CombinedIntermediateSortedReader.class
    Clustering/build/classes/org/apache/hadoop/mapred/ResortPartialResub$ExpectedRange.class
    Clustering/build/classes/org/apache/hadoop/mapred/SortPartialResults.class
    Clustering/build/classes/org/apache/hadoop/mapred/CombinedIntermediateSortedReader$Holder.class
    Clustering/build/classes/org/apache/hadoop/mapred/ReadPartialResultFile.class
    Clustering/build/classes/org/apache/hadoop/mapred/ResortPartialResub.class
    Clustering/build/classes/org/apache/hadoop/mapred/SummarizeAttempts.class
    Clustering/build/classes/org/apache/hadoop/mapred/ResortPartialResult$ExpectedRange.class
    Clustering/build/classes/org/apache/hadoop/mapred/ResortPartialResult.class
    Clustering/build/built-jar.properties
    Clustering/README.md
    Clustering/mcupgma.py
    Clustering/build.xml
    Clustering/.git/
    Clustering/.git/hooks/
    Clustering/.git/hooks/update.sample
    Clustering/.git/hooks/post-update.sample
    Clustering/.git/hooks/pre-applypatch.sample
    Clustering/.git/hooks/post-receive.sample
    Clustering/.git/hooks/prepare-commit-msg.sample
    Clustering/.git/hooks/pre-rebase.sample
    Clustering/.git/hooks/post-commit.sample
    Clustering/.git/hooks/commit-msg.sample
    Clustering/.git/hooks/pre-commit.sample
    Clustering/.git/hooks/applypatch-msg.sample
    Clustering/.git/description
    Clustering/.git/logs/
    Clustering/.git/logs/refs/
    Clustering/.git/logs/refs/heads/
    Clustering/.git/logs/refs/heads/master
    Clustering/.git/logs/HEAD
    Clustering/.git/FETCH_HEAD
    Clustering/.git/config
    Clustering/.git/HEAD
    Clustering/.git/branches/
    Clustering/.git/index
    Clustering/.git/refs/
    Clustering/.git/refs/tags/
    Clustering/.git/refs/remotes/
    Clustering/.git/refs/remotes/origin/
    Clustering/.git/refs/remotes/origin/HEAD
    Clustering/.git/refs/heads/
    Clustering/.git/refs/heads/master
    Clustering/.git/packed-refs
    Clustering/.git/info/
    Clustering/.git/info/exclude
    Clustering/.git/objects/
    Clustering/.git/objects/info/
    Clustering/.git/objects/pack/
    Clustering/.git/objects/pack/pack-3daf23b0c75dd9ee353e2ec559db03c723f4097b.idx
    Clustering/.git/objects/pack/pack-3daf23b0c75dd9ee353e2ec559db03c723f4097b.pack
    Clustering/LICENSE
    Clustering/manifest.mf


Install python packages
~~~~~~~~~~~~~~~~~~~~~~~

Comment out following cells if already have the packages installed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    %%script bash
    source ~/.bashrc
.. code:: python

    !pip install -U pip

.. parsed-literal::

    Requirement already up-to-date: pip in /usr/local/anaconda/lib/python2.7/site-packages


.. code:: python

    !pip install screed

.. parsed-literal::

    Requirement already satisfied (use --upgrade to upgrade): screed in /usr/local/anaconda/lib/python2.7/site-packages
    Requirement already satisfied (use --upgrade to upgrade): bz2file in /usr/local/anaconda/lib/python2.7/site-packages (from screed)


.. code:: python

    !pip install brewer2mpl

.. parsed-literal::

    Requirement already satisfied (use --upgrade to upgrade): brewer2mpl in /usr/local/anaconda/lib/python2.7/site-packages


.. code:: python

    !pip install biom-format

.. parsed-literal::

    Collecting biom-format
      Downloading biom-format-2.1.3.tar.gz (571kB)
    [K    100% |████████████████████████████████| 573kB 585kB/s 
    [?25hRequirement already satisfied (use --upgrade to upgrade): numpy>=1.3.0 in /usr/local/anaconda/lib/python2.7/site-packages (from biom-format)
    Collecting pyqi==0.3.2 (from biom-format)
      Downloading pyqi-0.3.2.tar.gz (240kB)
    [K    100% |████████████████████████████████| 241kB 1.2MB/s 
    [?25hRequirement already satisfied (use --upgrade to upgrade): scipy>=0.13.0 in /usr/local/anaconda/lib/python2.7/site-packages (from biom-format)
    Installing collected packages: pyqi, biom-format
      Running setup.py install for pyqi
      Running setup.py install for biom-format
    Successfully installed biom-format-2.1.3 pyqi-0.3.2


Install numpy, matplotlib, scipy, and pandas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, you can install **anaconda** that have most popular
python packages installed: https://store.continuum.io/cshop/anaconda/

.. code:: python

    # !pip install numpy matplotlib scipy pandas
check dependencies installed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    !make -f SSUsearch/Makefile tool_check Hmmsearch=hmmsearch Mothur=mothur Flash=flash Mcclust_jar=./Clustering/dist/Clustering.jar

.. parsed-literal::

    *** Dependencies are installed


