#!/bin/sh

git reflog expire --all --expire-unreachable=now &&
git gc --aggressive --prune=now