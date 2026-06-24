---
name: metabolomics-study-design-interpretation
description: Use when when you have received Sciex Multiquant TXT export files from
  a completed metabolomics or lipidomics analytical run and need to verify that QC
  pool samples were injected at the designed regular intervals throughout the sequence(s).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - ricoderks/QComics
  - Sciex Multiquant
  - QComics
  license_tier: restricted
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

# metabolomics-study-design-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret and validate the quality control design of metabolomics or lipidomics studies by parsing exported analytical sequences, locating pooled QC samples (QCpool), and verifying their regular injection intervals across one or more measurement sequences. This skill ensures that QC strategy matches study design expectations and flags sequence deviations early.

## When to use

When you have received Sciex Multiquant TXT export files from a completed metabolomics or lipidomics analytical run and need to verify that QC pool samples were injected at the designed regular intervals throughout the sequence(s). Use this skill if study documentation specifies that QCpool samples should appear at fixed injection positions (e.g., every nth sample) and you need to validate compliance before downstream data quality assessment.

## When NOT to use

- Input is already a processed feature table or normalized intensity matrix; this skill requires raw sequence metadata from the instrument export.
- Study design does not include pooled QC samples (QCpool) measured at regular intervals; this skill is specific to interval-based QC validation.
- Sciex Multiquant export file is missing sample annotation or sequence order information needed to locate QCpool markers.

## Inputs

- Sciex Multiquant TXT export file(s) containing sample metadata and injection sequence
- Study protocol or sequence design document specifying expected QCpool injection interval

## Outputs

- Structured table of QCpool samples with injection index, sequence ID, and interval position
- Interval validation report flagging deviations from expected QCpool spacing
- Quality control sequence map for downstream QComics analysis

## How to apply

Load the Sciex Multiquant TXT export file and parse the sample metadata and injection sequence information to extract all samples with QCpool or quality control pool annotations. Scan the injection index sequentially and record the position, injection order, and sequence identifier for each QCpool sample detected. Calculate the intervals between consecutive QCpool injections and compare against the designed interval from study protocol (e.g., expected every 10 injections, or every 20 minutes of run time). Validate that observed intervals match or fall within acceptable tolerance of the design specification; flag any missing or irregularly-spaced QCpool samples. Compile results into a structured table with columns for sample name, injection index, sequence ID, and computed interval position for review before quality assessment.

## Related tools

- **Sciex Multiquant** (Instrument software that analyzes metabolomics/lipidomics samples and exports sequence metadata and QCpool annotations to TXT format)
- **QComics** (R/Python package that consumes parsed QCpool interval tables and annotated sequences to generate quality overview and trend plots for metabolomics studies) — https://github.com/ricoderks/QComics

## Evaluation signals

- All rows in output table contain non-null values for sample name, injection index, sequence ID, and interval position; no missing QCpool samples match study design count.
- Computed intervals between consecutive QCpool injections match or exceed 95% of the designed interval specified in protocol; deviations are documented and explained.
- Output table structure matches expected schema (columns for sample name, injection index, sequence ID, interval position) and can be directly ingested by QComics package without reformatting.
- Validation report explicitly states whether QCpool spacing conforms to study design or flags which injection positions deviate from specification.
- All QCpool samples in the TXT export are successfully identified and no non-QCpool samples are incorrectly classified as QCpool based on annotation field parsing.

## Limitations

- Method relies on correct and consistent QCpool annotation or marking in the Sciex Multiquant export; mislabeled or unmarked QC samples will not be detected.
- Sciex Multiquant version must be ≥ v3.0.3 to ensure consistent TXT export format and metadata structure; older versions may have different field layouts.
- Only detects QCpool samples explicitly marked in the injection sequence metadata; implicit or inferred QC samples (e.g., pooled reference standards without explicit annotation) will be missed.
- Does not validate the chemical identity or concentration of QCpool samples themselves, only their temporal placement in the sequence.

## Evidence

- [intro] a pooled sample (QCpool) needs to be measured in regular intervals during one or more sequences: "a pooled sample (QCpool) needs to be measured in regular intervals during one or more sequences"
- [intro] QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to txt format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [intro] The goal of the QComics package is to have a quick overview of the quality of a metabolomics or lipidomics study: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
- [other] Scan the injection sequence to identify samples marked or annotated as QCpool or quality control pool samples; Record the injection index, sample position within sequence, and any sequence identifier for each detected QCpool sample: "Scan the injection sequence to identify samples marked or annotated as QCpool or quality control pool samples. 3. Record the injection index, sample position within sequence, and any sequence"
