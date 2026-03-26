#!/bin/bash
# release.sh - Tag and package a new release
set -e

if [ -z "$1" ]; then
  echo "Usage: ./release.sh vX.Y.Z"
  exit 1
fi

git tag $1
zip -r python-unix-shell-$1.zip unix/
git push origin $1 