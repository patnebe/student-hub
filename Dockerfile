FROM python:3.7-slim-buster

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc postgresql postgresql-contrib && \
    apt-get clean

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /student-hub

RUN mkdir /student-hub/src

COPY ./src /student-hub/src

WORKDIR /student-hub
RUN pip install --upgrade pip
RUN pip install -r src/requirements.txt


# WORKDIR /student-hub/src
# RUN rm -rf ./migrations
# RUN flask db init
# RUN flask db migrate -m "Initial databse migration"
# RUN flask db upgrade

RUN adduser --disabled-login fsndstudenthub
USER fsndstudenthub

WORKDIR /student-hub
CMD gunicorn -b :$PORT src.run:app