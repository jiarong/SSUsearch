rule taxa_summary:
    input:
        expand('{project}/search/{sample}/{sample}.align.filter.wang.silva.taxonomy.count', project=Project, sample=Samples),
    output:
        '{project}/taxa_summary/{project}.taxa.summary'.format(project=Project),
    params:
        alltaxonomy=lambda wildcards, input: ' '.join(input)
    conda: 'envs/ssusearch.yaml'
    shell:
        """
        mkdir -p {Project}/taxa_summary
        # taxon distribution
        for i in {1..5}; do
            python {Srcdir}/scripts/summarize-taxa-count.py \
                {Project}/taxa_summary/level.$i.tsv {params.alltaxonomy}
        """

