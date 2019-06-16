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
      do_date 1995-06-06
      # 1995-07-14 is mislabeled as 1995-06-14
      do_date 1995-06-14
      ;;
    1996-07-05)
      do_date $date
      # 1996-07-12 is mislabeled as 1996-70-12
      do_date 1996-70-12
      ;;
    1998-12-30)
      do_date $date
      # 1999-01-01 and 1999-01-04 through 1999-01-07 are mislabeled as 1998
      do_date 1998-01-01
      do_date 1998-01-04
      do_date 1998-01-05
      do_date 1998-01-06
      do_date 1998-01-07
      ;;
    2000-12-29)
      do_date $date
      # 2001-01-02 is mislabeled as 2000-01-02
      do_date 2000-01-02
      ;;
    2000-10-05)
      do_date $date
      # 2000-10-06 is mislabeled as 2000-09-06
      do_date 2000-09-06
      # 2000-10-09 is mislabeled as 2000-09-09
      do_date 2000-09-09
      ;;
    2002-12-29)
      do_date $date
      # 2003-01-02 is mislabeled as 2002-01-02
      do_date 2002-01-02
      ;;
    2002-09-28)
      do_date $date
      # 2002-10-02 is mislabeled as 2002-09-02
      do_date 2002-09-02
      # 2002-10-03 is mislabeled as 2002-09-03
      do_date 2002-09-03
      ;;
    2002-08-30)
      do_date $date
      # 2002-09-05 is mislabeled as 2002-09-30
      do_date 2002-09-30
      ;;
    2004-12-31)
      do_date $date
      # 2005-01-01 through 2005-01-04 are mislabeled as 2004
      do_date 2004-01-01
      do_date 2004-01-02
      do_date 2004-01-03
      do_date 2004-01-04
      ;;
    2006-12-31)
      do_date $date
      # 2007-01-01 through 2007-01-03 are mislabeled as 2006
      do_date 2006-01-01
      do_date 2006-01-02
      do_date 2006-01-03
      ;;
    2007-05-31)
      do_date $date
      # 2007-06-01 through 2007-06-11 are mislabeled as 2007-00
      do_date 2007-00-01
      do_date 2007-00-03
      do_date 2007-00-04
      do_date 2007-00-05
      do_date 2007-00-06
      do_date 2007-00-07
      do_date 2007-00-10
      do_date 2007-00-11
      ;;
    2012-12-31)
      do_date $date
      # 2013-01-01 is mislabeled as 2012-01-01
      do_date 2012-01-01
      ;;
    2014-12-31)
      do_date $date
      # 2015-01-01 through 2015-01-04 are mislabeled as 2014
      do_date 2014-01-01
      do_date 2014-01-02
      do_date 2014-01-03
      do_date 2014-01-04
      ;;
    2015-10-31)
      do_date $date
      # with the following exceptions, most of November 2015
      # was overwritten with December data, so do these first
      do_date 2015-11-08
      do_date 2015-11-12
      do_date 2015-11-13
      do_date 2015-11-14
      do_date 2015-11-26
      ;;
    2017-12-31)
      do_date $date
      # 2018-01-01 through 2018-01-05 are mislabeled as 2017
      do_date 2017-01-01
      do_date 2017-01-02
      do_date 2017-01-03
      do_date 2017-01-04
      do_date 2017-01-05
      ;;
    1995-06-06 | 1995-06-14 | 1996-70-12 | 1998-01-01 | 1998-01-04 | 1998-01-05 | \
                 1998-01-06 | 1998-01-07 | 2000-01-02 | 2000-09-06 | 2000-09-09 | \
                 2002-01-02 | 2002-09-02 | 2002-09-03 | 2002-09-30 | 2004-01-01 | \
                 2004-01-02 | 2004-01-03 | 2004-01-04 | 2006-01-01 | 2006-01-02 | \
                 2006-01-03 | 2007-00-01 | 2007-00-03 | 2007-00-04 | 2007-00-05 | \
                 2007-00-06 | 2007-00-07 | 2007-00-10 | 2007-00-11 | 2012-01-01 | \
                 2014-01-01 | 2014-01-02 | 2014-01-03 | 2014-01-04 | 2015-11-08 | \
                 2015-11-12 | 2015-11-13 | 2015-11-14 | 2015-11-26 | 2017-01-01 | \
                 2017-01-02 | 2017-01-03 | 2017-01-04 | 2017-01-05 | 2010-10-01)
      # 2010-10-01 is an empty file
      echo "skipping bad date $date";;
    *-*-*)
      do_date $date;;
    *)
      echo "skipping bad date $date";;
  esac
done
