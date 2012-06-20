#! /usr/bin/env bash
# make the bash files to ssu search pipe
# by gjr; Jan 26, 12

set -e

#Usage: bash <thisFile> -s <sample(s)> -m <SSU.hmm> -r <SSU.refs> -t <ecoli.afa> -b <start> -e <end>

if ( ! getopts :s:m:r:t:b:e:h opt ); then
  echo "Usage: $(basename $0) -s <sample(s)> -m <SSU.hmm> -r <SSU.refs> -t <ecoli.afa> -b <start> -e <end>" >&2
  echo "-h for help" >&2
  exit $E_OPTERROR;
fi

while getopts :s:m:r:t:b:e:h opt; do
  case $opt in
    h) echo "Usage: $(basename $0) -s <sample(s)> -m <SSU.hmm> -r <SSU.refs> -t <ecoli.afa> -b <start> -e <end>" >&2
       ;;
    s) echo "option s, sample(s): $OPTARG" >&2
       samplePath=$OPTARG
       ;;
    m) echo "option m, hmm model : $OPTARG" >&2
       HMM=$OPTARG
       ;;
    r) echo "option r, ref SSU sequences: $OPTARG" >&2
       REF=$OPTARG
       ;;
    t) echo "option t, E.coli template alignment : $OPTARG" >&2
       ECO=$OPTARG
       ;;
    b) echo "option b, start position of cut region: $OPTARG" >&2
       STA=$OPTARG
       ;;
    e) echo "option e, end position of cut region: $OPTARG" >&2
       END=$OPTARG
       ;; 
    \?) echo "Invalid option: -$OPTARG" >&2
        exit 1
        ;;
    :) echo "Option -$OPTARG requires an argument." >&2
       exit 1
  esac
done
echo
echo
# get absolute path of argvs
SSUhmm=$(cd $(dirname $HMM); pwd)/$(basename $HMM)
SSUrefs=$(cd $(dirname $REF); pwd)/$(basename $REF)
ECOLI=$(cd $(dirname $ECO); pwd)/$(basename $ECO)
if [ -d "$samplePath" ]; then
    time(
    echo "$samplePath is a directory.."
    sampleDir=$samplePath
    sampleList=$(ls $(find $sampleDir -maxdepth 1 -type f ))
    sampleNum=$(ls $(find $sampleDir -maxdepth 1 -type f )|wc -l)
    echo "${sampleNum} samples are founded:"
    echo "$sampleList"
    echo
    echo
    
    for ff in $sampleList; do
        f=$(cd $(dirname $ff); pwd)/$(basename $ff)
        fName=$(basename $f)
        #sample=$(basename $f bz2)
        sample=${fName%%.*}
        echo "start processing $fName"

        outDir=${f}.out

        if [ ! -d $outDir ]; then
            echo "making $outDir"
            mkdir $outDir
        else
            echo "$outDir already exists.."
        fi
        echo "#"
        echo "#cd into $outDir"
        echo "#"
        cd $outDir
        cleanup_script()
        {
            echo 'Error, cleaning up..'
            cd ..
            rm -rf $f.out 
        }
        #trap 'cleanup_script' ERR
        # turn -x on if DEBUG is set to a non-empty string
        [ -n "$DEBUG" ] && set -x

        echo 'data filter and pair ends assembly:'

        time(
        quality-trim-sepPairEnds.py $f
        echo 'separate pair-ends done..'

        flash ${fName}.1 ${fName}.2 -m 10 -M 120 -x 0.20 -p 33 -o $sample -r 140 -f 250 -s 25 -d $outDir 
        rm ${fName}.1 ${fName}.2
        sumFlashOut.py $sample $outDir > flashOut.sum
        echo 'merge by flash done..'

        cat ${sample}.extendedFrags.fastq ${sample}.notCombined_1.fastq ${sample}.notCombined_2.fastq > ${sample}.afterMerge.fastq
        rm ${sample}.extendedFrags.fastq ${sample}.notCombined_1.fastq ${sample}.notCombined_2.fastq
        echo 'combine assembled and unassembled done..'

        makeFastaForDNAHmmer.py ${sample}.afterMerge.fastq
        echo 'reverse complement added for hmmsearch..'
        )
        echo 'prefilter and combining pair ends done' >&2

        echo 'start hmmsearch'
        time hmmsearch --incE 10 --incdomE 10 -A ${sample}.afterMerge.SSU.sto -o ${sample}.afterMerge.SSU.hmmout --tblout ${sample}.afterMerge.SSU.hmmtblout --domtblout ${sample}.afterMerge.SSU.hmmdomtblout $SSUhmm ${sample}.afterMerge.fastq.RCaddedForHmmer
        echo 'hmmsearch done' >&2

        parseHMMgetSeq.py ${sample}.afterMerge.SSU.hmmdomtblout ${sample}.afterMerge.SSU.sto
        rm ${sample}.afterMerge.fastq ${sample}.afterMerge.fastq.RCaddedForHmmer
        echo 'hmm filter and MSA conversion done..'

        echo 'start mothur align'
        time mothur "#align.seqs(candidate=${sample}.afterMerge.SSU.fa, template=$SSUrefs, search=suffix, threshold=0.5, flip=t, processors=1)"
        mothurAlignReportParser.py  ${sample}.afterMerge.SSU.align.report  ${sample}.afterMerge.SSU.align

        #cat 16s_ecoli_J01695.afa  ${sample}.afterMerge.SSU.align.badSeqsFiltered > ${sample}.afterMerge.SSU.align.badSeqsFiltered.RFadded
        cat $ECOLI ${sample}.afterMerge.SSU.align.badSeqsFiltered > ${sample}.afterMerge.SSU.align.badSeqsFiltered.RFadded
        #
        # pay att to the ave read len: 75, 100 , 125; minLen are 2/3 of ave len;
        #
        tempLenCutOff=$((($END-$STA)*2/3))
        # get absolute number
        lenCutOff=$(echo $tempLenCutOff | nawk '{ print ($1 >= 0) ? $1 : 0 - $1}')
        regionCut.py ${sample}.afterMerge.SSU.align.badSeqsFiltered.RFadded $STA $END $lenCutOff
        mv ${sample}.afterMerge.SSU.align.badSeqsFiltered.RFadded.${STA}to${END}.cut.lenScreened.afa $sample
        echo 'ready for clustering ..'
        echo $fName processed ..
        echo "#"
        echo "#cd to current directory"
        cd -
        echo '-----------------------'
        echo
    done
    echo "$sampleDir processed.."
    )

else
    time(
    echo "$samplePath is a file"
    ff=$samplePath
    f=$(cd $(dirname $ff); pwd)/$(basename $ff)
    fName=$(basename $f)
    #sample=$(basename $f bz2)
    sample=${fName%%.*}

    outDir=${f}.out

    if [ ! -d ${outDir} ]; then
        echo "making $outDir"
        mkdir $outDir
    else
        echo "$outDir already exists.."
    fi
    cd $outDir
    cleanup_script()
    {
        echo 'Error, cleaning up..'
        cd ..
        rm -rf $f.out 
    }
    #trap 'cleanup_script' ERR
    # turn -x on if DEBUG is set to a non-empty string
    [ -n "$DEBUG" ] && set -x

    echo 'data filter and pair ends assembly:'
    time(
    quality-trim-sepPairEnds.py $f
    echo 'separate pair-ends done..'

    flash ${fName}.1 ${fName}.2 -m 10 -M 120 -x 0.20 -p 33 -o $sample -r 140 -f 250 -s 25 -d $outDir 
    rm ${fName}.1 ${fName}.2
    sumFlashOut.py $sample $outDir > flashOut.sum
    echo 'merge by flash done..'

    cat ${sample}.extendedFrags.fastq ${sample}.notCombined_1.fastq ${sample}.notCombined_2.fastq > ${sample}.afterMerge.fastq
    rm ${sample}.extendedFrags.fastq ${sample}.notCombined_1.fastq ${sample}.notCombined_2.fastq
    echo 'combine assembled and unassembled done..'

    makeFastaForDNAHmmer.py ${sample}.afterMerge.fastq
    echo 'reverse complement added for hmmsearch..'
    )
    echo 'prefilter and combining pair ends done' >&2


    echo 'start hmmsearch'
    time hmmsearch --incE 10 --incdomE 10 -A ${sample}.afterMerge.SSU.sto -o ${sample}.afterMerge.SSU.hmmout --tblout ${sample}.afterMerge.SSU.hmmtblout --domtblout ${sample}.afterMerge.SSU.hmmdomtblout $SSUhmm ${sample}.afterMerge.fastq.RCaddedForHmmer
    echo 'hmmsearch done' >&2

    parseHMMgetSeq.py ${sample}.afterMerge.SSU.hmmdomtblout ${sample}.afterMerge.SSU.sto
    rm ${sample}.afterMerge.fastq ${sample}.afterMerge.fastq.RCaddedForHmmer
    echo 'hmm filter and MSA conversion done..'

    echo 'start mothur align'
    time mothur "#align.seqs(candidate=${sample}.afterMerge.SSU.fa, template=$SSUrefs, search=suffix, threshold=0.5, flip=t, processors=1)"
    echo 'alignment done ..' >&2
    mothurAlignReportParser.py  ${sample}.afterMerge.SSU.align.report  ${sample}.afterMerge.SSU.align

    #cat 16s_ecoli_J01695.afa  ${sample}.afterMerge.SSU.align.badSeqsFiltered > ${sample}.afterMerge.SSU.align.badSeqsFiltered.RFadded
    cat $ECOLI ${sample}.afterMerge.SSU.align.badSeqsFiltered > ${sample}.afterMerge.SSU.align.badSeqsFiltered.RFadded
    #
    # pay att to the ave read len: 75, 100 , 125; minLen are 2/3 of ave len;
    #
    tempLenCutOff=$((($END-$STA)*2/3))
    # get absolute number
    lenCutOff=$(echo $tempLenCutOff | nawk '{ print ($1 >= 0) ? $1 : 0 - $1}')
    regionCut.py ${sample}.afterMerge.SSU.align.badSeqsFiltered.RFadded $STA $END $lenCutOff
    mv ${sample}.afterMerge.SSU.align.badSeqsFiltered.RFadded.${STA}to${END}.cut.lenScreened.afa $sample
    echo 'ready for clustering ..'
    echo $fName processed ..
    )
fi

echo 'pay att to the ave read len: 75, 100 , 125; minLen are 2/3 of ave len'
