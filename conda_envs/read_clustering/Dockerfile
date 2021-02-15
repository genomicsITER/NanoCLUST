FROM continuumio/miniconda3
LABEL authors="Hector Rodriguez-Perez, Laura Ciuffreda" \
      description="Docker image containing all requirements for cluster_nanoclust pipeline"

COPY environment.yml /
RUN apt update && apt install -y procps build-essential
RUN conda env create -f environment.yml && conda clean -a
RUN chmod -R 777 /opt/conda/envs/read_clustering
ENV PATH /opt/conda/envs/read_clustering/bin:$PATH
