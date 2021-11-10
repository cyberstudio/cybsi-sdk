FROM python:3.8.12-alpine3.14

WORKDIR /cybsi_sdk
ADD . /cybsi_sdk
# gcc is for regex package build (regex is black dependency), see https://github.com/psf/black/issues/1112
RUN apk add gcc libc-dev
RUN pip3 install -r requirements.txt
RUN pip3 install -r docs/requirements.txt
