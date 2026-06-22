---
name: isotopologue-adduct-link-identification
description: Use when you have selected statistically significant features from multi-assay untargeted LC-MS metabolomics data and need to group them by structural relationships defined by their mass-to-charge ratios (m/z) and retention times (RT).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0157
  - http://edamontology.org/topic_3172
  tools:
  - networkx
  - pyvis
  - matplotlib
  - pandas
  - Python
  - MamsiStructSearch
  - numpy
  - scikit-learn
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- 'Dependencies: networkx'
- 'Dependencies: pyvis'
- 'Dependencies: matplotlib'
- import pandas as pd
- MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets.
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

# Isotopologue-Adduct Link Identification

## Summary

A structural clustering method that identifies mass spectrometry features linked by isotopologue signatures (mass difference ~1.00335 Da) and common adduct patterns within retention time windows, enabling grouping of related features into structural clusters for multi-assay LC-MS metabolomics datasets.

## When to use

Apply this skill when you have selected statistically significant features from multi-assay untargeted LC-MS metabolomics data and need to group them by structural relationships defined by their mass-to-charge ratios (m/z) and retention times (RT). Use it to reduce feature complexity by linking adducts and isotopologues of the same underlying metabolites before visualization or downstream interpretation.

## When NOT to use

- Input features are already annotated and confirmed as unique metabolites (structural grouping would mask valid compound diversity)
- Data come from targeted LC-MS assays where feature identity is pre-determined (isotopologue search is designed for untargeted feature discovery)
- RT precision is <1 second or highly variable, violating the 5-second RT window assumption

## Inputs

- DataFrame with statistically significant LC-MS features (columns: Feature, m/z, Retention Time, Assay)
- RT window parameter (seconds; default 5)
- Mass tolerance parameter (ppm; default 10)
- List of common adducts (e.g., [M+H]+, [M-H]−, [M+Na]+)

## Outputs

- DataFrame with structural cluster assignments (Isotopologue group, Isotopologue pattern, Adduct group, Adduct, Structural cluster)
- Cluster membership index mapping features to structural clusters
- Optional: cross-assay link annotations indicating features linked across different ionization modes

## How to apply

Organize features into retention time (RT) windows of 5-second intervals. Within each RT window, systematically search for isotopologue signatures by identifying mass differences of 1.00335 Da between feature m/z values; cluster features meeting this criterion. Then search for common adduct signatures by calculating hypothetical neutral masses based on electrospray ionisation adducts (e.g., [M+H]+, [M-H]−) and matching neutral masses within a 10 ppm (or user-specified) tolerance across features. Merge overlapping isotopologue and adduct clusters to form structural clusters. Additionally, search cross-assay clusters using [M+H]+/[M-H]− mass difference (~1.008 Da) as link references to identify the same metabolite across different ionization modes. The resulting structural clusters reduce feature redundancy while preserving mechanistic information about ionization artifacts and metabolite identities.

## Related tools

- **MamsiStructSearch** (Primary Python class implementing isotopologue/adduct detection, mass matching, RT windowing, and structural cluster merging) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data storage and manipulation of feature tables and cluster assignments)
- **numpy** (Numerical computation for mass difference calculations and tolerance matching)
- **scikit-learn** (Optional: hierarchical clustering for correlation-based cluster flattening post-structural search)

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected_features)
struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- Isotopologue clusters contain ≥2 features with observed mass differences within ±0.003 Da of theoretical 1.00335 Da (13C–12C)
- Adduct clusters show calculated neutral masses that match within the specified ppm tolerance (default 10 ppm) across all members
- Cross-assay links correctly identify [M+H]+ and [M-H]− pairs with mass differences ≈1.008 Da when both ionization modes are present
- Structural clusters do not contain overlapping features (each feature belongs to exactly one structural cluster)
- Features in the same structural cluster co-elute within the same RT window (5-second interval by default)

## Limitations

- Mass measurement accuracy must be <10 ppm (default tolerance) to reliably discriminate adducts; low-resolution or miscalibrated instruments will produce false positives
- The method assumes common electrospray ionisation adducts; other ionization modes (ESI+ vs. ESI− vs. APCI) may have different adduct patterns not captured by default settings
- Highly abundant metabolites with many isotopologues (>4 peaks) may be misclassified if isotope fine structure or 13C natural abundance distributions are not accounted for
- Cross-assay linking assumes [M+H]+ and [M-H]− ionization modes are both present; missing assays prevent detection of potential cross-assay links
- RT windows of 5 seconds may be too coarse for compound co-elution in chromatography with <1-second peak widths, risking false negative groupings

## Evidence

- [readme] all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da: "all features are split into retention time (RT) windows of 5 seconds intervals, then each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da"
- [readme] This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [readme] Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [readme] Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references.: "Further, we search cross-assay clusters using [M+H]+/[M-H]- as link references."
- [methods] Create edges between features based on structural relationships: isotopologue links (weight=1), adduct links (weight=5), and cross-assay links (weight=10).: "Create edges between features based on structural relationships: isotopologue links (weight=1), adduct links (weight=5), and cross-assay links (weight=10)."
- [readme] struct = MamsiStructSearch(rt_win=5, ppm=10): "struct = MamsiStructSearch(rt_win=5, ppm=10)"
