---
name: transcript-abundance-quantification-with-salmon
description: Use when you have adapter-trimmed FASTQ files and need to obtain transcript-level abundance estimates without performing full genomic alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0099
  tools:
  - SRA toolkit
  - trimgalore
  - Salmon
  - Docker
  - Singularity
  - Trimgalore
  - FastQC
  - Nextflow
  - nf-core/modules
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- Genes, miRNA, isoforms | SRA download | SRA toolkit
- Genes, miRNA, isoforms | Quality control | FastQC, trimgalore
- Genes, miRNA, isoforms | Align and Assembly | Salmon, samtools, STAR, Hisat2, StringTie2
- It then employs [salmon](../modules/nf-core/salmon) in order to obtain quantification files
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

# transcript-abundance-quantification-with-salmon

## Summary

Salmon quantifies transcript-level abundances from trimmed FASTQ files using quasi-mapping, producing transcript counts and TPM (transcripts per million) values in quant.sf format. This skill is essential for converting quality-controlled sequencing reads into normalized expression matrices suitable for downstream differential expression analysis.

## When to use

Apply this skill when you have adapter-trimmed FASTQ files and need to obtain transcript-level abundance estimates without performing full genomic alignment. Use Salmon when your goal is to quantify mRNA, miRNA, or isoform-level expression across multiple samples for differential expression or functional annotation workflows.

## When NOT to use

- Input FASTQ files have not been quality-trimmed or adapter-removed; run FastQC and Trimgalore first.
- Your goal is to perform splice-aware genomic alignment and variant calling; use STAR or HISAT2 instead.
- You already have a pre-computed feature matrix or transcript count table; Salmon quantification is redundant.

## Inputs

- trimmed FASTQ files (output from Trimgalore adapter removal)
- transcriptome reference index (built from FASTA sequences)
- sample metadata (SampleID, FASTQ file paths)

## Outputs

- quant.sf files (per-sample transcript quantification with counts and TPM)
- aggregated feature matrix (transcript-by-sample expression table)
- salmon quantification logs and statistics

## How to apply

Run Salmon in quasi-mapping mode on trimmed FASTQ files (output from Trimgalore) to generate per-sample quant.sf files containing transcript identifiers, counts, and TPM normalized values. Salmon performs lightweight pseudoalignment rather than full alignment, making it computationally efficient while preserving quantification accuracy. Execute Salmon within the Nextflow workflow using the nf-core/modules Salmon process, specifying the transcriptome reference index and sample-specific FASTQ inputs. Output quant.sf files are organized in the directory structure $OUTDIR/salmon_genes/$sampleID/quant.sf. Aggregate quantification results across all samples into a feature matrix for downstream statistical analysis. Validate quantification by checking that TPM values sum to approximately 1 million per sample and that transcript count distributions are reasonable for your biological context.

## Related tools

- **Salmon** (quasi-mapping-based transcript quantification producing counts and TPM values) — https://github.com/ASAGlab/MOI
- **Trimgalore** (upstream adapter trimming and quality filtering of FASTQ files before Salmon quantification) — https://github.com/ASAGlab/MOI
- **FastQC** (upstream quality control assessment of raw FASTQ files prior to trimming) — https://github.com/ASAGlab/MOI
- **Nextflow** (workflow orchestration and containerized execution of Salmon processes) — https://github.com/nf-core/modules
- **nf-core/modules** (standardized Nextflow module implementations of Salmon and related RNAseq tools) — https://github.com/nf-core/modules

## Evaluation signals

- All samples produce valid quant.sf files with non-zero transcript counts and TPM values summing to ~1,000,000 per sample.
- Per-sample quantification logs show successful quasi-mapping and bootstrapping (if used); no error messages or failed alignments.
- Aggregated feature matrix dimensions are [number_of_transcripts × number_of_samples] with no missing or NaN values in abundance columns.
- TPM distributions across samples show reasonable variance and no extreme outliers (e.g., single transcript >90% of total).
- Downstream differential expression analysis (DESeq2, edgeR) on Salmon counts produces biologically interpretable results with expected numbers of significant genes.

## Limitations

- Salmon requires a pre-built transcriptome reference index; index construction is not included in this skill—user must provide or build reference separately.
- Quasi-mapping does not provide alignment coordinates (BAM/SAM files) for downstream variant calling or splice-site validation.
- TPM normalization is sample-wise only; cross-sample comparisons require additional statistical normalization (e.g., TMM, quantile normalization) before differential expression testing.
- Salmon accuracy depends on transcriptome reference completeness and correctness; misannotated or missing transcripts will not be quantified.
- Paired-end and single-end reads require different Salmon parameters; incorrect library type specification can bias quantification.

## Evidence

- [methods] Salmon quasi-mapping mode produces quant.sf files: "Quantify transcript abundances from trimmed FASTQ files using Salmon in quasi-mapping mode, generating quant.sf output files containing transcript-level counts and TPM values."
- [methods] Output directory structure for Salmon results: "The genes workflow front-end processes raw sequencing data through four sequential stages: (1) SRA download and FASTQ conversion or local FASTQ input, (2) quality control using FASTQC, (3) adapter"
- [readme] Salmon integration in nf-core/modules and multiOmicsIntegrator: "Where possible, these processes have been submitted to and installed from nf-core/modules in order to make them available to all nf-core pipelines, and to everyone within the Nextflow"
- [methods] Salmon as part of RNAseq analysis workflow: "Genes, miRNA, isoforms | Align and Assembly | Salmon, samtools, STAR, Hisat2, StringTie2"
- [methods] Aggregation of quantification results: "Aggregate quantification results across all samples into a feature matrix for downstream analysis."
