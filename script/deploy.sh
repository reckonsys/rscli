set -xeuo pipefail

BUMP_VERSION=$1
if [ "$BUMP_VERSION" = "" ]
then
    BUMP_VERSION="a"
fi

rscli bump -r $BUMP_VERSION

rm -rf dist/
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
