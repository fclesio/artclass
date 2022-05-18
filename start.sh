#!/bin/bash
set -euo pipefail

VERSION="latest"

docker build -t mlopsde/artclass:$VERSION . && \

docker push mlopsde/artclass:$VERSION  && \

docker run -it -p 8501:8501 -p 8888:8888 mlopsde/artclass:$VERSION
