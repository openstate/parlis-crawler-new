#!/bin/sh

/usr/bin/awk '
BEGIN {
  FS="\t";
  FIELD_NAME="'$1'";
  print FIELD_NAME;
}

NR == 1 {
  for(i=0;i<=NF;i++){
    if ($(i)==FIELD_NAME) {
      FIELD_NUM=i;
    }
  }
}

NR > 1 {
  if (FIELD_NUM <= NF) {
    print $(FIELD_NUM);
  } else {
    print "NULL";
  }
}' $2