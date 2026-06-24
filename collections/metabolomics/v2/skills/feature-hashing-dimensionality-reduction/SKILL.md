---
name: feature-hashing-dimensionality-reduction
description: Use when you have high-resolution tandem mass spectra (mzML, mzXML, or
  MGF format) and need to cluster or index millions of spectra efficiently without
  exhaustive pairwise comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - falcon
  - spectrum-utils
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly
  efficient processing of millions of MS/MS spectra.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-hashing-dimensionality-reduction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert high-resolution MS/MS spectra into low-dimensional dense or sparse vectors using feature hashing with mass binning, preserving cosine similarity while enabling efficient nearest-neighbor indexing and clustering of millions of spectra.

## When to use

You have high-resolution tandem mass spectra (mzML, mzXML, or MGF format) and need to cluster or index millions of spectra efficiently without exhaustive pairwise comparison. Feature hashing is the first critical step when you cannot afford to store or compare full-resolution sparse vectors, and you need to approximate cosine similarity between spectra while reducing memory and computational overhead for downstream nearest-neighbor searching.

## When NOT to use

- Spectra are already binned or already converted to low-dimensional vectors; re-hashing introduces unnecessary information loss.
- You require exact (not approximate) cosine similarity; feature hashing sacrifices precision for speed and memory efficiency.
- Input spectra are very sparse or have few peaks; the binning and hashing overhead may not be justified for small datasets.

## Inputs

- High-resolution MS/MS spectra in mzML, mzXML, or MGF format
- Raw peak list (m/z and intensity pairs) per spectrum

## Outputs

- Low-dimensional hashed spectrum vectors (dense or sparse format)
- Vector file compatible with nearest-neighbor index construction
- Hashed vectors preserving cosine similarity to original spectra

## How to apply

First, load raw high-resolution MS/MS spectra using spectrum-utils and bin them into small mass bins (typically 0.1 Da or smaller) to discretize the m/z and intensity dimensions into sparse, high-dimensional vectors. Apply the non-cryptographic MurmurHash3 algorithm to map these mass bins to a smaller number of hash bins (controlled by the `low_dim` parameter; the README recommends tuning this to balance accuracy versus memory), producing low-dimensional vectors. Feature hashing conserves cosine similarity between the original and hashed vectors, allowing the resulting vectors to serve as accurate proxies for spectrum similarity. Save the hashed vectors to a format compatible with nearest-neighbor index construction. The choice of hash dimensionality (`low_dim`) and bin width directly governs the trade-off between clustering accuracy and speed; larger `low_dim` values more accurately approximate true cosine distance at the cost of longer searching and higher memory requirements.

## Related tools

- **falcon** (Primary spectrum clustering tool that orchestrates feature hashing as the first step of the clustering pipeline) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for loading and preprocessing raw MS/MS spectra before hashing)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Output vectors have dimensionality equal to `low_dim` parameter and no larger
- Cosine similarity between pairs of hashed vectors approximates cosine similarity between original binned spectra (verify on a random subset)
- Output vectors can be successfully ingested by nearest-neighbor indexing without format errors
- Hashed vectors are either all dense or all sparse; no mixed representations within a batch
- Memory footprint of hashed vectors is significantly smaller than the original high-dimensional binned vectors (typically 10–100× reduction depending on `low_dim` choice)

## Limitations

- Feature hashing is lossy; some information is discarded during dimensionality reduction, which may affect the precision of downstream similarity estimates (acceptable trade-off for large-scale clustering).
- The quality of hashing depends on choice of `low_dim`; too-small values increase hash collisions and degrade accuracy, while too-large values negate memory and speed benefits.
- Performance is sensitive to bin width; the README does not explicitly recommend a bin width, so practitioners must tune this empirically based on their spectral characteristics and mass accuracy.
- Feature hashing assumes that cosine similarity is the target metric; if a different distance metric is needed downstream, hashing may not be appropriate.

## Evidence

- [intro] High-resolution spectra are binned and converted to low-dimensional vectors using feature hashing: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [readme] Binning and mass-bin hashing via MurmurHash3 conserves cosine similarity: "First, spectra are converted to sparse vectors using small mass bins to tightly capture their fragment masses. Next, the sparse, high-dimensional, vectors are hashed to lower-dimensional vectors by"
- [readme] low_dim parameter tunes accuracy vs. memory for hashed vectors: "`low_dim`: The length of the low-dimensional vectors used for nearest neighbor searching. Larger vectors will more accurately approximate the true cosine distance, at the expense of longer nearest"
- [readme] Spectrum-utils required for loading spectra before hashing: "You can easily install _falcon_ with pip: pip install falcon-ms spectrum-utils==0.3.5"
- [intro] Output vectors enable efficient nearest-neighbor construction: "the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching."
