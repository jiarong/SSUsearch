#! /usr/bin python
# parse tabular output from HMMER, do identity filter and MSA convert
# by gjr; Jan 25, 12

"""
Parse tabular output from HMMER, do length filter (30 bp minimum)
Convert .sto to .fa

% python get-seq-from-hmmout.py <hmmdomtblout> <hmmseqout.sto> <outfile.fa>
"""

import sys
import os
import screed
import cPickle

N = 10
M = None

def getDict_wholeSeq(fp):
    """
    Parse .tblout file from hmmsearch

    Parameters:
    -----------
    fp : file object
        file object of .tblout file

    Returns:
    --------
    dict:
        a dictionary with sequence name as key (str)
        and e-value, bit score as value (tuple)

    """

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
            if bit < M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit

    return d


def getDict_domain(fp):
    """
    Parse .hmmtblout file from hmmsearch

    Parameters:
    -----------
    fp : file object
        file object of .hmmtblout file

    Returns:
    --------
    dict:
        a dictionary with sequence name as key (str)
        and e-value, bit score, read length as value (tuple)

    """
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
            if bit < M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit, qlen

    return d

def getDict_domain_addFilter(fp):
    """
    Parse .hmmtblout file from hmmsearch
    Filter hits based on read lenght and percent identity

    Parameters:
    -----------
    fp : file object
        file object of .hmmtblout file

    Returns:
    --------
    dict:
        a dictionary with sequence name as key (str)
        and e-value, bit score, identity, read length as value (tuple)

    """
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
            if bit < M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit, iden, qlen

    return d

def getDict_domain_noIdenFilter(fp):
    """
    Parse .hmmtblout file from hmmsearch
    Filter hits based on read lenght

    Parameters:
    -----------
    fp : file object
        file object of .hmmtblout file

    Returns:
    --------
    dict:
        a dictionary with sequence name as key (str)
        and e-value, bit score, identity, read length as value (tuple)

    """
    # >= 30bp
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

        if M:
            if bit < M:
                continue  
        else:
            if e_val > N:
                continue
        d[name] = e_val, bit, iden, qlen

    return d

if __name__ == '__main__':

    #read seqs into a dict, not memory efficient
    if len(sys.argv) != 4:
        mes = 'python {} <hmmdomtblout> <hmmseqout.sto> <outfile.fa>'
        print >> sys.stderr, mes.format(os.path.basename(sys.argv[0]))
        sys.exit(1)

    hmmfile = sys.argv[1]
    infile = sys.argv[2]
    outfile = sys.argv[3]
    hmm = getDict_domain_noIdenFilter(open(hmmfile))  
    #dict of hmm hits, may take big memory if too many hits
    cPickle.dump(hmm, open(sys.argv[1]+'.parsedToDictWithScore.pickle', 'w'))
    print >> sys.stderr, 'parsing hmmdotblout done..'

    input_handle = open(infile, 'rU')
    output_handle = open(outfile, 'wb')

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

    print '%d of %d seqs are kept after hmm parser' %(cnt2, cnt1)
