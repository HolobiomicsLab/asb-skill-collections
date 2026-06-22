---
name: isotopologue-pattern-detection-lcms
description: Use when after filtering LC-MS features by statistical significance (e.g., p-value < 0.01) and you wish to group features that represent the same metabolite at different isotopologue states.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - MamsiStructSearch
  - peakPantheR
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets.
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
  dedup_kept_from: coll_mamsi_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Isotopologue Pattern Detection in LC-MS

## Summary

Detects and groups isotopologue signatures in LC-MS features by identifying mass differences characteristic of stable isotope distributions (1.00335 Da between successive isotopologues). This skill enables structural annotation of metabolite features by recognizing the fingerprint of natural or introduced isotopic labeling within retention-time windows.

## When to use

Apply this skill after filtering LC-MS features by statistical significance (e.g., p-value < 0.01) and you wish to group features that represent the same metabolite at different isotopologue states. Particularly useful when analyzing untargeted metabolomics data where multiple isotopologue variants of the same compound are expected to co-elute within narrow retention-time windows (e.g., 5-second intervals).

## When NOT to use

- Input features are not yet filtered by statistical significance or p-value threshold; isotopologue detection is downstream of feature selection.
- Targeted (SRM/MRM) LC-MS data where features are pre-defined by expected transitions rather than discovered and grouped de novo.
- RT resolution is too coarse (>> 5 seconds) such that true isotopologues would be separated into different RT windows and missed.

## Inputs

- LC-MS feature table (pandas DataFrame) with m/z and retention time (RT) columns, filtered by statistical significance threshold
- Retention time window size (integer, seconds; typically 5)
- Mass-to-charge (m/z) tolerance (integer, ppm; typically 10)

## Outputs

- Isotopologue cluster assignments (feature-to-cluster mapping)
- Grouped feature table with cluster IDs annotated
- Cluster summary table (cluster ID, member features, neutral mass, RT range)

## How to apply

Partition statistically significant LC-MS features into retention-time windows of 5-second intervals. Within each RT window, compute all pairwise mass differences (Δm/z) between features. Identify pairs or multiplets where Δm/z ≈ 1.00335 Da, which is the characteristic mass shift between successive isotopologues (e.g., 13C vs. 12C). Group features exhibiting this mass pattern into isotopologue clusters. The rationale is that isotopologues of the same metabolite elute together and share the same neutral mass but differ by exactly one or more isotopic mass units; detecting this signature allows you to recognize structurally identical features differing only in isotopic composition, which can then be merged into higher-level structural clusters.

## Related tools

- **MamsiStructSearch** (Primary component performing isotopologue detection, RT windowing, mass difference calculation, and cluster merging in the MAMSI framework) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Tabular data manipulation for feature table I/O, column filtering, and cluster assignment tracking)
- **numpy** (Vectorized mass difference calculations and tolerance comparisons)
- **scipy** (Numerical operations supporting distance and clustering computations)
- **peakPantheR** (Optional complementary tool for targeted extraction and retention-time anchoring of annotated metabolites to improve clustering stability) — https://github.com/phenomecentre/peakPantheR

## Examples

```
from mamsi.mamsi_struct_search import MamsiStructSearch
import pandas as pd
selected_features = pd.concat([hpos, lpos, lneg], axis=1).iloc[:, mask]
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected_features)
iso_clusters = struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- Verify that all detected isotopologue clusters have pairwise mass differences equal to 1.00335 Da ± ppm tolerance (typically 10 ppm ≈ 0.00001 Da at m/z 100–300).
- Check that cluster members all fall within a single 5-second retention-time window and have overlapping or adjacent m/z ranges.
- Confirm that isotopologue clusters are subsequently merged correctly with adduct clusters and that no features are lost or duplicated in the final structural cluster output.
- Validate that cross-assay isotopologue links (e.g., same neutral mass detected in both positive and negative ion modes) match expected [M+H]+/[M-H]− patterns.
- Inspect cluster size distribution: isotopologue clusters should typically contain 2–5 features (representing natural isotope abundance or spiked labeled variants), not singleton features.

## Limitations

- Relies on accurate m/z calibration and RT alignment; instrumental drift or poor peak picking can cause false negatives (missed isotopologues) or false positives (non-isotopologue mass differences randomly near 1.00335 Da).
- The fixed 5-second RT window may be suboptimal for complex mixtures with severe peak tailing or for different chromatographic methods; the README and article do not address window-size optimization.
- Natural isotope patterns for elements heavier than carbon (e.g., sulfur with 32S/34S ≈ 1.996 Da, or bromine with 79Br/81Br ≈ 1.997 Da) are not explicitly handled; the method focuses on carbon-13 signatures.
- No changelog or version history is available in the repository, making it difficult to track improvements or bug fixes to the isotopologue algorithm over time.

## Evidence

- [methods] all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da: "all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da"
- [other] MamsiStructSearch groups features by first splitting them into retention time windows of 5-second intervals, searching each window for isotopologue signatures (1.00335 Da mass differences): "MamsiStructSearch groups features by first splitting them into retention time windows of 5-second intervals, searching each window for isotopologue signatures (1.00335 Da mass differences)"
- [readme] Firstly, all features are split into retention time (*RT*) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (*m/z*) of the features; if two or more features resemble a mass isotopologue signature then they are grouped together.: "each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (*m/z*) of the features; if two or more features resemble a mass"
- [methods] Load selected LC-MS features (filtered by p-value threshold) into MamsiStructSearch with retention time window of 5 seconds and m/z tolerance of 10 ppm.: "Load selected LC-MS features (filtered by p-value threshold) into MamsiStructSearch with retention time window of 5 seconds and m/z tolerance of 10 ppm."
- [methods] Select features with p-value < 0.01. You can also apply multiple testing correction methods to adjust the p-value threshold.: "Select features with p-value < 0.01. You can also apply multiple testing correction methods to adjust the p-value threshold."
