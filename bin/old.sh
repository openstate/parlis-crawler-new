#!/bin/sh

PARLIS_CRAWLER_HOME=/home/breyten/parlis-crawler-new
PARLIS_HTDOCS_UPDATES=/mnt/projects/appsvoordemocratie/data/htdocs/updates
PARLIS_VIRTUAL_ENV=parlis_new

export WORKON_HOME=$HOME/.virtualenvs
source /usr/bin/virtualenvwrapper.sh

cd $PARLIS_CRAWLER_HOME
workon $PARLIS_VIRTUAL_ENV

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


