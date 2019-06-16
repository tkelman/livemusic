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
for date in $ALLDATES; do
  case $date in
    *-*-*)
      curl -Sso thelist.txt http://jon.luini.com/thelist/archive/$date
      git add thelist.txt
      # skip this date if no modifications
      # don't want the empty commits --allow-empty would create
      if git diff-index --quiet HEAD; then
        echo "skipping $date because there are no changes"
      else
        git commit -m "the list for $date"
      fi
      ;;
    *)
      echo "skipping bad date $date";;
  esac
done
