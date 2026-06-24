---
name: mass-to-charge-tolerance-matching
description: Use when you have statistically significant LC-MS features and need to
  group them into structural clusters. Specifically, use it after selecting features
  by p-value threshold (e.g., p < 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - MamsiStructSearch
  - Mummichog 3
  - mass2chem
  - JMS
  - metDataModel
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
- doi: 10.1371/journal.pcbi.1003123
  title: ''
evidence_spans:
- MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry
  datasets.
- import pandas as pd
- import numpy as np
- 'Dependencies: scipy'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi_cq
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  - build: coll_mummichog
    doi: 10.1371/journal.pcbi.1003123
    title: mummichog
  dedup_kept_from: coll_mamsi_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  - 10.1371/journal.pcbi.1003123
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-to-charge-tolerance-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Matches mass-to-charge (m/z) values of LC-MS features within a specified parts-per-million (ppm) tolerance to link features with identical or related neutral masses across ionization adducts or retention time windows. This is a core operation in LC-MS feature clustering that groups features likely to originate from the same metabolite.

## When to use

Apply this skill when you have statistically significant LC-MS features and need to group them into structural clusters. Specifically, use it after selecting features by p-value threshold (e.g., p < 0.01) and need to identify which features share the same neutral mass despite different ionization states or isotopologue compositions. It is essential when working with multi-assay LC-MS metabolomics datasets where the same compound may appear in multiple ionization modes or assays.

## When NOT to use

- Input features are already annotated with confirmed metabolite identities — use targeted extraction instead.
- Working with targeted (known compound list) rather than untargeted LC-MS data — tolerance matching is designed for discovery-driven workflows.
- RT information is missing or unreliable — the skill partitions features by RT window first; missing RT prevents proper grouping.
- ppm tolerance is set too wide (> 15 ppm) — will merge unrelated masses and reduce specificity; too narrow (< 5 ppm) may fragment true isotopologues due to instrument calibration drift.

## Inputs

- Filtered LC-MS feature table (rows=samples, columns=features, filtered by p-value threshold)
- Feature m/z values (numeric, high precision)
- Feature retention time (RT) values (numeric, in seconds or minutes)
- List of common ESI adduct mass shifts (e.g., +1.007276 for [M+H]+, −1.007276 for [M-H]−, +22.98922 for [M+Na]+)

## Outputs

- Structural cluster assignments table (feature → cluster ID mapping)
- Cluster composition matrix (features grouped by neutral mass equivalence)
- Annotated cluster metadata (neutral mass, RT range, adduct types per cluster)
- Cross-assay cluster links (features in different assays/ionization modes)

## How to apply

Within each retention time (RT) window (typically 5-second intervals), calculate hypothetical neutral masses for each feature by applying common electrospray ionization (ESI) adduct transformations (e.g., [M+H]+, [M-H]−, [M+Na]+). Then, for each pair of features within the same RT window, compute the ppm error between their hypothetical neutral masses using the formula: ppm = |mass1 − mass2| / ((mass1 + mass2) / 2) × 10^6. Group features whose ppm error falls below the tolerance threshold (typically 10 ppm in MAMSI) into adduct clusters. Merge overlapping adduct and isotopologue clusters (identified by 1.00335 Da mass differences) to form final structural clusters. Cross-assay cluster linking uses [M+H]+/[M-H]− mass differences as reference patterns.

## Related tools

- **MamsiStructSearch** (Python class that encapsulates m/z tolerance matching, adduct detection, and isotopologue clustering; loads filtered LC-MS features and returns structural cluster assignments) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data structure (DataFrame) for managing feature tables, m/z/RT columns, and cluster assignments)
- **numpy** (Numerical computation of ppm error and mass difference thresholds)
- **scipy** (Statistical utilities for clustering and distance calculations (implicit in MamsiStructSearch))

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- All features within a cluster have hypothetical neutral masses matching within the specified ppm tolerance (e.g., ≤10 ppm); manually spot-check 5–10 clusters by recomputing ppm error on representative feature pairs.
- Isotopologue pairs within a cluster have m/z differences of approximately 1.00335 Da (or multiples thereof); verify at least one isotopologue cluster per assay.
- Cross-assay links between features are marked correctly: features from different assays (e.g., HPOS vs. LNEG) are linked only if their neutral masses match and no other clusters contain both; sample cross-assay verification.
- Cluster counts increase monotonically with input feature count and RT window size; a sudden drop in clusters suggests a parameter boundary issue (e.g., ppm or RT window too strict).
- No single feature appears in multiple structural clusters (mutual exclusivity); verify using cluster ID uniqueness check.
- Retention time span for features within a cluster does not exceed the specified RT window size (e.g., 5 seconds); audit boundary cases near window edges.

## Limitations

- Mass spectrometer calibration drift can inflate measured ppm errors; recalibration (lock mass correction) should be applied before clustering. The framework assumes high-resolution MS data (e.g., Orbitrap, Q-ToF with ppm accuracy).
- Common adduct list is predefined (ESI adducts); unusual or solvent-specific adducts (e.g., ammonium, formate) must be manually added to the adduct library. The README notes MAMSI was tested on metabolomics data but should be usable with other LC-MS types, implying validation on non-metabolomics data is limited.
- Features without reliable RT values (e.g., from different chromatographic methods) cannot be correctly clustered; cross-assay links rely on [M+H]+/[M-H]− patterns but may fail if assays use incompatible ionization modes.
- ppm tolerance is a global parameter; heterogeneous instrument performance across assays may require per-assay tolerance tuning, which is not supported in the current implementation.
- Isotopologue detection (1.00335 Da difference) assumes natural isotope abundance patterns; synthetic isotope-labeled standards or deuterated compounds will not match this signature and may be misclassified.

## Evidence

- [readme] Calculate hypothetical neutral masses based on common adducts in electrospray ionisation: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [methods] Features within RT window matched within ppm tolerance: "Load selected LC-MS features (filtered by p-value threshold) into MamsiStructSearch with retention time window of 5 seconds and m/z tolerance of 10 ppm."
- [methods] Isotopologue detection via mass difference: "all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da"
- [methods] Merging overlapping clusters into structural clusters: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [readme] Cross-assay cluster linking procedure: "Further, we search cross-assay clusters using [M+H]+/[M-H]− as link references."
- [intro] Purpose of structural clustering in multi-assay context: "the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters"
