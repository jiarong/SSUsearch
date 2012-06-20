#! /usr/bin python
# parse tabular output from HMMER, do identity filter and MSA convert
# by gjr; Jan 25, 12

import sys
import os
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed
import cPickle

N = 10
M = None

def getDict_domain(fp):
    '''
    DONOT use, bad function
    still need to verify the position of item in list
    '''
    d = {}
    for line in fp:
        if line.startswith('#'):
            continue
        line = line.strip()
        lis = line.split()
        name = lis[2]
        e_val = float(lis[5])
        bit = float(lis[6])
        if M:
            if bit > M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit

    return d

def getDict_wholeSeq(fp):
    d = {}
    for line in fp:
        if line.startswith('#'):
            continue
        line = line.strip()
        lis = line.split()
        name = lis[0]
        e_val = float(lis[4])
        bit = float(lis[5])
        if M:
            if bit > M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit

    return d


def getDict_domian(fp):
    d = {}
    for line in fp:
        if line.startswith('#'):
            continue
        line = line.strip()
        lis = line.split()
        name = lis[0]
        qlen = int(lis[2])
        e_val = float(lis[6])
        bit = float(lis[7])
        if M:
            if bit > M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit, qlen

    return d

def getDict_domain_addFilter(fp):
    # (>= 50% and >= 30bp) or (< 50% and > 80bp)
    d = {}
    for line in fp:
        if line.startswith('#'):
            continue
        line = line.strip()
        lis = line.split()
        name = lis[0]
        #rm '-RC-' suffix
        name = name.rstrip('-RC-')
        qlen = int(lis[2])
        e_val = float(lis[6])
        bit = float(lis[7])
        aliS = int(lis[17])
        aliE = int(lis[18])
        ali = (aliE - aliS + 1)
        # add filter
        if ali < 30:
            continue
        iden = ali/float(qlen)
        if ((iden < 0.5) and (ali < 80)):
            continue

        if M:
            if bit > M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit, iden, qlen

    return d


if __name__ == '__main__':
    if 0:
        fp = open(sys.argv[1])
        N = 1e-8
        d = getDict_wholeSeq(fp)
        print '%d hits got at %s cutoff' %(len(d), str(N))
        names = d.keys()
        fw = open(sys.argv[3], 'w')
        for record in fasta.fasta_iter(open(sys.argv[2])):
            name = record['name']
            if name not in names:
                continue
            seq = record['sequence']
            print >> fw, '>%s\n%s' %(name, seq)

    if 0:
        '''
        funGenes hmmHits on multiple samples
        python <thisFile><hmmtbloutDir><table.txt>
        '''
        #N = 1e-6
        hmmOutList = os.listdir(sys.argv[1])
        outFile = open(sys.argv[2], 'w')
        fields = set() #samples
        names = set()  #genes
        d2 = {}
        for f in hmmOutList:
            sample, _, gene, _ = f.split('.')
            fields.add(gene)
            names.add(sample)

        fields = list(fields)
        names = list(names)
        fields.sort()
        names.sort()
        dd = {}
        for sample in names:
            dd[sample] = {}
            
        for f in hmmOutList:
            fp = open(sys.argv[1].rstrip('/')+'/'+f)
            sample, _, gene, _ = f.split('.')
            d = getDict_wholeSeq(fp)
            print '%s-%s: %d hits got at %s cutoff' %(sample, gene, len(d), str(N))
            dd[sample][gene] = len(d)

        header = 'name\t'+ '\t'.join(fields)
        print >> outFile, header
        for sample in names:
            lis = [sample]
            for gene in fields:
                n = str(dd[sample][gene])
                lis.append(n)
            print >> outFile, '\t'.join(lis)


    if 0:
        '''
        funGenes hmmHits on multiple samples
        python <thisFile><hmmtbloutDir><seqDir><outDir>
        '''
        #N = 1e-6

        hmmOutList = os.listdir(sys.argv[1])
        fields = set() #gene
        names = set()  #samples
        d2 = {}
        for f in hmmOutList:
            sample, _, gene, _ = f.split('.')
            fields.add(gene)
            names.add(sample)

        fields = list(fields)
        names = list(names)
        fields.sort()
        names.sort()
        dd = {}
        for sample in names:
            # dict in dict
            dd[sample] = {}
            
        for f in hmmOutList:
            fp = open(sys.argv[1].rstrip('/')+'/'+f)
            sample, _, gene, _ = f.split('.')
            d = getDict_wholeSeq(fp)
            print '%s-%s: %d hits got at %s cutoff' %(sample, gene, len(d), str(N))
            dd[sample][gene] = d.keys()

        os.mkdir(sys.argv[3])
        path = os.path.abspath(sys.argv[3])
        for sample in names:
            proteinFiles = os.listdir(sys.argv[2])
            for file in proteinFiles:
                if sample in file:
                    sample_proteinFile = file
                 
            for record in screed.open('%s/%s' %(os.path.abspath(sys.argv[2]), sample_proteinFile)):
                name = record['name']
                seq = record['sequence']
                for gene in fields:
                    if len(dd[sample][gene]) == 0:
                        break
                    fw = open('%s/%s.%s.hmmout.fa' %(path, sample, gene), 'w')
                    if name in dd[sample][gene]:
                        print >> fw, '>%s\n%s' %(name, seq)



    if 0:
        N = 1e-8 
        f1 = sys.argv[1]
        f2 = sys.argv[2]
        d1 = getDict_wholeSeq(open(f1))
        d2 = getDict_wholeSeq(open(f2))

        s1 = set(d1.keys())
        s2 = set(d2.keys())

        print len(s1)
        print len(s1.intersection(s2))
        print len(s2)


    if 0:
        #convert hmmearch output seq.sto to seq.fa and add qlen to end of name
        #read seqs into a dict, not memory efficient
        '''
        usage:
        python <thisFile><hmmdomtblout><hmmseqout.sto>
        '''

        hmm = getDict_domain_addFilter(open(sys.argv[1]))  
        #dict of hmm hits, may take big memory if too many hits
        cPickle.dump(hmm, open(sys.argv[1]+'.parsedToDictWithScore.pickle', 'w'))
        print >> sys.stderr, 'parsing hmmdotblout done..'

        input_handle = open(sys.argv[2], 'rU')
        output_handle = open(sys.argv[2].rstrip('.sto')+'.fa', 'w')

        cnt1 = 0
        cnt2 = 0
        d_seq = {}
        for line in input_handle:
            if line.startswith('#'):
                continue
            if line.startswith('//'):
                #end of file
                continue
            line = line.rstrip()
            if not line:
                continue
            # assume no space in names
            name, subseq = line.split()
            subseq = subseq.replace('-','').replace('.','')
            if subseq == '':
                continue

            if d_seq.has_key(name):
                curseq = d_seq[name]
                # combined parts of interleaved MSA
                d_seq[name] = curseq + subseq
            else:
                d_seq[name] = subseq

        for key in d_seq:
            id = key
            name = id.rsplit('/',1)[0].rstrip('-RC-')
            cnt1 += 1
            if (cnt1) % 1000 == 0:
                print >> sys.stderr, '%d seqs scanned..' %(cnt1)
            if not hmm.has_key(name):
                continue
            qlen = hmm[name][-1]
            assert type(qlen) == int
            l = hmm.pop(name) # assuming very few seqs with multi domain hits  or with both strands having hits
            name = name + '-length-%d' %(qlen)
            seq = d_seq[key]
            print >> output_handle, '>%s\n%s' %(name, seq)
            cnt2 += 1

        print '%d of %d seqs are kept' %(cnt2, cnt1)


    if 1:
        #convert hmmearch output seq.sto to seq.fa and do NOT add qlen to end of name
        #read seqs into a dict, not memory efficient
        '''
        usage:
        python <thisFile><hmmdomtblout><hmmseqout.sto>
        '''

        hmm = getDict_domain_addFilter(open(sys.argv[1]))  
        #dict of hmm hits, may take big memory if too many hits
        cPickle.dump(hmm, open(sys.argv[1]+'.parsedToDictWithScore.pickle', 'w'))
        print >> sys.stderr, 'parsing hmmdotblout done..'

        input_handle = open(sys.argv[2], 'rU')
        output_handle = open(sys.argv[2].rstrip('.sto')+'.fa', 'w')

        cnt1 = 0
        cnt2 = 0
        d_seq = {}
        for line in input_handle:
            if line.startswith('#'):
                continue
            if line.startswith('//'):
                #end of file
                continue
            line = line.rstrip()
            if not line:
                continue
            # assume no space in names
            name, subseq = line.split()
            subseq = subseq.replace('-','').replace('.','')
            if subseq == '':
                continue

            if d_seq.has_key(name):
                curseq = d_seq[name]
                # combined parts of interleaved MSA
                d_seq[name] = curseq + subseq
            else:
                d_seq[name] = subseq

        for key in d_seq:
            id = key
            name = id.rsplit('/',1)[0].rstrip('-RC-')
            cnt1 += 1
            if (cnt1) % 1000 == 0:
                print >> sys.stderr, '%d seqs scanned..' %(cnt1)
            if not hmm.has_key(name):
                continue
            qlen = hmm[name][-1]
            assert type(qlen) == int
            l = hmm.pop(name) # assuming very few seqs with multi domain hits  or with both strands having hits
            #name = name + '-length-%d' %(qlen)
            seq = d_seq[key]
            print >> output_handle, '>%s\n%s' %(name, seq)
            cnt2 += 1

        print '%d of %d seqs are kept' %(cnt2, cnt1)
