---
name: hi-c-fastq-read-preprocessing
description: Use when you have raw Hi-C FASTQ files from a Hi-C wet-lab protocol and need to convert them into processed Hi-C contact maps (.hic files) for loop detection, TAD identification, or 3D structure inference. Use when starting from deposited public Hi-C datasets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0749
  tools:
  - Juicer
  - Juicer 1.6
  - Juicer 2
  - ENCODE Hi-C uniform processing pipeline
  - BWA (Burrows-Wheeler Aligner)
derived_from:
- doi: 10.1016/j.cels.2016.07.002
  title: juicer
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_juicer
    doi: 10.1016/j.cels.2016.07.002
    title: juicer
  dedup_kept_from: coll_juicer
schema_version: 0.2.0
---

# hi-c-fastq-read-preprocessing

## Summary

Preprocess raw Hi-C FASTQ files through the Juicer pipeline to generate normalized Hi-C contact maps at kilobase resolution. This skill transforms raw sequencing reads into structured Hi-C interaction matrices suitable for downstream 3D genomics analysis.

## When to use

Apply this skill when you have raw Hi-C FASTQ files from a Hi-C wet-lab protocol and need to convert them into processed Hi-C contact maps (.hic files) for loop detection, TAD identification, or 3D structure inference. Use when starting from deposited public Hi-C datasets (e.g., from GEO or SRA) or newly sequenced Hi-C libraries.

## When NOT to use

- Input FASTQ files are from non-Hi-C protocols (e.g., RNA-seq, ChIP-seq, single-cell RNA-seq) — use appropriate pipelines for those modalities.
- Contact matrices are already in processed .hic or matrix format — skip directly to feature annotation or downstream analysis tools.
- Restriction enzyme used is not pre-configured in Juicer — manual enzyme coordinate file creation may be required, which is outside standard preprocessing scope.

## Inputs

- Hi-C raw FASTQ files (paired-end sequencing reads)
- Reference genome FASTA file
- Restriction enzyme site coordinates file
- Chromosome sizes file (chrom.sizes)

## Outputs

- .hic contact map file (normalized Hi-C interaction matrix)
- Merged alignment file (merged_nodups)
- Pipeline statistics and QC metrics

## How to apply

Clone the Juicer repository (selecting either stable release 1.6 or development version Juicer 2 based on your requirements) and configure it with the appropriate reference genome, restriction enzyme used in the Hi-C protocol, and computational resources (thread count and memory allocation matching your cluster capabilities). Place raw FASTQ files in the designated input directory and execute the Juicer pipeline via juicer.sh with the selected genome ID and restriction site parameters. The pipeline performs sequential read alignment (via BWA), contact matrix construction, and normalization to produce a final .hic output file. Verify completion by checking that the .hic file was generated successfully and contains valid contact frequency data at the expected resolution.

## Related tools

- **Juicer** (Primary pipeline for Hi-C read alignment, contact matrix construction, and normalization from FASTQ to .hic output) — https://github.com/aidenlab/juicer
- **Juicer 1.6** (Stable release version of Juicer for production Hi-C preprocessing) — https://github.com/aidenlab/juicer/releases/tag/1.6
- **Juicer 2** (Development version of Juicer (under active development) available from main repository clone) — https://github.com/aidenlab/juicer
- **ENCODE Hi-C uniform processing pipeline** (Cloud-optimized containerized wrapper around Juicer for AWS/cloud deployment) — https://github.com/ENCODE-DCC/hic-pipeline
- **BWA (Burrows-Wheeler Aligner)** (Read alignment tool used within Juicer pipeline to map FASTQ reads to reference genome) — http://bio-bwa.sourceforge.net/

## Examples

```
juicer.sh -g hg19 -d /path/to/experiment -s HindIII -p /path/to/chrom.sizes -z /path/to/reference.fasta
```

## Evaluation signals

- A valid .hic file is produced in the output directory with non-zero file size and readable contact matrix data
- Pipeline completion log indicates successful passage through all stages (chimeric handling, merging, deduplication, final hic file generation)
- Contact map resolution matches the expected kilobase resolution (e.g., 5 kb, 10 kb) based on sequencing depth and restriction enzyme fragment size
- QC statistics show reasonable alignment rates and contact read counts consistent with input FASTQ sequencing depth
- Normalized contact frequency values are within expected range (avoiding extreme artifacts or zero matrices)

## Limitations

- Juicer requires cluster or cloud computing infrastructure with ≥4 cores and ≥64 GB RAM for efficient execution; single-CPU mode is available but substantially slower
- AWS scripts included in the repository are deprecated; ENCODE Hi-C pipeline is recommended for cloud deployment instead
- CUDA GPU support (for HiCCUPS peak calling in post-processing) requires NVIDIA hardware and compatible CUDA 7/7.5 libraries; CPU-based HiCCUPS is available as slower alternative
- Requires pre-configuration of restriction enzyme site coordinates and reference genome; non-standard genomes or enzymes need manual file generation
- No changelog is formally tracked in the repository, making it difficult to identify breaking changes between development versions

## Evidence

- [readme] Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files: "Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files"
- [other] Execute the Juicer pipeline on the raw FASTQ files to perform read alignment, contact matrix construction, and normalization.: "Execute the Juicer pipeline on the raw FASTQ files to perform read alignment, contact matrix construction, and normalization"
- [other] Clone the Juicer repository from aidenlab/juicer on GitHub and select either Juicer 1.6 (stable release) or Juicer 2 (development version) depending on deployment requirements.: "Clone the Juicer repository from aidenlab/juicer on GitHub and select either Juicer 1.6 (stable release) or Juicer 2 (development version) depending on deployment requirements"
- [other] Verify that the pipeline completes successfully and produces a .hic output file containing the processed Hi-C contact map.: "Verify that the pipeline completes successfully and produces a .hic output file containing the processed Hi-C contact map"
- [readme] Juicer is a pipeline optimized for parallel computation on a cluster. Juicer consists of two parts: the pipeline that creates Hi-C files from raw data, and the post-processing command line tools.: "Juicer is a pipeline optimized for parallel computation on a cluster. Juicer consists of two parts: the pipeline that creates Hi-C files from raw data"
- [readme] Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM): "Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM)"
- [readme] We recommend ENCODE's Hi-C processing pipeline, based on Juicer to run in the cloud; the AWS scripts are out of date.: "We recommend ENCODE's Hi-C processing pipeline, based on Juicer to run in the cloud; the AWS scripts are out of date"
