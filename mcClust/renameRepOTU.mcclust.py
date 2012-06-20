# by gjr; Apr 10, 12

import sys

if 0:
    '''
    usage: python<thisFile><OTUrep_cutoff.fasta><OTU.rename.fasta>
    '''
    fw = open(sys.argv[2], 'wb')
    for line in open(sys.argv[1]):
        line = line.rstrip()
        if not line.startswith('>'):
            line = line.replace('.','-')
            print >> fw, line
            continue
        # name and annot are separated by '  ' (two spaces)
        #>GJ4ZA3T01CUFZ5  prefered=false,cluster=0,clustsize=39
        #print line.split('  ',1)
        name, annot = line.split('  ',1)
        temp = annot.split(',')[1]
        cluNum = temp.split('=')[1]
        cluNum = int(cluNum)
        print >> fw, '>OTU%d' %(cluNum)


if 1:
    '''
    usage: python<thisFile><OTUrep_cutoff.fasta><file.iTolData>
    '''

    fw = open('%s.renamed.fasta' %(sys.argv[1]), 'wb')
    names = (line.rstrip().split('\t')[0] for line in open(sys.argv[2]))
    names = set(names)
    triger = True
    for line in open(sys.argv[1]):
        line = line.rstrip()
        if (not line.startswith('>')):
            if not triger:
                continue
            line = line.replace('.','-')
            print >> fw, line
            continue
        # name and annot are separated by '  ' (two spaces)
        #>GJ4ZA3T01CUFZ5  prefered=false,cluster=0,clustsize=39
        #print line.split('  ',1)
        name, annot = line.split('  ',1)

        temp = annot.split(',')[1]
        cluNum = temp.split('=')[1]
        cluNum = int(cluNum)
        newName = 'OTU%d' %(cluNum)
        if not newName in names:
            triger = False
            continue
        print >> fw, '>%s' %(newName)
        triger = True
