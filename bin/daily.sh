#!/bin/sh

PARLIS_CRAWLER_HOME=/home/breyten/parlis-crawler-new
PARLIS_HTDOCS_UPDATES=/mnt/projects/appsvoordemocratie/data/htdocs/updates
PARLIS_VIRTUAL_ENV=parlis_new

cd $PARLIS_CRAWLER_HOME
workon $PARLIS_VIRTUAL_ENV

# Zaken
./bin/crawler.py
# Stemmingen
./bin/crawler.py -e Stemmingen
# Besluiten
./bin/crawler.py -e Besluiten
# Documenten
./bin/crawler.py -e Documenten
# Activiteiten
./bin/crawler.py -e Activiteiten
# Reserveringen
./bin/crawler.py -e Reserveringen

cd "$PARLIS_CRAWLER_HOME/output"
find . -name '*.zip' -exec mv \{\} $PARLIS_HTDOCS_UPDATES \;

cd -


