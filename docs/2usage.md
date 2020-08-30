# Usage

## Introduction
Nextflow handles job submissions on SLURM or other environments, and supervises the run. Thus the Nextflow process must run until the pipeline is finished. We recommend that you put the process running in the background through `screen` / `tmux` or similar tool. Alternatively you can run Nextflow within a cluster job submitted your job scheduler.

It is recommended to limit the Nextflow Java virtual machines memory. We recommend adding the following line to your environment (typically in `~/.bashrc` or `~./bash_profile`):

```bash
NXF_OPTS='-Xms1g -Xmx4g'
```

<!-- TODO nf-core: Document required command line parameters to run the pipeline-->

## Running the pipeline
The typical command for running the pipeline is as follows:

```bash
nextflow run main.nf --reads 'data/mock_sample.fastq' --db 'db/blastdb' --tax 'db/taxdb' -profile <conda,docker>
```
This will launch the pipeline with the `conda` or `docker` configuration profiles. See below for more information about profiles.

*Database and taxdb should be downloaded in the NanoCLUST dir.

*--min_cluster_size and --polishing reads have default values to 50 and 100 respectively. We recommend to manually assign these when working with your own data to see how the pipeline output may change specially at low taxonomic levels such as species.

Note that the pipeline will create the following files in your working directory:

```bash
work            # Directory containing the nextflow working files
results         # Finished results (configurable, see below)
.nextflow_log   # Log file from Nextflow
# Other nextflow hidden files, eg. history of pipeline runs and old logs.
```

### Updating the pipeline
When you run the above command, Nextflow automatically pulls the pipeline code from GitHub and stores it as a cached version. When running the pipeline after this, it will always use the cached version if available - even if the pipeline has been updated since. To make sure that you're running the latest version of the pipeline, make sure that you regularly update the cached version of the pipeline:

```bash
nextflow pull nf-core/nanoclust
```

### Reproducibility
It's a good idea to specify a pipeline version when running the pipeline on your data. This ensures that a specific version of the pipeline code and software are used when you run your pipeline. If you keep using the same tag, you'll be running the same version of the pipeline, even if there have been changes to the code since.

First, go to the [nf-core/nanoclust releases page](https://github.com/nf-core/nanoclust/releases) and find the latest version number - numeric only (eg. `1.3.1`). Then specify this when running the pipeline with `-r` (one hyphen) - eg. `-r 1.3.1`.

This version number will be logged in reports when you run the pipeline, so that you'll know what you used when you look back in the future.


## Main arguments

#### `-profile`
Use this parameter to choose a configuration profile. Profiles can give configuration presets for different compute environments. Note that multiple profiles can be loaded, for example: `-profile docker` - the order of arguments is important!

If `-profile` is not specified at all, the pipeline will be run locally and expects all software to be installed and available on the `PATH`.

* `conda`
A generic configuration profile to be used with [conda](https://conda.io/docs/)
Pulls most software from [Bioconda](https://bioconda.github.io/)

* `docker`
A generic configuration profile to be used with [Docker](http://docker.com/)
Pulls software from dockerhub: [`nfcore/nanoclust`](http://hub.docker.com/r/nfcore/nanoclust/)

* `singularity`
A generic configuration profile to be used with [Singularity](http://singularity.lbl.gov/)
Pulls software from DockerHub: [`nfcore/nanoclust`](http://hub.docker.com/r/nfcore/nanoclust/)

* `test`
A profile with a complete configuration for automated testing
Includes links to test data so needs no other parameters

<!-- TODO nf-core: Document required command line parameters -->

#### `--reads`
Use this to specify the location of your input FastQ files. For example:

```bash
--reads 'sample.fastq'
```

Please note the following requirements:

1. The path must be enclosed in quotes
2. The path must have at least one `*` wildcard character

#### `--demultiplex`
If you have pooled data, you need to specify `--demultiplex` on the command line to enable initial demultiplex process of samples.

#### `--demultiplex_porechop`
Same as above but uses porechop software for demultiplexing.

```bash
--reads 'pooled_sample.fastq' --demultiplex[_porechop]
```

#### `--kit` (RAB204)
(Only with --demultiplex). Barcoding kit

Kits supported:
{Auto,PBC096,RBK004,NBD104/NBD114,PBK004/LWB001,RBK001,RAB204,VMK001,PBC001,NBD114,NBD103/NBD104,DUAL,RPB004/RLB001}

## UMAP and HDBSCAN configuration parameters

#### `--umap_set_size` (default 100000)
Number of reads that are used for the UMAP projection.

#### `--cluster_sel_epsilon` (0.5)
Minimum distance to separate a cluster from another. This parameter will depend on your input data and may have practical effect on the number of clusters generated. More information is available in [HDBSCAN parameter section](https://hdbscan.readthedocs.io/en/latest/parameter_selection.html).

#### `--min_cluster_size` (100)
Minimum number of reads necessary to call a cluster. Note that sensitivity decreases when this parameter is increased.

## Polishing parameters

#### `--polishing_reads` (100)
Numbers of reads used in the canu, racon and medaka polishing steps.

## Taxonomic and taxdb databases 

The pipeline uses blastn software for the classification of the polished sequence of each cluster. The following parameters allows database configuration:

#### `--db`
Path to the local blast database. Database files can be downloaded using FTP directly from [NCBI](ftp://ftp.ncbi.nlm.nih.gov/blast/db/)

For 16S rRNA database, download 16S_ribosomal_RNA.tar.gz, decompress the file under a db directory and specify the full path:
  * `--db "/path/to/nanoclust/db/16S_ribosomal_RNA"`

#### `--tax`
--db option will only output the tax ID for the target. For complete classification output, specify the taxdb path along with the local database. Taxdb database is also available from [NCBI databases](ftp://ftp.ncbi.nlm.nih.gov/blast/db/) (taxdb.tar.gz)


## Job resources
### Automatic resubmission
Each step in the pipeline has a default set of requirements for number of CPUs, memory and time. For most of the steps in the pipeline, if the job exits with an error code of `143` (exceeded requested resources) it will automatically resubmit with higher requests (2 x original, then 3 x original). If it still fails after three times then the pipeline is stopped.

## Other command line parameters

<!-- TODO nf-core: Describe any other command line flags here -->

#### `--min_read_length`
Minimum length of reads (bp) used in analysis.

#### `--max_read_length`
Maximum length of reads (bp) used in analysis.

#### `--outdir`
The output directory where the results will be saved.

#### `--email`
Set this parameter to your e-mail address to get a summary e-mail with details of the run sent to you when the workflow exits. If set in your user config file (`~/.nextflow/config`) then you don't need to specify this on the command line for every run.

#### `--email_on_fail`
This works exactly as with `--email`, except emails are only sent if the workflow is not successful.

#### `-name`
Name for the pipeline run. If not specified, Nextflow will automatically generate a random mnemonic.

This is used in the MultiQC report (if not default) and in the summary HTML / e-mail (always).

**NB:** Single hyphen (core Nextflow option)

#### `-resume`
Specify this when restarting a pipeline. Nextflow will used cached results from any pipeline steps where the inputs are the same, continuing the pipeline steps from there.

You can also supply a run name to resume a specific run: `-resume [run-name]`. Use the `nextflow log` command to show previous run names.

**NB:** Single hyphen (core Nextflow option)

#### `-c`
Specify the path to a specific config file (this is a core Nextflow command).

**NB:** Single hyphen (core Nextflow option)

Note - you can use this to override pipeline defaults.

#### `--custom_config_version`
Provide git commit id for custom Institutional configs hosted at `nf-core/configs`. This was implemented for reproducibility purposes. Default is set to `master`.

```bash
## Download and use config file with following git commid id
--custom_config_version d52db660777c4bf36546ddb188ec530c3ada1b96
```

#### `--custom_config_base`
If you're running offline, nextflow will not be able to fetch the institutional config files
from the internet. If you don't need them, then this is not a problem. If you do need them,
you should download the files from the repo and tell nextflow where to find them with the
`custom_config_base` option. For example:

```bash
## Download and unzip the config files
cd /path/to/my/configs
wget https://github.com/nf-core/configs/archive/master.zip
unzip master.zip

## Run the pipeline
cd /path/to/my/data
nextflow run /path/to/pipeline/ --custom_config_base /path/to/my/configs/configs-master/
```

> Note that the nf-core/tools helper package has a `download` command to download all required pipeline
> files + singularity containers + institutional configs in one go for you, to make this process easier.

#### `--max_memory`
Use to set a top-limit for the default memory requirement for each process.
Should be a string in the format integer-unit. eg. `--max_memory '8.GB'`

#### `--max_time`
Use to set a top-limit for the default time requirement for each process.
Should be a string in the format integer-unit. eg. `--max_time '2.h'`

#### `--max_cpus`
Use to set a top-limit for the default CPU requirement for each process.
Should be a string in the format integer-unit. eg. `--max_cpus 1`

#### `--plaintext_email`
Set to receive plain-text e-mails instead of HTML formatted.

#### `--monochrome_logs`
Set to disable colourful command line output and live life in monochrome.

#### `--multiqc_config`
Specify a path to a custom MultiQC configuration file.

