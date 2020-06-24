#! /bin/bash

set -euxo pipefail

SNAPS=lemonde_snaps.txt
CRAWLS=lemonde_crawls.txt
PENDING=lemonde_pending.txt
DATA=../data/lemondefr-unes-elections2017-wa-html/
>$PENDING
touch $CRAWLS

comm -23 <(sort $SNAPS) <(sort $CRAWLS) > $PENDING

while read snap; do
  wget -N "http://web.archive.org/web/${snap}/http://www.lemonde.fr/" -O ${DATA}index_lemonde_${snap}.html && echo "$snap" >> $CRAWLS
done <$PENDING