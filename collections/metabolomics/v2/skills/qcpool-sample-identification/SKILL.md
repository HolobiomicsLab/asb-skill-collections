---
name: qcpool-sample-identification
description: Use when you have Sciex Multiquant (≥v3.0.3) TXT export files containing metabolomics or lipidomics analytical sequences that include pooled QC samples, and you need to verify that QCpool samples were injected at the designed regular intervals and extract their positional metadata for quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qcomics
    doi: 10.1021/acs.analchem.3c03660
    title: QComics
  dedup_kept_from: coll_qcomics
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c03660
  all_source_dois:
  - 10.1021/acs.analchem.3c03660
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# qcpool-sample-identification

## Summary

Identifies and locates quality control pooled (QCpool) samples from Sciex Multiquant text export files to validate their injection at regular intervals across metabolomics or lipidomics sequences. This skill extracts injection metadata and validates temporal distribution for downstream quality assessment.

## When to use

Apply this skill when you have Sciex Multiquant (≥v3.0.3) TXT export files containing metabolomics or lipidomics analytical sequences that include pooled QC samples, and you need to verify that QCpool samples were injected at the designed regular intervals and extract their positional metadata for quality overview.

## When NOT to use

- Input is from a non-Sciex platform or not exported in Sciex Multiquant TXT format
- QCpool samples were not injected at regular intervals by design (irregular quality control scheme)
- Sequence metadata does not contain explicit QCpool sample annotations or markers

## Inputs

- Sciex Multiquant TXT export file (≥v3.0.3)
- Sample metadata and injection sequence table
- Study design specification (expected QCpool interval)

## Outputs

- QCpool detection and location table (sample name, injection index, sequence ID, interval position)
- Interval validation report (regularity confirmation, gap detection)

## How to apply

Load the Sciex Multiquant TXT export file and parse the sample metadata and injection sequence information. Scan the injection sequence to identify samples marked or annotated as QCpool or quality control pool samples, recording the injection index, sample position within sequence, and sequence identifier for each detected QCpool. Validate that QCpool samples occur at regular intervals as expected from study design by checking the spacing between consecutive QCpool injection indices. Compile results into a structured table with columns for sample name, injection index, sequence ID, and calculated interval position, ensuring no gaps or irregularities violate the expected sampling frequency.

## Related tools

- **Sciex Multiquant** (Source software that acquires and exports metabolomics/lipidomics data and QCpool injection sequences in TXT format)
- **QComics** (R/Python package that consumes parsed QCpool metadata to provide quick quality overview of metabolomics or lipidomics studies) — https://github.com/ricoderks/QComics

## Evaluation signals

- All QCpool samples in the sequence are correctly identified and marked in output table (no false negatives or false positives)
- Injection indices are sequential integers with no gaps or duplicates
- Interval spacing between consecutive QCpool samples is constant or matches the designed interval specification within tolerance
- Sequence IDs correctly map to each QCpool sample and match the input file's sequence organization
- Output table structure matches specification: columns for sample name, injection index, sequence ID, and interval position all populated

## Limitations

- Requires explicit QCpool annotation or marking in the Sciex Multiquant export; unlabeled or ambiguously named pooled samples may not be detected
- No changelog available for QComics package versioning, limiting traceability of parsing rule changes
- Validation of interval regularity depends on accurate study design specification input; misspecified expected intervals will yield false irregularity detections

## Evidence

- [intro] a pooled sample (QCpool) needs to be measured in regular intervals during one or more sequences: "a pooled sample (QCpool) needs to be measured in regular intervals during one or more sequences"
- [intro] QCpool samples need to be analysed with Sciex Multiquant software and exported to txt format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [intro] The goal of the QComics package is to have a quick overview of the quality of a metabolomics or lipidomics study: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
- [other] Record injection index, sample position, sequence identifier for each QCpool and validate regular intervals: "Record the injection index, sample position within sequence, and any sequence identifier for each detected QCpool sample. 4. Validate that QCpool samples occur at regular intervals"
