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
        if 'RF' in name:
            refs[name] = seq
            cnt += 1 
        if cnt >= n_ref:
            break

    if cnt < n_ref:
        print 'not enough RF seqs'
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
        if 'RF' in name:   #pass the ref seq
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
        
    if 0:
        '''
        python <thisFile><file.afa><start><end>
        longer scripts but more memory efficient
        cut afa alignment for primers
        produce MSA without insertions
        '''
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

        print >> fw, '>%s\n%s' %(refName, template[start1:(end1+1)])

        fp.seek(0,0)
        ref_primer =  template[start1:(end1+1)]
        length_cut = len(ref_primer)

        fw2 = open('%s.%sto%s.cut.table' %(sys.argv[1], start, end), 'w')
        fw3 = open('%s.%sto%s.cut.table.noInsert' %(sys.argv[1], start, end), 'w')
        ### get align primer region for sequence logo
        fw4 = open('%s.%sto%s.cut.noInsert.afa' %(sys.argv[1], start, end), 'w')
        print >> fw2, '%s\t%s' %('postion', 'A\tT\tC\tG\tTotal')
        print >> fw3, '%s\t%s' %('postion', 'A\tT\tC\tG\tTotal')
        pos = 0
        insert_triger = False
        l = []
        for i in range(length_cut):
            l.append([0, 0, 0, 0, 0])   #[A, T, C, G, total]  
        for record in fasta.fasta_iter(fp):
            name = record['name']
            if 'RF' in name:   #pass the ref seq
                continue
            seq = record['sequence']
            assert len(seq) == length, 'not afa format'

            subSeq = seq[start1:(end1+1)]
            print >> fw, '>%s\n%s' %(name, subSeq)

            for i in range(length_cut):

                if ref_primer[i] in '.-':   #maybe should remove reads cause insertions
                    insert_triger = True

                l[i][4]+= 1               #total += 1
                if subSeq[i] == 'A':
                    l[i][0]+=1
                elif subSeq[i] == 'T':
                    l[i][1]+=1
                elif subSeq[i] == 'C':
                    l[i][2]+=1
                elif subSeq[i] == 'G':
                    l[i][3]+=1

                ### get dict of aligned seqs withou insertion
                if insert_triger:
                    subSeq = subSeq[:i]+' '+subSeq[i+1:]

                insert_triger = False

            subSeq = ''.join(subSeq.split())
            temp = subSeq.strip('.').strip('-')
            if len(temp) == 0:
                continue
            print >> fw4, '>%s\n%s' %(name, subSeq)

        for i in range(length_cut):
            ll = l[i]
            st = '\t'.join('%s' % i for i in ll)

            if ref_primer[i] in '.-':   #maybe should remove reads cause insertions
                pass
                print >> fw2, '  %s\t%s' %('IN', st)

            else:
                pos += 1
                print >> fw2, '%d%s\t%s' %(pos, ref_primer[i], st)
                print >> fw3, '%d%s\t%s' %(pos, ref_primer[i], st)


    if 1:
        '''
        python <thisFile><file.afa><start><end>
        longer scripts but more memory efficient
        cut afa alignment for primers
        produce MSA without insertions
        show #percentage#
        '''
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

        print >> fw, '>%s\n%s' %(refName, template[start1:(end1+1)])

        fp.seek(0,0)
        ref_primer =  template[start1:(end1+1)]
        length_cut = len(ref_primer)

        fw2 = open('%s.%sto%s.cut.table' %(sys.argv[1], start, end), 'w')
        fw3 = open('%s.%sto%s.cut.table.noInsert' %(sys.argv[1], start, end), 'w')
        ### get align primer region for sequence logo
        fw4 = open('%s.%sto%s.cut.noInsert.afa' %(sys.argv[1], start, end), 'w')
        print >> fw2, '%s\t%s' %('postion', 'A\tT\tC\tG\tTotal\tTotalSeqs')
        print >> fw3, '%s\t%s' %('postion', 'A\tT\tC\tG\tTotal\tTotalSeqs')
        pos = 0
        insert_triger = False
        l = []
        for i in range(length_cut):
            l.append([0, 0, 0, 0, 0])   #[A, T, C, G, total_seq]  
        for record in fasta.fasta_iter(fp):
            name = record['name']
            if 'RF' in name:   #pass the ref seq
                continue
            seq = record['sequence']
            assert len(seq) == length, 'not afa format'

            subSeq = seq[start1:(end1+1)]
            print >> fw, '>%s\n%s' %(name, subSeq)

            for i in range(length_cut):

                if ref_primer[i] in '.-':   #maybe should remove reads cause insertions
                    insert_triger = True

                l[i][4]+= 1               #total_seq += 1
                if subSeq[i] == 'A':
                    l[i][0]+=1
                elif subSeq[i] == 'T':
                    l[i][1]+=1
                elif subSeq[i] == 'C':
                    l[i][2]+=1
                elif subSeq[i] == 'G':
                    l[i][3]+=1

                ### get dict of aligned seqs withou insertion
                if insert_triger:
                    subSeq = subSeq[:i]+' '+subSeq[i+1:]

                insert_triger = False

            subSeq = ''.join(subSeq.split())
            temp = subSeq.strip('.').strip('-')
            if len(temp) == 0:
                continue
            print >> fw4, '>%s\n%s' %(name, subSeq)

        for i in range(length_cut):
            ll = l[i]
            #
            # use percetage
            #
            total = float(sum(ll[:4]))
            if total == 0.0:
                st = '%.3f\t%.3f\t%.3f\t%.3f\t%d\t%d' %(0,0,0,0,0,ll[4])
            else:
                st = '%.3f\t%.3f\t%.3f\t%.3f\t%d\t%d' %(ll[0]/total,
                                                         ll[1]/total,
                                                          ll[2]/total,
                                                           ll[3]/total,
                                                            int(total),
                                                             ll[4])

            if ref_primer[i] in '.-':   #maybe should remove reads cause insertions
                pass
                print >> fw2, '  %s\t%s' %('IN', st)

            else:
                pos += 1
                print >> fw2, '%d%s\t%s' %(pos, ref_primer[i], st)
                print >> fw3, '%d%s\t%s' %(pos, ref_primer[i], st)
