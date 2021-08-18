FROM python:3.8-buster

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update -y \
    && apt-get install -y python3-dev python3-pip build-essential \
    && apt-get install gcc -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt /requirements.txt

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

RUN mkdir -p /data_extraction
WORKDIR /data_extraction

RUN useradd -ms /bin/bash docker
USER docker
COPY --chown=docker:docker . /data_extraction

EXPOSE 8051
