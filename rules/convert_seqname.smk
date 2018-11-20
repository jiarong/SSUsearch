def sc_input(wildcards):
    R1 = str(Df.loc[wildcards.sample, 'R1'])
    R2 = str(Df.loc[wildcards.sample, 'R2'])
    Merged = str(Df.loc[wildcards.sample, 'Merged'])
    names = ['R1', 'R2', 'Merged']
    d = {}
    for name, f in zip(names, [R1, R2, Merged]):
        if f == 'nan':
            continue
        d[name] = f
    print(d)
    return d

rule convert_seqname:
    input: unpack(sc_input)
    output:
        '{project}/seqname_convert/{{sample}}.fa'.format(project=Project),
    conda: 'envs/ssusearch.yaml'
    shell:
        """
        echo {input}

        mkdir -p {Project}/seqname_convert
        python {Srcdir}/scripts/convert_seqname.py {input} > {output}
        """
