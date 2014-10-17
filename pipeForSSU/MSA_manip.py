#! /usr/bin/env python
# make position coverage histogram from cmalignOut.afa
# by gjr; Apr 12, 11

# MSA_manip see part 2

import sys
sys.path.insert(0, '/mnt/home/guojiaro/Documents/lib/screed')
import screed
from screed import fasta
import re

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    pass

def getPos(f, n_ref):   #make it easy, just use 1 refSeq
    refs = {}
    reads = {}
    cnt = 0
    for record in fasta.fasta_iter(open(f)):
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

    pos = []
    for record in fasta.fasta_iter(open(f)):
        name = record['name']
        if 'RF' in name:
            continue
        seq = record['sequence']
        assert len(seq) == length, 'seq length not the same'
        start = length - len(seq.lstrip('.').lstrip('-'))    ###indel are '.' or '-' in afa format
        end = len(seq.rstrip('.').rstrip('-')) - 1

        start_seq = sum(profile[:(start+1)])
        end_seq = sum(profile[:(end+1)])

        reads[name] = range(start_seq, end_seq+1)
        #pos.extend(range(start_seq, end_seq+1))

    return reads

def getCoverageByColumn(fp, n_ref):
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

    rows = {}
    fp.seek(0,0)
    for record in fasta.fasta_iter(fp):
        name = record['name']
        if 'RF' in name:
            continue
        seq = record['sequence']
        assert len(seq) == length, 'not afa format'
        rows[name] = seq

    pos1 = []  #number of nt in that colum
    pos2 = []  #number of nt same as RF
    for i in range(length):
        if profile[i] == 0:
            continue
        j = sum(profile[:i+1])
        for key in rows:
            if rows[key][i] not in ('-.'):
                pos1.append(j)
            if rows[key][i] == template[i]:
                pos2.append(j) 

    return pos1, pos2, len(rows)

###--------------------------------------above same as infMapping.py
#part 2
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
        f = sys.argv[1]
        n_ref = int(sys.argv[2])
        reads = getPos(f, n_ref)

        pos = []
        for key in reads:
            pos.extend(reads[key])
     
        n, bins, batches = plt.hist(pos, max(pos), cumulative = False, histtype = 'step',label = 'bla')
        plt.xlabel ('Position')
        plt.ylabel ('Coverage')
        plt.grid(1)

        plt.plot( (69,100), (-10,-10), (143,220), (-10,-10), (447,488), (-10,-10), (589,650), (-10,-10), (812,878), (-10,-10), (998,1043), (-10,-10), (1129,1145), (-10,-10), (1239,1298), (-10,-10), (1436,1457), (-10,-10), linewidth=5.0, color='green') 


        plt.xticks(range(0,2000, 200), range(0,2000,200))
        plt.xlim(xmax=2000)
        plt.gca().xaxis.grid(False)
        plt.gca().yaxis.grid(True)
        leg = plt.legend(loc = 'upper left', shadow = True, borderpad = 0.1)
        for t in leg.get_texts():
            t.set_fontsize('small')
        for l in leg.get_lines():
            l.set_linewidth(5) 
        #plt.show()
        plt.savefig('PCoverage_cmalign.png')
        plt.clf()

    if 0:
        '''
        get position coverage based afa file

        usage: python <thisFile> <file.afa> numberOfRefSeq
        '''

        f = sys.argv[1]
        n_ref = int(sys.argv[2])
        pos1, pos2, seqNum = getCoverageByColumn(open(f), n_ref)

	n, bins, batches = plt.hist(pos1, max(pos1), cumulative = False, histtype = 'step',label = '# of mapped bp', color='red')
        n, bins, batches = plt.hist(pos2, max(pos2), cumulative = False, histtype = 'step',label = '# of matched bp')
        plt.axhline(y=seqNum, color='black', label='# of seqs')
        plt.xlabel ('Position')
        plt.ylabel ('Coverage')
        #plt.grid(1)
        plt.gca().xaxis.grid(False)
        plt.gca().yaxis.grid(True)

        plt.plot( (69,100), (-10,-10), (143,220), (-10,-10), (447,488), (-10,-10), (589,650), (-10,-10), (812,878), (-10,-10), (998,1043), (-10,-10), (1129,1145), (-10,-10), (1239,1298), (-10,-10), (1436,1457), (-10,-10), linewidth=5.0, color='green') 


        leg = plt.legend(loc = 'upper left', shadow = True, borderpad = 0.1)
        for t in leg.get_texts():
            t.set_fontsize('small')
        for l in leg.get_lines():
            l.set_linewidth(5) 
        #plt.show()
        plt.savefig('PCoverageByColumn.png')
        plt.clf()

        n, bins, batches = plt.hist(pos1, max(pos1), cumulative = False, histtype = 'step',label = '# of mapped bp')
        plt.axhline(y=seqNum, color='black', label='# of seqs')
        plt.xlabel ('Position')
        plt.ylabel ('Coverage')
        #plt.grid(1)
        plt.gca().xaxis.grid(False)
        plt.gca().yaxis.grid(True)

        plt.plot( (69,100), (-10,-10), (143,220), (-10,-10), (447,488), (-10,-10), (589,650), (-10,-10), (812,878), (-10,-10), (998,1043), (-10,-10), (1129,1145), (-10,-10), (1239,1298), (-10,-10), (1436,1457), (-10,-10), linewidth=5.0, color='green') 


        leg = plt.legend(loc = 'upper left', shadow = True, borderpad = 0.1)
        for t in leg.get_texts():
            t.set_fontsize('small')
        for l in leg.get_lines():
            l.set_linewidth(5) 
        #plt.show()
        plt.savefig('PCoverageByColumn_mapped.png')
        plt.clf()

    if 0:
        '''
        python <thisFile><file.afa><start><end>
        cut afa alignment for primers
        '''
        fp = open(sys.argv[1])
        start = sys.argv[2]
        end = sys.argv[3]
        ref_primer, rows = cutMSA(fp, sys.argv[2], sys.argv[3])
        length = len(ref_primer)
        d = {}
        fw2 = open('%s.%sto%s.cut.table' %(sys.argv[1], start, end), 'w')
        fw3 = open('%s.%sto%s.cut.table.noInsert' %(sys.argv[1], start, end), 'w')
        print >> fw2, '%s\t%s' %('postion', 'A\tT\tC\tG\tTotal')
        pos = 0
        for i in range(length):
            cnt_A = 0
            cnt_T = 0
            cnt_C = 0 
            cnt_G = 0
            total = 0
            for key in rows:
                total += 1
                if rows[key][i] == 'A':
                    cnt_A+=1
                elif rows[key][i] == 'T':
                    cnt_T+=1
                elif rows[key][i] == 'C':
                    cnt_C+=1
                elif rows[key][i] == 'G':
                    cnt_G+=1
            lis = str(cnt_A), str(cnt_T), str(cnt_C), str(cnt_G), str(total)
            st = '\t'.join(lis)

            if ref_primer[i] in '.-':   #maybe should remove reads cause insertions
                print >> fw2, '  %s\t%s' %('IN', st)

            else:
                pos += 1
                print >> fw2, '%d %s\t%s' %(pos, ref_primer[i], st)
                print >> fw3, '%d %s\t%s' %(pos, ref_primer[i], st)


    if 0:
        '''
        python <thisFile><file.afa><start><end>
        cut afa alignment for primers
        produce MSA without insertions
        '''
        fp = open(sys.argv[1])
        start = sys.argv[2]
        end = sys.argv[3]
        ref_primer, rows = cutMSA(fp, sys.argv[2], sys.argv[3])
        length = len(ref_primer)
        d = {}
        fw2 = open('%s.%sto%s.cut.table' %(sys.argv[1], start, end), 'w')
        fw3 = open('%s.%sto%s.cut.table.noInsert' %(sys.argv[1], start, end), 'w')
        ### get align primer region for sequence logo
        fw4 = open('%s.%sto%s.cut.noInsert.afa' %(sys.argv[1], start, end), 'w')
        print >> fw2, '%s\t%s' %('postion', 'A\tT\tC\tG\tTotal')
        print >> fw3, '%s\t%s' %('postion', 'A\tT\tC\tG\tTotal')
        pos = 0
        rows2 = rows.copy()
        insert_triger = False
        for i in range(length):
            cnt_A = 0
            cnt_T = 0
            cnt_C = 0 
            cnt_G = 0
            total = 0

            if ref_primer[i] in '.-':   #maybe should remove reads cause insertions
                insert_triger = True
            for key in rows:
                total += 1
                if rows[key][i] == 'A':
                    cnt_A+=1
                elif rows[key][i] == 'T':
                    cnt_T+=1
                elif rows[key][i] == 'C':
                    cnt_C+=1
                elif rows[key][i] == 'G':
                    cnt_G+=1

                ### get dict of aligned seqs withou insertion
                if insert_triger:
                    seq = rows2[key]
                    seq2 = seq[:i]+' '+seq[i+1:]
                    rows2[key] = seq2

            insert_triger = False

            lis = str(cnt_A), str(cnt_T), str(cnt_C), str(cnt_G), str(total)
            st = '\t'.join(lis)

            if ref_primer[i] in '.-':   #maybe should remove reads cause insertions
                pass
                print >> fw2, '  %s\t%s' %('IN', st)

            else:
                pos += 1
                print >> fw2, '%d %s\t%s' %(pos, ref_primer[i], st)
                print >> fw3, '%d %s\t%s' %(pos, ref_primer[i], st)

        for key in rows2:
            seq = ''.join(rows2[key].split())
            temp = seq.strip('.').strip('-')
            if len(temp) == 0:
                continue
            print >> fw4, '>%s\n%s' %(key, seq)
        

    if 1:
        '''
        python <thisFile><file.afa><start><end>
        cut afa alignment for a region
        '''
        ### length cutoff set to 100bp ###
        #minLen = 30    # one V region
        minLen = 100    # for pyrotag region + # 971to1118
        #minLen = 0     # for 250-1250; singleton analysis
        fp = open(sys.argv[1])
        start = sys.argv[2]
        end = sys.argv[3]
        ref_primer, rows = cutMSA(fp, sys.argv[2], sys.argv[3])
        length = len(ref_primer)
        d = {}
        fw2 = open('%s.%sto%s.cut.lenScreened.fa' %(sys.argv[1], start, end), 'w')
        fw3 = open('%s.%sto%s.cut.lenScreened.afa' %(sys.argv[1], start, end), 'w')
        cnt = 0
        for key in rows:
            #if 'RF' in key or 'clu' in key:       ###screen for short reads

            '''
            if 'RF' in key or 'MSB1' in key:       ###screen for short reads
                continue
            '''

            '''
            if 'MSB1' not in key:       ###screen for pyrotag reads
                continue
            '''

            seq = rows[key]
            seq1 = seq.strip('.').strip('-')
            seq_noGap  = seq1.replace('-', '')
            if len(seq_noGap) < minLen:                 ###screen length
                continue
            print >> fw2, '>%s\n%s' %(key, seq_noGap)
            print >> fw3, '>%s\n%s' %(key, seq)
            cnt += 1

        print '%d sequences are matched to %s-%s region' %(cnt, sys.argv[2], sys.argv[3])
