---
name: mass-tolerance-calibration-ppm-units
description: Use when when linking statistically significant LC-MS features into structural
  clusters based on adduct signatures and cross-assay references (e.g., [M+H]+/[M-H]−),
  and you need to specify the maximum allowed deviation (in ppm) between observed
  m/z values and calculated neutral masses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MamsiStructSearch
  - peakPantheR
  - pandas / numpy
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- import pandas as pd
- import numpy as np
- scipy
- 'Dependencies: scipy'
- from sklearn.model_selection import train_test_split
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-tolerance-calibration-ppm-units

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calibrate and apply mass-to-charge ratio (m/z) tolerance thresholds expressed in parts-per-million (ppm) units to match features across LC-MS assays during structural clustering and adduct annotation. This skill ensures that hypothetical neutral masses calculated from common electrospray ionization (ESI) adducts are correctly paired with observed features within instrument-specific accuracy bounds.

## When to use

When linking statistically significant LC-MS features into structural clusters based on adduct signatures and cross-assay references (e.g., [M+H]+/[M-H]−), and you need to specify the maximum allowed deviation (in ppm) between observed m/z values and calculated neutral masses. Essential when multiple ESI adducts are tested against a feature set and false-positive clustering must be minimized.

## When NOT to use

- Input feature m/z values are already in nominal (integer) mass units rather than high-resolution monoisotopic masses; ppm calculations require accurate decimal m/z values.
- Mass spectrometer calibration quality is unknown or instrument drift is suspected; ppm tolerance must be set to match instrument performance, and uncalibrated data will violate the tolerance assumptions.
- Features have already been annotated with metabolite identity and adduct type; use this skill only on unidentified, statistically significant features requiring structural linking.

## Inputs

- LC-MS feature table with columns: (AssayName)_(RTsec)_(m/z)m/z format
- Preprocessed feature metadata: m/z values, retention time (RT in seconds), assay identifiers
- List of common ESI adduct masses (e.g., [M+H]+: +1.0073 Da, [M+Na]+: +22.9898 Da, [M−H]−: −1.0073 Da)

## Outputs

- Adduct cluster assignments: groupings of features with matching neutral masses
- Structural clusters: merged adduct and isotopologue clusters
- Annotated feature table with cluster membership and assigned adduct type per cluster

## How to apply

Initialize the MamsiStructSearch object with a ppm tolerance parameter (default 15 ppm, though 10 ppm is used in the PathIntegrate article example). During the adduct search phase, calculate hypothetical neutral masses for each feature by subtracting or adding known ESI adduct masses (e.g., +1.0073 Da for [M+H]+, −1.0073 Da for [M-H]−) and check whether the resulting neutral mass matches any other feature's neutral mass within the specified ppm tolerance. The ppm deviation is computed as: (|observed_mz − calculated_mz| / calculated_mz) × 10^6. Features whose neutral masses agree within this tolerance are grouped into the same adduct cluster; this tolerance directly controls specificity—lower ppm values reduce spurious cross-assay or cross-adduct matches, while higher values risk conflating distinct molecules. Document the chosen ppm value in your workflow to ensure reproducibility.

## Related tools

- **MamsiStructSearch** (Loads LC-MS data, accepts ppm tolerance as initialization parameter, performs adduct and isotopologue clustering using the specified tolerance) — https://github.com/kopeckylukas/py-mamsi
- **peakPantheR** (Generates region-of-interest (ROI) files and retention time annotations used downstream to validate structural clusters) — https://github.com/phenomecentre/peakPantheR
- **pandas / numpy** (Data manipulation and numerical computation for ppm deviation calculation and feature matching)
- **scikit-learn** (Hierarchical clustering via scipy linkage to refine structural clusters after adduct matching)

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected_features)
struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- Verify that all features in a single adduct cluster have neutral masses within the specified ppm tolerance; compute max ppm deviation for each cluster and confirm it is ≤ the input threshold.
- Cross-validate cluster assignments: re-run the same data with two different ppm values (e.g., 10 and 15 ppm) and confirm that lower ppm yields fewer but more specific clusters, while higher ppm yields larger clusters with increased risk of conflation.
- Check structural cluster counts and composition: expect isotopologue clusters (mass diff ≈ 1.00335 Da) to remain stable across ppm variations, while adduct clusters should be sensitive to the tolerance parameter.
- Compare predicted neutral mass against literature or database values for annotated features in the cluster; neutral masses should be chemically plausible (typically 50–2000 Da for metabolomics).
- Inspect inter-assay cluster links using [M+H]+/[M-H]− reference pairs; confirm that linked features across positive and negative assays share consistent neutral masses within tolerance.

## Limitations

- The ppm tolerance is a global parameter applied uniformly across all features; in practice, instrument mass accuracy may vary with m/z (lower accuracy at higher m/z). The framework does not model this m/z-dependent uncertainty and may under- or over-cluster features in extreme mass ranges.
- ESI adduct masses are assumed to be exact (e.g., [M+H]+ = +1.00783 Da); isotope effects and in-source modifications (e.g., loss of H2O, gain of NH3) are not considered, which may cause real adduct pairs to exceed the tolerance.
- The skill assumes high-resolution accurate mass data (e.g., from Q-ToF instruments with <5 ppm intrinsic error); application to lower-resolution instruments (e.g., unit-mass quadrupole) will require substantially higher ppm tolerances and risk spurious clustering.
- No guidance is provided in the article or README for automated ppm threshold selection based on instrument performance; users must set this parameter manually or via cross-validation.

## Evidence

- [methods] Define retention time tolerance window (rt_win, default 5 seconds) and mass tolerance (ppm, default 15 ppm) for structural matching.: "Define retention time tolerance window (rt_win, default 5 seconds) and mass tolerance (ppm, default 15 ppm) for structural matching."
- [readme] This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation. If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 ppm) then these features are grouped together.: "calculating hypothetical neutral masses based on common adducts in electrospray ionisation. If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 ppm) then"
- [methods] Search for adduct signatures by calculating hypothetical neutral masses from common ESI adducts and matching within ppm tolerance; group features with matching neutral masses.: "calculating hypothetical neutral masses from common ESI adducts and matching within ppm tolerance; group features with matching neutral masses"
- [readme] struct = MamsiStructSearch(rt_win=5, ppm=10) struct.load_lcms(selected): "MamsiStructSearch(rt_win=5, ppm=10)"
