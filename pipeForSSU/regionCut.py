#! /usr/bin/env python
# cut primer, primer analysis
# by gjr;Apr 12, 11

import sys
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed
from screed import fasta
import re

#script to manipulate MSA, cut seqs, and primer region check
#by gjr; Apr 28, 11

def getRef(fp, n_ref):
    refs = {}
    reads = {}
    cnt = 0
    for record in fasta.fasta_iter(fp):
        name = record['name']
        seq = record['sequence']
        #
        # ref seq name changed due to some 454 seqs have 'RF' in names
        #
        if 'ReFeReNcE' in name:
        #if 'RF' in name:
            refs[name] = seq
            cnt += 1 
        if cnt >= n_ref:
            break

    if cnt < n_ref:
        print 'not enough ReFeReNcE seqs'
        sys.exit(1)

    #get profile
    template = refs.values()[0].upper()  #use the first refSeq as template
    profile = []
    length = len(template)
    for i in range(length):
        ###in this case 'nnnn' at the beginning or end of seq should treated as indels (0)
        ###more generally 'n' should be treat as a base (1)
        if template[i] == 'N' or not template[i].isalpha():
            profile.append(0)
        else:
            profile.append(1)

    return name, template, profile  #return the ref seq and its mask profile

def cutMSA(fp, start, end):
    '''
    cut MSA base on the coordination on ecoli 16s
    '''
    fw = open('%s.%sto%s.cut' %(sys.argv[1], start, end), 'w')
    refName, template, profile = getRef(fp, 1)

    length = len(profile)
    for i in range(length):
        if profile[i] == 0:
            continue
        j = sum(profile[:i+1])
        if j == int(start):
            start1 = i
        if j == int(end):
            end1 = i
            break

    print >> fw, '>%s\n%s' %(refName, template[start1:(end1+1)])

    rows = {}          #ref seq not included
    fp.seek(0,0)
    for record in fasta.fasta_iter(fp):
        name = record['name']
        #
        # ref seq name changed due to some 454 seqs have 'RF' in names
        #
        if 'ReFeReNcE' in name:
        #if 'RF' in name:   #pass the ref seq
            continue
        seq = record['sequence']
        assert len(seq) == length, 'not afa format'

        subSeq = seq[start1:(end1+1)]
        rows[name] = subSeq
        print >> fw, '>%s\n%s' %(name, subSeq)
        
    return template[start1:(end1+1)], rows

def getSeqPos(ref_profile, seq):
    # get the start and end position when mapped to refSeq 
    # seq to feed to the func should be afa format (e.x. one from mothurAligner)
    profile = ref_profile
    length = len(profile)
    assert length == len(seq), 'check if afa format'
    tempLen = len(seq.lstrip('.').lstrip('-'))
    # use first position 0 system
    start1 = length - tempLen
    end1 = len(seq.rstrip('.').rstrip('-')) - 1

    start = sum(profile[:start1])
    end = sum(profile[:end1])

    return start, end

if __name__ == '__main__':
        
    if 1:
        '''
        python <thisFile><file.afa><start><end><minLen>
        longer scripts but more memory efficient
        cut afa alignment for region
        '''
        # length cutoff
        minLen = int(sys.argv[4])
        #

        fp = open(sys.argv[1])
        start = sys.argv[2]
        end = sys.argv[3]

        fw = open('%s.%sto%s.cut' %(sys.argv[1], start, end), 'w')
        refName, template, profile = getRef(fp, 1)

        length = len(profile)
        for i in range(length):
            if profile[i] == 0:
                continue
            j = sum(profile[:i+1])
            if j == int(start):
                start1 = i
            if j == int(end):
                end1 = i
                break

        ref_primer =  template[start1:(end1+1)]
        length_cut = len(ref_primer)

        fw2 = open('%s.%sto%s.cut.lenScreened.fa' %(sys.argv[1], start, end), 'w')
        fw3 = open('%s.%sto%s.cut.lenScreened.afa' %(sys.argv[1], start, end), 'w')
        cnt = 0
        #for record in fasta.fasta_iter(fp):
        for record in screed.open(sys.argv[1]):
            name = record['name']
            #
            # ref seq name changed due to some 454 seqs have 'RF' in names
            #
            if 'ReFeReNcE' in name:
            #if 'RF' in name:   #pass the ref seq
                continue
            seq = record['sequence']
            assert len(seq) == length, 'not afa format'

            subSeq = seq[start1:(end1+1)]
            seq1 = subSeq.strip('.').strip('-')
            seq_noGap = seq1.replace('-', '')
            if len(seq_noGap) < minLen:
                continue
            print >> fw2, '>%s\n%s' %(name, seq_noGap)
            print >> fw3, '>%s\n%s' %(name, subSeq)
            cnt += 1

        print '%d sequences are matched to %s-%s region' %(cnt, sys.argv[2], sys.argv[3])
