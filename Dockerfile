FROM python:3.8.7-slim-buster

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update -y && apt-get install -y \
    dumb-init \
    python3-dev \
    python3-pip \
    build-essential \
    gcc \
    apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


COPY requirements.txt /requirements.txt

RUN pip install -U pip \
    && pip install -r requirements.txt

RUN mkdir -p /src
WORKDIR /src

COPY /src /src

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["/bin/bash"]
