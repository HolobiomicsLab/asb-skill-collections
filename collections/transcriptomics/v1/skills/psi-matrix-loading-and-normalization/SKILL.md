---
name: psi-matrix-loading-and-normalization
description: Use when you have generated PSI matrices for alternative splicing events or transcripts across two or more biological conditions using SUPPA's psiPerEvent or psiPerIsoform subcommand, and you need to align and standardize these matrices with corresponding transcript expression quantification files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_3308
  tools:
  - SUPPA2
derived_from:
- doi: 10.1186/s13059-018-1417-1
  title: suppa2
evidence_spans:
- 'SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_suppa2
    doi: 10.1186/s13059-018-1417-1
    title: suppa2
  dedup_kept_from: coll_suppa2
schema_version: 0.2.0
---

# psi-matrix-loading-and-normalization

## Summary

Load PSI (percent-spliced-in) matrix files computed across multiple conditions and normalize transcript expression values to prepare for differential splicing analysis. This skill ensures consistent representation of splicing inclusion levels and expression quantification across samples before statistical comparison.

## When to use

You have generated PSI matrices for alternative splicing events or transcripts across two or more biological conditions using SUPPA's psiPerEvent or psiPerIsoform subcommand, and you need to align and standardize these matrices with corresponding transcript expression quantification files before computing differential splicing statistics (ΔPSIand p-values).

## When NOT to use

- PSI matrices have not yet been computed from transcript quantification data; use psiPerEvent or psiPerIsoform first.
- You are working with a single condition with no replicates; differential splicing analysis requires ≥2 replicates per condition.
- Expression data are already integrated into the PSI calculation (some tools compute PSI-normalized values that do not need separate expression input).

## Inputs

- PSI matrix files (.tsv or .txt) for each condition, with events/transcripts as rows and samples as columns
- Transcript expression quantification files (one per sample), containing transcript identifiers and abundance estimates (e.g., TPM, counts, or FPKM)
- Sample metadata mapping file (optional) linking sample names to conditions and replicates

## Outputs

- Aligned and normalized PSI matrices (one per condition) with consistent sample ordering
- Aligned and normalized expression matrices (one per condition) corresponding to the same samples
- Data quality report documenting missing values, outliers, and normalization parameters applied

## How to apply

First, load all PSI matrix files generated for each condition, verifying that rows correspond to event or transcript identifiers and columns to individual samples. Simultaneously load transcript expression quantification files (e.g., TPM or abundance estimates) for the same samples. Align samples across conditions by matching sample identifiers between PSI and expression files. If expression values exhibit large scale differences between conditions or datasets, apply normalization (e.g., quantile normalization or log-transformation) to stabilize variance and improve comparability. Verify that the number and order of samples are consistent across all matrices before passing them to the diffSplice subcommand, which will compute per-event ΔPSI and uncertainty-aware p-values using the aligned, normalized data as input.

## Related tools

- **SUPPA2** (Generates PSI matrices via psiPerEvent/psiPerIsoform and consumes aligned, normalized PSI and expression matrices in the diffSplice subcommand to compute differential splicing statistics) — https://github.com/comprna/SUPPA

## Evaluation signals

- All PSI matrix files load without errors; row and column counts match expected event/transcript and sample counts.
- Expression quantification files align with PSI matrices: every sample in the PSI matrix has a corresponding expression file with matching identifiers.
- After normalization, expression value distributions across conditions show similar statistical properties (e.g., comparable median and variance).
- No missing values (NaN) or infinite values remain in the aligned matrices; any NaN in PSI values are explicitly documented and handled per SUPPA protocol.
- Sample replicates within a condition cluster together in principal component space or correlation heatmaps, confirming successful alignment and normalization.

## Limitations

- PSI values are bounded between 0 and 1; extreme values near these bounds can reduce statistical power and may indicate low expression or ambiguous isoform assignment.
- Normalization choice (quantile, log, etc.) can influence downstream statistical inference; the README and paper do not prescribe a single normalization method, so sensitivity analysis is recommended.
- Expression-dependent uncertainty in PSI calculation means that samples with very low transcript expression may contribute high variance; filtering low-expression events before loading matrices may improve results.
- Cross-condition normalization (e.g., global quantile normalization) may mask true biological differences in splicing; condition-specific normalization may be more appropriate if conditions differ dramatically in overall expression profiles.

## Evidence

- [other] Load PSI matrix files for each condition and transcript expression quantification files.: "Load PSI matrix files for each condition and transcript expression quantification files."
- [other] Align samples across conditions and normalize expression values if needed.: "Align samples across conditions and normalize expression values if needed."
- [readme] SUPPA reads the ioe file generated in the previous step and a transcript expression file with the transcript abundances to calculate the PSI value for each of the events.: "SUPPA reads the ioe file generated in the previous step and a transcript expression file with the transcript abundances to calculate the PSI value for each of the events."
- [readme] Statistical significance is calculated by comparing the observed ΔPSI between conditions with the distribution of the ΔPSI between replicates as a function of the expression of the transcripts defining the events: "Statistical significance is calculated by comparing the observed ΔPSI between conditions with the distribution of the ΔPSI between replicates as a function of the expression of the transcripts"
- [intro] SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions: "SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions"
