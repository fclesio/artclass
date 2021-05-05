FROM python:3.6-buster

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update -y \
    && apt-get install -y python3-dev python3-pip build-essential \
    && apt-get install gcc -y \
    && apt-get clean

COPY requirements.txt /requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN mkdir -p /app
WORKDIR /app

COPY ./ /app

EXPOSE 8051

CMD ["streamlit", "run", "src/app/run.py" ]
