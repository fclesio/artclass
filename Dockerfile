FROM python:3.8.7-slim-buster

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1

COPY install-packages.sh /app/install-packages.sh
COPY requirements.txt /app/requirements.txt

RUN /app/install-packages.sh

RUN mkdir /app/src \
    && mkdir /app/models

COPY /src /app/src
COPY /models /app/models

WORKDIR /app

EXPOSE 8888
EXPOSE 8501

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

CMD ["/bin/bash"]
