rule classify:
    input:
        '{project}/search/{{sample}}/{{sample}}.align.filter.fa'.format(project=Project),
    output:
        '{project}/search/{{sample}}/{{sample}}.align.filter.wang.gg.taxonomy'.format(project=Project),
        '{project}/search/{{sample}}/{{sample}}.align.filter.wang.gg.taxonomy.count'.format(project=Project),
        '{project}/search/{{sample}}/{{sample}}.align.filter.wang.silva.taxonomy'.format(project=Project),
        '{project}/search/{{sample}}/{{sample}}.align.filter.wang.silva.taxonomy.count'.format(project=Project),
    threads: config['Cpu']
    conda: 'envs/ssusearch.yaml'
    shell:
        """
        (cd {Project}/search/{wildcards.sample}
        # silva tax
        rm -f {wildcards.sample}.align.filter.*.wang.taxonomy
        mothur -q  \
            "#set.logfile(name={wildcards.sample}.mothur.log, append=T); \
            classify.seqs(\
                fasta={wildcards.sample}.align.filter.fa, \
                template={Gene_db}, taxonomy={Gene_tax}, \
                cutoff=50, processors={threads})" \
        > /dev/null \
        || ( echo -e "*** Rule classify: classify.seqs (mothur) with SILVA failed; See details in {wildcards.sample}.mothur.log\n"; exit 1; )

        mv {wildcards.sample}.align.filter.*.wang.taxonomy \
            {wildcards.sample}.align.filter.wang.silva.taxonomy
        
        python {Srcdir}/scripts/count-taxon.py \
            {wildcards.sample}.align.filter.wang.silva.taxonomy \
            {wildcards.sample}.align.filter.wang.silva.taxonomy.count

        # greengene tax
        rm -f {wildcards.sample}.align.filter.*.wang.taxonomy
        mothur -q \
            "#set.logfile(name={wildcards.sample}.mothur.log, append=T); \
            classify.seqs(\
                fasta={wildcards.sample}.align.filter.fa, \
                template={Gene_db_cc}, taxonomy={Gene_tax_cc}, \
                cutoff=50, processors={threads})" \
        > /dev/null \
        || ( echo -e "*** Rule classify: classify.seqs (mothur) with Greengene failed; See details in {wildcards.sample}.mothur.log\n"; exit 1; )

        mv {wildcards.sample}.align.filter.*.wang.taxonomy \
            {wildcards.sample}.align.filter.wang.gg.taxonomy
        python {Srcdir}/scripts/count-taxon.py \
            {wildcards.sample}.align.filter.wang.gg.taxonomy \
            {wildcards.sample}.align.filter.wang.gg.taxonomy.count
        )
        """
