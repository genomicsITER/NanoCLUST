# NanoCLUST

**De novo clustering and consensus building for ONT 16S sequencing data**.

## Introduction

The pipeline is built using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. It comes with docker containers making installation trivial and results highly reproducible.

## Quick Start

i. Install [`nextflow`](https://nf-co.re/usage/installation) (min. version 20.07.1)

ii. Install [`docker`](https://docs.docker.com/engine/installation/) or [`conda`](https://conda.io/miniconda.html)

iii. Clone the NanoCLUST repository and test the pipeline on a minimal dataset with a single command and docker/conda profiles.

*Download a BLAST database in the NanoCLUST dir for cluster sequence classification. For NCBI 16S rRNA database:

```bash
mkdir db db/taxdb
wget https://ftp.ncbi.nlm.nih.gov/blast/db/16S_ribosomal_RNA.tar.gz && tar -xzvf 16S_ribosomal_RNA.tar.gz -C db
wget https://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz && tar -xzvf taxdb.tar.gz -C db/taxdb
```

Test execution with example dataset:
```bash
#Use either conda or docker profiles for dependency packages 
nextflow run main.nf -profile test,<conda/docker>
```

*MacOS users should use only the docker profile to ensure compatibility. Using conda profile in Mac downloads a Canu v1.5 env, while v2.0 is required by NanoCLUST and any lower version would crash the pipeline. Increase the Docker machine memory (value is 2GB by default) and cpus in the Docker Desktop settings to higher values depending on your machine specs (minimum 8-16GB recommended for testing purposes).

iv. Start running your own analysis!

Run a single sample analysis inside NanoCLUST dir using default parameters:

```bash
nextflow run main.nf \ 
             -profile docker \ 
             --reads 'sample.fastq' \ 
             --db "db/16S_ribosomal_RNA" \ 
             --tax "db/taxdb/"
```

See usage and output sections in the documentation (/docs) for all of the available options when running the pipeline.

## Computing requirements note
NanoCLUST has been tested on Ubuntu 16,18 and 20, CentOS 7 (docker and conda profiles) and Mac OS X 10.15 (only with docker profile).

Clustering step uses up to 32-36GB RAM when working with a real dataset analysis and default parameters (umap_set_size = 100000). Setting umap_set_size to 50000, will diminish memory consumption to 10-13GB RAM. When running the pipeline, kmer_freqs or mostly read_clustering processes could be terminated with status 137 when not enough RAM.

Nextflow automatically uses all available resources in your machine. More cpu threads enable the pipeline to compute and classify the different clusters at the same time and hence reduces the overall execution time.

Using the -with-trace option, it is possible to get an execution trace file which includes computing times and memory consumption metrics for all pipeline processes.

*The execution of the test profile (minimum testing dataset and default parameters) can be done with a regular 4 cores and 16GB RAM machine.

## Troubleshooting

- Errors may occur in read_correction step due to a small value for min_cluster_size that could generate poor quality clusters from your dataset. We recommend to set this parameter around 0.1%-1% of umap_set_size as minimum value and avoid small values for min_cluster_size (eg. values <100).

- Docker memory and cpu limitations should be checked in Mac OS since default memory limit (2GB) is not compatible with NanoCLUST


## Credits

Rodríguez-Pérez H, Ciuffreda L, Flores C (2020). NanoCLUST: a species-level analysis of 16S rRNA nanopore sequencing data. Submitted.

This work was supported by Instituto de Salud Carlos III [PI14/00844, PI17/00610, and FI18/00230] and co-financed by the European Regional Development Funds, “A way of making Europe” from the European Union; Ministerio de Ciencia e Innovación [RTC-2017-6471-1, AEI/FEDER, UE]; Cabildo Insular de Tenerife [CGIEU0000219140]; Fundación Canaria Instituto de Investigación Sanitaria de Canarias [PIFUN48/18]; and by the agreement with Instituto Tecnológico y de Energías Renovables (ITER) to strengthen scientific and technological education, training, research, development and innovation in Genomics, Personalized Medicine and Biotechnology [OA17/008]. 

## Acknowledgements

Thank you to Andreas Sjödin for his contributions and bugfixes regarding conda environments.

Thank you to NanoCLUST testers Adrían Muñoz, Eva Tosco, Luis Rubio, Víctor García and Alejandro Mendoza

## Contributions and Support

If you would like to contribute to this pipeline, please see the contributing guidelines
