ARG MINIFORGE_VERSION=22.9.0-2
ARG UBUNTU_VERSION=20.04

FROM condaforge/mambaforge:${MINIFORGE_VERSION} AS builder

# Use conda to install tools and dependencies into /usr/local
ARG PYTHON_VERSION=3.10
ARG VCFTOOLS_VERSION=0.1.16
RUN mamba create -qy -p /usr/local \
    -c bioconda \
    -c conda-forge \
    python==${PYTHON_VERSION} \
    vcftools==${VCFTOOLS_VERSION} \
    perl-vcftools-vcf==${VCFTOOLS_VERSION} \
    tabix \
    pip

# Deploy the target tools into a base image
FROM ubuntu:${UBUNTU_VERSION} AS final
COPY --from=builder /usr/local /usr/local

# create directory for python script
RUN mkdir -p /tool/validate/

# install all requirements, including validate module
# COPY requirements.txt /tool
COPY setup.py /tool
COPY setup.cfg /tool
COPY pyproject.toml /tool
COPY /validate/ /tool/validate/
WORKDIR /tool
RUN pip install build && \
    pip install .

# add tool folder to path
ENV PYTHONPATH "${PYTHONPATH}:/tool/"

# Add a new user/group called bldocker
RUN groupadd -g 500001 bldocker && \
    useradd -r -u 500001 -g bldocker bldocker

# Change the default user to bldocker from root
USER bldocker

LABEL   maintainer="Arpi Beshlikyan <abeshlikyan@mednet.ucla.edu>" \
        org.opencontainers.image.source=https://github.com/uclahs-cds/public-tool-PipeVal
