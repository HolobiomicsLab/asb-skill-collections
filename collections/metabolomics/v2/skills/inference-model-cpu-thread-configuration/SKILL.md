---
name: inference-model-cpu-thread-configuration
description: Use when when running Mass2SMILES inference on a TensorFlow-CPU build (e.g., delser292/mass2smiles:final container) and you need to optimize inference speed by controlling CPU core allocation.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Python
  - Mass2SMILES TensorFlow-CPU Docker container
  - Docker
  - TensorFlow (CPU build)
derived_from:
- doi: 10.1101/2023.07.06.547963v1
  title: Mass2SMILES
evidence_spans:
- open-source Python based deep learning approach
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# InferenceModel CPU-thread configuration

## Summary

Configure the number of CPU cores allocated to TensorFlow-CPU inference in Mass2SMILES by setting the cpu_threads parameter on the InferenceModel class. This skill enables performance tuning on CPU-bound inference runs without GPU acceleration.

## When to use

When running Mass2SMILES inference on a TensorFlow-CPU build (e.g., delser292/mass2smiles:final container) and you need to optimize inference speed by controlling CPU core allocation. This is particularly relevant when GPU-based acceleration is unavailable or when inference speed is limited by CPU parallelism on multi-core systems.

## When NOT to use

- Input MGF file is already preprocessed or does not contain valid MS/MS spectral data; cpu_threads tuning assumes the inference bottleneck is CPU parallelism, not data quality or format errors.
- The Mass2SMILES container is already built on GPU (e.g., delser292/mass2smiles:gpu or CUDA-enabled variant); cpu_threads applies only to TensorFlow-CPU builds.
- System has fewer available CPU cores than the configured cpu_threads value; operating system thread scheduling may not achieve the desired parallelism.

## Inputs

- InferenceModel instance (from Mass2SMILES TensorFlow-CPU build)
- MGF file (GNPS-style spectral data) with MS/MS fragment intensities and m/z values
- cpu_threads integer parameter (number of CPU cores to allocate)

## Outputs

- Inference execution with specified thread count allocated
- Thread usage logs or system observation confirming cpu_threads allocation
- Verification report comparing configured vs. observed thread count

## How to apply

Instantiate the InferenceModel class with an explicit cpu_threads parameter set to the desired number of CPU cores (e.g., cpu_threads=128). Execute a test inference run on sample MGF spectral data to verify the configured thread count is actually utilized during execution. Monitor system thread usage via logs or system tools to confirm that the InferenceModel respects the cpu_threads setting. The rationale is that TensorFlow-CPU inference can be accelerated by distributing work across multiple cores; the parameter directly controls this parallelism without requiring code changes to the inference pipeline itself.

## Related tools

- **Mass2SMILES TensorFlow-CPU Docker container** (Execution environment providing the InferenceModel class with TensorFlow-CPU backend; cpu_threads parameter is exposed at this level) — https://github.com/volvox292/mass2smiles
- **Docker** (Container runtime for isolating and executing the Mass2SMILES inference with controlled resource allocation)
- **TensorFlow (CPU build)** (Underlying deep learning framework that respects cpu_threads for thread pool configuration in inference execution)
- **Python** (Language for instantiating InferenceModel, passing cpu_threads parameter, and logging/verifying thread usage)

## Examples

```
from mass2smiles import InferenceModel; model = InferenceModel(cpu_threads=128); predictions = model.predict('sample.mgf')
```

## Evaluation signals

- Configured cpu_threads value is accepted by InferenceModel constructor without error
- Inference execution on sample MGF data completes without crashing or hanging
- System-level thread monitoring (e.g., htop, ps, or TensorFlow logs) shows actual thread count matches or approaches configured cpu_threads value
- Inference latency is lower when cpu_threads is increased on multi-core systems, compared to single-threaded or under-provisioned runs
- Verification report documents expected vs. observed thread count with ≤10% deviation tolerance

## Limitations

- TensorFlow-CPU inference speed is fundamentally slower than GPU-accelerated inference; cpu_threads tuning is a mitigation, not a replacement for GPU acceleration.
- Actual thread utilization depends on system load, OS scheduling, and physical core availability; configured cpu_threads may not be fully realized if the system is resource-constrained.
- CDDD model component in Mass2SMILES does not work on newer CUDA drivers, hence the TensorFlow-CPU build; this constraint is fixed at container build time and cannot be changed via cpu_threads alone.
- Increasing cpu_threads beyond available physical cores may cause thread oversubscription and reduce performance rather than improve it.

## Evidence

- [other] cpu_threads parameter controls thread allocation in TensorFlow-CPU Mass2SMILES: "it can be speed up by changing the number of cores: e.g. InferenceModel(cpu_threads=128)"
- [readme] TensorFlow-CPU build is used because CDDD does not work on newer CUDA drivers: "the cddd does not seem to work on newer cuda drivers, therefore it is build using tensorflow cpu"
- [readme] Inference speed improvement is achieved via cpu_threads tuning on CPU build: "Using this setup inference speed is highly improved"
- [other] InferenceModel class accepts cpu_threads as a configurable parameter: "The InferenceModel accepts a configurable cpu_threads parameter (e.g., cpu_threads=128) to adjust the number of CPU cores used during inference"
