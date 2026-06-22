---
name: fastq-quality-assessment-with-fastqc
description: Use when immediately after FASTQ file acquisition (whether from SRA download or local ingestion) and before any trimming or alignment steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3168
  - http://edamontology.org/topic_0080
  tools:
  - SRA toolkit
  - FastQC
  - trimgalore
  - Docker
  - Singularity
  - Trimgalore
  - Nextflow
  - Docker/Singularity
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- Genes, miRNA, isoforms | SRA download | SRA toolkit
- Genes, miRNA, isoforms | Quality control | FastQC, trimgalore
- It then performs quality control with [FASTQC](../modules/nf-core/fastqc)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae175
  all_source_dois:
  - 10.1093/bioadv/vbae175
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fastq-quality-assessment-with-fastqc

## Summary

FastQC performs rapid quality control assessment of raw FASTQ sequencing files to detect sequence quality issues, adapter contamination, and GC bias before downstream processing. This skill is essential for diagnosing data quality problems that may affect trimming, alignment, and quantification outcomes.

## When to use

Apply this skill immediately after FASTQ file acquisition (whether from SRA download or local ingestion) and before any trimming or alignment steps. Use it when you need to assess whether sequence quality, adapter content, or nucleotide composition will impact downstream analysis—particularly before committing to resource-intensive trimming or quantification workflows.

## When NOT to use

- Input FASTQ files have already been trimmed and quality-filtered by the sequencing provider.
- Analysis workflow explicitly prohibits pre-trimming QC (e.g., requires raw-only analysis).
- Computational resources are extremely limited and only summary statistics are available.

## Inputs

- raw FASTQ files (single-end or paired-end)
- sample metadata (SRA accession or file path)

## Outputs

- FastQC HTML quality report (per sample)
- FastQC text summary data (quality scores, adapter flags, GC content)
- sequence quality metrics (mean Phred score per position)

## How to apply

Run FastQC on raw FASTQ files as the second step in the RNAseq preprocessing chain, after SRA download or local FASTQ input but before adapter trimming. FastQC generates per-file quality reports assessing sequence quality scores, adapter content, and GC bias distributions. Examine the HTML/text outputs to identify problematic samples or lanes; samples with mean quality scores below 30 in the 3' tail or high adapter content flags warrant aggressive trimming parameters in downstream Trimgalore steps. The reports inform whether standard or stringent quality thresholds should be applied to subsequent processing stages.

## Related tools

- **FastQC** (Performs per-file quality assessment of raw FASTQ sequence quality, adapter content, and nucleotide composition)
- **Trimgalore** (Downstream tool that uses FastQC findings to decide trimming stringency and adapter removal thresholds)
- **Nextflow** (Workflow orchestration engine that parallelizes FastQC across multiple FASTQ files) — https://www.nextflow.io
- **Docker/Singularity** (Containerization enabling reproducible FastQC execution across compute environments)

## Evaluation signals

- FastQC report successfully generated for all input FASTQ files with no crashes or incomplete outputs.
- Per-position quality score distributions documented; median Phred score ≥30 across most of the read length indicates acceptable base quality.
- Adapter content flags present in report; if detected, confirms need for Trimgalore adapter removal in subsequent step.
- GC content distribution and bias metrics reported; extreme deviations (e.g., >60% GC or multimodal distribution) flagged for investigation.
- No missing or corrupted FASTQ records; sequence count matches input file headers.

## Limitations

- FastQC reports quality patterns but does not perform trimming; poor-quality reads still present in output and require downstream Trimgalore processing.
- GC bias and adapter detection are descriptive, not prescriptive—interpretation requires manual review or downstream tool integration (e.g., Trimgalore configuration) to act on findings.
- FastQC assumes standard Illumina FASTQ format; non-standard headers or encodings may produce incomplete or misleading reports.
- Per-base quality reporting becomes uninformative for very long reads (>500 bp) where position-level granularity may obscure local problems.

## Evidence

- [methods] Quality control and reporting: "Run FastQC on raw FASTQ files to assess sequence quality, adapter content, and GC bias."
- [methods] Preprocessing chain context: "Genes workflow front-end processes raw sequencing data through four sequential stages: (1) SRA download and FASTQ conversion or local FASTQ input, (2) quality control using FASTQC"
- [intro] Tool integration in pipeline: "The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software"
- [intro] Reproducibility mechanism: "It uses Docker/Singularity containers making installation trivial and results highly reproducible."
