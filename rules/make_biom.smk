rule make_biom:
    input:
        taxfiles=expand('{project}/search/{sample}/{sample}.align.filter.wang.silva.taxonomy', project=Project, sample=Samples),
        clustfile='{project}/clust/complete.clust'.format(project=Project),
    output:
        '{project}/{project}.biom'.format(project=Project),
    params:
        alltaxonomy=lambda wildcards, input: ' '.join(input.taxfiles)
    conda: 'envs/ssusearch.yaml'
    shell:
        """
        cat {params.alltaxonomy} > {Project}/clust/{Project}.taxonomy

        (cd {Project}/clust
        python {Srcdir}/scripts/mcclust2mothur-list-cutoff.py \
            complete.clust {Project}.list {Otu_dist_cutoff}
        Clustering rep-seqs -c -l -s complete.clust {Otu_dist_cutoff} \
            combined_seqs.afa
        mv complete.clust_rep_seqs.fasta otu_rep_align.fa
        mothur -q \
            "#set.logfile(name=mothur.log, append=T); \
            make.shared(\
                list={Project}.list, \
                group={Project}.groups, \
                label={Otu_dist_cutoff});" \
        > /dev/null \
        || ( echo -e "*** Rule clust: make.shared (mothur) faied; See details in {Project}/clust/mothur.log\n"; exit 1; )
        mothur -q \
            "#set.logfile(name=mothur.log, append=T); \
            classify.otu(\
                list={Project}.list, \
                taxonomy={Project}.taxonomy, \
                label={Otu_dist_cutoff})" \
        > /dev/null \
        || ( echo -e "*** Rule clust: classify.otu (mothur) faied; See details in {Project}/clust/mothur.log\n"; exit 1; )
        mothur -q \
            "#set.logfile(name=mothur.log, append=T); \
            make.biom(\
                shared={Project}.shared, \
                constaxonomy={Project}.{Otu_dist_cutoff}.cons.taxonomy)" \
        > /dev/null \
        || ( echo -e "*** Rule clust: make.biom (mothur) faied; See details in {Project}/clust/mothur.log\n"; exit 1; )
        mv {Project}.{Otu_dist_cutoff}.biom {Project}.biom
        cp {Project}.biom ..

        # clean up tempfiles
        rm -f mothur.*.logfile *rabund derep.fasta \
            matrix.bin nonoverlapping.bin temp.*
        )
        """

