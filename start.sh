#!/bin/sh

docker build -t fclesio/capivara:0.1 . &&
docker run -p 8501:8501 fclesio/capivara:0.1