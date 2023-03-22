# syntax=docker/dockerfile:1
FROM rabbitmq:management
LABEL maintainer="soaring alano"
LABEL repository="cloudservice"

ENV HOME=/home/soaringalano

WORKDIR ${HOME}

# RUN apt update \
RUN  apt update \
     && apt install -y wget \
     && apt install -y unzip \
     && apt install -y git-all \
     && wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
     && wget -O stable-diffusion.zip https://codeload.github.com/CompVis/stable-diffusion/zip/refs/heads/main \
     && bash ./miniconda.sh -b -p ${HOME}/anaconda3 \
     && ln -s ${HOME}/anaconda3/bin/conda /usr/bin/conda \
     && ${HOME}/anaconda3/bin/conda init \
     && unzip stable-diffusion.zip \
     && cd stable-diffusion-main \
     && ${HOME}/anaconda3/bin/conda env create -f environment.yaml


COPY run_master.sh ${HOME}/stable-diffusion-main/

EXPOSE 80/tcp 15691/tcp 15692/tcp 25672/tcp 4369/tcp 5671/tcp 5672/tcp

CMD ["/bin/bash ${HOME}/stable-diffusion-main/run_master.sh"]


