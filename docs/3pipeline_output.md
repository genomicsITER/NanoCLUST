# Pipeline output

This page describes the output produced by the pipeline.

## QC reports

### FastQC
[FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/) gives general quality metrics about your reads. It provides information about the quality score distribution across your reads and the per base sequence content (%T/A/G/C). You get information about adapter contamination and other overrepresented sequences.

For further reading and documentation see the [FastQC help](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/Help/).

> **NB:** The FastQC plots displayed in the MultiQC report shows _untrimmed_ reads. They may contain adapter sequence and potentially regions with low quality. To see how your reads look after trimming, look at the FastQC reports in the `trim_galore` directory.

**Output directory: `results/fastqc`**

* `sample_fastqc.html`
FastQC report, containing quality metrics for your untrimmed raw fastq files

* `zips/sample_fastqc.zip`
zip file containing the FastQC report, tab-delimited data file and plot images


### MultiQC
[MultiQC](http://multiqc.info) is a visualisation tool that generates a single HTML report summarising all samples in your project. Most of the pipeline QC results are visualised in the report and further statistics are available in the report data directory.

**Output directory: `results/multiqc`**

* `Project_multiqc_report.html`
MultiQC report - a standalone HTML file that can be viewed in your web browser
* `Project_multiqc_data/`
Directory containing parsed statistics from the different tools used in the pipeline

## NanoCLUST output

### UMAP and HDBSCAN steps
The pipeline uses UMAP technique to project sequence read data. The cluster assignment is performed by HDBSCAN. 

* `results/sample_name/output.hdbscan.tsv`
HDBSCAN raw output in TSV format. Contains the read IDs and assigned cluster

### Polished sequences extraction and classification
NanoCLUST builds a polished sequence from each cluster using Canu, Racon and Medaka. The sequence is then classified using blastn and a local database provided by the user. The polished sequence and the classification output table is included in the output:

* `results/sample_name/clusterX/draft_read.fasta`
Draft sequence extracted from the cluster

* `results/sample_name/clusterX/consensus_medaka.fasta`
Draft sequence extracted from the cluster

* `results/sample_name/clusterX/consensus_classification.csv`
Blast classification output 

### Additional plots
NanoCLUST generates the UMAP projection plot and stacked barplots for single and pooled samples at different taxonomic levels. The plot module uses the taxid included in the classification table and [Unipept Taxonomy API](http://api.unipept.ugent.be)

* `results/sample_name/hdbscan.output.png`
UMAP projection and HDBSCAN clustering plot.

* `results/rel_abundance_[FGS].png`
Relative abundance barplot at different taxonomic levels for samples processed by the pipeline. 