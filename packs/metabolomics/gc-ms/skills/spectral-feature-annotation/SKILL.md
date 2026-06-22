---
name: spectral-feature-annotation
description: Use when after auto-deconvolution has resolved co-eluting GC-MS peaks into individual component spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - GNPS_GC
  - GNPS (Global Natural Products Social Molecular Networking)
  techniques:
  - GC-MS
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub_cq
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-020-0700-3
  all_source_dois:
  - 10.1038/s41587-020-0700-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Feature Annotation

## Summary

Assign chemical identity and structural features to deconvolved mass spectra by matching experimental spectra against reference libraries and extracting retention time, m/z, and intensity metadata. This skill bridges raw GC-MS signal separation to chemically interpretable peak tables.

## When to use

Apply this skill after auto-deconvolution has resolved co-eluting GC-MS peaks into individual component spectra. Use it when you have a collection of deconvolved mass spectra (one per resolved component) and need to assign molecular identities, standardize feature descriptors (retention time, m/z, intensity), and generate a validated peak table suitable for downstream molecular networking or comparative analysis.

## When NOT to use

- Input is already a fully annotated feature table with validated compound identities — re-annotation risks overwriting high-confidence assignments.
- Deconvolution has not yet been applied and peaks remain co-eluting; annotation quality will be severely degraded by spectral convolution.
- Reference spectral library is unavailable or chemically incompatible with your sample matrix (e.g., lipid library applied to metabolite samples).

## Inputs

- Deconvolved mass spectra (one spectrum per resolved GC-MS component)
- Retention time array (minutes)
- m/z array (mass-to-charge values in Daltons)
- Intensity array (raw ion counts or normalized signal)
- Reference spectral library (NIST, GNPS, or proprietary format)

## Outputs

- Annotated peak table (tabular format: one row per deconvolved component with columns for intensity, m/z, retention time, and spectral library match identifier)
- Annotation metadata (library match score, confidence rank, alternative candidates ranked by similarity)

## How to apply

Load the set of deconvolved mass spectra and match each against a curated reference spectral library (e.g., NIST or in-house standards) using cosine similarity or analogous spectral comparison metrics. For each match above a defined threshold, extract and standardize the feature metadata: retention time (min), m/z (Daltons), and intensity (raw or normalized counts). Resolve multiple candidate matches by evaluating consistency of retention time with known reference compounds and spectral coherence (signal-to-noise, peak purity). Consolidate results into a tabular peak table with one row per annotated component, including all metadata columns. Validate the annotation quality by confirming that annotated peaks show expected chromatographic separation, that m/z and retention time values fall within instrument calibration tolerances, and that the annotated spectral library matches are reproducible across technical replicates.

## Related tools

- **GNPS_GC** (Companion repository implementing auto-deconvolution and spectral annotation workflow for GC-MS data; provides reference implementation for feature extraction and peak table generation) — https://github.com/bittremieux/GNPS_GC
- **GNPS (Global Natural Products Social Molecular Networking)** (Spectral library and molecular networking platform supporting GC-MS spectra matching and annotation)

## Evaluation signals

- Peak table row count matches the number of resolved components from deconvolution; no rows are duplicated or missing.
- All m/z values are positive and within the instrument's detectable mass range; all retention times are positive and within total analysis time.
- Annotated peaks show expected chromatographic order: retention times increase monotonically (within instrumental precision) for a sequence of standards or known homologs.
- Spectral library match scores (e.g., cosine similarity) for true positives are above a predefined threshold (article does not specify exact cutoff; use domain convention, e.g., cosine ≥ 0.7); false-positive matches are scored below threshold.
- When replicate injections are available, annotated peak intensities and retention times are reproducible (relative standard deviation < 10% for intensity; ±0.05 min for retention time).

## Limitations

- Annotation accuracy is directly limited by the completeness and accuracy of the reference spectral library; compounds absent from the library will remain unannotated or be misidentified.
- Isomers and isobars cannot be distinguished by mass spectrometry alone; co-eluting compounds with identical m/z and similar fragmentation will be conflated or produce ambiguous matches.
- Retention time is instrument and method dependent; robust annotation requires that reference standards have been run on the same GC column, temperature program, and carrier gas conditions.
- Deconvolution artifacts (false peaks, incomplete separation of co-eluting signals) propagate directly into the annotation table; deconvolution quality must be validated independently.

## Evidence

- [other] Extract deconvolved peak features including retention time, m/z values, and intensity for each resolved component.: "Extract deconvolved peak features including retention time, m/z values, and intensity for each resolved component."
- [other] Generate output peak table in tabular format with one row per deconvolved component, including intensity, m/z, and retention time columns.: "Generate output peak table in tabular format with one row per deconvolved component, including intensity, m/z, and retention time columns."
- [other] Validate deconvolution quality by confirming peak count increase and verifying spectral coherence of separated components.: "Validate deconvolution quality by confirming peak count increase and verifying spectral coherence of separated components."
- [intro] Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data: "Development of methods for auto-deconvolution of gas chromatography–mass spectrometry data"
