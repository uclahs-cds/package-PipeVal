FROM python:3.8-slim

MAINTAINER Gina Kim <ginakim@mednet.ucla.edu>

# ps and command for reporting metrics
RUN apt-get update && apt-get install -y \
        bzip2 \
        g++ \
        libbz2-dev \
        liblzma-dev \
        make \
        ncurses-dev \
        wget \
        zlib1g-dev \
        procps

# create samtools install dir
ENV SAMTOOLS_INSTALL_DIR=/opt/samtools

# install samtools
WORKDIR /tmp
RUN wget https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2 && \
  tar --bzip2 -xf samtools-1.9.tar.bz2

WORKDIR /tmp/samtools-1.9
RUN ./configure --enable-plugins --prefix=$SAMTOOLS_INSTALL_DIR && \
  make all all-htslib && \
  make install install-htslib

WORKDIR /
RUN ln -s $SAMTOOLS_INSTALL_DIR/bin/samtools /usr/bin/samtools && \
  rm -rf /tmp/samtools-1.9

# create directory for python script
RUN mkdir -p /tool/validate/

# install all requirements, including validate module
COPY requirements.txt /tool
COPY /validate/* /tool/validate/
WORKDIR /tool
RUN pip install -r requirements.txt

# add tool folder to path
ENV PYTHONPATH "${PYTHONPATH}:/tool/"