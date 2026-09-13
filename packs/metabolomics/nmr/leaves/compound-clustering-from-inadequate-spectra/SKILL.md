---
name: compound-clustering-from-inadequate-spectra
description: Use when after peak picking has identified individual signals in an INADEQUATE
  NMR spectrum, apply this skill when you need to collapse thousands of individual
  peaks into fewer, more interpretable compound-level peak networks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - PyINETA
  - Python
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-clustering-from-inadequate-spectra

## Summary

Group picked peaks from INADEQUATE NMR spectra into networks representing individual compounds using spectral similarity and co-occurrence patterns. This clustering step bridges peak picking and metabolite database matching, reducing false positives by associating only peaks likely originating from the same chemical entity.

## When to use

After peak picking has identified individual signals in an INADEQUATE NMR spectrum, apply this skill when you need to collapse thousands of individual peaks into fewer, more interpretable compound-level peak networks. Use it when the downstream goal is matching peak networks to a metabolite database rather than analyzing individual peaks, or when you need a mapping of peaks to their parent compounds for downstream finding and matching modules.

## When NOT to use

- Input is already a pre-clustered or pre-annotated database of metabolites; use clustering only on de novo picked peaks
- Spectrum contains only isolated, non-overlapping peaks with no co-occurrence patterns; clustering requires multi-peak associations
- Downstream analysis requires individual peak-level resolution rather than compound-level networks

## Inputs

- Picked peaks from PyINETA.picking module (list with peak coordinates, intensities, and picking metadata)
- INADEQUATE NMR spectrum reference or peak occurrence matrix

## Outputs

- Peak-to-cluster mapping file (peak ID → cluster ID)
- Clustered peak dataset with cluster identifiers attached
- Cluster-level summary statistics (peaks per cluster, cluster intensity distributions)

## How to apply

Load the output from the peak-picking module (picked peak list with coordinates and intensities). Apply PyINETA's clustering algorithm, which groups peaks based on spectral similarity metrics and co-occurrence patterns—peaks that frequently appear together in the spectrum and have similar spectral characteristics are assigned to the same cluster. Each peak receives a unique cluster identifier, and a mapping file is generated documenting peak-to-cluster assignments. Export the clustered data in a format compatible with the downstream matching module, preserving both the cluster identifiers and the original peak metadata. Verify that cluster assignments are consistent and that no single cluster contains an implausibly large number of peaks for a single compound.

## Related tools

- **PyINETA** (Implements the clustering module (pyineta.clustering) that groups peaks into networks based on spectral similarity and co-occurrence) — https://github.com/edisonomics/PyINETA
- **Python** (Runtime environment for PyINETA clustering execution)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s cluster -o output_dir
```

## Evaluation signals

- Cluster identifiers are assigned to all input peaks with no missing or duplicate assignments
- Peak-to-cluster mapping file is well-formed and references valid cluster IDs for each input peak
- Cluster size distribution is reasonable (no single cluster contains an implausible fraction of all peaks, e.g. >50%)
- Clustered peak output is compatible with and accepted by downstream PyINETA matching module without format errors
- Peaks within the same cluster exhibit correlated intensity patterns or spectral similarity above the algorithm's internal threshold

## Limitations

- Clustering accuracy depends on quality of preceding peak picking; noisy or over-picked spectra may produce artifactual clusters
- Algorithm assumes peaks from the same compound show co-occurrence and spectral similarity; highly variable or fragmented signals from a single compound may be split across clusters
- No changelog available in repository, limiting visibility into algorithm changes or parameter tuning across versions
- Clustering module documentation does not specify distance metrics, similarity thresholds, or linkage criteria explicitly in the provided materials

## Evidence

- [readme] pyINETA is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound: "It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [other] Clustering module operates as a downstream step after peak picking and before matching to metabolite databases: "clustering module that filters picked peaks to identify networks of peaks from the same compound, operating as a downstream step after peak picking and before matching to metabolite databases"
- [other] Clustering algorithm groups peaks based on spectral similarity and co-occurrence patterns: "Apply the PyINETA clustering algorithm to group peaks into networks based on spectral similarity and co-occurrence patterns"
- [methods] Clustering is one of the documented modules in PyINETA's workflow: "Clustering
----------
.. automodule:: pyineta.clustering"
- [other] Output format must be compatible with downstream matching and finding modules: "Export the clustered peak data in a format compatible with downstream matching and finding modules"
