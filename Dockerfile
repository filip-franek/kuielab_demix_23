FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu18.04

ENV DEBIAN_FRONTEND=noninteractive

COPY apt.txt /tmp/apt.txt
RUN apt -qq update && apt -qq install -y --no-install-recommends `cat /tmp/apt.txt` \
 && rm -rf /var/cache/*

ENV HOME_DIR=/root
WORKDIR ${HOME_DIR}
ENV CONDA_DIR ${HOME_DIR}/.conda

RUN wget -nv -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py38_22.11.1-1-Linux-x86_64.sh \
 && bash miniconda.sh -b -p ${CONDA_DIR} \
 && . ${CONDA_DIR}/etc/profile.d/conda.sh \
 && conda clean -y -a \
 && rm -rf miniconda.sh

ENV PATH ${CONDA_DIR}/bin:${PATH}

RUN conda install cmake -y && conda clean -y -a
COPY requirements.txt ${HOME_DIR}/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /app