---
name: runtime-performance-benchmarking
description: Use when when you have implemented or adopted a new clustering or analysis tool and need to validate that it meets stated runtime claims on a representative production-scale dataset. Particularly important when the tool uses hardware acceleration (GPU) and the claimed speedup is a core contribution;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8+
  - HyperSpec
  - CUDA
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jproteome.2c00612
  title: HyperSpec
evidence_spans:
- HyperSpec requires `Python 3.8+` with `CUDA` environment
- HyperSpec requires `Python 3.8+` with `CUDA` environment.
- github.com__wh-xu__Hyper-Spec
- github.com/wh-xu/Hyper-Spec
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hyperspec_cq
    doi: 10.1021/acs.jproteome.2c00612
    title: HyperSpec
  dedup_kept_from: coll_hyperspec_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00612
  all_source_dois:
  - 10.1021/acs.jproteome.2c00612
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# runtime-performance-benchmarking

## Summary

Measure and verify the end-to-end runtime of a mass spectra clustering algorithm on a realistic, large-scale dataset under controlled hardware conditions (GPU type, memory, SSD storage). This skill confirms whether claimed performance thresholds (e.g., <15 minutes for 25M spectra) are met in practice.

## When to use

When you have implemented or adopted a new clustering or analysis tool and need to validate that it meets stated runtime claims on a representative production-scale dataset. Particularly important when the tool uses hardware acceleration (GPU) and the claimed speedup is a core contribution; dataset scale should be comparable to the tool's intended use case (e.g., draft human proteome with 25 million spectra for HyperSpec).

## When NOT to use

- Input dataset is orders of magnitude smaller or simpler than the benchmark (e.g., single organism, <1M spectra); runtime extrapolation from toy data is unreliable.
- Hardware differs substantially and is not documented (e.g., older GPU, CPU-only execution, spinning disk instead of SSD); results will not be comparable to published benchmarks.
- Tool is not the primary focus of your analysis; benchmarking adds overhead and is unnecessary for exploratory or proof-of-concept work.

## Inputs

- MGF (Mascot Generic Format) peak files containing MS/MS spectra
- Spectra dataset (millions of spectra; e.g., draft human proteome with ~25M spectra)
- Tool configuration parameters (HD dimension, quantization level, clustering algorithm, eps threshold, charge states, tolerance values)

## Outputs

- End-to-end runtime (in seconds or minutes)
- Clustering results (CSV or Parquet file with cluster assignments and metadata)
- Performance report documenting hardware specs, parameter choices, and runtime validation

## How to apply

Load the target dataset (e.g., MGF files containing mass spectra) into the tool with GPU acceleration enabled and configured for the claimed hardware (e.g., CUDA on GTX 3090 or equivalent). Configure clustering parameters to match the published setup (e.g., HD dimension, quantization level, clustering algorithm, charge ranges, tolerance thresholds). Execute the full pipeline from raw input to final clustering output, recording wall-clock time from start to finish. Document the specific GPU model, compute capacity, storage device type (SSD recommended), and key parameter choices. Compare measured runtime against the claimed threshold; if runtime is significantly longer, investigate whether hardware specifications differ, parameters were modified, or the dataset size/composition differs from the benchmark.

## Related tools

- **HyperSpec** (Hyperdimensional computing-based mass spectra clustering tool being benchmarked) — https://github.com/wh-xu/Hyper-Spec
- **CUDA** (GPU acceleration runtime enabling HD encoding and Hamming distance computation on NVIDIA GPUs)
- **Python 3.8+** (Runtime environment for HyperSpec execution and timing instrumentation)

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --cluster_alg dbscan --use_gpu_cluster --cluster_charges 2 3 --eps=0.2 --refine
```

## Evaluation signals

- Measured end-to-end runtime is below the claimed threshold (e.g., <15 minutes for 25M spectra on GTX 3090)
- All input spectra are successfully processed and assigned cluster labels; output row count matches input spectrum count (allowing for optional refinement or filtering steps)
- Hardware specifications (GPU model, CUDA version, CPU cores, storage type) are documented and match or exceed the minimum stated requirements
- Runtime remains consistent across multiple independent runs on the same dataset and hardware, indicating reproducibility (coefficient of variation <10%)
- Output Parquet/CSV schema includes expected columns (bucket, precursor_charge, precursor_mz, cluster, is_representative) and no unexpected NaN or malformed entries

## Limitations

- Runtime is highly sensitive to hardware configuration (GPU memory, SSD vs. HDD, CPU core count for preprocessing); measurements on different hardware are not directly comparable to published benchmarks.
- Dataset composition (spectral complexity, charge state distribution, precursor m/z range) can affect runtime; the draft human proteome dataset used in the paper may not be representative of all MS/MS datasets.
- Clustering for large-scale datasets (e.g., PXD000561) requires high-end GPU (GTX 3090) with larger memory; smaller GPUs (e.g., GTX 1080Ti) may fail or run significantly slower.
- Parameter choices (HD dimension, quantization level, clustering algorithm, eps threshold) directly impact both runtime and clustering quality; changing parameters from published settings invalidates direct comparison.

## Evidence

- [intro] HyperSpec shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes.: "HyperSpec shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes."
- [other] Load the draft human proteome dataset (~25 million spectra) into HyperSpec. Configure HyperSpec with CUDA GPU acceleration (GTX 3090 or equivalent). Execute HyperSpec hyperdimensional clustering to project spectra into binary hyperdimensional space. Record the total end-to-end runtime in seconds or minutes. Verify that the measured runtime is below 15 minutes and document the result.: "Load the draft human proteome dataset (~25 million spectra) into HyperSpec. Configure HyperSpec with CUDA GPU acceleration (GTX 3090 or equivalent). Execute HyperSpec hyperdimensional clustering."
- [readme] HyperSpec requires Python 3.8+ with CUDA environment. A GPU should be installed properly. HyperSpec has been tested on two types of NVIDIA GPUs on a Linux platform, including GTX 1080Ti and GTX 3090. Clustering for PXD000561 dataset requires GTX 3090 with larger memory.: "HyperSpec requires Python 3.8+ with CUDA environment. A GPU should be installed properly. Clustering for PXD000561 dataset requires GTX 3090 with larger memory"
- [readme] HyperSpec supports running using the command line and takes MGF peak files as input and exports the clustering result as a CSV file with each MS/MS spectrum and its cluster label on a single line.: "HyperSpec takes MGF peak files as input and exports the clustering result as a CSV file with each MS/MS spectrum and its cluster label on a single line."
- [readme] The exported meta data for clustering results are compressed and stored in parquet file, which records bucket, precursor_charge, precursor_mz, identifier, scan, retention_time, cluster, and is_representative information.: "The exported meta data for clustering results are compressed and stored in parquet file, which records bucket, precursor_charge, precursor_mz, identifier, scan, retention_time, cluster, and"
- [readme] We recommend using high-performance SSD as the storage device for the best performance.: "We recommend using high-performance SSD as the storage device for the best performance."
