---
name: retention-time-mass-proximity-matching
description: Use when after sample alignment and grouping of isotopologues and adducts
  have been completed, when the aligned feature table contains NA or zero entries
  (missing intensities) for features that are detected in some samples but fall below
  the detection threshold in others.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - Centwave
  - manual expert review
  - SLAW
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Retention Time and Mass Proximity Matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A recursive matching strategy that identifies missing feature intensities by searching across related samples using retention time and m/z proximity windows to recover intensity values absent in some samples but present in others. This is a core component of gap-filling in untargeted LC-MS feature tables.

## When to use

After sample alignment and grouping of isotopologues and adducts have been completed, when the aligned feature table contains NA or zero entries (missing intensities) for features that are detected in some samples but fall below the detection threshold in others. This occurs in untargeted LC-MS workflows where detection sensitivity varies across sample batches or replicates.

## When NOT to use

- Input feature table is already complete with no missing values (no gap-filling needed).
- Samples are from entirely different biological or experimental conditions where cross-sample matching is not biologically valid.
- RT and m/z windows are set so wide that they match unrelated features, introducing systematic bias rather than recovering true missing values.

## Inputs

- Aligned feature intensity matrix (sample-feature table) with NA or zero entries from prior alignment step
- Sample metadata indicating sample type (QC, sample, MS2, blank) and injection order
- Peak picking and alignment parameter set (RT and m/z tolerances)

## Outputs

- Gap-filled feature intensity matrix (CSV or mzTab format) with recovered intensities
- Quality metrics on filling rate and confidence (number/proportion of recovered values per feature and sample)

## How to apply

Load the aligned feature table produced by prior alignment and isotopologue/adduct grouping steps. For each missing feature intensity (NA or zero entry), apply a recursive search algorithm that examines related samples identified by retention time (RT) and m/z proximity windows. The algorithm searches through alternate sample batches or replicates to locate intensity values for the same feature. Once a value is recovered from a related sample, it is filled into the missing entry while preserving the sample-feature matrix structure. The completed feature table is then output in CSV or mzTab format. Parameter optimization can adjust the RT and m/z tolerance windows to balance sensitivity (recovery of true missing values) against specificity (avoiding false matches).

## Related tools

- **SLAW** (Complete untargeted LC-MS processing workflow that implements gap-filling by data recursion as one step following peak picking and alignment) — https://github.com/zamboni-lab/SLAW
- **Centwave** (One of three peak picking algorithms wrapped by SLAW (alternatives: FeatureFinderMetabo, ADAP); produces initial feature list used upstream of alignment and gap-filling)

## Evaluation signals

- Check that the proportion of filled intensities is consistent with the detection frequency distribution across samples (features present in many samples should have higher fill rates than rare features).
- Verify that filled intensities fall within expected intensity ranges for the feature across samples (e.g., no filled values are statistical outliers).
- Confirm that retention time and m/z of recovered features match the original feature within the specified tolerance windows (RT window and m/z window parameters).
- Inspect sample-feature matrix structure: row and column counts should remain unchanged; only NA/zero entries should be replaced with numeric values.
- Assess gap-filling success by comparing downstream analyses (univariate statistics, PCA, clustering) before and after gap-filling to ensure recovered values improve signal quality without introducing artifacts.

## Limitations

- Effectiveness depends on sufficient within-batch or within-replicate replication; highly imbalanced sample designs (e.g., single replicate per group) provide limited recursive sources.
- RT and m/z tolerance windows must be carefully calibrated: windows that are too narrow will miss true matches; windows that are too wide will introduce false positive matches to unrelated features.
- The algorithm assumes that missing intensities represent true absence (below detection) rather than biological absence; if a feature is genuinely absent in some samples, recursive recovery may introduce false positives.
- Automated parameter optimization via SLAW requires QC samples (pooled study samples scattered through the sequence) as reference; if QC samples are absent or poorly representative, optimization may produce suboptimal tolerance windows.

## Evidence

- [other] SLAW includes gap-filling by data recursion as a processing step within its complete untargeted LC-MS workflow, following peak picking, sample alignment, and grouping of isotopologues and adducts.: "gap-filling by data recursion as a processing step within its complete untargeted LC-MS workflow, following peak picking, sample alignment, and grouping of isotopologues and adducts"
- [other] For each missing feature intensity, search recursively through related samples (by retention time and m/z proximity) to locate intensity values in alternate sample batches or replicates.: "For each missing feature intensity, search recursively through related samples (by retention time and m/z proximity) to locate intensity values in alternate sample batches or replicates"
- [other] Load aligned feature table with missing intensity values (NA or zero entries) from prior alignment step. Apply data recursion algorithm to identify features present in some samples but absent (below detection) in others.: "Load aligned feature table with missing intensity values (NA or zero entries) from prior alignment step. Apply data recursion algorithm to identify features present in some samples but absent (below"
- [other] Fill missing intensities using the recursively retrieved values, maintaining sample-feature matrix structure. Output completed feature table with filled intensities to CSV or mzTab format.: "Fill missing intensities using the recursively retrieved values, maintaining sample-feature matrix structure. Output completed feature table with filled intensities to CSV or mzTab format"
- [readme] Automated parameter optimization for picking, alignment, gap-filling: "Automated parameter optimization for picking, alignment, gap-filling"
