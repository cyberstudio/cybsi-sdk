FROM docker-hub.ptsecurity.ru/python:3.8

WORKDIR /cybsi_sdk
ADD . /cybsi_sdk
RUN pip3 install -r requirements.txt
