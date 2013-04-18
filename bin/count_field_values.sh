#!/bin/sh

for j in *.tsv; do echo $j; echo "--------"; for i in `head -1 $j`; do NUM=`./list_field.sh $i $j |sort |uniq -c |wc -l |awk '{print $1}'`; echo "$i $NUM"; done; echo; done