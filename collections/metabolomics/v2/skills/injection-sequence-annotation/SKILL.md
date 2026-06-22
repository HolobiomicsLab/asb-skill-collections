---
name: injection-sequence-annotation
description: Use when you have a Sciex Multiquant TXT export file containing a metabolomics or lipidomics analytical sequence and need to locate QCpool samples that were injected at regular intervals, validate their spacing matches study design expectations, and compile structured metadata for downstream.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# injection-sequence-annotation

## Summary

Identifies and annotates quality control pool (QCpool) samples within metabolomics or lipidomics injection sequences exported from Sciex Multiquant, recording their positions and validating regular interval spacing to support quality assessment workflows.

## When to use

You have a Sciex Multiquant TXT export file containing a metabolomics or lipidomics analytical sequence and need to locate QCpool samples that were injected at regular intervals, validate their spacing matches study design expectations, and compile structured metadata for downstream quality control analysis.

## When NOT to use

- Input is not a Sciex Multiquant TXT export (e.g., raw mzML/mzXML files, already-processed feature tables, or output from other vendor software)
- QCpool samples are not marked or annotated in the sequence metadata—the skill requires explicit QCpool labeling to function
- Study design does not specify regular interval injection of QCpool samples

## Inputs

- Sciex Multiquant TXT export file (version > 3.0.3) containing sample metadata and injection sequence

## Outputs

- Structured annotation table with columns: sample name, injection index, sequence ID, interval position
- Validation report confirming QCpool regularity or flagging deviations from expected intervals

## How to apply

Load the Sciex Multiquant TXT export and parse the injection sequence metadata to extract sample names and position indices. Scan the sequence to identify samples annotated or marked as QCpool or quality control pool samples. For each detected QCpool, record the injection index, position within sequence, and sequence identifier. Validate that detected QCpool samples occur at regular intervals as specified by study design—this is a critical check that the QC strategy was executed as planned. Compile results into a structured table with columns for sample name, injection index, sequence ID, and interval position for integration into quality assessment pipelines.

## Related tools

- **Sciex Multiquant** (Generates and exports the TXT file containing sample metadata and injection sequence that is parsed to locate QCpool samples)
- **QComics** (Downstream package that consumes parsed QCpool annotations and injection sequence metadata for quality assessment and visualization of metabolomics/lipidomics study quality) — https://github.com/ricoderks/QComics

## Evaluation signals

- All samples labeled as QCpool in the input file are detected and recorded in the output table with correct injection indices
- Interval validation confirms QCpool samples are spaced at equal or near-equal distances across the sequence (e.g., every N injections as per study design)
- Output table has no missing values in required columns (sample name, injection index, sequence ID, interval position)
- Sequence ID values correctly reflect which analytical run each QCpool belongs to (important for multi-sequence studies)
- Detected deviations from expected regularity (e.g., missing QCpool, uneven spacing) are flagged and reported for manual review

## Limitations

- Skill depends on QCpool samples being explicitly annotated or marked in the Sciex Multiquant metadata—ambiguously labeled samples may be missed
- Requires knowledge of the expected QCpool injection interval (study design specification) to validate regularity; the skill can detect spacing but cannot infer the correct interval on its own
- Works only with Sciex Multiquant TXT exports (version > 3.0.3); other vendor formats or software versions are not supported
- No changelog or version history is documented for the QComics package, limiting ability to track changes in expected input/output formats across releases

## Evidence

- [intro] a pooled sample (QCpool) needs to be measured in regular intervals during one or more sequences: "a pooled sample (QCpool) needs to be measured in regular intervals during one or more sequences"
- [intro] QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to txt format: "QCpool samples need to be analysed with Sciex Multiquant (> v3.0.3) software and exported to `txt` format"
- [intro] The goal of the QComics package is to have a quick overview of the quality of a metabolomics or lipidomics study: "The goal of the `QComics` package is to have a quick overview of the quality of a metabolomics or lipidomics study"
- [other] workflow describes scanning injection sequence to identify QCpool samples, recording indices and positions, and validating regular intervals: "Scan the injection sequence to identify samples marked or annotated as QCpool or quality control pool samples. Record the injection index, sample position within sequence, and any sequence identifier"
