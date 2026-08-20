---
name: adduct-signature-identification-mass-spectrometry
description: Use when you have statistically significant LC-MS features (e.g., filtered by p-value < 0.01) from multi-assay metabolomics datasets and need to group features that represent the same metabolite ionized under different ESI conditions (e.g., [M+H]+, [M+Na]+, [M+NH4]+).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - MamsiStructSearch
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Adduct Signature Identification in Mass Spectrometry

## Summary

Identifies common electrospray ionization (ESI) adduct signatures in LC-MS features by calculating hypothetical neutral masses and grouping features with matching neutral masses within ppm tolerance. This enables structural annotation and cross-assay linking of metabolite features.

## When to use

You have statistically significant LC-MS features (e.g., filtered by p-value < 0.01) from multi-assay metabolomics datasets and need to group features that represent the same metabolite ionized under different ESI conditions (e.g., [M+H]+, [M+Na]+, [M+NH4]+). This is especially valuable when features from positive and negative ionization modes need to be linked or when the same metabolite appears across replicate assays under different adduct forms.

## When NOT to use

- Input is already a targeted feature table with known metabolite identities and single ionization mode — adduct identification is redundant.
- LC-MS data is from a single assay with a single ionization mode and no cross-assay validation is needed.
- Features are unfiltered or include low-significance noise features (p-value >> 0.05) — adduct grouping will conflate false positives.

## Inputs

- Statistically significant LC-MS features table (filtered by p-value threshold, e.g., p < 0.01)
- Feature metadata including m/z values, retention time (RT), and assay/ionization mode labels
- Mass tolerance parameter (ppm, typically 10 ppm)
- Retention time window size (typically 5 seconds)

## Outputs

- Adduct clusters: groups of features with matching neutral masses within ppm tolerance
- Structural clusters: merged adduct and isotopologue clusters with feature-to-cluster assignments
- Annotated structural clusters table with cross-assay adduct links identified

## How to apply

For each significant LC-MS feature within a 5-second retention time window, calculate hypothetical neutral masses by reversing the ionization of common ESI adducts (e.g., [M+H]+, [M+Na]+, [M+NH4]+, [M-H]−). Group features whose calculated neutral masses match within the specified ppm tolerance (typically 10 ppm). The rationale is that adduct ions of the same neutral molecule will have distinct m/z values but identical neutral masses; matching within mass accuracy tolerance confirms they represent the same metabolite. Merge these adduct clusters with isotopologue clusters (detected separately via 1.00335 Da mass differences) to form final structural clusters. Cross-assay adduct links can be validated using [M+H]+/[M-H]− reference patterns across ionization modes.

## Related tools

- **MamsiStructSearch** (Performs adduct signature search by calculating hypothetical neutral masses for common ESI adducts and grouping features with matching neutral masses within ppm tolerance) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data manipulation and feature table organization for adduct clustering workflow)
- **numpy** (Numerical computation of mass differences and neutral mass calculations)
- **scipy** (Statistical utilities for ppm tolerance comparisons and mass matching)

## Examples

```
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected_features)
struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- All features within an adduct cluster have calculated neutral masses differing by ≤ the specified ppm tolerance (e.g., ≤ 10 ppm)
- Features within an adduct cluster reside in the same retention time window (e.g., 5-second intervals) to avoid false grouping across unrelated metabolites
- Cross-assay adduct links are validated: features from positive and negative modes that share [M+H]+/[M-H]− reference patterns have matching neutral masses
- Adduct clusters do not contain features with m/z differences inconsistent with known ESI adduct mass shifts (e.g., [M+Na]+ − [M+H]+ ≈ 21.98 Da)
- Structural cluster assignments are non-overlapping: each feature belongs to exactly one adduct or structural cluster

## Limitations

- Accuracy depends on instrument mass resolution and calibration; ppm tolerance must be set appropriately (typically 10–15 ppm for high-resolution instruments).
- Rare or unconventional adducts not in the common ESI list ([M+H]+, [M+Na]+, [M+NH4]+, [M-H]−, etc.) will not be detected; custom adduct lists can be specified but require domain knowledge.
- In high-density metabolomic datasets, false matches may occur by chance if multiple metabolites have neutral masses within ppm tolerance; post-hoc validation (e.g., correlation clustering or manual inspection) is recommended.
- Annotation of cross-assay adduct links is only supported for assays analyzed by the National Phenome Centre using Region of Interest (ROI) files; other centers must supply custom annotations.
- The method was tested on metabolomics phenotyping data; applicability to other LC-MS data types (e.g., proteomics, lipidomics without validated adduct lists) may require optimization.

## Evidence

- [methods] Search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation.: "This is followed by a search for common adduct signatures. This is achieved by calculating hypothetical neutral masses based on common adducts in electrospray ionisation."
- [methods] Features with matching neutral masses within ppm tolerance are grouped together.: "If hypothetical neutral masses match for two or more features within a pre-defined tolerance (15 *ppm*) then these features are grouped together."
- [methods] Cross-assay adduct links are searched using [M+H]+/[M-H]− as reference patterns.: "Further, we search cross-assay clusters using [M+H]<sup>+</sup>/[M-H]<sup>-</sup> as link references."
- [methods] Adduct clusters are merged with isotopologue clusters to form structural clusters.: "Overlapping adduct clusters and isotopologue clusters are then merged to form structural clusters."
- [readme] The framework was tested on metabolomics phenotyping data but should be usable with other types of LC-MS data.: "the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data."
