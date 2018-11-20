rule taxa_summary:
    input:
        expand('{project}/search/{sample}/{sample}.align.filter.wang.silva.taxonomy.count', project=Project, sample=Samples),
    output:
        expand('{project}/taxa_summary/level.{i}.tsv', project=Project, i=[1,2,3,4,5]),
    params:
        alltaxonomy=lambda wildcards, input: ' '.join(input)
    conda: 'envs/ssusearch.yaml'
    shell:
        """
        mkdir -p {Project}/taxa_summary
        # taxon distribution
        for i in {{1..5}}; do
            python {Srcdir}/scripts/summarize-taxon-count.py \
                $i {Project}/taxa_summary/level.$i.tsv {params.alltaxonomy}
        done
        """

