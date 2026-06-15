---
name: quality-control-interval-detection
description: Use when when you have Sciex Multiquant TXT export files containing injection sequences from metabolomics or lipidomics studies where pooled QC samples were deliberately injected at regular intervals to monitor analytical quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - ricoderks/QComics
  - Sciex Multiquant
  - QComics
derived_from:
- doi: 10.1021/acs.analchem.3c03660
  title: QComics
evidence_spans:
- codecov.io/gh/ricoderks/QComics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcomics
    doi: 10.1021/acs.analchem.3c03660
    title: QComics
  dedup_kept_from: coll_qcomics
schema_version: 0.2.0
---

# quality-control-interval-detection

## Summary

Identifies and validates regular injection intervals of pooled QC samples (QCpool) within metabolomics or lipidomics analytical sequences exported from Sciex Multiquant. This skill ensures quality control samples are distributed at expected intervals across one or more measurement runs for quality assessment.

## When to use

When you have Sciex Multiquant TXT export files containing injection sequences from metabolomics or lipidomics studies where pooled QC samples were deliberately injected at regular intervals to monitor analytical quality. Use this skill if you need to verify that QC pool samples were actually measured at the designed intervals and to extract their positions for downstream quality assessment.

## When NOT to use

- When QC samples are not pooled or were not measured at regular intervals by design
- When the input is already a pre-filtered feature table or peak intensity matrix—this skill operates on raw sequence metadata, not processed analytical data
- When Sciex Multiquant software version is < 3.0.3, as required format compatibility cannot be guaranteed

## Inputs

- Sciex Multiquant TXT export file
- Injection sequence metadata
- Expected QCpool interval specification (e.g., number of injections between QCpool measurements)

## Outputs

- Structured table of detected QCpool samples with columns: sample name, injection index, sequence ID, interval position
- Validation report indicating whether QCpool intervals match expected regularity
- Quality assessment summary for metabolomics/lipidomics study

## How to apply

Load the Sciex Multiquant TXT export file and parse the sample metadata and injection sequence information. Scan through the injection sequence to identify all samples marked as QCpool or quality control pool samples, recording their injection index, position within the sequence, and sequence identifier. Validate that detected QCpool samples occur at regular intervals consistent with the study design—this may involve computing differences between successive QCpool injection indices and confirming they match the expected interval (e.g., every 10th injection). Compile results into a structured table with columns for sample name, injection index, sequence ID, and interval position. Flag any deviations from regularity for manual review.

## Related tools

- **Sciex Multiquant** (Instrument software that analyzes pooled QC samples and exports injection sequence to TXT format for interval detection)
- **QComics** (R/Python package that processes Sciex Multiquant TXT exports to identify QCpool samples and provide quick overview of metabolomics or lipidomics study quality) — https://github.com/ricoderks/QComics

## Evaluation signals

- All QCpool samples in the output table have injection indices that differ by the expected interval (e.g., constant step size across the sequence)
- No QCpool samples are marked as missing or undetected when they appear in the Sciex Multiquant export with explicit QCpool annotation
- Sequence IDs in the output correctly match the input file's sequence identifier metadata
- Validation report confirms interval regularity matches study design expectations; deviations (if any) are flagged with specific injection indices
- Output table schema is complete and consistent with no null values in required columns (sample name, injection index, sequence ID)

## Limitations

- Detection accuracy depends on consistent labeling or annotation of QCpool samples in the Sciex Multiquant export—mislabeled or unlabeled QC samples will be missed
- Requires Sciex Multiquant version > 3.0.3; compatibility with earlier versions is not guaranteed
- Does not assess the actual analytical quality of QCpool measurements (peak intensity, retention time drift, etc.)—only validates temporal distribution of QCpool injections
- The skill assumes QCpool samples are intended to occur at regular intervals; studies with irregular or adaptive QC schedules may produce false-positive interval violations

## Evidence

- [intro] a pooled sample (QCpool) needs to be measured in regular intervals during one or more sequences: "a pooled sample (QCpool) needs to be measured in regular intervals during one or more sequences"
- [intro] QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to txt format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [intro] The goal of the QComics package is to have a quick overview of the quality of a metabolomics or lipidomics study: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
- [other] Record the injection index, sample position within sequence, and any sequence identifier for each detected QCpool sample: "Record the injection index, sample position within sequence, and any sequence identifier for each detected QCpool sample"
- [other] Validate that QCpool samples occur at regular intervals as expected from study design: "Validate that QCpool samples occur at regular intervals as expected from study design"
