#!/bin/sh

docker build -t fclesio/artclass:0.1 .

docker run -it -p 8501:8501 -p 8888:8888 fclesio/artclass:0.1
