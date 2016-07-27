#!/bin/bash

set -o errexit

commit_msg=$(git log -1 --pretty=tformat:"publish %h: %s")
cd _pages
git add .
git commit -m "$commit_msg"
