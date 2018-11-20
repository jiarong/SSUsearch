rule copy_correction:
    input:
        listfile='{project}/clust/{project}.list'.format(project=Project),
        groupfile='{project}/clust/{project}.biom'.format(project=Project),
        taxfile=expand('{project}/search/{sample}/{sample}.align.filter.wang.gg.taxonomy', project=Project, sample=Samples),
    output:
        '{project}/copy_correction/{project}.cc.biom'.format(project=Project),
    conda: 'envs/ssusearch.yaml'
    shell:
        """
        mkdir -p {Project}/copy_correction
        rm -f {Project}/copy_correction/{Project}.list \
            {Project}/copy_correction/{Project}.group
        cp {input.listfile} {Project}/copy_correction
        cp {input.groupfile} {Project}/copy_correction
        cat {input.taxfile} > {Project}/copy_correction/{Project}.gg.taxonomy

        (cd {Project}/copy_correction
        mothur -q \
            "#set.logfile(name=mothur.log); \
            classify.otu(\
                list={Project}.list, \
                taxonomy={Project}.gg.taxonomy, \
                label={Otu_dist_cutoff})" \
        > /dev/null \
        || ( echo -e "mothur classify.otu failed..\n"; exit 1; )

        mv {Project}.{Otu_dist_cutoff}.cons.taxonomy {Project}.cons.taxonomy
        mv {Project}.{Otu_dist_cutoff}.cons.tax.summary {Project}.cons.tax.summary

        mothur -q \
            "#set.logfile(name=mothur.log, append=T); \
            make.shared(biom={Project}.biom)" \
        > /dev/null \
        || ( echo -e "*** mothur make.shared failed..\n"; exit 1; )

        python {Srcdir}/scripts/copyrighter-otutable.py {Copy_db_cc} {Project}.cons.taxonomy {Project}.shared {Project}.cc.shared

        mothur -q \
            "#set.logfile(name=mothur.log, append=T); \
            make.biom(
                shared={Project}.cc.shared, \
                constaxonomy={Project}.cons.taxonomy);"\
        > /dev/null \
        || ( echo -e "*** mothur make.biom failed..\n"; exit 1; )
        mv {Project}.cc.userLabel.biom {Project}.cc.biom

        ) 
        """

