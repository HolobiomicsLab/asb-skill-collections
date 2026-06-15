---
name: hi-c-fastq-to-contact-map-pipeline
description: Use when you have raw Hi-C FASTQ files from a sequencing experiment and need to generate kilobase-resolution Hi-C contact maps conforming to ENCODE reference standards.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3182
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0654
  tools:
  - ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)
  - Juicer
  - Caper
  - BWA (Burrows-Wheeler Aligner)
  - Juicer Tools
derived_from:
- doi: 10.1016/j.cels.2016.07.002
  title: juicer
evidence_spans:
- ENCODE's Hi-C uniform processing pipeline based on Juicer can be found [here](https://github.com/ENCODE-DCC/hic-pipeline)
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

# hi-c-fastq-to-contact-map-pipeline

## Summary

A unified workflow for converting raw Hi-C sequencing reads (FASTQ format) into contact maps (.hic binary files) via alignment, deduplication, and contact matrix construction. This skill enables reproducible Hi-C data processing following ENCODE uniform processing standards using the Juicer platform.

## When to use

You have raw Hi-C FASTQ files from a sequencing experiment and need to generate kilobase-resolution Hi-C contact maps conforming to ENCODE reference standards. Use this when you need to validate pipeline reproducibility by comparing output checksums against reference outputs, or when integrating Hi-C processing into a larger genomic analysis workflow.

## When NOT to use

- Input is already a processed .hic or contact matrix file; use downstream analysis tools instead.
- FASTQ files are from non-Hi-C protocols (e.g. standard RNA-seq, WGS); this pipeline is specific to Hi-C.
- You require real-time or streaming processing; Juicer is designed for batch processing on clusters or cloud.

## Inputs

- Hi-C raw sequencing reads (FASTQ files, paired-end)
- genome reference sequence (FASTA)
- restriction site file (text, enzyme motifs)
- chromosome sizes file (chrom.sizes format)

## Outputs

- Hi-C contact map (.hic binary format)
- aligned and deduplicated read pairs (intermediate BAM/SAM files)
- pipeline statistics and QC metrics (text/JSON)
- output file checksum (MD5/SHA hash)

## How to apply

Clone the ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline) from ENCODE-DCC/hic-pipeline and configure Caper for your compute environment (local, cluster, or cloud). Prepare FASTQ input files in a designated directory and invoke the pipeline via `caper run hic.wdl` with a JSON configuration specifying genome ID, restriction enzyme site, and input paths. The pipeline performs read alignment via BWA, chimeric junction handling, deduplication, and contact matrix binning to produce a .hic binary file. Validate output correctness by computing file checksums (MD5 or SHA) and comparing against ENCODE reference checksums to confirm reproducibility.

## Related tools

- **Juicer** (Core pipeline for generating Hi-C maps from FASTQ and annotating Hi-C features; provides alignment, deduplication, and contact matrix construction) — https://github.com/aidenlab/juicer
- **ENCODE Hi-C uniform processing pipeline (encode_hic_pipeline)** (Production-ready WDL/Cromwell wrapper around Juicer; recommended for cloud and cluster execution with standardized outputs) — https://github.com/ENCODE-DCC/hic-pipeline
- **Caper** (Python workflow execution engine (wraps Cromwell); required to run ENCODE hic.wdl pipeline across different compute platforms) — https://github.com/ENCODE-DCC/caper
- **BWA (Burrows-Wheeler Aligner)** (Read alignment; aligns FASTQ sequences to reference genome within Juicer pipeline) — http://bio-bwa.sourceforge.net/
- **Juicer Tools** (Command-line toolset for contact map post-processing and feature annotation (e.g., HiCCUPS peak calling)) — https://github.com/aidenlab/juicer

## Examples

```
caper run hic.wdl -i tests/functional/json/test_hic.json --docker
```

## Evaluation signals

- Output .hic file exists and is in valid binary format; can be opened by Juicebox or Juicer Tools without errors.
- Computed MD5/SHA checksum of output .hic file matches ENCODE reference checksum exactly, confirming bit-for-bit reproducibility.
- Pipeline completion logs report successful stages: alignment → merge → deduplication → final contact matrix generation with no fatal errors.
- Quality metrics (e.g. percentage of valid pairs, duplication rate) fall within expected ranges for the organism and restriction enzyme used.
- Contact map resolution matches specified binning parameters (e.g. 5 kB, 10 kB bins); matrix dimensions match expected genome size for the specified reference.

## Limitations

- Juicer requires substantial computational resources (≥4 cores, ≥64 GB RAM recommended; minimum 1 core, 16 GB RAM); not suitable for resource-constrained environments.
- AWS scripts in the main aidenlab/juicer repository are deprecated; ENCODE-DCC/hic-pipeline is recommended for cloud execution.
- HiCCUPS peak calling requires an NVIDIA GPU and CUDA installation; CPU version available but slower. Native libraries compiled for CUDA 7/7.5; other versions require downloading new JCuda libraries.
- Pipeline currently supports SLURM and single-CPU execution as most up-to-date options; LSF, UGER, and OpenLava support may be outdated.
- Accuracy depends on correct specification of genome ID and restriction enzyme site; mismatched parameters will produce invalid contact maps.

## Evidence

- [readme] Juicer is a platform for analyzing kilobase resolution Hi-C data. In this distribution, we include the pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps.: "pipeline for generating Hi-C maps from fastq raw data files and command line tools for feature annotation on the Hi-C maps"
- [readme] ENCODE's Hi-C uniform processing pipeline based on Juicer can be found [here](https://github.com/ENCODE-DCC/hic-pipeline).: "ENCODE's Hi-C uniform processing pipeline based on Juicer can be found [here]"
- [other] The Juicer includes a pipeline for generating Hi-C maps from fastq raw data files, which forms the basis for ENCODE's Hi-C uniform processing pipeline.: "pipeline for generating Hi-C maps from fastq raw data files, which forms the basis for ENCODE's Hi-C uniform processing pipeline"
- [other] Run the encode_hic_pipeline wrapper on the FASTQ input files to generate aligned reads and construct the Hi-C contact map. Validate the output Hi-C map file format (e.g. .hic binary format) and compute checksum or file hash. Compare the computed checksum against the ENCODE reference output checksum to confirm pipeline reproducibility and correctness.: "Run the encode_hic_pipeline wrapper on the FASTQ input files to generate aligned reads and construct the Hi-C contact map...Compare the computed checksum against the ENCODE reference output checksum"
- [readme] Juicer requires the use of a cluster or the cloud, with ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM): "Juicer requires...ideally >= 4 cores (min 1 core) and >= 64 GB RAM (min 16 GB RAM)"
- [readme] The SLURM and CPU scripts are the most up to date. For cloud computing, we recommend the [ENCODE uniform processing pipeline based on Juicer](https://github.com/ENCODE-DCC/hic-pipeline): "The SLURM and CPU scripts are the most up to date. For cloud computing, we recommend the ENCODE uniform processing pipeline"
- [readme] Install [Caper](https://github.com/ENCODE-DCC/caper), requires `java` >= 1.8 and `python` >= 3.6, Caper >= 0.8.2.1 is required to run the pipeline. Caper is a Python wrapper for [Cromwell](https://github.com/broadinstitute/cromwell).: "Install Caper...Caper is a Python wrapper for Cromwell"
- [readme] You must have an NVIDIA GPU to install CUDA. ...The native libraries included with Juicer are compiled for CUDA 7 or CUDA 7.5.: "You must have an NVIDIA GPU to install CUDA...native libraries included with Juicer are compiled for CUDA 7 or CUDA 7.5"
