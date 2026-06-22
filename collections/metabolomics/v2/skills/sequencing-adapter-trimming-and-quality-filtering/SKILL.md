---
name: sequencing-adapter-trimming-and-quality-filtering
description: Use when after receiving raw FASTQ files from SRA or local sequencing input, and after FastQC has identified adapter content and quality issues.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3192
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3372
  tools:
  - SRA toolkit
  - trimgalore
  - Docker
  - Singularity
  - FastQC
  - Trimgalore
  - Cutadapt
  - Salmon
  - Nextflow
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae175
  all_source_dois:
  - 10.1093/bioadv/vbae175
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sequencing-adapter-trimming-and-quality-filtering

## Summary

Remove sequencing adapters and low-quality bases from raw FASTQ files using Trimgalore (which wraps Cutadapt) following quality assessment with FastQC. This preprocessing step prepares trimmed reads for downstream quantification tools like Salmon.

## When to use

After receiving raw FASTQ files from SRA or local sequencing input, and after FastQC has identified adapter content and quality issues. Apply this skill when adapter contamination or low-quality base calls are present in the QC report before proceeding to transcript quantification or alignment.

## When NOT to use

- Input FASTQ files have already been trimmed and quality-filtered by an upstream process.
- Downstream tool (e.g., pseudo-aligner) explicitly handles adapter removal internally.
- Analysis requires preservation of all original reads including low-quality bases (e.g., for specialized variant calling or error-rate studies).

## Inputs

- raw FASTQ files (paired-end or single-end)
- FastQC quality control report identifying adapter sequences and quality scores

## Outputs

- trimmed FASTQ files with adapters and low-quality bases removed
- trimming statistics and logs

## How to apply

Run FastQC on raw FASTQ files to assess sequence quality, adapter content, and GC bias. Examine the FastQC report to confirm the presence of adapters and quality issues. Apply Trimgalore, which wraps Cutadapt, to automatically detect and remove sequencing adapters and trim low-quality bases from the 3' end of reads. Trimgalore outputs cleaned FASTQ files suitable for downstream quantification. Verify trimming success by confirming adapter removal in post-trimming FastQC reports and checking that read length distributions are appropriate for your downstream tool (e.g., Salmon typically requires minimum read lengths of ~20–31 bp).

## Related tools

- **FastQC** (Quality control assessment to identify adapters, quality scores, GC bias, and other metrics before trimming)
- **Trimgalore** (Adapter detection and removal; wrapper around Cutadapt for automated trimming of adapters and low-quality bases)
- **Cutadapt** (Underlying tool invoked by Trimgalore to perform adapter clipping and quality trimming)
- **Salmon** (Downstream quantification tool that consumes trimmed FASTQ files to produce quant.sf files)
- **Nextflow** (Workflow orchestration engine to chain together FastQC, Trimgalore, and subsequent steps in automated pipelines) — https://www.nextflow.io

## Evaluation signals

- FastQC 'Per base sequence quality' plot shows quality scores remain above Q30 across the majority of read length after trimming.
- Adapter content in FastQC report drops to 0% or near-zero after Trimgalore application.
- Trimgalore output log confirms number of reads removed and average read length post-trimming.
- Downstream Salmon quantification completes successfully with trimmed FASTQ inputs, producing valid quant.sf files with non-zero transcript counts.
- Read length distribution post-trimming is suitable for the downstream tool (e.g., ≥20 bp for Salmon quasi-mapping).

## Limitations

- Trimgalore's adapter detection is pattern-based and may not identify novel or non-standard adapter sequences not in its built-in library.
- Aggressive trimming settings can remove short but valid reads, potentially reducing sensitivity for low-abundance transcripts.
- Trimming does not account for sample-specific quality issues (e.g., systematic errors in specific cycles) that may require specialized handling.
- Quality thresholds and minimum read length are fixed defaults; overly stringent settings may discard usable data.

## Evidence

- [intro] sequential_processing_steps: "quality control using FASTQC, (3) adapter detection and removal with Trimgalore, and (4) quantification using salmon to produce quant.sf files"
- [methods] workflow_detail: "Run FastQC on raw FASTQ files to assess sequence quality, adapter content, and GC bias. (3) Trim sequencing adapters and low-quality bases using Trimgalore, which wraps Cutadapt."
- [methods] tool_integration: "Quality control | FastQC, trimgalore"
- [methods] downstream_output: "Quantify transcript abundances from trimmed FASTQ files using Salmon in quasi-mapping mode, generating quant.sf output files"
