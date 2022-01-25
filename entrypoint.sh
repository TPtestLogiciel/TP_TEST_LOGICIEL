#Les commandes comprises dans ce fichier seront executées lorsque le container sera run sur le runner !"
#!/bin/sh -l
#/bin/echo "Welcome !"


cd workflow/
find ./ -type f -name "test*.py" | xargs -n 1 python3

#ls

#find ./client/ -type f -name "test*.py" | xargs -n 1 python3
#find ./server/ -type f -name "test*.py" | xargs -n 1 python3
#find ./p2p/ -type f -name "test*.py" | xargs -n 1 python3

echo "Hello $1"
time=$(date)
echo "::set-output name=time::$time"

workflow_log=$(date)
echo "::set-output name=workflow_log::$workflow_log"

