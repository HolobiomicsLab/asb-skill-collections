---
name: feature-table-gap-filling
description: Use when you have an aligned feature table from untargeted LC-MS with missing intensity values (NA or zero entries) for features that are present in some samples but fell below detection threshold in others.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Centwave
  - manual expert review
  - SLAW
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Feature-Table Gap-Filling by Data Recursion

## Summary

Gap-filling by data recursion recovers missing feature intensities (NA or zero entries) in aligned LC-MS feature tables by recursively searching related samples to locate intensity values in alternate sample batches or replicates. This step follows peak picking, alignment, and grouping of isotopologues and adducts to produce a complete sample-feature matrix.

## When to use

Apply this skill when you have an aligned feature table from untargeted LC-MS with missing intensity values (NA or zero entries) for features that are present in some samples but fell below detection threshold in others. This occurs after sample alignment and before statistical analysis or export when you need to recover intensity information across the complete cohort while maintaining data integrity.

## When NOT to use

- Input is already a fully populated feature table with no missing values—gap-filling is unnecessary.
- Features are genuinely absent (not detected) across all samples or sample groups—recursion cannot recover non-existent signal.
- Targeted LC-MS workflows where features are defined a priori and absence indicates true biological absence rather than instrumental detection failure.

## Inputs

- Aligned feature table with missing intensity values (NA/zero entries) in CSV or tabular format
- Sample metadata (retention time and m/z values for each feature)
- Sample batch or replicate grouping information

## Outputs

- Completed feature table with filled missing intensities in CSV or mzTab format
- Sample-feature matrix with no NA or zero entries for detected features

## How to apply

Load the aligned feature table containing missing intensity values from the prior alignment step. Apply the data recursion algorithm to identify features present in some samples but absent (below detection) in others. For each missing feature intensity, search recursively through related samples using retention time and m/z proximity as matching criteria to locate intensity values in alternate sample batches or replicates. Fill missing intensities using the recursively retrieved values, ensuring the sample-feature matrix structure is maintained. Output the completed feature table to CSV or mzTab format. The recursion leverages the assumption that a feature's true signal exists across related samples even if it fell below the instrumental detection limit in a particular sample.

## Related tools

- **SLAW** (Complete untargeted LC-MS workflow that implements gap-filling by data recursion as a processing step following alignment and grouping) — https://github.com/zamboni-lab/SLAW
- **Centwave** (Peak picking algorithm wrapped by SLAW upstream of gap-filling; provides initial feature detection)

## Evaluation signals

- Verify that missing intensity entries (NA/zero) in the input table are replaced with numeric values in the output table for the same sample-feature pairs.
- Check that the sample-feature matrix structure is preserved: row and column counts match, and only previously missing values are modified.
- Confirm that filled intensity values fall within the expected dynamic range and are consistent with intensity values for the same feature in other samples (no outliers introduced by recursion).
- Validate that filled features maintain retention time and m/z coherence with their respective feature definitions across all samples.
- Inspect the output format (CSV or mzTab) to ensure it is readable by downstream analysis tools and contains all required metadata (sample IDs, feature names, m/z, RT).

## Limitations

- Gap-filling by recursion is most effective when related samples (same batch or replicate group) have sufficient coverage; if all related samples lack a feature, no intensity can be recovered.
- The method relies on correct retention time and m/z proximity matching; misalignment or retention time drift upstream will reduce recursion accuracy.
- For very sparse feature tables (high proportion of missing values), recursion may impute values that do not truly reflect the original sample composition.
- SLAW's gap-filling is currently limited to DDA (data-dependent acquisition) LC-MS workflows; DIA-MS is not supported by the full SLAW pipeline.

## Evidence

- [other] SLAW includes gap-filling by data recursion as a processing step within its complete untargeted LC-MS workflow, following peak picking, sample alignment, and grouping of isotopologues and adducts.: "gap-filling by data recursion as a processing step within its complete untargeted LC-MS workflow, following peak picking, sample alignment, and grouping of isotopologues and adducts"
- [other] Load aligned feature table with missing intensity values (NA or zero entries) from prior alignment step. Apply data recursion algorithm to identify features present in some samples but absent (below detection) in others. For each missing feature intensity, search recursively through related samples (by retention time and m/z proximity) to locate intensity values in alternate sample batches or replicates. Fill missing intensities using the recursively retrieved values, maintaining sample-feature matrix structure.: "Apply data recursion algorithm to identify features present in some samples but absent (below detection) in others. For each missing feature intensity, search recursively through related samples (by"
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic data: "gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic data"
- [readme] SLAW is a scalable, containerized workflow for untargeted LC-MS processing (DDA only).: "SLAW is a scalable, containerized workflow for untargeted LC-MS processing (DDA only)"
