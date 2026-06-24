---
name: cpu-gpu-performance-benchmarking
description: Use when you have implemented both CPU and GPU versions of a spectral
  search algorithm (e.g., approximate nearest neighbor indexing with cascade filtering)
  and need to validate whether GPU acceleration is justified.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  - NumPy
  techniques:
  - mass-spectrometry
  license_tier: open
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

# CPU-GPU Performance Benchmarking

## Summary

Systematically measure and compare execution latency, throughput, and memory utilization between CPU and GPU implementations of the same algorithm to quantify acceleration gains. This skill is essential for validating whether GPU-accelerated approaches offer practical speedup for high-throughput spectral matching workflows.

## When to use

You have implemented both CPU and GPU versions of a spectral search algorithm (e.g., approximate nearest neighbor indexing with cascade filtering) and need to validate whether GPU acceleration is justified. Apply this skill when query throughput or per-spectrum latency is a critical performance metric and you must demonstrate speedup factor and resource trade-offs to justify deployment.

## When NOT to use

- Spectral library is very small (<10k spectra) such that GPU setup overhead dominates—CPU may be faster.
- Query set is tiny (single spectrum) without opportunity for batch parallelization—GPU acceleration unlikely to amortize initialization cost.
- Identification accuracy (sensitivity/specificity) differs between CPU and GPU paths—benchmark is invalid until both produce identical hits.

## Inputs

- Query mass spectra (mzML or vendor format)
- Spectral library (indexed or raw format)
- CPU implementation of spectral search algorithm
- GPU implementation of spectral search algorithm
- Cascade search parameters (k for ANN index size, FDR threshold)

## Outputs

- Per-spectrum latency (milliseconds)
- Throughput (spectra per second)
- GPU memory utilization (MB or GB)
- CPU memory utilization (MB or GB)
- Speedup factor (CPU latency ÷ GPU latency)
- Benchmark report with sensitivity/specificity unchanged between implementations

## How to apply

Run identical batches of query mass spectra through both CPU and GPU implementations under controlled conditions (same library size, same query set, same hardware environment). Measure three key metrics for each implementation: (1) query latency in milliseconds per spectrum, (2) throughput in spectra per second, and (3) GPU/CPU memory utilization. Compute speedup factor as the ratio of CPU latency to GPU latency. Report both absolute times and the fold-change to assess whether GPU acceleration overcomes overhead costs. Use the same cascade search strategy and false discovery rate thresholds on both paths to ensure algorithmic equivalence.

## Related tools

- **ANN-SoLo** (Reference implementation providing both CPU and GPU paths for cascade spectral search using approximate nearest neighbor indexing; enables direct latency and throughput comparison.) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (GPU-accelerated library for approximate nearest neighbor search; provides the indexing backend for GPU path in ANN-SoLo.) — https://github.com/facebookresearch/faiss
- **NumPy** (CPU-side feature vector and matrix operations for baseline implementation; required prior to ANN-SoLo installation.)

## Evaluation signals

- GPU speedup factor is >1.5× for typical query batch sizes (e.g., 1000+ spectra); speedup <1.2× suggests overhead not justified.
- Identification counts (true positives, false positives at FDR threshold) are identical between CPU and GPU outputs for same query set.
- GPU memory footprint scales linearly with library size; CPU memory does not exceed available system RAM.
- Query latency per spectrum is stable across multiple runs (coefficient of variation <5%), indicating reproducible performance.
- Cascade search strategy (top-k ANN retrieval → shifted dot product → FDR filter) is identical in both implementations; no algorithmic shortcuts on GPU path.

## Limitations

- GPU acceleration requires NVIDIA CUDA-capable hardware and Linux OS; no benefit on CPU-only or non-NVIDIA platforms.
- Python version locked to 3.6–3.9; Faiss dependency on specific GPU compute capability may break forward compatibility.
- Speedup highly sensitive to library size and query batch size; smaller libraries or single-spectrum queries may see negligible gain or slowdown due to PCIe transfer overhead.
- Memory bottleneck on GPUs with limited VRAM (e.g., <8 GB) may force smaller batch sizes and negate throughput advantage.
- Benchmark results are specific to hardware configuration (GPU model, CPU generation, PCIe version); generalization requires repeated testing on target deployment hardware.

## Evidence

- [other] Measure query latency (milliseconds per spectrum), throughput (spectra per second), and identification accuracy (sensitivity/specificity) for GPU implementation.: "Measure query latency (milliseconds per spectrum), throughput (spectra per second), and identification accuracy (sensitivity/specificity) for GPU implementation. Compare GPU performance metrics"
- [other] Extremely Fast and Accurate Open Modification Spectral Library Searching of High-Resolution Mass Spectra Using Feature Hashing and Graphics Processing Units.: "Wout Bittremieux, Kris Laukens, William Stafford Noble. **Extremely Fast and Accurate Open Modification Spectral Library Searching of High-Resolution Mass Spectra Using Feature Hashing and Graphics"
- [readme] The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms.: "The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms."
- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [intro] A cascade search strategy is combined with approximate nearest neighbor indexing to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score.: "A cascade search strategy is combined with approximate nearest neighbor indexing to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery"
