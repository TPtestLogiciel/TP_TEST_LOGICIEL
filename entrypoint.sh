#!/bin/sh -l

echo "Hello $1"
time=$(date)
echo "::set-output name=time::$time"
myvar1=$(ls)
echo "::set-output name=myvar1::$myvar1"
myvar2=$(pwd)
echo "::set-output name=myvar2::$myvar2"

python3 --version



#for d in */ ; do
#    cd $d
#    find ./ -type f -name "test*.py" | xargs -n 1 python3 || true
#done

#https://stackoverflow.com/questions/10446186/cd-into-directory-in-while-loop-doesnt-work/10446617

ls -1 | while read d
do 
    test -d "$d" || continue
    echo " "
    echo " "
    echo "dossier" $d ":"
    echo " "
    echo " "
    (cd $d ; find ./ -type f -name "test*.py" | xargs -n 1 python3 || true)
done



rm -rf ./*

