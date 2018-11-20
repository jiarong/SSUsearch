#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import screed

def check_cassava18(f):
    for n, record in enumerate(screed.open(f)):
        name = record.name
        items = name.split()
        if len(items) < 2:
            return False
        desc = items[1]
        desc_items = desc.split(':')

        if len(desc_items) != 4:
            return False

        #*** 1st item should be 1 or 2 in seq description, e.g. 1:N:0:ACTTGA
        PE, is_filtered, ctrl_num, index_seq = desc_items
        if not PE == '1' or PE == '2':
            return False

        mes = ('*** WARNING: {} has seq description like cassava1.8 '
                'but seq name like pre-cassava1.8\n'
                '*** Here proceed as cassava1.8; '
                '*** See details: https://support.illumina.com/help/'
                'BaseSpace_OLH_009008/Content/Source/Informatics/BS/'
                'FileFormat_FASTQ-files_swBS.htm')
        if items[0].endswith('/1') or items[0].endswith('/2'):
            sys.stderr.write(mes)

        return True


def main():
    mes = """
    Convert paired end seq names in R1 to name/1 and R2 to name/2 
    (pre-cassava1.8)

    % python convert_seqname.py <file_R1.fa> <file_R2.fa> <file_extended.fa> ..
    input: 
        output files from paired end merging tools (flash or pandaseq);
        could be fasta or fastq or gziped

    output: stdout
    """
    if len(sys.argv) < 2:
        sys.stderr.write(mes)
        sys.exit(1)

    fs = sys.argv[1:]
    for f in fs:
        check = check_cassava18(f)
        if check:
            sys.stderr.write(
                ('*** {} have sequence name as cassava1.8\n'
                '*** converting R1 to pre-cassava1.8..'
                ).format(os.path.basename(f))
            )

            for n, record in enumerate(screed.open(f)):
                name = record['name']
                items = name.split()
                id = items[0]
                end = items[1].split(':')[0]
                seq = record['sequence']
                sys.stdout.write('>{}/{}\n{}\n'.format(id, end, seq))

        else:
            for n, record in enumerate(screed.open(f)):
                name = record['name']
                seq = record['sequence']
                sys.stdout.write('>{}\n{}\n'.format(name, seq))

if __name__ == '__main__':
    main()
