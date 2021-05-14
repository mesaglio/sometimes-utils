#!/bin/bash

DIR=#TO DEFINE
MY_PATH="`dirname \"$0\"`"
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"

for f in $(ls $DIR)
do
    echo "Moving to $f"
    cd $DIR/$f
    git branch -r | grep -v '\->' | while read remote; do git branch --track "${remote#origin/}" "$remote";done
    echo "Back ..."
    sleep 1
    cd $MY_PATH
done
echo "Done!"