FROM python:3.8.12-alpine3.14

WORKDIR /cybsi_sdk
ADD . /cybsi_sdk
RUN pip3 install -r requirements.txt
RUN pip3 install -r docs/requirements.txt
