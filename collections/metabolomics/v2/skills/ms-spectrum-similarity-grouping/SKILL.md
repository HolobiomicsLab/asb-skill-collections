---
name: ms-spectrum-similarity-grouping
description: Use when after computing a sparse pairwise distance matrix from nearest
  neighbor indexes of MS/MS spectra (in mzML, mzXML, or MGF format), and you need
  to assign each spectrum to a cluster group for downstream analysis such as peptide
  identification or spectral library construction.
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
  license_tier: restricted
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

# ms-spectrum-similarity-grouping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply density-based clustering (DBSCAN) to a sparse pairwise distance matrix derived from nearest neighbor indexes to group similar MS/MS spectra into clusters. This is the final step in the falcon pipeline for large-scale spectrum clustering, assigning each spectrum a cluster label based on cosine distance thresholds and local density.

## When to use

After computing a sparse pairwise distance matrix from nearest neighbor indexes of MS/MS spectra (in mzML, mzXML, or MGF format), and you need to assign each spectrum to a cluster group for downstream analysis such as peptide identification or spectral library construction. Use this skill when you have millions of spectra to group by similarity and want to balance cluster purity (one peptide per cluster) with computational efficiency.

## When NOT to use

- Input is already a pre-computed cluster assignment or a feature table; skip directly to downstream analysis.
- Spectra have not yet been preprocessed (binned, hashed, or indexed); apply feature hashing and nearest neighbor indexing first.
- You need exact exhaustive pairwise distances rather than approximate sparse distances; use all-vs-all cosine similarity instead.

## Inputs

- sparse pairwise distance matrix (from nearest neighbor indexes, in a format compatible with DBSCAN)
- spectrum identifiers and metadata (precursor m/z, spectrum ID)
- eps parameter value (cosine distance threshold, typically 0.05–0.15 for pure clustering)

## Outputs

- cluster assignment table (CSV with spectrum identifiers and cluster labels)
- representative spectra per cluster (optional, MGF format)

## How to apply

Load the sparse pairwise distance matrix (output from nearest neighbor indexing) and apply DBSCAN with the eps parameter set to govern cluster purity. The eps parameter is the maximum cosine distance between two spectra for them to be considered neighbors; values between 0.05 and 0.15 typically yield pure clustering results (one peptide per cluster), while values up to 0.30 allow more aggressive clustering. The algorithm identifies dense subspaces of spectra and assigns cluster labels to each spectrum based on its neighborhood connectivity. Generate a cluster assignment table (CSV format) with spectrum identifiers and their corresponding cluster membership, optionally exporting representative spectra for each cluster to an MGF file. The choice of eps depends on your spectral preprocessing settings (scaling method, peak filtering) and the spectral characteristics of your dataset (proteomics vs. metabolomics).

## Related tools

- **falcon** (spectrum clustering tool that implements the complete pipeline including density-based clustering as the final step) — https://github.com/bittremieux/falcon
- **spectrum-utils** (utility library for spectrum file I/O and preprocessing (required dependency, version 0.3.5))
- **DBSCAN** (density-based clustering algorithm applied to the sparse pairwise distance matrix to find clusters)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- All spectra in the input dataset receive a cluster label (or are marked as noise points); no spectra are left unassigned.
- Cluster assignment CSV file contains exactly one row per input spectrum with valid spectrum ID and non-negative integer cluster label.
- Cluster purity: when cross-validated against known peptide annotations, clusters contain spectra from a single peptide sequence (if eps is set to 0.05–0.15 range).
- Representative spectra file (if exported) contains one MGF entry per identified cluster with correct precursor mass and fragment peaks.
- Sensitivity vs. specificity trade-off is appropriate for the application; adjusting eps parameter produces more or fewer clusters as expected.

## Limitations

- Cluster quality depends critically on the eps parameter; values must be tuned for the spectral characteristics of your data (proteomics vs. metabolomics, bottom-up vs. top-down).
- DBSCAN results are sensitive to the quality of the input sparse distance matrix; errors or gaps in nearest neighbor indexing will propagate.
- The algorithm groups spectra by cosine similarity only; peptide-level confidence, modification status, or other metadata are not considered during clustering.
- For metabolomics or top-down proteomics data, default spectrum preprocessing settings (min 5 peaks, 250 m/z range, 101–500 m/z window) may need adjustment before clustering.
- Very large datasets may produce clusters with widely varying sizes; smaller clusters are more prone to noise contamination.

## Evidence

- [intro] Finally, density-based clustering is performed to group similar spectra into clusters.: "Finally, density-based clustering is performed to group similar spectra into clusters."
- [other] Density-based clustering uses sparse pairwise distance matrix from nearest neighbor indexes.: "Density-based clustering is performed as the final step to group similar spectra into clusters, using the sparse pairwise distance matrix computed from nearest neighbor indexes as input."
- [readme] eps parameter controls cluster purity and governs cosine distance threshold for neighbors.: "The maximum cosine distance between two spectra for them to be considered as neighbors of each other. This parameter crucially governs cluster purity (i.e. clusters contain spectra corresponding to"
- [readme] falcon exports clustering result as comma-separated file with spectrum and cluster label.: "_falcon_ takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line."
- [readme] DBSCAN algorithm finds spectra that are close and form dense data subspace.: "The DBSCAN algorithm is used to find spectra that are close to each other and that form a dense data subspace, and group them into clusters."
