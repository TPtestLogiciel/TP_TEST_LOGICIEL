#!/bin/sh -l

echo "Hello $1"
time=$(date)
echo "::set-output name=time::$time"
myvar1=$(ls)
echo "::set-output name=myvar1::$myvar1"
myvar2=$(pwd)
echo "::set-output name=myvar2::$myvar2"

ls workflow/
cd workflow/
find ./ -type f -name "test*.py" | xargs -n 1 python3 || true

