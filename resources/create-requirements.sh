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

# Install shared python code from other private repo
# (Commented out just so you can run the demo)
#
#ACME_COMMON_VERSION=release/1.0
#$PIPINSTALL -e "git+ssh://git@github.com/acme/python-common.git@${ACME_COMMON_VERSION}#egg=acme_common&subdirectory=acme_common"

# NB: Even though boto3 is already installed by AWS,
# best practice is to explicitly ship all dependencies.
# https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
$PIPINSTALL boto3
$PIPINSTALL requests
$PIPINSTALL aws-xray-sdk
$PIPINSTALL aws_lambda_powertools

echo "# Generated by create-requirements.sh; DO NOT EDIT" > requirements.txt
echo "# Date: `date`" >> requirements.txt

# Workaround stupid ubuntu bug
pip3 freeze | grep -v pkg-resources==0.0.0 >> requirements.txt

# And another stupid pip freeze bug
sed -i 's/^-e //' requirements.txt

rm -rf $TMP_VIRTUALENV
