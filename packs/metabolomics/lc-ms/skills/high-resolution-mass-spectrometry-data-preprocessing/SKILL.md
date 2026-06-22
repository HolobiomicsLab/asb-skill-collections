---
name: high-resolution-mass-spectrometry-data-preprocessing
description: Use when you have acquired high-resolution MS/MS spectra in mzML, mzXML, or MGF format and need to prepare them for large-scale clustering or similarity searching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - spectrum-utils
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# high-resolution-mass-spectrometry-data-preprocessing

## Summary

Transform high-resolution tandem mass spectrometry (MS/MS) spectra from mzML, mzXML, or MGF format into low-dimensional hashed feature vectors suitable for fast nearest-neighbor indexing and clustering. This preprocessing step is essential for scaling spectrum similarity searching to millions of spectra without exhaustive pairwise comparisons.

## When to use

You have acquired high-resolution MS/MS spectra in mzML, mzXML, or MGF format and need to prepare them for large-scale clustering or similarity searching. Apply this skill when your analysis goal requires finding similar spectra across thousands or millions of spectra efficiently, or when you intend to construct nearest-neighbor indexes to avoid computing all pairwise distances exhaustively.

## When NOT to use

- Input spectra are already in low-dimensional vector or feature table form (e.g., quantification matrices from label-free or labeled proteomics).
- Your analysis requires interpretation of individual fragment ion assignments; feature hashing obscures which specific m/z bins contributed to each hash bucket.
- You need to preserve exact mass precision for substructure annotation or metabolite identification; binning and hashing approximate similarity at the cost of exact mass fidelity.

## Inputs

- mzML peak files
- mzXML peak files
- MGF peak files

## Outputs

- Low-dimensional hashed feature matrix (NumPy array or SciPy sparse matrix format)
- CSV file with spectrum identifiers and corresponding feature vectors
- Filtered spectrum metadata (precursor m/z, charge state, retention time)

## How to apply

Load peak files in mzML, mzXML, or MGF format using spectrum-utils or equivalent tools. Apply spectrum-level filtering (e.g., discard spectra with fewer than 5 peaks or spanning less than 250 m/z range; default min_mz 101, max_mz 500) to remove low-quality spectra before vectorization. Bin high-resolution spectra into small mass bins to create sparse, high-dimensional vectors that tightly capture fragment mass values. Apply feature hashing using a non-cryptographic hash function (e.g., MurmurHash3) to map the sparse bins into a fixed, low-dimensional vector space (controlled by the `low_dim` parameter). Optionally scale peak intensities (square root, logarithm, or rank scaling) to improve downstream cosine similarity estimates. Output the resulting hashed feature matrix as a dense or sparse numerical format (NumPy array, SciPy sparse matrix, or CSV). The hashing step preserves cosine similarity between the original high-resolution spectra while reducing dimensionality and memory footprint, making the vectors suitable for fast nearest-neighbor searching.

## Related tools

- **falcon** (Full spectrum clustering pipeline that consumes the hashed feature vectors produced by this preprocessing step to perform density-based clustering via nearest-neighbor indexes) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for reading, filtering, and normalizing MS/MS spectra from mzML, mzXML, and MGF formats prior to feature hashing)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Output feature vectors have fixed dimensionality equal to the `low_dim` parameter (e.g., all rows in NumPy array or sparse matrix have same number of columns).
- Cosine similarity between hashed vectors approximates the true cosine similarity of the original high-resolution spectra (verify on a representative sample by comparing hashed vs. unhashed cosine scores).
- Memory footprint of the feature matrix is substantially smaller than the original mzML/mzXML files (sparse matrix representation should be ≤ 10% of raw file size for typical proteomics data).
- Filtered spectra retain expected precursor m/z and charge state distributions; no unexpected loss of spectra outside the specified min_mz and max_mz bounds.
- Downstream nearest-neighbor indexing succeeds without out-of-memory errors, and clustering results show expected cluster purity (spectra in the same cluster correspond to the same peptide or compound).

## Limitations

- Feature hashing reduces interpretability: the contribution of specific fragment ions to similarity scores is obscured by the hash function, making post-hoc validation of cluster assignments difficult.
- The choice of `low_dim` parameter trades off memory and speed against accuracy; smaller vectors may miss true neighbors in high-dimensional space, resulting in spurious cluster fragmentation.
- Spectrum preprocessing settings (min_peaks, min_mz_range, min_mz, max_mz, scaling method) are optimized for bottom-up proteomics by default; metabolomics or top-down data require manual adjustment of these thresholds.
- Feature hashing is sensitive to the choice of hash function and collision rate; collision-induced artifacts can accumulate if the vector dimensionality is too low relative to the number of mass bins.
- The method assumes mass spectral cosine similarity is the appropriate metric for downstream clustering; other similarity measures (e.g., spectral angle, entropy-based) are not accounted for in the hashing scheme.

## Evidence

- [readme] Spectrum vectorization and hashing mechanism: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [readme] Input file formats accepted: "falcon takes peak files (in the mzML, mzXML, or MGF format) as input"
- [readme] Feature hashing algorithm details: "the sparse, high-dimensional, vectors are hashed to lower-dimensional vectors by using a hash function (the non-cryptographic MurmurHash3 algorithm) to map the mass bins separately to a small number"
- [readme] Cosine similarity preservation: "This feature hashing conserves the cosine similarity between hashed vectors and can be used to approximate the similarity between the original spectra."
- [readme] Default spectrum filtering thresholds: "Default values are minimum 5 peaks and 250 m/z range. Default values are 101 m/z and 500 m/z, respectively."
- [readme] Spectrum preprocessing rationale and adjustment guidance: "The default settings are intended for clustering bottom-up proteomics data. When analyzing metabolomics or top-down data, these settings likely need to be adjusted accordingly."
- [readme] Intensity scaling options: "Scale the peak intensities by their square root, logarithm, rank, or no scaling. Default is no scaling, with square root scaling often giving good results as well."
- [readme] Role in broader clustering pipeline: "the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching"
