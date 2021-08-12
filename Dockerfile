# syntax=docker/dockerfile:1.2

FROM python:3.8.10-buster

RUN apt-get update && apt-get install -y build-essential awscli jq
RUN pip install --upgrade pip

WORKDIR /sewing

COPY . .
RUN pip install . 
