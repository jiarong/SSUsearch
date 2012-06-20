#! /bin/bash
#usage: bash <thisFile><sampleDir><field>
# field is the field you want to be new name of file after split by '.'

set -e

cd $1
for f in `ls`; do
    ff=`echo "$f" | cut -f $2 -d \.`
    mv "$f" "$ff"
done
