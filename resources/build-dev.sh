#!/bin/sh

# Generate requirements.txt (pinned versions of dependencies, including transitive dependencies)
# Explanation: https://www.kennethreitz.org/essays/a-better-pip-workflow

set -e
cd `dirname $0`

TMP_VIRTUALENV=`mktemp -d`
PIPINSTALL="pip3 --no-cache-dir install"

# NB: May need to run apt-get install python3-venv
python3 -m venv $TMP_VIRTUALENV
. $TMP_VIRTUALENV/bin/activate

$PIPINSTALL -r requirements.txt

echo "Now Run: . ${TMP_VIRTUALENV/bin/activate" 


