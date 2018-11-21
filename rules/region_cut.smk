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
        
        (cd {Project}/search/{wildcards.sample}
        rm -f mothur.*.logfile
        mothur -q \
            "#set.logfile(name={wildcards.sample}.mothur.log); \
            align.seqs(candidate={wildcards.sample}.RFadded, \
                template={Ali_template}, \
                threshold=0.5, flip=t, \
                processors={threads})" \
        > /dev/null \
        || ( echo -e "*** Rule region_cut: align.seqs (mothur) failed; Check {Project}/search/{wildcards.sample}/{wildcards.sample}.mothur.log for details..\n"; exit 1; )

        python {Srcdir}/scripts/mothur-align-report-parser-cutoff.py \
            {wildcards.sample}.align.report \
            {wildcards.sample}.align \
            {wildcards.sample}.align.filter \
            0.5
        
        python {Srcdir}/scripts/remove-gap.py \
            {wildcards.sample}.align.filter \
            {wildcards.sample}.align.filter.fa

        python {Srcdir}/scripts/region-cut.py \
            {wildcards.sample}.align.filter \
            {Start} {End} {Len_cutoff}
        
        mv {wildcards.sample}.align.filter.{Start}to{End}.cut.lenscreen \
            {wildcards.sample}.forclust
        )
        """
