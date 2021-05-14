#!/bin/bash

DIR=#TO DEFINE
WORD=password #TO DEFINE
PRE=pass #TO DEFINE

for f in $(ls $DIR)
do
    python3 finder.py $DIR/$f $WORD | jq | tee results/$PRE_$f.json
done
echo "Done!"
