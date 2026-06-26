---
name: structural-cluster-annotation-metabolomics
description: Use when after identifying statistically significant LC-MS features (e.g.,
  via MB-VIP with p < 0.01 and permutation testing), when you need to consolidate
  multiple ionization and isotopic forms of the same metabolite into structural groups
  for annotation and pathway mapping.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - MamsiStructSearch
  - MamsiPls
  - peakPantheR
  - networkx
  - pyvis
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
  dedup_kept_from: coll_mamsi_cq
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

# Reconstruct MAMSI structural feature clustering of significant LC-MS features by m/z and RT

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Group statistically significant LC-MS features into structural clusters by systematically detecting isotopologue and adduct signatures across retention-time windows, then merge overlapping clusters and annotate cross-assay links. This enables metabolite-level interpretation of untargeted metabolomics by linking ionization variants and mass isotopologues to putative neutral masses.

## When to use

After identifying statistically significant LC-MS features (e.g., via MB-VIP with p < 0.01 and permutation testing), when you need to consolidate multiple ionization and isotopic forms of the same metabolite into structural groups for annotation and pathway mapping. Apply this skill when features span multiple assays (e.g., HPOS, LPOS, LNEG) or when you want to reduce feature dimensionality by resolving isotope patterns and common adducts (e.g., [M+H]+, [M-H]−, [M+Na]+ in ESI modes).

## When NOT to use

- Input features are from a targeted assay with pre-assigned molecular identities (you would skip clustering and instead validate against a reference library).
- Features have already been manually curated or collapsed into metabolite groups (redundant clustering step).
- Dataset uses non-ESI ionization or unknown adduct chemistry (isotope mass shift and adduct signatures are instrument- and ionization-dependent; the method assumes ESI adducts).
- Retention-time reproducibility across assays or runs is poor (clustering relies on RT co-elution; extreme RT drift will merge unrelated features).

## Inputs

- pandas DataFrame of selected LC-MS features (columns = m/z and RT values, rows = samples; already filtered by statistical significance p-value threshold)
- retention-time window size in seconds (default: 5 s)
- m/z tolerance in parts per million (default: 10 ppm)
- optional: ROI (region of interest) files from peakPantheR for automated metabolite annotation by RT and assay type

## Outputs

- annotated structural clusters table with feature-to-cluster assignments
- cluster-level metadata including detected isotopologue signatures, adduct types, and cross-assay links
- network representation of structural relationships (nodes = features, edges = isotope/adduct/cross-assay links)
- optionally: metabolite name annotations matched to NPC LC-MS assay libraries (HPOS, LPOS, LNEG, RPOS, RNEG, BANEG)

## How to apply

Load filtered LC-MS features (p-value threshold applied) into MamsiStructSearch with retention-time window = 5 seconds and m/z tolerance = 10 ppm. Split features into RT bins and search for isotopologue signatures by detecting mass differences of 1.00335 Da (13C–12C) between m/z values within each window. Calculate hypothetical neutral masses for common ESI adducts and group features with matching neutral masses within the ppm tolerance. Merge overlapping isotopologue and adduct clusters to form structural clusters. Search for cross-assay links using [M+H]+/[M-H]− as reference patterns. Return an annotated structural clusters table with feature-to-cluster assignments, optionally including automated metabolite name annotations if ROI files from peakPantheR are available for your chromatography method.

## Related tools

- **MamsiStructSearch** (Primary clustering engine: instantiates isotopologue, adduct, and cross-assay searches; merges overlapping clusters and optionally annotates features using peakPantheR ROI data) — https://github.com/kopeckylukas/py-mamsi
- **MamsiPls** (Preceding step: performs multi-block PLS and MB-VIP to identify statistically significant features that feed into structural clustering) — https://github.com/kopeckylukas/py-mamsi
- **peakPantheR** (Provides ROI files with annotated retention time and m/z for known metabolites in NPC LC-MS assays; used by MamsiStructSearch for optional automated feature annotation) — https://github.com/phenomecentre/peakPantheR
- **pandas** (Data structure and manipulation (DataFrame input/output for features and metadata))
- **numpy** (Numerical operations (mass difference calculations, ppm tolerance comparisons))
- **scipy** (Statistical and distance-based operations (optional clustering distance metrics))
- **networkx** (Graph construction and analysis for structural relationship networks (feature-to-feature links))
- **pyvis** (Interactive visualization of structural and correlation cluster networks)

## Examples

```
from mamsi.mamsi_struct_search import MamsiStructSearch; struct = MamsiStructSearch(rt_win=5, ppm=10); struct.load_lcms(selected); struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- All features in the input are assigned to exactly one structural cluster (no orphans or duplicates across clusters).
- Isotopologue cluster members differ by ≤ 1.00335 Da × n (where n = number of 13C atoms) and co-elute within the 5-second RT window.
- Adduct cluster members share a calculated neutral mass within ±10 ppm (or specified tolerance); neutral mass is consistent across multiple features.
- Cross-assay links connect features from different assays (e.g., HPOS and LNEG) with matching neutral masses and RT within assay-specific calibration bounds.
- Annotated features (when ROI matching is enabled) have RT differences < ±30 seconds from the reference ROI and m/z within ±10 ppm of the library entry; annotation confidence is reported for each match.

## Limitations

- Assumes electrospray ionization (ESI) adducts; not applicable to other ionization methods (APCI, MALDI, etc.).
- Relies on accurate retention-time alignment across assays; poor RT reproducibility or large systematic RT shifts will cause false merges or false negatives.
- The 1.00335 Da isotope mass shift assumes carbon-13 isotopologues; heterogeneous isotope patterns (e.g., 15N, 34S, 37Cl) may not be detected or may be misclassified as adducts.
- Automated metabolite annotation (via peakPantheR ROI matching) is only supported for NPC LC-MS assays (HPOS, LPOS, LNEG, RPOS, RNEG, BANEG); custom assays require manual ROI curation.
- No changelog found for the MAMSI package; versioning and bug fixes are tracked on GitHub but not formally documented in release notes.

## Evidence

- [methods] all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da: "all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da"
- [methods] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [methods] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [methods] Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references.: "Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references."
- [intro] the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters: "the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters"
- [methods] Select features with p-value < 0.01. You can also apply multiple testing correction methods to adjust the p-value threshold.: "Select features with p-value < 0.01. You can also apply multiple testing correction methods to adjust the p-value threshold."
- [methods] struct = MamsiStructSearch(rt_win=5, ppm=10) - struct.load_lcms(selected) - struct.get_structural_clusters(annotate=True): "struct = MamsiStructSearch(rt_win=5, ppm=10) - struct.load_lcms(selected) - struct.get_structural_clusters(annotate=True)"
- [readme] Additionally, our structural search tool, that utilises region of interest [(ROI) files] from peakPantheR, allows for automated annotation of some features based on the RT for a given chromatography and m/z.: "Additionally, our structural search tool, that utilises region of interest [(ROI) files] from peakPantheR, allows for automated annotation of some features based on the RT for a given chromatography"
