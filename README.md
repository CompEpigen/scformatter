# SCBridge
SCBridge uses singularity and snakemake workflow to handle interoperability between Seurat, SingleCellExperiment, and Scanpy anndata.

# Installation
## Prerequisites
* [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html)
* [singularity](https://sylabs.io/guides/3.5/user-guide/quick_start.html)

In ODCF clusters (e.g. worker01), singularity was installed. As for snakemake, you can use miniconda to install snakemake without root privilege.
* [miniconda](https://docs.conda.io/en/latest/miniconda.html)

## Create snakemake enviroment if using conda
```
cd scbridge
conda env create -f snakemake.yml
```

# Quick start
## Activate snakemake enviroment
```
source ~/.bashrc
conda activate snakemake
```

## Run SCBridge
```
python scbridge.py -h
```
Testing command:
```
python scbridge.py -t S3toH5AD -i test/input/ 
```
