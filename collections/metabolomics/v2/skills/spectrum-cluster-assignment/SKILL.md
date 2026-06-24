---
name: spectrum-cluster-assignment
description: 'Use when you have computed a sparse pairwise distance matrix from nearest
  neighbor indexes and need to group spectra into clusters. Use this skill when: (1)
  you have a sparse similarity or distance matrix as input;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - spectrum-utils==0.3.5
  - spectrum-utils
  - DBSCAN
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly
  efficient processing of millions of MS/MS spectra.
- pip install falcon-ms spectrum-utils==0.3.5
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectrum Cluster Assignment

## Summary

Apply density-based clustering (DBSCAN) to a sparse pairwise distance matrix to assign each MS/MS spectrum a cluster label, grouping similar spectra based on local density and neighborhood connectivity. This is the final step in the falcon pipeline for large-scale spectrum clustering.

## When to use

You have computed a sparse pairwise distance matrix from nearest neighbor indexes and need to group spectra into clusters. Use this skill when: (1) you have a sparse similarity or distance matrix as input; (2) you want to identify groups of spectra with cosine distance below a density threshold; (3) your goal is to assign each spectrum a cluster label for downstream analysis (e.g., spectral library construction, peptide identification).

## When NOT to use

- Input is not a pairwise distance/similarity matrix (e.g., raw spectrum data or feature vectors); use nearest neighbor indexing first.
- You need soft clustering or probabilistic cluster membership; DBSCAN produces hard assignments only.
- Spectral data have not been preprocessed (binned, hashed, filtered); preprocessing precedes distance computation and clustering.

## Inputs

- sparse pairwise distance matrix (from nearest neighbor indexing step)
- spectrum identifiers (associated with distance matrix rows/columns)

## Outputs

- cluster assignment table (CSV) with spectrum identifier and cluster label columns
- optional: representative spectra for each cluster (MGF format)

## How to apply

Load the sparse pairwise distance matrix output from nearest neighbor indexing into a format compatible with density-based clustering. Apply DBSCAN with the `eps` parameter set to the maximum cosine distance threshold for neighborhood; typical values range from 0.05 to 0.15 for pure clustering or up to 0.30 for more aggressive clustering, depending on spectral characteristics and preprocessing applied. The algorithm identifies dense regions by grouping spectra where neighbors fall within the `eps` distance threshold. Assign each spectrum a cluster label and export the cluster membership table (CSV or tabular format) with spectrum identifiers and corresponding cluster IDs. Validate cluster purity by checking that assigned clusters contain spectra from a single peptide (or chemical entity, for metabolomics data).

## Related tools

- **falcon** (command-line tool that executes the full clustering pipeline including density-based clustering on the sparse distance matrix) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Python library for spectrum handling and I/O (mzML, mzXML, MGF formats))
- **DBSCAN** (density-based clustering algorithm applied to the sparse distance matrix to identify spectrum clusters)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Cluster assignment table contains one row per spectrum with non-null cluster label; no spectrum is unassigned (unless identified as noise by DBSCAN).
- Cluster sizes and count are consistent with expected spectrum diversity; verify that clusters are not all singletons or a single giant cluster (indicates eps parameter tuning needed).
- Spot-check cluster membership: representative spectra from the same cluster should have cosine similarity ≥ (1 − eps) and share similar precursor m/z (within precursor_tol) and fragment patterns.
- Compare cluster purity: clusters should group spectra from the same peptide sequence or chemical structure; cross-validate with reference identifications if available.
- Output file format matches specification: CSV with columns for spectrum ID and cluster label, no missing values, no duplicate rows.

## Limitations

- DBSCAN performance is sensitive to the eps parameter; optimal value depends on spectral preprocessing and data characteristics; values between 0.05–0.15 are typical but require tuning.
- Sparse distance matrix must be loaded in memory; for extremely large datasets (billions of spectra), memory requirements may exceed available resources.
- Clustering results reflect the accuracy of the upstream nearest neighbor indexing; if the sparse distance matrix is incomplete or inaccurate, cluster assignments will be degraded.
- Default preprocessing settings in falcon are tuned for bottom-up proteomics; metabolomics and top-down data require adjusted min_peaks, min_mz_range, and scaling parameters.
- DBSCAN may assign many spectra to noise (unassigned) if eps is too small; conversely, eps too large will merge distinct clusters.

## Evidence

- [intro] Finally, density-based clustering is performed to group similar spectra into clusters.: "Finally, density-based clustering is performed to group similar spectra into clusters."
- [readme] Density-based clustering using the pairwise distance matrix is performed to find spectrum clusters. The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters.: "Density-based clustering using the pairwise distance matrix is performed to find spectrum clusters. The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense"
- [intro] The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other.: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [readme] eps: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. This parameter crucially governs cluster purity (i.e. clusters contain spectra corresponding to only a single peptide). The ideal value of this parameter depends on the spectral characteristics of your data and optional spectrum preprocessing configured in falcon. Values between 0.05 and 0.15 will typically generate a pure clustering result. For more aggressive clustering values up to 0.30 can be used.: "eps: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. This parameter crucially governs cluster purity (i.e. clusters contain spectra corresponding"
- [readme] falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line. Representative spectra for each cluster can optionally be exported to an MGF file.: "falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line."
- [other] Apply density-based clustering (such as DBSCAN or equivalent) to the distance matrix to identify spectrum clusters based on local density and neighborhood connectivity.: "Apply density-based clustering (such as DBSCAN or equivalent) to the distance matrix to identify spectrum clusters based on local density and neighborhood connectivity."
- [other] Assign each spectrum a cluster label and generate a cluster assignment table with spectrum identifiers and corresponding cluster membership.: "Assign each spectrum a cluster label and generate a cluster assignment table with spectrum identifiers and corresponding cluster membership."
