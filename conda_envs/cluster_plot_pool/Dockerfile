FROM continuumio/miniconda3
LABEL authors="Hector Rodriguez-Perez, Laura Ciuffreda" \
      description="Docker image containing all requirements for cluster_nanoclust pipeline"

COPY environment.yml /
RUN conda env create -f environment.yml && conda clean -a
RUN apt update && apt install -y procps

ENV PATH /opt/conda/envs/cluster_plot_pool/bin:$PATH

