#!/bin/sh
set -e # stop on error
curl -O http://jon.luini.com/thelist/thelist.txt
git add thelist.txt
# do nothing if no modifications
# don't want the empty commits --allow-empty would create
if git diff-index --quiet HEAD; then
  echo "doing nothing because there are no changes"
else
  git commit -m "the list for $(env TZ="America/Los_Angeles" date -Iminute)"
fi
