FROM python:3.6.12-slim-buster
RUN pip install --upgrade pip
RUN pip install requests
RUN mkdir /tmp/aos-python/
COPY . /tmp/aos-python/
RUN apt-get update
RUN apt-get install nano





