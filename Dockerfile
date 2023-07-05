FROM ubuntu:latest

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y python3-pip sqlite3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /code/
