---
name: juicer-pipeline-configuration-and-execution
description: Use when you have raw Hi-C FASTQ files from a high-throughput chromatin conformation capture experiment and need to generate a normalized contact matrix (.hic file) for downstream genomic analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0092
  tools:
  - Juicer
  - Juicer 1.6
  - Juicer 2
  - ENCODE-DCC/hic-pipeline
  - BWA
  - Java Runtime Environment (≥1.8)
derived_from:
- doi: 10.1016/j.cels.2016.07.002
  title: juicer
evidence_spans:
- Juicer is a platform for analyzing kilobase resolution Hi-C data
- To access Juicer 1.6 (last stable release)
- If you clone the Juicer repo directly from Github, it will clone Juicer 2, which is under active development
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

# juicer-pipeline-configuration-and-execution

## Summary

Configure and execute the Juicer pipeline to transform raw Hi-C FASTQ data into processed Hi-C contact maps (.hic files) through read alignment, contact matrix construction, and normalization. This skill is essential for generating kilobase-resolution Hi-C datasets from sequencing output.

## When to use

You have raw Hi-C FASTQ files from a high-throughput chromatin conformation capture experiment and need to generate a normalized contact matrix (.hic file) for downstream genomic analysis. Use this skill when starting from FASTQ-format sequencing reads rather than pre-aligned BAM or existing contact matrices.

## When NOT to use

- Input data is already in .hic format or pre-processed contact matrix form — use Juicer Tools for post-processing instead
- You have only single-end sequencing reads — Juicer requires paired-end Hi-C reads
- Your restriction enzyme is not pre-configured in the pipeline and you lack the ability to define custom restriction site coordinates

## Inputs

- Hi-C FASTQ files (paired-end sequencing reads)
- Reference genome sequence (FASTA)
- Restriction enzyme site file (e.g., HindIII or MboI coordinates)
- Chromosome sizes file (.chrom.sizes)

## Outputs

- .hic file (processed Hi-C contact map with normalized contacts)
- merged_nodups file (deduplicated alignments)
- Pipeline statistics and QC metrics

## How to apply

Clone either Juicer 1.6 (stable) or Juicer 2 (development) from the aidenlab/juicer GitHub repository based on your deployment requirements. Obtain Hi-C FASTQ data from public repositories (GEO, SRA) or your own sequencing experiment. Configure the pipeline by specifying the reference genome ID (e.g., 'hg19', 'mm10'), restriction enzyme site (e.g., 'HindIII', 'MboI'), and computational resources (thread count, memory allocation ≥64 GB RAM recommended for cluster, minimum 16 GB). Select the appropriate execution environment script (SLURM or CPU recommended as most up-to-date; AWS, LSF, and UGER are deprecated). Execute juicer.sh with your parameters, which orchestrates read alignment via BWA, chimeric read handling, duplicate removal, and contact matrix normalization. Monitor completion and verify that a .hic output file is generated in the aligned directory.

## Related tools

- **Juicer 1.6** (Stable pipeline version for Hi-C FASTQ-to-contact-map processing) — https://github.com/aidenlab/juicer/releases/tag/1.6
- **Juicer 2** (Development version with active updates for Hi-C pipeline execution) — https://github.com/aidenlab/juicer
- **ENCODE-DCC/hic-pipeline** (Cloud-ready dockerized wrapper around Juicer for scalable Hi-C processing) — https://github.com/ENCODE-DCC/hic-pipeline
- **BWA** (Burrows-Wheeler aligner used internally by Juicer for read alignment) — http://bio-bwa.sourceforge.net/
- **Java Runtime Environment (≥1.8)** (Minimum software requirement for running Juicer tools) — https://www.java.com/download

## Examples

```
juicer.sh -g hg19 -d /path/to/topDir -q short -l long -s HindIII -z /path/to/hg19.fasta -p /path/to/chrom.sizes
```

## Evaluation signals

- Pipeline completes without errors and produces a non-empty .hic output file in the aligned directory
- .hic file contains valid contact matrix data readable by Juicer Tools and downstream analysis software
- Merged and deduplicated read counts in merged_nodups align with input FASTQ file sizes and expected library complexity
- Quality control statistics (duplication rate, unique read percentage, contact distribution) fall within expected ranges for Hi-C libraries
- Generated contact map shows expected diagonal strength and off-diagonal decay characteristic of Hi-C normalized matrices

## Limitations

- Juicer requires ≥4 cores and ≥64 GB RAM (minimum 1 core and 16 GB RAM) for optimal performance; single-CPU execution is slower
- AWS deployment scripts are deprecated; cloud users should use ENCODE-DCC/hic-pipeline instead
- CUDA and dedicated GPU are required for HiCCUPS peak calling; CPU-based alternative is available but slower
- Pre-configured genomes and restriction enzymes must be specified; custom genomes require manual definition of restriction site coordinates
- Pipeline assumes paired-end sequencing; single-end reads will not be processed correctly

## Evidence

- [other] Juicer includes a pipeline that generates Hi-C maps from fastq raw data files as input, producing processed Hi-C map artifacts.: "Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files"
- [readme] Configuration requires selection of Juicer version, reference genome, restriction enzyme, and computational resources.: "Configure the Juicer pipeline with appropriate parameters for the reference genome, restriction enzyme, and computational resources (number of threads, memory allocation)"
- [readme] Juicer 1.6 is the last stable release; main repository is focused on Juicer 2.0 under active development.: "To access Juicer 1.6 (last stable release), please see [the Github Release]. If you clone the Juicer repo directly from Github, it will clone Juicer 2, which is under active development"
- [other] Pipeline execution performs read alignment, contact matrix construction, and normalization.: "Execute the Juicer pipeline on the raw FASTQ files to perform read alignment, contact matrix construction, and normalization"
- [readme] Cluster infrastructure and resource management are required; SLURM and CPU scripts are most current.: "Juicer is a pipeline optimized for parallel computation on a cluster. The SLURM and CPU scripts are the most up to date"
- [readme] Cloud deployment should use ENCODE's Hi-C pipeline; AWS scripts in Juicer are out of date.: "We recommend [ENCODE's Hi-C processing pipeline, based on Juicer] to run in the cloud; the AWS scripts are out of date"
- [other] Verification of successful pipeline completion requires checking for .hic output file.: "Verify that the pipeline completes successfully and produces a .hic output file containing the processed Hi-C contact map"
