---
name: retention-time-and-mz-based-alignment
description: Use when after peak detection has been completed on individual LC-MS samples and you have a collection of detected peaks with m/z, retention time, and intensity values from each sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MetaboAnalystR
derived_from:
- doi: 10.1038/s41467-024-48009-6
  title: metaboanalystr
evidence_spans:
- 'MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboanalystr
    doi: 10.1038/s41467-024-48009-6
    title: metaboanalystr
  dedup_kept_from: coll_metaboanalystr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-48009-6
  all_source_dois:
  - 10.1038/s41467-024-48009-6
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-and-mz-based-alignment

## Summary

Align detected peaks across LC-MS samples using retention time (RT) and mass-to-charge ratio (m/z) as joint matching criteria to consolidate features into a quantitative feature table. This step resolves the same metabolite detected at different scan positions across samples and accounts for instrumental drift.

## When to use

After peak detection has been completed on individual LC-MS samples and you have a collection of detected peaks with m/z, retention time, and intensity values from each sample. Use this skill when you need to create a unified feature matrix across multiple samples for downstream statistical or pathway analysis.

## When NOT to use

- Input is already a consolidated feature table with no sample-level peak coordinates available.
- Peaks have been detected from only a single sample (no cross-sample alignment needed).
- Raw spectral data are in formats other than mzML or mzXML that MetaboAnalystR cannot parse.

## Inputs

- collection of detected peaks from individual LC-MS samples (m/z, retention time, intensity values per sample)
- peak detection results (output from peak detection module)

## Outputs

- aligned quantitative feature table (features × samples matrix with m/z, RT, and intensity)
- alignment quality metrics (missing value patterns, feature counts across samples)

## How to apply

Execute MetaboAnalystR's alignment function on the collection of detected peaks from all samples, using both retention time and m/z coordinates as joint matching criteria. The function groups peaks across samples that fall within defined RT and m/z tolerances (typical values depend on instrument resolution; the README mentions the approach leverages 'best practices established by the community'). Consolidate the aligned peaks into a single quantitative feature table where rows represent unique features (identified by RT and m/z) and columns represent samples, with cell values as peak intensities. Following alignment, validate the resulting feature table for completeness (missing value patterns), data quality metrics, and feature counts to confirm successful consolidation.

## Related tools

- **MetaboAnalystR** (Provides the alignment function and quality assessment module for RT/m/z-based peak consolidation across samples) — https://github.com/xia-lab/MetaboAnalystR

## Evaluation signals

- Feature table dimensions match expected number of unique RT/m/z combinations and input sample count.
- Missing value patterns are documented and consistent across samples; no unexpected sparsity introduced by alignment.
- Features detected in multiple samples show consistent m/z (within stated tolerance) and RT drift patterns across the sample set.
- Alignment does not create duplicate features for the same metabolite at different RT/m/z positions.
- Peak intensity sums per sample are preserved (or scale proportionally) before and after alignment, indicating no data loss during consolidation.

## Limitations

- Alignment quality depends critically on RT and m/z tolerance parameters; overly strict tolerances may fragment features, while loose tolerances may incorrectly merge distinct metabolites.
- Instrumental drift or calibration issues across the sample run can cause peaks from the same metabolite to fall outside alignment windows, resulting in false feature splitting.
- Missing peaks in some samples (due to low abundance or signal loss) result in missing values in the feature table; imputation may be required downstream.
- MetaboAnalystR 4.0 uses auto-optimized feature detection parameters but does not provide explicit user control over RT/m/z tolerance values in the README.

## Evidence

- [other] Perform retention-time and m/z-based alignment of detected peaks across all samples using MetaboAnalystR's alignment function.: "Perform retention-time and m/z-based alignment of detected peaks across all samples using MetaboAnalystR's alignment function."
- [other] Consolidate aligned peaks into a quantitative feature table with m/z, retention time, and intensity values for each detected feature across all samples.: "Consolidate aligned peaks into a quantitative feature table with m/z, retention time, and intensity values for each detected feature across all samples."
- [readme] an auto-optimized feature detection and quantification module for LC-MS1 spectra processing: "an auto-optimized feature detection and quantification module for LC-MS1 spectra processing"
- [other] Validate the feature table for completeness, missing value patterns, and quality metrics as defined in the MetaboAnalystR quality assessment module.: "Validate the feature table for completeness, missing value patterns, and quality metrics as defined in the MetaboAnalystR quality assessment module."
