---
name: peak-similarity-assessment
description: Use when you have a set of picked peaks from INADEQUATE NMR spectra and need to group them into networks to identify which peaks co-originate from the same metabolite compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0637
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

# peak-similarity-assessment

## Summary

Assess spectral similarity and co-occurrence patterns among picked peaks in INADEQUATE NMR spectra to group peaks originating from the same compound. This skill operates as a clustering step after peak picking and before database matching, using spectral similarity metrics to identify peak networks.

## When to use

Apply this skill when you have a set of picked peaks from INADEQUATE NMR spectra and need to group them into networks to identify which peaks co-originate from the same metabolite compound. Use it as a downstream filtering step after peak picking and before attempting to match peak networks to a metabolite database.

## When NOT to use

- Peak picking has not yet been performed; apply peak picking first
- Input peaks are already grouped or pre-clustered by an external method incompatible with PyINETA's clustering module
- Spectral data does not contain co-occurrence patterns (e.g., single isolated spectra with no replicate or multi-dimensional data)

## Inputs

- Picked peaks from PyINETA peak-picking module output
- Spectral data (INADEQUATE NMR spectra in PyINETA-compatible format)
- Peak coordinates and intensity values

## Outputs

- Peak cluster assignments (peak-to-cluster mapping file)
- Clustered peak networks with cluster identifiers
- Network metadata documenting co-occurrence and similarity patterns
- Clustered peak data compatible with downstream matching module

## How to apply

Load picked peaks from the peak-picking module output using PyINETA's picking interface. Apply the PyINETA clustering algorithm to group peaks based on spectral similarity and co-occurrence patterns—peaks that appear together across spectra and exhibit similar spectral features are clustered together. Assign each peak a unique cluster identifier and generate a mapping file documenting the peak-to-cluster assignments. Export the clustered peak data in a format compatible with downstream matching and finding modules. The clustering acts as a dimensionality reduction step that simplifies the search space for metabolite database matching by reducing noise and grouping related signals.

## Related tools

- **PyINETA** (Implements the clustering module (pyineta.clustering) that groups peaks by spectral similarity and co-occurrence patterns) — https://github.com/edisonomics/PyINETA
- **Python** (Runtime environment and language for PyINETA execution)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s cluster -o output_dir
```

## Evaluation signals

- Peak-to-cluster mapping file is generated and contains a valid cluster identifier for every input peak
- Cluster size distribution is reasonable and peaks within each cluster exhibit high spectral similarity scores (exact threshold depends on algorithm configuration)
- Clusters preserve co-occurrence relationships observed in raw spectra (e.g., peaks that co-appear in spectra remain in the same cluster)
- Clustered output can be successfully loaded and processed by the downstream matching module without format errors
- Manual inspection of representative clusters confirms that grouped peaks correspond to expected multiplet patterns or correlated signals from the same compound structure

## Limitations

- Clustering performance depends on quality of upstream peak picking; poor peak picking produces unreliable clusters
- Algorithm assumes co-occurrence patterns are present in the spectral data; spectra with limited replication or single-scan acquisitions may produce uninformative clusters
- No changelog is publicly available for PyINETA, making it difficult to track changes in clustering algorithm behavior across versions
- Clustering operates on spectral similarity metrics without chemical structure validation; chemically unrelated peaks may cluster if they share spectral patterns

## Evidence

- [intro] pyINETA implements a clustering module that filters picked peaks to identify networks of peaks from the same compound: "It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [methods] Clustering is a core workflow step in the PyINETA pipeline: "Clustering
----------
.. automodule:: pyineta.clustering"
- [other] Clustering operates on spectral similarity and co-occurrence patterns: "Apply the PyINETA clustering algorithm to group peaks into networks based on spectral similarity and co-occurrence patterns."
- [other] Clustering precedes matching to the metabolite database: "operating as a downstream step after peak picking and before matching to metabolite databases"
- [readme] PyINETA reads and processes INADEQUATE spectra with peak picking and clustering: "pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking"
