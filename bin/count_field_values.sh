#!/bin/sh
DIR=`dirname $0`
for j in *.tsv; do echo $j; echo "--------"; for i in `head -1 $j`; do NUM=`$DIR/list_field.sh $i $j |sort |uniq -c |wc -l |awk '{print $1}'`; echo "$i $NUM"; done; echo; done