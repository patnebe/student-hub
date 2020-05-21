FROM python:3.7-slim-buster

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc postgresql postgresql-contrib && \
    apt-get clean

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create working directory and copy files into it
RUN mkdir /student-hub
RUN mkdir /student-hub/src
COPY ./src /student-hub/src

# upgrade pip and install dependencies
WORKDIR /student-hub
RUN pip install --upgrade pip
RUN pip install -r src/requirements.txt

# create new user
RUN adduser --disabled-login fsndstudenthub
USER fsndstudenthub

# start gunicorn server
WORKDIR /student-hub
CMD gunicorn -b :$PORT src.run:app