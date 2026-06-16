---
name: tandem-mass-spectrum-clustering
description: Use when you have a large collection of tandem mass spectra (mzML, mzXML, or MGF format) and want to group similar spectra into clusters to identify redundancy, discover novel peptides or metabolites, or prepare data for downstream annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - spectrum-utils==0.3.5
  - falcon-ms
  - Python 3.8+
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
- pip install falcon-ms spectrum-utils==0.3.5
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon
schema_version: 0.2.0
---

# tandem-mass-spectrum-clustering

## Summary

Cluster millions of MS/MS spectra by converting high-resolution peaks to low-dimensional vectors via feature hashing, constructing nearest neighbor indexes for fast similarity searching, and applying density-based clustering to group similar spectra. This workflow enables efficient large-scale spectral organization without exhaustive pairwise comparisons.

## When to use

You have a large collection of tandem mass spectra (mzML, mzXML, or MGF format) and want to group similar spectra into clusters to identify redundancy, discover novel peptides or metabolites, or prepare data for downstream annotation. This is especially valuable when the spectrum collection is too large for exhaustive pairwise comparison or when you need to balance clustering purity (grouping only spectra from the same peptide/metabolite) with speed.

## When NOT to use

- Input spectra have already been clustered or deduplicated by another tool; re-clustering may introduce noise or redundant grouping logic.
- Analysis requires retention of all individual spectrum metadata beyond cluster assignment; the falcon output is lightweight and may lose auxiliary peak-level or scan-level annotations depending on input format.
- Data is from non-proteomics domains (e.g., pure synthetic chemistry, pharmaceuticals with atypical fragmentation patterns) where default preprocessing thresholds (min_mz 101–500 Da, min 5 peaks, 250 Da range) are unsuitable and extensive validation of parameter tuning is not feasible.

## Inputs

- Peak files in mzML, mzXML, or MGF format containing tandem MS/MS spectra
- Spectrum collection of any size (from thousands to millions of spectra)
- Configuration parameters: precursor tolerance, fragment tolerance, clustering epsilon, spectrum preprocessing settings

## Outputs

- Comma-separated file with cluster assignments (one spectrum–cluster label pair per line)
- Optional MGF file of representative spectra for each cluster

## How to apply

Install falcon-ms and spectrum-utils==0.3.5 in a Python 3.8+ environment on Linux or OSX. Prepare peak files in mzML, mzXML, or MGF format. Run the falcon command-line tool, specifying key parameters: precursor_tol (e.g., 20 ppm) and fragment_tol (e.g., 0.05 Da) for spectrum comparison, and eps (typically 0.05–0.15) to control the maximum cosine distance threshold for clustering purity. The tool internally binds spectra to buckets by precursor m/z, applies feature hashing to convert each spectrum into a low-dimensional vector, constructs nearest neighbor indexes within each bucket, computes a sparse pairwise distance matrix, and finally runs DBSCAN density-based clustering. Adjust spectrum preprocessing parameters (min_peaks, min_mz_range, scaling) if analyzing metabolomics or top-down data rather than bottom-up proteomics. Output includes a comma-separated cluster assignment file and optionally an MGF file of representative spectra per cluster.

## Related tools

- **falcon-ms** (Primary command-line tool for spectrum clustering via feature hashing, nearest neighbor indexing, and DBSCAN density-based clustering) — https://github.com/bittremieux/falcon
- **spectrum-utils==0.3.5** (Dependency for spectrum preprocessing and manipulation; must be installed alongside falcon)
- **Python 3.8+** (Runtime environment required for falcon execution)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Output cluster assignment CSV file is non-empty and contains one spectrum identifier and one cluster label per row.
- Number of clusters is non-zero and reasonable relative to the input spectrum count (typically much smaller than input size, indicating genuine grouping).
- If representative spectra are exported, the MGF file contains valid fragmentation patterns and does not duplicate spectra across clusters.
- When eps parameter is tuned within the recommended range (0.05–0.15), cluster purity is high, meaning spectra within the same cluster correspond to the same peptide or metabolite (verify by manual inspection or by downstream peptide identification agreement).
- Execution completes without errors or warnings related to missing peaks, out-of-range m/z values, or invalid file formats; check exit code and log output.

## Limitations

- Clustering quality is sensitive to the eps parameter, which depends on spectral characteristics and preprocessing settings; no single value is optimal across all datasets, and values between 0.05 and 0.15 are recommended, but metabolomics and top-down data may require manual tuning.
- Default spectrum preprocessing parameters (min_mz_range 250 Da, min_mz 101, max_mz 500) are tuned for bottom-up proteomics and may discard or mishandle spectra from metabolomics or top-down proteomics; adjustment is required for non-standard domains.
- The algorithm trades accuracy for speed via the n_probe and n_neighbors parameters; reducing these values speeds up nearest neighbor searching but risks missing true neighbors in high-dimensional space and producing suboptimal clusters.
- falcon is available only on Linux and OSX; Windows users must use a virtual machine, WSL, or alternative clustering tools.
- Output does not include confidence scores or cluster membership probabilities; clusters are hard assignments without uncertainty quantification.

## Evidence

- [readme] First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing.: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [readme] The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other.: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [readme] Finally, density-based clustering is performed to group similar spectra into clusters.: "Finally, density-based clustering is performed to group similar spectra into clusters."
- [readme] falcon requires Python 3.8+ and is available on the Linux and OSX platforms.: "falcon requires Python 3.8+ and is available on the Linux and OSX platforms."
- [readme] You can easily install falcon with pip: pip install falcon-ms spectrum-utils==0.3.5: "You can easily install _falcon_ with pip: pip install falcon-ms spectrum-utils==0.3.5"
- [readme] falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file: "falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file"
- [readme] eps: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. This parameter crucially governs cluster purity. Values between 0.05 and 0.15 will typically generate a pure clustering result.: "eps: The maximum cosine distance between two spectra for them to be considered as neighbors of each other. This parameter crucially governs cluster purity. Values between 0.05 and 0.15 will typically"
- [readme] The default settings are intended for clustering bottom-up proteomics data. When analyzing metabolomics or top-down data, these settings likely need to be adjusted accordingly.: "The default settings are intended for clustering bottom-up proteomics data. When analyzing metabolomics or top-down data, these settings likely need to be adjusted accordingly."
- [readme] Exploring more cells during searching decreases the chance of missing a nearest neighbor in the high-dimensional space, at the expense of a longer searching time.: "Exploring more cells during searching decreases the chance of missing a nearest neighbor in the high-dimensional space, at the expense of a longer searching time."
