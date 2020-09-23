FROM python:3.8-slim

MAINTAINER Gina Kim <ginakim@mednet.ucla.edu>

# ps and command for reporting metrics
RUN apt-get update && apt-get install -y procps

# create directory for python script
RUN mkdir -p /tool/validate/

# install all requirements, including validate module
COPY requirements.txt /tool
COPY /validate/* /tool/validate/
WORKDIR /tool
RUN pip install -r requirements.txt

# add tool folder to path
ENV PYTHONPATH "${PYTHONPATH}:/tool/"