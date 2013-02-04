#!/bin/sh

PARLIS_CRAWLER_HOME=/home/breyten/parlis-crawler-new
PARLIS_HTDOCS_UPDATES=/mnt/projects/appsvoordemocratie/data/htdocs/updates
PARLIS_VIRTUAL_ENV=parlis_new

cd $PARLIS_CRAWLER_HOME
workon $PARLIS_VIRTUAL_ENV

YESTERDAY=`date -d yesterday '+%Y-%m-%d'`

# Zaken
./bin/crawler.py -f $YESTERDAY -t $YESTERDAY 2>&1 >$PARLIS_CRAWLER_HOME/daily.log
# Stemmingen
./bin/crawler.py -e Stemmingen -f $YESTERDAY -t $YESTERDAY 2>&1 >>$PARLIS_CRAWLER_HOME/daily.log
# Besluiten
./bin/crawler.py -e Besluiten -f $YESTERDAY -t $YESTERDAY 2>&1 >>$PARLIS_CRAWLER_HOME/daily.log
# Documenten
./bin/crawler.py -e Documenten -f $YESTERDAY -t $YESTERDAY 2>&1 >>$PARLIS_CRAWLER_HOME/daily.log
# Activiteiten
./bin/crawler.py -e Activiteiten -f $YESTERDAY -t $YESTERDAY 2>&1 >>$PARLIS_CRAWLER_HOME/daily.log
# Reserveringen
./bin/crawler.py -e Reserveringen -f $YESTERDAY -t $YESTERDAY 2>&1 >>$PARLIS_CRAWLER_HOME/daily.log

cd "$PARLIS_CRAWLER_HOME/output"
find . -name '*.zip' -exec mv \{\} $PARLIS_HTDOCS_UPDATES \;

cd -


