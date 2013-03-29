#!/bin/sh

printf "%40s\torig\tuniq\tdiff\n" "file"
for i in *.tsv
do 
  orig_lines=`wc -l $i |awk '{print $1}'`
  now_lines=`cat $i |sort |uniq -c |wc -l |awk '{print $1}'`
  lines_diff=`expr $orig_lines - $now_lines`
  printf "%40s\t%d\t%d\t%d\n" $i $orig_lines $now_lines $lines_diff
done