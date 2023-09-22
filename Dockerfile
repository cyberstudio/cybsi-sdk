FROM python:3.8.12-alpine3.14

ARG PIP_INDEX_URL

# gcc is for regex package build (regex is black dependency), see https://github.com/psf/black/issues/1112
# libffi-dev is for poetry.
RUN apk add --no-cache gcc libc-dev make libffi-dev

RUN pip3 install poetry==1.1.12

WORKDIR /cybsi_sdk
ADD . /cybsi_sdk

RUN poetry install
