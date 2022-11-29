# NanoCLUST

**De novo clustering and consensus building for ONT 16S sequencing data**.

## Introduction

The pipeline is built using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. It comes with docker containers making installation trivial and results highly reproducible.

## Quick Start

i. Install [`nextflow`](https://nf-co.re/usage/installation)

ii. Install [`docker`](https://docs.docker.com/engine/installation/) or [`conda`](https://conda.io/miniconda.html)

iii. Clone the NanoCLUST repository and test the pipeline on a minimal dataset with a single command and docker/conda profiles.

*Download a BLAST database in the NanoCLUST dir for cluster sequence classification. For NCBI 16S rRNA database:

```bash
mkdir db db/taxdb
wget https://ftp.ncbi.nlm.nih.gov/blast/db/16S_ribosomal_RNA.tar.gz && tar -xzvf 16S_ribosomal_RNA.tar.gz -C db
wget https://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz && tar -xzvf taxdb.tar.gz -C db/taxdb
```

```bash
#Using docker profile with container-based dependencies (recommended).
nextflow run main.nf -profile test,docker
```

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

Clustering step uses up to 32-36GB RAM when working with a real dataset analysis and default parameters (umap_set_size = 100000). Setting umap_set_size to 50000, will diminish memory consumption to 10-13GB RAM. When running the pipeline, kmer_freqs or mostly read_clustering processes could be terminated with status 137 when not enough RAM.

Nextflow automatically uses all available resources in your machine. More cpu threads enable the pipeline to compute and classify the different clusters at the same time and hence reduces the overall execution time.

Using the -with-trace option, it is possible to get an execution trace file which includes computing times and memory consumption metrics for all pipeline processes.

*The execution of the test profile (minimum testing dataset and default parameters) can be done with a regular 4 cores and 16GB RAM machine.

## Troubleshooting

- Using conda profile, some issues can arise due to unknown problems with the read_clustering and kmer_freq conda environments. If it is the case, we recommend using the docker profile to ensure all dependencies run in the right environments and these are tested and available in the cloud (automatically downloaded when using docker profile).

- In some machines, the read_clustering process exits with error status(_RuntimeError: cannot cache function '...'_). We have seen that this condition can be avoided running the pipeline with sudo privileges (even if Docker was previously available without sudo permissions). 

## Credits

Rodríguez-Pérez H, Ciuffreda L, Flores C. NanoCLUST: a species-level analysis of 16S rRNA nanopore sequencing data. Bioinformatics. 2021;37(11):1600-1601. doi:https://doi.org/10.1093/bioinformatics/btaa900

This work was supported by Instituto de Salud Carlos III [PI14/00844, PI17/00610, and FI18/00230] and co-financed by the European Regional Development Funds, “A way of making Europe” from the European Union; Ministerio de Ciencia e Innovación [RTC-2017-6471-1, AEI/FEDER, UE]; Cabildo Insular de Tenerife [CGIEU0000219140]; Fundación Canaria Instituto de Investigación Sanitaria de Canarias [PIFUN48/18]; and by the agreement with Instituto Tecnológico y de Energías Renovables (ITER) to strengthen scientific and technological education, training, research, development and innovation in Genomics, Personalized Medicine and Biotechnology [OA17/008]. 

## Contributions and Support

If you would like to contribute to this pipeline, please see the [contributing guidelines](.github/CONTRIBUTING.md).
