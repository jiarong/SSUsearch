#!/usr/bin/env bash

### use absolute path
SSUsearch=~/Documents/software/gits/SSUsearch/ssusearch
Configfile=config.yaml

logdir=hpc-log
mkdir -p $logdir
src="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

SUB="sbatch --nodes=1 --cpus-per-task={threads} "
SUB="$SUB --time={cluster.time} --mem={cluster.mem}"
QSUB="$SUB --output $logdir/{cluster.name}.%j.o"

$SSUsearch --configfile $Configfile --unlock

$SSUsearch                               \
    --configfile $Configfile             \
    --cores 100                          \
    --local-cores 2                      \
    --cluster-config $src/cluster.yaml   \
    --js $src/jobscript.sh               \
    --latency-wait 120                   \
    --max-jobs-per-second 1              \
    --use-conda                          \
    --rerun-incomplete                   \
    --keep-going                         \
    --cluster \""$QSUB"\" $@             \
    |& tee $logdir/snakemake.log

