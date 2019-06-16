#!/bin/sh
set -e # stop on error
PUP=./pup
if pup --version > /dev/null 2>&1; then
  echo "using pup found on path at $(which pup)"
  PUP=pup
elif ! $PUP --version > /dev/null 2>&1; then
  # download locally if not found
  PUP_VERSION=v0.4.0
  # don't really care about running this on other platforms
  PUP_ZIPFILE=pup_${PUP_VERSION}_linux_amd64.zip
  curl -LO https://github.com/ericchiang/pup/releases/download/$PUP_VERSION/$PUP_ZIPFILE
  unzip $PUP_ZIPFILE
fi
ALLDATES=$(curl http://jon.luini.com/thelist/archive/ | $PUP 'a attr{href}')

do_date () {
  curl -Sso thelist.txt http://jon.luini.com/thelist/archive/$1
  git add thelist.txt
  # skip this date if no modifications
  # don't want the empty commits --allow-empty would create
  if git diff-index --quiet HEAD; then
    echo "skipping $1 because there are no changes"
  else
    git commit -m "the list for $1"
  fi
}

for date in $ALLDATES; do
  case $date in
    1995-06-30)
      do_date $date
      # 1995-07-07 is mislabeled as 1995-06-06
      do_date 1995-06-06;;
    1996-07-05)
      do_date $date
      # 1996-07-12 is mislabeled as 1996-70-12
      do_date 1996-70-12;;
    1995-06-06 | 1996-70-12 | 2010-10-01)
      # 2010-10-01 is an empty file
      echo "skipping bad date $date";;
    *-*-*)
      do_date $date;;
    *)
      echo "skipping bad date $date";;
  esac
done
