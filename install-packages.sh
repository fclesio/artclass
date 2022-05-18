#!/bin/bash

# Basically this script is being used because it removes all the
# bloat of Ubuntu running everything in a single step.
# Reference: https://pythonspeed.com/articles/system-packages-docker/

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# Update the package listing, so we know what package exist:
apt-get update

# Install security updates:
apt-get -y upgrade

# Install a new package, without unnecessary recommended packages:
apt-get -y install --no-install-recommends nano \
  dumb-init \
  build-essential \
  gcc \
  libgmp3-dev \
  libpq-dev \
  git \
  htop

# Install all Python libraries
pip install --upgrade pip

pip --no-cache-dir install -r /app/requirements.txt

# Delete cached files we don't need anymore (note that if you're
# using official Docker images for Debian or Ubuntu, this happens
# automatically, you don't need to do it yourself):
apt-get clean

# Delete index files we don't need anymore:
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
