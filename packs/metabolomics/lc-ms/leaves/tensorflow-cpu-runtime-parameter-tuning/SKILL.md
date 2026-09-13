---
name: tensorflow-cpu-runtime-parameter-tuning
description: Use when deploying Mass2SMILES on a TensorFlow-CPU build and you need
  to optimize inference throughput on multi-core systems. This is particularly necessary
  when GPU inference is unavailable due to CUDA driver incompatibility, or when inference
  hardware has variable core counts (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3379
  tools:
  - Python
  - TensorFlow
  - InferenceModel
  - Docker
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2023.07.06.547963v1
  title: Mass2SMILES
evidence_spans:
- open-source Python based deep learning approach
- cddd does not seem to work on newer cuda drivers, therefore it is build using tensorflow
  cpu
- this Mass2SMILES model container is using GPU, the cddd does not seem to work on
  newer cuda drivers, therefore it is build using tensorflow cpu
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2smiles_cq
    doi: 10.1101/2023.07.06.547963v1
    title: Mass2SMILES
  dedup_kept_from: coll_mass2smiles_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2023.07.06.547963v1
  all_source_dois:
  - 10.1101/2023.07.06.547963v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tensorflow-cpu-runtime-parameter-tuning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Tune TensorFlow-CPU inference performance in Mass2SMILES by configuring the cpu_threads parameter to control the number of CPU cores allocated during model execution. This skill is essential when deploying the model on systems where GPU acceleration is unavailable or incompatible (e.g., newer CUDA driver conflicts) and CPU-bound inference speed must be optimized.

## When to use

Use this skill when deploying Mass2SMILES on a TensorFlow-CPU build and you need to optimize inference throughput on multi-core systems. This is particularly necessary when GPU inference is unavailable due to CUDA driver incompatibility, or when inference hardware has variable core counts (e.g., shared compute clusters, containerized environments). Apply this skill before batch-processing large MGF spectral datasets to establish the configuration that maximizes throughput for your target hardware.

## When NOT to use

- GPU acceleration is available and CUDA drivers are stable — use GPU-based inference (delser292/mass2smiles:transformer_v1 or equivalent GPU container) for significantly faster inference.
- Single-core or embedded systems where cpu_threads > 1 may degrade performance due to context-switching overhead.
- Real-time inference with strict latency SLAs where thread tuning experiments risk exceeding acceptable prediction time — use a pre-validated configuration instead.

## Inputs

- Mass2SMILES TensorFlow-CPU Docker container (delser292/mass2smiles:final)
- MGF file (GNPS-style) containing MS/MS spectral data
- Target cpu_threads parameter value (integer, e.g., 1–256)

## Outputs

- Inference predictions (SMILES structures and functional groups) for query spectra
- Execution log capturing thread count and inference latency
- Verification report comparing configured vs. observed thread allocation and throughput metrics

## How to apply

Instantiate the InferenceModel class with an explicit cpu_threads parameter (e.g., cpu_threads=128) to specify the number of CPU cores to allocate during inference execution. The parameter value should be set to match the number of physical cores available on your target hardware, or to a conservative fraction if sharing resources. Execute a test inference run on a representative sample MGF file containing MS/MS spectral data, and capture the actual thread count and wall-clock execution time. Compare the configured thread count against observed thread utilization (via system monitoring tools or TensorFlow logging) and measure inference latency to establish the optimal core allocation. Document the configuration and resulting throughput in a verification report to guide production deployment.

## Related tools

- **InferenceModel** (Instantiated with cpu_threads parameter to control CPU core allocation during inference) — https://github.com/volvox292/mass2smiles
- **Docker** (Container runtime for deploying the TensorFlow-CPU build of Mass2SMILES with reproducible environment) — https://hub.docker.com/r/delser292/mass2smiles
- **TensorFlow** (Deep learning framework providing cpu_threads parameter and CPU-only inference backend)
- **Python** (Language for scripting InferenceModel instantiation, test execution, and logging) — https://github.com/volvox292/mass2smiles

## Examples

```
from mass2smiles_inference import InferenceModel; model = InferenceModel(cpu_threads=128); predictions = model.predict('sample.mgf'); print(f'Processed {len(predictions)} spectra with {model.get_thread_count()} threads')
```

## Evaluation signals

- Configured cpu_threads value matches the integer parameter passed to InferenceModel constructor.
- Actual thread count observed during execution (via ps, top, or TensorFlow debug logs) is ≤ configured value and > 0.
- Inference completes without errors on sample MGF file and produces valid SMILES output.
- Wall-clock inference time decreases monotonically (or reaches a plateau) as cpu_threads increases, indicating effective parallelization up to a hardware saturation point.
- Verification report documents baseline throughput (inferences/sec or ms per spectrum) for the target thread configuration, enabling reproducible comparison across deployments.

## Limitations

- The cpu_threads parameter only applies to the TensorFlow-CPU build; GPU containers use different memory/compute management and do not expose this parameter.
- Optimal cpu_threads value is hardware-dependent and must be experimentally tuned for each target system; no universal default is specified in the documentation.
- Thread allocation overhead may reduce throughput at very high core counts (e.g., > 256) on systems with limited memory bandwidth; diminishing returns should be monitored.
- The recent update containing Dockerfiles (Zenodo 14778327) references the ability to tune cpu_threads but provides no explicit guidance on validation, convergence criteria, or recommended ranges.
- Inference speed improvement from tuning is incremental and bounded by single-sample latency; batching MGF files may be a more effective throughput optimization than parameter tuning alone.

## Evidence

- [readme] cpu_threads parameter controls thread allocation in TensorFlow-CPU inference: "can be speed up by changing the number of cores: e.g. InferenceModel(cpu_threads=128)"
- [readme] TensorFlow-CPU build used due to CUDA driver incompatibility: "cddd does not seem to work on newer cuda drivers, therefore it is build using tensorflow cpu"
- [readme] Inference speed improvement from tuning and container-based deployment: "Using this setup inference speed is highly improved"
- [readme] MGF input format and Docker container deployment for inference: "Spectral data can be provided as MGF files (GNPS-syle) and model inference is most effciently performed via the provided docker container"
- [readme] GPU-based alternative for performance comparison: "this Mass2SMILES model container is using GPU, the cddd does not seem to work on newer cuda drivers, therefore it is build using tensorflow cpu"
