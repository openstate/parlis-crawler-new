#!/bin/sh

PARLIS_CRAWLER_HOME=/home/breyten/parlis-crawler-new
PARLIS_HTDOCS_UPDATES=/home/breyten/parlis-crawler-new/updates

cd $PARLIS_CRAWLER_HOME
source .venv/bin/activate

# Zaken
./bin/crawler.py -A
# Stemmingen
./bin/crawler.py -e Stemmingen -A
# Besluiten
./bin/crawler.py -e Besluiten -A
# Documenten
./bin/crawler.py -e Documenten -A
# Activiteiten
# ./bin/crawler.py -e Activiteiten -f $FIRST -t $YESTERDAY
# Reserveringen
./bin/crawler.py -e Reserveringen -A

cd "$PARLIS_CRAWLER_HOME/output"
find . -name '*.zip' -exec mv \{\} $PARLIS_HTDOCS_UPDATES \;

cd -


