rule hmmsearch:
    input:
        '{project}/seqname_convert/{{sample}}.fa'.format(project=Project)
    output:
        '{project}/search/{{sample}}/{{sample}}'.format(project=Project),
    threads: config['Cpu']
    conda: 'envs/ssusearch.yaml'
    shell:
        """
        mkdir -p {Project}/search/{wildcards.sample}

        ### start hmmsearch
        echo "*** hmmsearch starting"
        time hmmsearch --incE 10 --incdomE 10 --cpu {threads} \
            --domtblout {Project}/search/{wildcards.sample}/{wildcards.sample}.hmmdomtblout \
            -o /dev/null \
            -A {Project}/search/{wildcards.sample}/{wildcards.sample}.sto \
            {Hmm} \
            {Project}/seqname_convert/{wildcards.sample}.fa
        echo "*** hmmsearch finished"

        python {Srcdir}/scripts/get-seq-from-hmmout.py \
            {Project}/search/{wildcards.sample}/{wildcards.sample}.hmmdomtblout \
            {Project}/search/{wildcards.sample}/{wildcards.sample}.sto \
            {Project}/search/{wildcards.sample}/{wildcards.sample}
        """
