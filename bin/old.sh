#!/bin/sh

PARLIS_CRAWLER_HOME=/home/breyten/parlis-crawler-new
PARLIS_HTDOCS_UPDATES=/mnt/projects/appsvoordemocratie/data/htdocs/updates
PARLIS_VIRTUAL_ENV=parlis_new

cd $PARLIS_CRAWLER_HOME
workon $PARLIS_VIRTUAL_ENV

FIRST="2008-01-01"
YESTERDAY=`date -d yesterday '+%Y-%m-%d'`

# Zaken
./bin/crawler.py -f $FIRST -t $YESTERDAY
# Stemmingen
./bin/crawler.py -e Stemmingen -f $FIRST -t $YESTERDAY
# Besluiten
./bin/crawler.py -e Besluiten -f $FIRST -t $YESTERDAY
# Documenten
./bin/crawler.py -e Documenten -f $FIRST -t $YESTERDAY
# Activiteiten
./bin/crawler.py -e Activiteiten -f $FIRST -t $YESTERDAY
# Reserveringen
./bin/crawler.py -e Reserveringen -f $FIRST -t $YESTERDAY

cd "$PARLIS_CRAWLER_HOME/output"
find . -name '*.zip' -exec mv \{\} $PARLIS_HTDOCS_UPDATES \;

cd -


