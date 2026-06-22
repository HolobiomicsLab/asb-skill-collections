---
name: sra-data-retrieval-and-ingestion
description: Use when your analysis requires raw sequencing reads stored in NCBI SRA (identified by SRR, SRX, or SRP accessions) OR you have local FASTQ files organized in a directory structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3182
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0654
  tools:
  - SRA toolkit
  - trimgalore
  - Docker
  - Singularity
  - Nextflow
  - Docker/Singularity
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- Genes, miRNA, isoforms | SRA download | SRA toolkit
- Genes, miRNA, isoforms | Quality control | FastQC, trimgalore
- It uses Docker/Singularity containers making installation trivial and results highly reproducible.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiomicsintegrator_cq
    doi: 10.1093/bioadv/vbae175
    title: MultiOmicsIntegrator
  dedup_kept_from: coll_multiomicsintegrator_cq
schema_version: 0.2.0
---

# sra-data-retrieval-and-ingestion

## Summary

Retrieve raw sequencing data from NCBI SRA accessions using SRA toolkit or ingest user-provided FASTQ files from local directories as defined in input configuration. This is the entry point for RNA-seq and multi-omics preprocessing pipelines that convert archived or local sequence data into standardized FASTQ format for downstream quality control and quantification.

## When to use

Your analysis requires raw sequencing reads stored in NCBI SRA (identified by SRR, SRX, or SRP accessions) OR you have local FASTQ files organized in a directory structure. Use this skill at the start of any RNA-seq, small RNA, or isoform analysis workflow when you need to stage data from a CSV manifest or SRA IDs specified in params.yml before running FastQC quality assessment.

## When NOT to use

- Your input data is already trimmed, aligned, or in BAM/SAM format — skip directly to alignment or quantification.
- You have pre-computed quantification matrices (quant.sf, counts table) — use differential expression analysis instead.
- Your FASTQ files are corrupted or incomplete — validate file integrity before ingestion.

## Inputs

- SRA accession IDs (SRR/SRX/SRP format) via CSV manifest
- params.yml configuration file with SRA identifiers
- Local FASTQ files in user-specified directory
- Input manifest CSV with sample metadata and file paths

## Outputs

- FASTQ files in $OUTDIR/fastq directory structure
- FASTQ files organized by sample ID
- Staged raw sequencing reads ready for FastQC analysis

## How to apply

Provide either SRA accession numbers or local FASTQ file paths in an input CSV and configuration file (params.yml). If retrieving from SRA, invoke SRA toolkit to download and convert SRA archives to FASTQ format; if using local files, validate the directory structure matches the sample manifest. The workflow will output FASTQ files to a standardized staging directory ($OUTDIR/fastq or equivalent) where they are immediately available for downstream processing (FastQC, trimming, quantification). Success is verified by confirming FASTQ files exist, are non-empty, and contain valid sequence records in the expected output directory before proceeding to quality control.

## Related tools

- **SRA toolkit** (Download and convert SRA accessions to FASTQ format)
- **Nextflow** (Workflow orchestration for data retrieval and staging across compute infrastructures) — https://www.nextflow.io
- **Docker/Singularity** (Container execution of SRA toolkit and file staging processes for reproducibility) — https://github.com/nf-core/modules

## Evaluation signals

- FASTQ files exist in the expected output directory ($OUTDIR/fastq/$sampleID/) with correct sample naming convention.
- Each FASTQ file is non-empty and contains valid sequence records (starts with '@', contains sequence lines, '+' separator, and quality scores).
- File sizes and read counts match expectations from SRA metadata or the input manifest.
- No corrupted or truncated records; FASTQ format validation passes (all reads have 4 lines per record).
- Downstream FastQC can successfully read the FASTQ files without I/O errors.

## Limitations

- SRA accessions may have restricted access or be temporarily unavailable; network connectivity and SRA server status affect retrieval.
- Large SRA projects (high number of samples or read depth) require significant storage and bandwidth; consider filtering or subsetting before ingestion.
- Local FASTQ ingestion requires careful path specification and directory structure matching; inconsistent naming or missing files will cause workflow failure.
- The skill does not validate sequence quality, adapter content, or contamination — quality assessment occurs in the next workflow step (FastQC).

## Evidence

- [methods] Retrieve FASTQ files from SRA accessions using SRA toolkit or ingest user-provided FASTQ files from a specified directory as defined in the input CSV and params.yml configuration.: "Retrieve FASTQ files from SRA accessions using SRA toolkit or ingest user-provided FASTQ files from a specified directory as defined in the input CSV and params.yml configuration."
- [methods] SRA download and FASTQ conversion or local FASTQ input is the first sequential stage in the genes workflow preprocessing chain.: "(1) SRA download and FASTQ conversion or local FASTQ input, (2) quality control using FASTQC, (3) adapter detection and removal with Trimgalore, and (4) quantification using salmon to produce"
- [methods] The workflow outputs FASTQ files to a standardized directory structure organized by sample.: "quantification using salmon to produce quant.sf files in the directory structure $OUTDIR/salmon_genes/$sampleID/quant.sf."
- [readme] The pipeline uses Nextflow DSL2 with one container per process, making installation trivial and results highly reproducible through containerization.: "The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software"
