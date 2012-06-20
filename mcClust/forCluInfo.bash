#! /usr/bin/env bash
# check seq number in files in dir

set -e

cd $1
for i in `ls`; do
    cnt=`grep '^>' -c $i`
    echo -e "$i\t$cnt"
done
