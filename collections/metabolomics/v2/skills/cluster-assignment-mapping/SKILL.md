---
name: cluster-assignment-mapping
description: Use when after density-based clustering (e.g., DBSCAN) has been performed on a sparse pairwise distance matrix derived from MS/MS spectra nearest neighbor indexes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - falcon
  - DBSCAN
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon_cq
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cluster-assignment-mapping

## Summary

Map spectrum identifiers to their assigned cluster IDs after density-based clustering on a sparse pairwise distance matrix. This skill produces a machine-readable assignment table and summary statistics that document cluster composition and quality.

## When to use

After density-based clustering (e.g., DBSCAN) has been performed on a sparse pairwise distance matrix derived from MS/MS spectra nearest neighbor indexes. Use this skill when you need to export cluster membership in a structured format suitable for downstream analysis, validation, or representative spectrum selection.

## When NOT to use

- The clustering step has not yet been performed—apply density-based clustering first.
- Input spectra have already been assigned to clusters by an external method and you only need to report the pre-computed mapping without re-clustering.
- The sparse pairwise distance matrix is missing or incompatible with the clustering algorithm (e.g., wrong format or corrupted data).

## Inputs

- Cluster assignments from density-based clustering algorithm (e.g., DBSCAN output with cluster ID per spectrum)
- Spectrum identifiers or scan numbers corresponding to each clustered spectrum
- Optional: original peak file metadata for spectrum name enrichment

## Outputs

- Comma-separated file (CSV) mapping spectrum identifiers to cluster IDs (one spectrum per line)
- Cluster summary statistics table (number of clusters, cluster sizes, noise count)
- Optional: cluster representative spectra list or MGF file for downstream validation

## How to apply

Load the clustering result (cluster IDs and spectrum identifiers) from the density-based clustering step and serialize it as a comma-separated table with one spectrum per row and its assigned cluster label per column. Simultaneously compute and report summary statistics including the total number of clusters formed, per-cluster size distribution, and the count of unclustered (noise) spectra if applicable. The mapping preserves the spectral identifiers (e.g., scan number, spectrum name) to enable traceability and cross-referencing with the original peak files. Quality can be assessed by verifying cluster sizes are non-empty and reasonable relative to the input spectrum count.

## Related tools

- **falcon** (Performs end-to-end spectrum clustering including density-based clustering and cluster assignment export; outputs CSV file with spectrum-to-cluster mappings) — https://github.com/bittremieux/falcon
- **DBSCAN** (Core density-based clustering algorithm applied to sparse pairwise distance matrix to generate cluster assignments)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- CSV output file is valid and parseable, with one spectrum identifier and one cluster ID per row
- Cluster ID values are consistent integers or identifiers with no gaps or NaN entries for assigned spectra
- Cluster size distribution is non-pathological: no single cluster contains >90% of spectra unless data is homogeneous
- Summary statistics (total clusters, per-cluster sizes) match manual count of unique cluster IDs and row counts in output
- Spectrum identifiers in the mapping are traceable back to the original peak file (mzML, mzXML, or MGF format)

## Limitations

- Cluster purity and biological validity depend critically on the eps parameter (maximum cosine distance): values between 0.05 and 0.15 are typical for proteomics, but metabolomics and top-down data may require different thresholds.
- Noise spectra (assigned to cluster ID −1 or 0 in DBSCAN) are included in the mapping but represent unclustered spectra; their prevalence may indicate insufficient nearest neighbor coverage or overly stringent eps.
- The mapping reflects only the density-based clustering result; it does not assess biological accuracy without manual validation or external ground truth (e.g., peptide sequence databases).
- Large-scale datasets (millions of spectra) may produce very large CSV files; consider chunking or using compressed formats for downstream storage.

## Evidence

- [other] Output cluster assignments as a table mapping spectrum identifiers to cluster IDs, and generate summary statistics (cluster sizes, number of clusters formed).: "Output cluster assignments as a table mapping spectrum identifiers to cluster IDs, and generate summary statistics (cluster sizes, number of clusters formed)."
- [readme] falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line.: "exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line"
- [readme] This will cluster all MS/MS spectra in mzML files in the `peak` directory with the specified settings and write (i) the cluster assignments to the `falcon.csv` file, and (ii) the cluster representatives to the `falcon.mgf` file.: "write (i) the cluster assignments to the `falcon.csv` file, and (ii) the cluster representatives to the `falcon.mgf` file"
- [intro] Finally, density-based clustering is performed to group similar spectra into clusters.: "density-based clustering is performed to group similar spectra into clusters"
- [readme] The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters.: "The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters."
