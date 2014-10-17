cd forClu
for i in `ls`; do
    cnt=`grep '^>' -c $i`
    echo -e "$i\t$cnt"
done
