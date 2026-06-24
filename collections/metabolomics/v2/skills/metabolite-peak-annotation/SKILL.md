---
name: metabolite-peak-annotation
description: Use when after peak detection has identified significant m/z and retention
  time features in untargeted or targeted mass spectrometry data (as a .raw, .d, or
  mzXML file).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - R
  - R GUI
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5c03225
  title: SMART 2.0
evidence_spans:
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_smart_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03225
  all_source_dois:
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-peak-annotation

## Summary

Annotation of detected metabolomics peaks by matching mass spectrometry features (m/z, retention time, intensity) against metabolite databases and reference spectra to assign chemical identities. This skill transforms a peak table into an annotated feature set suitable for downstream metabolite identification and quantification.

## When to use

After peak detection has identified significant m/z and retention time features in untargeted or targeted mass spectrometry data (as a .raw, .d, or mzXML file). Use this skill when you have a preliminary peak table with m/z values, retention times, and intensities, and need to assign putative metabolite identities to support compound identification and concentration calibration.

## When NOT to use

- Peak detection has not yet been completed; start with peak detection algorithms instead.
- Input is already a fully annotated and validated metabolite feature table; proceed directly to downstream statistical or pathway analysis.
- Mass spectrometry data quality is severely compromised (e.g., low signal-to-noise, extensive baseline drift) such that reliable peak detection cannot precede annotation.

## Inputs

- Peak table with columns: peak_id, m/z, retention_time, intensity
- Mass spectrometry data in supported formats (.raw, .d, mzXML)
- Metabolite reference database(s)
- Reference mass spectra library or spectral database

## Outputs

- Annotated peak table with columns: peak_id, m/z, retention_time, intensity, metabolite_annotation, database_identifier
- Peak annotation report with match scores and confidence metrics

## How to apply

Load the detected peak table containing m/z, retention time, and intensity values into SMART. Match each peak's m/z and retention time signature against integrated metabolite databases and reference mass spectra libraries. For each peak, select the best-scoring match (by mass accuracy and spectral similarity) and assign a metabolite annotation. Compile results into an annotated peak table that includes peak identifiers, original m/z and retention time, intensity measurements, and assigned metabolite names or database identifiers. Validate annotation quality by checking mass error tolerances (typical <5 ppm for high-resolution instruments) and spectral match scores before proceeding to post-analysis steps such as peak identification and concentration calibration.

## Related tools

- **R** (Core programming environment for executing peak annotation algorithms and database matching logic) — https://github.com/YuJenL/SMART
- **R GUI** (User-friendly graphical interface for SMART's peak annotation module, enabling interactive database selection and annotation review) — https://github.com/YuJenL/SMART

## Evaluation signals

- All detected peaks in the input peak table receive at least one annotation assignment (100% coverage).
- Mass error (observed m/z minus database reference m/z) falls within expected tolerance for the instrument type (typically <5 ppm for high-resolution MS).
- Spectral similarity scores (e.g., cosine similarity to reference spectrum) exceed a predefined threshold (e.g., >0.7), indicating high-quality matches.
- Annotated retention times are consistent with known metabolite retention indices in the experimental separation method (e.g., within ±1–2 min for reverse-phase LC).
- Annotated peak table contains no duplicate metabolite assignments for distinct peaks without justification (e.g., isobaric metabolites).

## Limitations

- Annotation quality depends on completeness and accuracy of the metabolite reference database; metabolites absent from the database remain unannotated.
- High-resolution mass accuracy (typically <5 ppm) is required for reliable m/z matching; lower-resolution instruments may produce ambiguous or incorrect annotations.
- Isobaric metabolites (same m/z, different structure) cannot be distinguished by m/z alone; retention time and reference spectra are needed to disambiguate.
- For untargeted data, annotation is semi-quantitative; concentrations require post-analysis calibration and standard curves.

## Evidence

- [intro] Peak Analysis and annotation: Implement peak analysis for both untargeted and targeted data and peak annotation.: "Peak Analysis and annotation: Implement peak analysis for both untargeted and targeted data and peak annotation."
- [other] Annotate detected peaks by matching against metabolite databases and reference spectra.: "Annotate detected peaks by matching against metabolite databases and reference spectra."
- [other] Compile results into a peak table containing peak identifiers, m/z, retention time, intensity, and assigned annotations.: "Compile results into a peak table containing peak identifiers, m/z, retention time, intensity, and assigned annotations."
- [intro] Execute peak identification and concentration calibration: "Post-analysis: Execute peak identification and concentration calibration"
