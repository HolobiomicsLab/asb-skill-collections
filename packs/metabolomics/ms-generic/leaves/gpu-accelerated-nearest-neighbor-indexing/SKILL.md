---
name: gpu-accelerated-nearest-neighbor-indexing
description: Use when when searching unknown mass spectra against large high-resolution
  spectral libraries for open modification identification and you need to reduce search
  latency from seconds to milliseconds while maintaining sensitivity and specificity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ANN-SoLo
  - Faiss
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- ANN-SoLo (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is
  a spectral library search engine
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary)
  is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00359
  all_source_dois:
  - 10.1021/acs.jproteome.8b00359
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# GPU-accelerated nearest neighbor indexing

## Summary

Accelerate open modification spectral library searching by building approximate nearest neighbor (ANN) indexes on GPU and executing cascade scoring strategies to retrieve only the most relevant library spectra for comparison to unknown query spectra. This combines feature hashing and GPU computation to achieve millisecond-scale query latency while maintaining strict false discovery rate control.

## When to use

When searching unknown mass spectra against large high-resolution spectral libraries for open modification identification and you need to reduce search latency from seconds to milliseconds while maintaining sensitivity and specificity. Apply this skill when the query throughput demand (spectra per second) exceeds what CPU-only approximate nearest neighbor search can deliver, or when you have access to NVIDIA CUDA-enabled GPUs on Linux systems.

## When NOT to use

- If your spectral library is small enough (<100k spectra) that CPU-only exact nearest neighbor search meets latency requirements; GPU setup and data transfer overhead may not be justified.
- If you do not have access to NVIDIA CUDA-enabled GPUs on Linux; ANN-SoLo GPU version is Linux-only and requires CUDA compatibility.
- If your input spectra are already pre-indexed or if you need to support platforms other than Linux (OSX or Windows) without CPU fallback options; CPU-only ANN-SoLo version supports these but cannot achieve the millisecond-scale latencies this skill targets.

## Inputs

- query mass spectra (in mzML or proprietary format compatible with ANN-SoLo)
- spectral library data (preprocessed peak lists with m/z and intensity values)
- feature-hashed spectrum representations (fixed-size vectors from deterministic hashing)
- false discovery rate control threshold (numeric, e.g., 1% or 5%)

## Outputs

- approximate nearest neighbor index (GPU-resident Faiss index or LSH structure)
- ranked candidate library spectra matches (top-k per query, with shifted dot product scores)
- query latency metrics (milliseconds per spectrum)
- throughput metrics (spectra per second processed)
- identification results with FDR-controlled confidence scores
- GPU memory utilization and speedup factor (vs. CPU baseline)

## How to apply

First, prepare query and library mass spectra as memory-aligned structures suitable for GPU processing. Compute deterministic feature hash representations of all spectra to map peaks into fixed-size feature vectors. Transfer feature-hashed vectors to GPU memory and build GPU-accelerated approximate nearest neighbor indexes using Faiss or locality-sensitive hashing. Execute a cascade search strategy on GPU: retrieve the top-k candidate spectra from the ANN index using fast approximate distance metrics, then compute exact shifted dot product scores with full precision on the top candidates, and finally filter results by false discovery rate threshold. Measure query latency (milliseconds per spectrum), throughput (spectra per second), and identification accuracy (sensitivity/specificity) and compare against CPU baselines to confirm the speedup factor and memory efficiency improvements justify the implementation.

## Related tools

- **ANN-SoLo** (GPU-powered spectral library search engine that implements approximate nearest neighbor indexing with cascade scoring and feature hashing for open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (GPU-accelerated approximate nearest neighbor indexing library; ANN-SoLo depends on Faiss for GPU index construction and similarity search operations) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo && python -m ann_solo.cli --input queries.mzML --library library.mzML --gpu --cascade --fdr 0.01 --output results.tsv
```

## Evaluation signals

- Query latency is reported in milliseconds per spectrum and shows at least 10–100× speedup over CPU baseline for large spectral libraries (≥1M spectra).
- Throughput (spectra per second) meets or exceeds the target query rate for the application (e.g., high-throughput proteomics workflows).
- Identification accuracy (sensitivity and specificity) is maintained or improved relative to exhaustive CPU-based search; false discovery rate remains below the specified control threshold (e.g., 1% or 5%).
- GPU memory utilization is reported and stays within the device capacity; peak memory is logged during ANN index construction and cascade scoring phases.
- Top-k candidate spectra retrieved from ANN index correctly rank true library matches within the top ranks before cascade filtering, confirming ANN quality.

## Limitations

- GPU version requires Linux with NVIDIA CUDA support; CPU-only version must be used on macOS or Windows, sacrificing the millisecond-scale latency benefit.
- Python 3.6–3.9 only; Python 3.10 and newer are not currently supported (per README).
- Accuracy of ANN index depends on feature hashing quality and choice of hash function; poor hash collision rates can degrade candidate retrieval quality.
- Cascade search strategy requires tuning of top-k retrieval parameter and shifted dot product score threshold; improper tuning can result in missed identifications or inflated false discovery rates.
- Data transfer overhead between host memory and GPU memory may not be negligible for workflows with very frequent small-batch queries; the skill is optimized for larger batch sizes.

## Evidence

- [readme] Extremely Fast and Accurate Open Modification Spectral Library Searching of High-Resolution Mass Spectra Using Feature Hashing and Graphics Processing Units: "Extremely Fast and Accurate Open Modification Spectral Library Searching of High-Resolution Mass Spectra Using Feature Hashing and Graphics Processing Units"
- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
- [readme] The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms: "The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms"
- [readme] ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet): "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet)"
- [other] Compute feature hash representations of all spectra using a deterministic hashing function to map peaks into fixed-size feature vectors: "Compute feature hash representations of all spectra using a deterministic hashing function to map peaks into fixed-size feature vectors"
- [other] Transfer feature-hashed vectors to GPU memory and build approximate nearest neighbor (ANN) indexes using locality-sensitive hashing or similar GPU-accelerated indexing: "Transfer feature-hashed vectors to GPU memory and build approximate nearest neighbor (ANN) indexes using locality-sensitive hashing or similar GPU-accelerated indexing"
- [other] Measure query latency (milliseconds per spectrum), throughput (spectra per second), and identification accuracy (sensitivity/specificity) for GPU implementation: "Measure query latency (milliseconds per spectrum), throughput (spectra per second), and identification accuracy (sensitivity/specificity) for GPU implementation"
