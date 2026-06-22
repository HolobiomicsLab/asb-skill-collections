---
name: spectral-peak-network-grouping
description: Use when after peak picking has been completed on INADEQUATE NMR spectra and you need to group correlated peaks into compound-specific networks before matching against a metabolite database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  tools:
  - PyINETA
  - Python
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.4c03966
  title: PyINETA
evidence_spans:
- This is the documentation for the PyINETA package version 2.0.0.
- '.. automodule:: pyineta.finding :members:'
- pyINETA is a Python package
- python run_pyineta.py <options>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyineta_cq
    doi: 10.1021/acs.analchem.4c03966
    title: PyINETA
  dedup_kept_from: coll_pyineta_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c03966
  all_source_dois:
  - 10.1021/acs.analchem.4c03966
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-network-grouping

## Summary

Group picked peaks from INADEQUATE NMR spectra into networks of peaks originating from the same compound using spectral similarity and co-occurrence patterns. This clustering step bridges peak picking and metabolite database matching by reducing the dimensionality of peak assignments and improving specificity for downstream identification.

## When to use

Apply this skill after peak picking has been completed on INADEQUATE NMR spectra and you need to group correlated peaks into compound-specific networks before matching against a metabolite database. Use when your input consists of picked peaks with positional and intensity information but you lack explicit assignments linking peaks to individual compounds.

## When NOT to use

- Input peaks have not yet been picked from the raw spectrum; use peak picking first.
- You already have explicit compound assignments or metabolite identifications; clustering adds no value.
- Input consists of 1D NMR or other spectroscopy types not supported by INADEQUATE-specific algorithms.

## Inputs

- Picked peaks from PyINETA picking module (with coordinates and intensities)
- INADEQUATE NMR spectrum data (processed, with basic referencing/shifting applied)

## Outputs

- Peak-to-cluster assignment mapping file
- Clustered peak networks (peaks grouped by cluster identifier)
- Cluster-annotated peak data compatible with downstream matching module

## How to apply

Load picked peaks from the PyINETA picking module output into the clustering module. Apply the PyINETA clustering algorithm to group peaks based on spectral similarity and co-occurrence patterns, which identifies peaks likely originating from the same compound. The algorithm assigns each peak a cluster identifier and generates a mapping file documenting peak-to-cluster assignments. Export clustered peak data in a format compatible with downstream matching and finding modules (typically as a peak network file with cluster IDs). Validate by checking that co-occurring peaks in the same spectral region are grouped together and that the number of clusters is reasonable relative to the expected number of compounds in the sample.

## Related tools

- **PyINETA** (Provides the clustering module (pyineta.clustering) that groups picked peaks into networks using spectral similarity and co-occurrence; orchestrates the full pipeline including picking, clustering, matching, and finding steps.) — https://github.com/edisonomics/PyINETA
- **Python** (Runtime environment in which PyINETA clustering is executed.)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s cluster -o output_dir
```

## Evaluation signals

- All picked peaks are assigned to exactly one cluster (no orphaned or multiply-assigned peaks).
- Peaks within the same cluster show consistent spectral similarity metrics and spatial co-localization in the 2D INADEQUATE spectrum.
- The number of clusters is consistent with the number of compounds expected in the sample (or is reduced to a tractable number for downstream database matching).
- Cluster mapping file contains complete, unambiguous peak-to-cluster identifiers with no missing values or malformed entries.
- Downstream matching module successfully processes the clustered peak data and produces metabolite assignments without error.

## Limitations

- Clustering quality depends on prior peak-picking accuracy; missed or spurious peaks in the picking step will propagate into clustering.
- The algorithm assumes peaks from the same compound exhibit co-occurrence and spectral similarity patterns; compounds with very weak or overlapping signals may not cluster correctly.
- No changelog is publicly available, making it difficult to assess version-specific improvements or bug fixes to the clustering algorithm.
- The README does not document clustering algorithm parameters (e.g., similarity threshold, distance metric) or their tunability via the config file.

## Evidence

- [readme] pyINETA is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound: "It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [other] pyINETA implements a clustering module that filters picked peaks to identify networks of peaks from the same compound, operating as a downstream step after peak picking and before matching to metabolite databases.: "pyINETA implements a clustering module that filters picked peaks to identify networks of peaks from the same compound, operating as a downstream step after peak picking and before matching to"
- [other] Apply the PyINETA clustering algorithm to group peaks into networks based on spectral similarity and co-occurrence patterns.: "Apply the PyINETA clustering algorithm to group peaks into networks based on spectral similarity and co-occurrence patterns"
- [other] Assign each peak a cluster identifier and generate a mapping file documenting peak-to-cluster assignments.: "Assign each peak a cluster identifier and generate a mapping file documenting peak-to-cluster assignments"
- [methods] Clustering. .. automodule:: pyineta.clustering: "Clustering
----------
.. automodule:: pyineta.clustering"
