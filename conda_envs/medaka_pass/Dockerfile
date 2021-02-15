FROM continuumio/miniconda3
LABEL authors="Hector Rodriguez-Perez, Laura Ciuffreda" \
      description="Docker image containing all requirements for cluster_nanoclust pipeline"

COPY environment.yml /
RUN conda env create -f environment.yml && conda clean -a
RUN apt update && apt install -y procps
RUN chmod -R 777 /opt/conda/envs/medaka_pass
ENV PATH /opt/conda/envs/medaka_pass/bin:$PATH
