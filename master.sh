#!/bin/sh
set -e # stop on error
# use or download https://github.com/ericchiang/pup, a command-line html parser
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
  # $1 = file name in the archive
  # $2 = actual date for contents of file
  curl -Sso thelist.txt http://jon.luini.com/thelist/archive/$1
  git add thelist.txt
  # skip this date if no modifications
  # don't want the empty commits --allow-empty would create
  if git diff-index --quiet HEAD; then
    echo "skipping $1 because there are no changes"
  else
    # fake the author and commit date
    export GIT_AUTHOR_DATE="$(env TZ="America/Los_Angeles" date -R -d "$2 23:55")"
    GIT_COMMITTER_DATE="$GIT_AUTHOR_DATE" git commit -m "the list for $1"
  fi
}

# most of the cases below are compensating for mislabeled files,
# to avoid overly-large commits from replaying history out of order
for date in $ALLDATES; do
  case $date in
    1995-06-30)
      do_date $date $date
      # 1995-07-07 is mislabeled as 1995-06-06
      do_date 1995-06-06 1995-07-07
      # 1995-07-14 is mislabeled as 1995-06-14
      do_date 1995-06-14 1995-07-14
      ;;
    1996-07-05)
      do_date $date $date
      # 1996-07-12 is mislabeled as 1996-70-12
      do_date 1996-70-12 1996-07-12
      ;;
    1998-12-30)
      do_date $date $date
      # 1999-01-01 and 1999-01-04 through 1999-01-07 are mislabeled as 1998
      do_date 1998-01-01 1999-01-01
      do_date 1998-01-04 1999-01-04
      do_date 1998-01-05 1999-01-05
      do_date 1998-01-06 1999-01-06
      do_date 1998-01-07 1999-01-07
      ;;
    2000-12-29)
      do_date $date $date
      # 2001-01-02 is mislabeled as 2000-01-02
      do_date 2000-01-02 2001-01-02
      ;;
    2000-10-05)
      do_date $date $date
      # 2000-10-06 is mislabeled as 2000-09-06
      do_date 2000-09-06 2000-10-06
      # 2000-10-09 is mislabeled as 2000-09-09
      do_date 2000-09-09 2000-10-09
      ;;
    2002-12-29)
      do_date $date $date
      # 2003-01-02 is mislabeled as 2002-01-02
      do_date 2002-01-02 2003-01-02
      ;;
    2002-09-28)
      do_date $date $date
      # 2002-10-02 is mislabeled as 2002-09-02
      do_date 2002-09-02 2002-10-02
      # 2002-10-03 is mislabeled as 2002-09-03
      do_date 2002-09-03 2002-10-03
      ;;
    2002-08-30)
      do_date $date $date
      # 2002-09-05 is mislabeled as 2002-09-30
      do_date 2002-09-30 2002-09-05
      ;;
    2004-12-31)
      do_date $date $date
      # 2005-01-01 through 2005-01-04 are mislabeled as 2004
      do_date 2004-01-01 2005-01-01
      do_date 2004-01-02 2005-01-02
      do_date 2004-01-03 2005-01-03
      do_date 2004-01-04 2005-01-04
      ;;
    2006-12-31)
      do_date $date $date
      # 2007-01-01 through 2007-01-03 are mislabeled as 2006
      do_date 2006-01-01 2007-01-01
      do_date 2006-01-02 2007-01-02
      do_date 2006-01-03 2007-01-03
      ;;
    2007-05-31)
      do_date $date $date
      # 2007-06-01 through 2007-06-11 are mislabeled as 2007-00
      do_date 2007-00-01 2007-06-01
      do_date 2007-00-03 2007-06-03
      do_date 2007-00-04 2007-06-04
      do_date 2007-00-05 2007-06-05
      do_date 2007-00-06 2007-06-06
      do_date 2007-00-07 2007-06-07
      do_date 2007-00-10 2007-06-10
      do_date 2007-00-11 2007-06-11
      ;;
    2012-12-31)
      do_date $date $date
      # 2013-01-01 and 2013-01-02 are mislabeled as 2012
      do_date 2012-01-01 2013-01-01
      do_date 2012-01-02 2013-01-02
      ;;
    2014-12-31)
      do_date $date $date
      # 2015-01-01 through 2015-01-04 are mislabeled as 2014
      do_date 2014-01-01 2015-01-01
      do_date 2014-01-02 2015-01-02
      do_date 2014-01-03 2015-01-03
      do_date 2014-01-04 2015-01-04
      ;;
    2015-10-31)
      do_date $date $date
      # with the following exceptions, most of November 2015
      # was overwritten with December data, so do these first
      do_date 2015-11-08 2015-11-08
      do_date 2015-11-12 2015-11-12
      do_date 2015-11-13 2015-11-13
      do_date 2015-11-14 2015-11-14
      do_date 2015-11-26 2015-11-26
      # then do 2015-12 data which is mislabeled as 2015-11
      for day in $(seq 1 7); do
        do_date 2015-11-0$day 2015-12-0$day
      done
      do_date 2015-11-09 2015-12-09
      do_date 2015-11-10 2015-12-10
      do_date 2015-11-11 2015-12-11
      do_date 2015-11-15 2015-12-15
      do_date 2015-11-16 2015-12-16
      do_date 2015-11-17 2015-12-17
      # no file for 2015-11-18
      for day in $(seq 19 25); do
        do_date 2015-11-$day 2015-12-$day
      done
      for day in $(seq 27 31); do
        do_date 2015-11-$day 2015-12-$day
      done
      ;;
    2017-12-31)
      do_date $date $date
      # 2018-01-01 through 2018-01-05 are mislabeled as 2017
      do_date 2017-01-01 2018-01-01
      do_date 2017-01-02 2018-01-02
      do_date 2017-01-03 2018-01-03
      do_date 2017-01-04 2018-01-04
      do_date 2017-01-05 2018-01-05
      ;;
    2019-01-31)
      do_date $date $date
      # 2019-02-01 is mislabeled as 2019-00-01
      do_date 2019-00-01 2019-02-01
      # 2019-02-02 is mislabeled as 2019-00-02
      do_date 2019-00-02 2019-02-02
      ;;
    1995-06-06 | 1995-06-14 | 1996-70-12 | 1998-01-01 | 1998-01-04 | 1998-01-05 | \
                 1998-01-06 | 1998-01-07 | 2000-01-02 | 2000-09-06 | 2000-09-09 | \
                 2002-01-02 | 2002-09-02 | 2002-09-03 | 2002-09-30 | 2004-01-01 | \
                 2004-01-02 | 2004-01-03 | 2004-01-04 | 2006-01-01 | 2006-01-02 | \
                 2006-01-03 | 2007-00-01 | 2007-00-03 | 2007-00-04 | 2007-00-05 | \
                 2007-00-06 | 2007-00-07 | 2007-00-10 | 2007-00-11 | 2012-01-01 | \
                 2012-01-02 | 2014-01-01 | 2014-01-02 | 2014-01-03 | 2014-01-04 | \
                 2015-11-*  | 2017-01-01 | 2017-01-02 | 2017-01-03 | 2017-01-04 | \
                 2017-01-05 | 2019-00-01 | 2019-00-02 | 2010-10-01 | 2011-03-14 | \
                 2016-07-09)
      # 2010-10-01 and 2011-03-14 and 2016-07-09 are empty files
      echo "skipping bad date $date";;
    *-*-*)
      do_date $date $date;;
    *)
      echo "skipping non-date $date";;
  esac
done
