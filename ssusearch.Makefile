# Makefile for  ssusearch
# key parameters


### path of sequence file if not defined in CMD line. 
#Seqfile?=./test/data/1c.fa

### start and end for cutting alignment if not definded in CMD line.
#Start?=
#End?=

Seqfile=$(realpath Seqfile)
Seqfile_name=$(notdir $(Seqfile))
Seqfile_name_parts=$(subst ., ,	$(Seqfile_name))

#Tag?=$(word 1,$(Seqfile_name_parts))
Tag?=dummy

Outdir=$(Seqfile).$(Gene).out

TERM?=linux

ssusearch: qc mothur_align

ssusearch_no_qc: no_qc mothur_align

.PHONY: qc no_qc hmmsearch mothur_align clean

no_qc: $(Seqfile)
	rm -f $(Tag).qc && ln -s $(Seqfile) $(Tag).qc

qc: $(Seqfile)
	@echo "*** Starting read quality control and pair end merging"
	python $(Script_dir)/quality-trim-sep-pe.py $(Phred) $(Seqfile) \
		$(Tag)
	$(Flash) $(Tag).1 $(Tag).2 \
		$(Flash_flags) -o $(Tag) | \
	tee $(Tag.flash.report)

	-(rm $(Tag).1 $(Tag).2)
	cat $(Tag).{extendedFrags,notCombined_1,notCombined_2}.fastq \
		> $(Tag).aftermerge.fastq

	(python $(Script_dir)/fq2fa.py $(Tag).aftermerge.fastq \
		$(Tag).qc.fa \
	) || (rm $(Tag).qc.fa && false)

	-(rm $(Tag).{extendedFrags,notCombined_1,notCombined_2}.fastq)


hmmsearch: $(Tag).qc.$(Gene)

$(Tag).qc.$(Gene): $(Tag).qc
	@echo
	@echo "*** Starting hmmsearch"
	python $(Script_dir)/add-rc.py $(Tag).qc - | \
	time $(Hmmsearch) --incE 10 --incdomE 10 --cpu 1 \
		-A $(Tag).qc.$(Gene).sto \
		-o $(Tag).qc.$(Gene).hmmout \
		--tblout $(Tag).qc.$(Gene).hmmtblout \
		--domtblout $(Tag).qc.$(Gene).hmmdomtblout $(Hmm) -
	@echo "hmmsearch done.."
	(python $(Script_dir)/get-seq-from-hmmout.py \
		$(Tag).qc.$(Gene).hmmdomtblout \
		$(Tag).qc.$(Gene).sto \
		$(Tag).qc.$(Gene) \
	) || (rm $(Tag).qc.$(Gene) && false)
	@echo "hmm filter and MSA conversion done.."

mothur_align: $(Tag).qc.$(Gene).align.filter

$(Tag).qc.$(Gene).align.filter: $(Tag).qc.$(Gene)
	@echo
	@echo "*** Starting mothur align"
	cat $(Gene_model_org) $(Tag).qc.$(Gene) > \
		$(Tag).qc.$(Gene).RFadded

	# mothur does not allow tab between its flags, thus no indents here
	time $(Mothur) "#align.seqs(\
	candidate=$(Tag).qc.$(Gene).RFadded, \
	template=$(Ali_template), search=suffix, threshold=0.5, \
	flip=t, processors=1)"

	(python $(Script_dir)/mothur-align-report-parser.py \
		$(Tag).qc.$(Gene).align.report \
		$(Tag).qc.$(Gene).align \
		$(Tag).qc.$(Gene).align.filter \
	) || (rm $(Tag).qc.$(Gene).align.filter && false)

	python $(Script_dir)/remove-gap.py \
		$(Tag).qc.$(Gene).align.filter \
		$(Tag).qc.$(Gene).align.filter.fa

	$(Mothur) "#classify.seqs(\
	fasta=$(Tag).qc.$(Gene).align.filter.fa, \
	template=$(Gene_db), taxonomy=$(Gene_tax), cutoff=50, \
	processors=1)"

clean:
	-(rm -f \
	$(filter-out %.filter %.filter.fa %.qc %.taxonomy $(Tag),\
	$(wildcard $(Tag)*)))

	@echo "*** Files kept after clean:"
	@ls
