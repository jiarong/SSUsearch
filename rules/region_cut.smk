rule region_cut:
    input:
        '{project}/search/{{sample}}/{{sample}}'.format(project=Project),
    output:
        '{project}/search/{{sample}}/{{sample}}.forclust'.format(project=Project),
        '{project}/search/{{sample}}/{{sample}}.align.filter.fa'.format(project=Project),
    threads: config['Cpu']
    conda: 'envs/ssusearch.yaml'
    shell:
        """
        echo "*** Starting mothur align"
        cat {Gene_model_org} {Project}/search/{wildcards.sample}/{wildcards.sample}  > {Project}/search/{wildcards.sample}/{wildcards.sample}.RFadded
        
        rm -f mothur.*.logfile
        mothur -q "#set.logfile(name={Project}/search/{wildcards.sample}/{wildcards.sample}.mothur.log); align.seqs(candidate={Project}/search/{wildcards.sample}/{wildcards.sample}.RFadded, template={Ali_template}, threshold=0.5, flip=t, processors={threads})"

        python {Srcdir}/scripts/mothur-align-report-parser-cutoff.py \
            {Project}/search/{wildcards.sample}/{wildcards.sample}.align.report \
            {Project}/search/{wildcards.sample}/{wildcards.sample}.align \
            {Project}/search/{wildcards.sample}/{wildcards.sample}.align.filter \
            0.5
        
        python {Srcdir}/scripts/remove-gap.py \
            {Project}/search/{wildcards.sample}/{wildcards.sample}.align.filter \
            {Project}/search/{wildcards.sample}/{wildcards.sample}.align.filter.fa

        python {Srcdir}/scripts/region-cut.py \
            {Project}/search/{wildcards.sample}/{wildcards.sample}.align.filter \
            {Start} {End} {Len_cutoff}
        
        mv {Project}/search/{wildcards.sample}/{wildcards.sample}.align.filter.{Start}to{End}.cut.lenscreen {Project}/search/{wildcards.sample}/{wildcards.sample}.forclust
        """
