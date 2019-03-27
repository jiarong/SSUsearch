#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --mem=1G

### activate snakemake env if it is not available in current shell
#source activate snakemake

### use absolute path to avoid trouble
Workdir=.
SSUsearch=ssusearch
Configfile=config.yaml
Clust_config=hpc/slurm/cluster.yaml
Jobscript=hpc/slurm/jobscript.sh

cd $Workdir

logdir=hpc-log
mkdir -p $logdir

QSUB="sbatch --nodes=1 --cpus-per-task={threads}"
QSUB="$QSUB --time={cluster.time} --mem={cluster.mem}"
QSUB="$QSUB --output=$logdir/{cluster.name}.%j.o"

$SSUsearch --configfile config.yaml --unlock

$SSUsearch                                \
    --configfile $Configfile              \
    --cores 100                           \
    --local-cores 1                       \
    --cluster-config $Clust_config        \
    --js $Jobscript                       \
    --cluster \""$QSUB"\"                 \
    --use-conda                           \
    --latency-wait 120                    \
    --rerun-incomplete                    \
    |& tee $logdir/snakemake.log
