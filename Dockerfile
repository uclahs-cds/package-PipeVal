FROM continuumio/miniconda3:4.8.2

MAINTAINER Gina Kim <ginakim@mednet.ucla.edu>

COPY . /validate

WORKDIR /validate

RUN pip install -r requirements.txt