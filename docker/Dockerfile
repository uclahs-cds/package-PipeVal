FROM blcdsdockerregistry/bl-base:1.0.0 AS builder

# Use conda to install tools and dependencies into /usr/local
ARG SAMTOOLS_VERSION=1.11
ARG VCFTOOLS_VERSION=0.1.16
RUN conda create -qy -p /usr/local \
    -c bioconda \
    -c conda-forge \
    samtools==${SAMTOOLS_VERSION} \
    vcftools==${VCFTOOLS_VERSION} \
    perl-vcftools-vcf==${VCFTOOLS_VERSION} \
    tabix \
    pip

# Deploy the target tools into a base image
FROM ubuntu:20.04
COPY --from=builder /usr/local /usr/local

# create directory for python script
RUN mkdir -p /tool/validate/

# install all requirements, including validate module
COPY requirements.txt /tool
COPY /validate/ /tool/validate/
WORKDIR /tool
RUN pip install -r requirements.txt

# add tool folder to path
ENV PYTHONPATH "${PYTHONPATH}:/tool/"

LABEL maintainer="Arpi Beshlikyan <abeshlikyan@mednet.ucla.edu>"
