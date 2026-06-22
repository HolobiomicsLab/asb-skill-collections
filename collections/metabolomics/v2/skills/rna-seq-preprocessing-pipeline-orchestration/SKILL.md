---
name: rna-seq-preprocessing-pipeline-orchestration
description: Use when when you have raw FASTQ files (from SRA or local storage) and need to produce normalized transcript quantification (quant.sf) files for a multi-sample RNA-seq cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3673
  tools:
  - SRA toolkit
  - trimgalore
  - Docker
  - Singularity
  - Nextflow DSL2
  - FastQC
  - Trimgalore
  - Salmon
  - nf-core/modules
  - nf-core/configs
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

# rna-seq-preprocessing-pipeline-orchestration

## Summary

Orchestrate a complete RNA-seq preprocessing workflow from raw FASTQ files through quality control, adapter trimming, and transcript quantification using containerized Nextflow DSL2 modules. This skill chains SRA retrieval, FastQC QC assessment, Trimgalore adapter removal, and Salmon quasi-mapping quantification to produce per-sample quant.sf files suitable for downstream differential expression analysis.

## When to use

When you have raw FASTQ files (from SRA or local storage) and need to produce normalized transcript quantification (quant.sf) files for a multi-sample RNA-seq cohort. Use this skill when the input data lacks quality control metrics, may contain adapter sequences, or when you require a reproducible, containerized end-to-end workflow that scales across compute infrastructures.

## When NOT to use

- Input data is already a quantification matrix or feature table (skip preprocessing and move directly to differential expression analysis).
- Raw reads are not in FASTQ format (e.g., BAM-only input; use alignment-to-quantification path instead).
- The workflow environment lacks containerization support (Docker or Singularity) and you cannot modify compute infrastructure permissions.

## Inputs

- Raw FASTQ files (gzipped or uncompressed, paired-end or single-end)
- SRA accession IDs (for remote download via SRA toolkit)
- Sample metadata CSV file with SRA accessions or FASTQ paths
- params.yml configuration file specifying output directory, sample sheet, and tool parameters

## Outputs

- Per-sample quant.sf files (transcript-level quantification with counts and TPM values) in $OUTDIR/salmon_genes/$sampleID/quant.sf
- FastQC HTML quality reports for raw FASTQ files
- Trimgalore trimming reports (adapter removal statistics)
- Aggregated feature matrix across all samples (transcript × sample)

## How to apply

Instantiate a Nextflow DSL2 workflow (version ≥21.10.3) that executes five sequential stages: (1) Retrieve or ingest FASTQ files via SRA toolkit or local directory import as specified in a params.yml configuration; (2) Run FastQC on raw FASTQ files to assess sequence quality, adapter content, and GC bias; (3) Trim adapters and low-quality bases using Trimgalore (which wraps Cutadapt) on all samples; (4) Quantify transcript abundances from trimmed FASTQ files using Salmon in quasi-mapping mode to generate quant.sf files containing transcript-level counts and TPM values in the directory structure $OUTDIR/salmon_genes/$sampleID/quant.sf; (5) Aggregate quantification results across all samples into a feature matrix. Execute each process within its own Docker or Singularity container to ensure reproducibility and portability across institutional compute clusters.

## Related tools

- **Nextflow DSL2** (Workflow orchestration engine that executes containerized processes across multiple compute infrastructures and manages task dependencies, resource allocation, and output aggregation.) — https://www.nextflow.io/docs/latest/dsl2.html
- **Docker** (Container runtime for packaging individual workflow processes (FastQC, Trimgalore, Salmon) with their dependencies to ensure reproducibility and portability.) — https://www.docker.com/
- **Singularity** (Alternative container runtime for HPC environments where Docker may not be available; provides same reproducibility benefits as Docker containers.) — https://sylabs.io/docs/
- **SRA toolkit** (Downloads FASTQ files from SRA accessions; executed as the first preprocessing stage to retrieve remote sequencing data.)
- **FastQC** (Quality control tool that assesses raw FASTQ sequence quality, adapter content, and GC bias; generates HTML reports informing trimming decisions.)
- **Trimgalore** (Adapter detection and removal tool (wraps Cutadapt) that trims sequencing adapters and low-quality bases from FASTQ files prior to quantification.)
- **Salmon** (Quasi-mapping quantification tool that generates transcript-level abundance estimates (counts and TPM) from trimmed FASTQ files into quant.sf output files.)
- **nf-core/modules** (Repository of Nextflow DSL2 modules (processes) for standardized, version-controlled implementation of each preprocessing step.) — https://github.com/nf-core/modules
- **nf-core/configs** (Repository of institutional compute environment configurations that define executor, resource allocation, and container backend settings for cluster submission.) — https://github.com/nf-core/configs

## Examples

```
nextflow run nf-core/rnaseq --reads 'data/*_R{1,2}.fastq.gz' --salmon_index salmon_index/ --outdir results/ -profile docker
```

## Evaluation signals

- All samples produce quant.sf files in the expected directory structure ($OUTDIR/salmon_genes/$sampleID/quant.sf) with non-zero transcript counts and TPM values.
- FastQC HTML reports are generated for all raw FASTQ files and show expected quality metrics (e.g., per-base quality ≥30 after trimming, adapter content detected).
- Trimgalore reports confirm adapter removal and base trimming occurred; compare raw vs. trimmed read counts to verify that ≥90% of reads are retained after trimming.
- Aggregated feature matrix rows (transcripts) and columns (samples) match expected sample count from input CSV and transcript reference annotation.
- Workflow execution log (Nextflow .nextflow/logs or trace file) shows all processes completed with exit code 0 and expected resource utilization within requested CPU/memory allocations.

## Limitations

- Pipeline does not handle mixed sequencing chemistries or long-read formats (PacBio, Oxford Nanopore); designed specifically for short-read Illumina-like FASTQ input.
- No built-in quality filtering step to exclude samples with extremely low mapping rates or contamination; downstream differential expression analysis must apply sample QC thresholds.
- SRA download stage requires internet connectivity; offline execution requires pre-downloaded FASTQ files staged in the local directory specified in params.yml.
- Salmon quantification in quasi-mapping mode does not produce alignment BAM files; if genome-level analysis or visual inspection of mapped reads is required, use alignment-based alternative (STAR or Hisat2) instead.

## Evidence

- [full_text] The genes workflow front-end processes raw sequencing data through four sequential stages: (1) SRA download and FASTQ conversion or local FASTQ input, (2) quality control using FASTQC, (3) adapter detection and removal with Trimgalore, and (4) quantification using salmon to produce quant.sf files: "The genes workflow front-end processes raw sequencing data through four sequential stages: (1) SRA download and FASTQ conversion or local FASTQ input, (2) quality control using FASTQC, (3) adapter"
- [full_text] Quantify transcript abundances from trimmed FASTQ files using Salmon in quasi-mapping mode, generating quant.sf output files containing transcript-level counts and TPM values.: "Quantify transcript abundances from trimmed FASTQ files using Salmon in quasi-mapping mode, generating quant.sf output files containing transcript-level counts and TPM values."
- [readme] The pipeline is built using Nextflow version 23.04.2.5870, a workflow tool to run tasks across multiple compute infrastructures. It uses Docker/Singularity containers making installation trivial and results highly reproducible.: "The pipeline is built using [Nextflow](https://www.nextflow.io) version 23.04.2.5870 (IMPORTANT), a workflow tool to run tasks across multiple compute infrastructures"
- [readme] The Nextflow DSL2 implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies.: "The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software"
- [full_text] Retrieve FASTQ files from SRA accessions using SRA toolkit or ingest user-provided FASTQ files from a specified directory as defined in the input CSV and params.yml configuration.: "Retrieve FASTQ files from SRA accessions using SRA toolkit or ingest user-provided FASTQ files from a specified directory as defined in the input CSV and params.yml configuration."
