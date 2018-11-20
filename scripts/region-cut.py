#! /usr/bin/env python
# cut primer, primer analysis
# by gjr;Apr 12, 11

"""
Cut a region in alignment based on start and end position in template sequence

% python region-cut.py <file.afa> start end min_len

"""
import sys, os
import screed
from screed import fasta
import re

def getRef(fp, n_ref):
    """
    Get template sequence from .afa file and a gap profile of the aligned 
    sequences (1 is a real base and 0 is a gap)

    Parameters:
    -----------
    fp : file object
        file object of aligned sequence file (.afa)
    n_ref : int
        number of template sequence to collect

    Returns:
    --------
    str
        name of the first template sequence
    str
        aligned sequence
    list
        a gap profile of aligned sequence

    """

    refs = {}
    reads = {}
    cnt = 0
    for record in fasta.fasta_iter(fp):
        name = record['name']
        seq = record['sequence']
        if 'ReFeReNcE' in name:
            refs[name] = seq
            cnt += 1 
        if cnt >= n_ref:
            break

    if cnt < n_ref:
        print 'not enough ReFeReNcE seqs'
        sys.exit(1)

    template = refs.values()[0].upper()  #use the first refSeq as template
    profile = []
    length = len(template)
    for i in range(length):
        if template[i] == 'N' or not template[i].isalpha():
            profile.append(0)
        else:
            profile.append(1)

    return name, template, profile  #return the ref seq and its mask profile

def cutMSA(fp, start, end):
    """
    Cut a region in Multiple Sequence Alignment based on the start and end 
    positions on template

    Parameters:
    -----------
    fp : file object
        file object of aligned sequence file (.afa)
    start : int
        start position of target region
    end : int
        end position of end region

    Returns:
    --------
    tuple
        a tuple with tow items. First item is target region in tempalte 
        and second item is a dictionary with sequence name as key 
        and target region of that sequence as value

    """
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
        if 'ReFeReNcE' in name:
            continue
        seq = record['sequence']
        assert len(seq) == length, 'not afa format'

        subSeq = seq[start1:(end1+1)]
        rows[name] = subSeq
        print >> fw, '>%s\n%s' %(name, subSeq)
        
    return template[start1:(end1+1)], rows

def getSeqPos(ref_profile, seq):
    """
    Get the start and end position when mapped to refSeq.
    Sequence to feed to the func should be afa format 
    (e.x. one from mothurAligner).

    Parameters:
    -----------
    ref_profile : list
        a gap profile, 0 is gap and 1 is real base pair.
    seq : str
        align sequence

    Returns:
    --------
    tuple
        a tuple of two int. 
        First one is start position and second one is end postion.

    """

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

def main():

    if len(sys.argv) != 5:
        mes = 'Usage: python %s <file.afa> start end min_len'
        print >> sys.stderr, mes %(os.path.basename(sys.argv[0]))
        sys.exit(1)

    # length cutoff
    minLen = int(sys.argv[4])

    fp = open(sys.argv[1])
    start = sys.argv[2]
    end = sys.argv[3]

    refName, template, profile = getRef(fp, 1)

    length = len(profile)
    for i in range(length):
        if profile[i] == 0:
            continue
        j = sum(profile[:i+1])
        # the template sequence starts at E.coli postion 27
        if j == int(start) - 27:
            start1 = i
        if j == int(end) - 27:
            end1 = i
            break

    ref_primer =  template[start1:(end1+1)]
    length_cut = len(ref_primer)

    fw2 = open('%s.%sto%s.cut.lenscreen.fa' %(sys.argv[1], start, end), 'w')
    fw3 = open('%s.%sto%s.cut.lenscreen' %(sys.argv[1], start, end), 'w')
    cnt = 0
    for record in screed.open(sys.argv[1]):
        name = record['name']
        if 'ReFeReNcE' in name:
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

    mes = '%d sequences are matched to %s-%s region' 
    print >> sys.stderr, mes %(cnt, sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()        
