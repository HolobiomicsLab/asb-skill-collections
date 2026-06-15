---
name: genome-alignment-and-contact-matrix-construction
description: Use when you have raw Hi-C FASTQ files from a kilobase-resolution Hi-C experiment and need to produce a processed Hi-C contact map (.hic file) for visualization, loop calling, or chromatin structure analysis. This is the entry point for any Hi-C dataset that has not yet been aligned and normalized.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0102
  tools:
  - Juicer
  - Juicer 1.6
  - Juicer 2
  - ENCODE Hi-C uniform processing pipeline
  - BWA (Burrows-Wheeler Aligner)
  - Juicer Tools
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

# genome-alignment-and-contact-matrix-construction

## Summary

Process raw Hi-C FASTQ sequencing data through read alignment, deduplication, and normalization to generate kilobase-resolution contact matrices in .hic format. This skill is essential when starting from FASTQ reads and needing to construct quantitative genome-wide interaction maps for downstream analysis.

## When to use

You have raw Hi-C FASTQ files from a kilobase-resolution Hi-C experiment and need to produce a processed Hi-C contact map (.hic file) for visualization, loop calling, or chromatin structure analysis. This is the entry point for any Hi-C dataset that has not yet been aligned and normalized.

## When NOT to use

- Input Hi-C data is already in .hic format or pre-processed contact matrix form — use downstream feature annotation tools instead.
- You have single-end Hi-C reads or non-standard pairing; Juicer is optimized for paired-end sequencing.
- Your restriction enzyme or genome is not supported without custom configuration of the pipeline.

## Inputs

- Raw Hi-C FASTQ files (paired-end sequencing reads)
- Reference genome FASTA file
- Chromosome sizes file (chrom.sizes)
- Restriction enzyme recognition site file

## Outputs

- .hic file (processed Hi-C contact map with normalized interactions)
- Intermediate alignment files (in aligned/ directory)
- Pipeline statistics and logs

## How to apply

Clone the Juicer repository (either stable Juicer 1.6 or development Juicer 2 depending on your requirements) and configure the pipeline with your reference genome, restriction enzyme recognition site, and computational resources (threads and memory allocation). Organize raw FASTQ files in a designated fastq/ subdirectory and run juicer.sh with appropriate flags (e.g., -g for genome ID, -y for restriction site file, -z for reference genome). The pipeline automatically handles read alignment via BWA, contact matrix construction, and normalization, producing a .hic output file. Verify success by confirming the .hic file is generated without errors and contains valid Hi-C contact data.

## Related tools

- **Juicer** (Primary pipeline for Hi-C FASTQ-to-.hic processing, including read alignment, contact matrix construction, and normalization) — https://github.com/aidenlab/juicer
- **Juicer 1.6** (Stable release version of Juicer for production Hi-C processing) — https://github.com/aidenlab/juicer/releases/tag/1.6
- **Juicer 2** (Development version of Juicer with active updates; clone directly from GitHub repository) — https://github.com/aidenlab/juicer
- **ENCODE Hi-C uniform processing pipeline** (Dockerized, cloud-ready implementation of Juicer-based Hi-C processing for AWS, Google Cloud, and local deployment) — https://github.com/ENCODE-DCC/hic-pipeline
- **BWA (Burrows-Wheeler Aligner)** (Performs read alignment of Hi-C FASTQ data to reference genome during pipeline execution) — http://bio-bwa.sourceforge.net/
- **Juicer Tools** (Command-line utilities for feature annotation and post-processing of .hic files after contact matrix construction) — https://github.com/theaidenlab/juicer/wiki/Download

## Examples

```
juicer.sh -g hg19 -d /path/to/work -y /path/to/restriction_sites.txt -z /path/to/hg19.fa
```

## Evaluation signals

- A valid .hic file is produced in the output directory without pipeline errors or crashes.
- The .hic file contains non-zero contact counts and can be opened and visualized in Juicebox or equivalent Hi-C browser.
- Pipeline statistics (merged_nodups file, alignment rates) show reasonable mapping efficiency (>50% expected for Hi-C).
- The contact matrix exhibits expected Hi-C topology: diagonal enrichment, distance-decay relationship, and compartmentalization patterns.
- Intermediate files (merged_sort, merged_nodups) progress through all pipeline stages (chimeric → merge → dedup → final) without truncation or data loss.

## Limitations

- Juicer requires significant computational resources (ideally ≥4 cores and ≥64 GB RAM; minimum 1 core and 16 GB RAM) and is optimized for cluster execution; single-CPU runs are supported but slow.
- AWS deployment scripts are deprecated; ENCODE's cloud-based pipeline is recommended for cloud environments.
- The pipeline requires manual configuration of restriction enzyme site files and reference genomes; unsupported genomes or enzymes need custom setup.
- CUDA support for HiCCUPS peak calling requires an NVIDIA GPU; CPU-only HiCCUPS is available but slower.
- Raw FASTQ file organization (must be in [topDir]/fastq/) and naming conventions must follow Juicer conventions or the pipeline will not auto-detect samples.

## Evidence

- [readme] Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files: "pipeline for generating Hi-C maps from fastq raw data files"
- [other] task_id=task_001 workflow step 4: "Execute the Juicer pipeline on the raw FASTQ files to perform read alignment, contact matrix construction, and normalization."
- [other] task_id=task_001 workflow step 5: "Verify that the pipeline completes successfully and produces a .hic output file containing the processed Hi-C contact map."
- [readme] README section Hardware and Software Requirements: "Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM)"
- [readme] README Quick Start section: "Run the Juicer pipeline on your cluster of choice with "juicer.sh [options]""
- [readme] README intro section: "If you clone the Juicer repo directly from Github, it will clone Juicer 2, which is under active development."
- [other] task_id=task_001 workflow step 3: "Configure the Juicer pipeline with appropriate parameters for the reference genome, restriction enzyme, and computational resources"
- [readme] README Cluster requirements: "Juicer currently works with the following resource management software: OpenLava, LSF, SLURM, GridEngine"
