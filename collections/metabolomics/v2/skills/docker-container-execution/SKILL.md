---
name: docker-container-execution
description: Use when you have GNPS-style MGF spectral files as input and need to run Mass2SMILES MS/MS-to-structure inference without installing TensorFlow, CUDA, or Python dependencies locally.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Docker
  - Python
  - delser292/mass2smiles:final
  - TensorFlow
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1101/2023.07.06.547963v1
  title: Mass2SMILES
evidence_spans:
- model inference is most effciently performed via the provided docker container
- model inference is most effciently performed via the provided docker container.
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

# docker-container-execution

## Summary

Execute a containerized inference model (Mass2SMILES) on spectral data by mounting input/output directories and passing MGF files to a Docker container. This skill encapsulates deployment, parameter tuning, and batch inference for MS/MS-to-structure prediction without local dependency installation.

## When to use

You have GNPS-style MGF spectral files as input and need to run Mass2SMILES MS/MS-to-structure inference without installing TensorFlow, CUDA, or Python dependencies locally. Use this when you want reproducible, containerized execution with tunable CPU thread allocation (via the cpu_threads parameter) on a TensorFlow-CPU or GPU build.

## When NOT to use

- Your spectral data is not in MGF format (e.g., mzML, NetCDF, or proprietary vendor formats) without prior conversion.
- You require GPU-accelerated inference and have CUDA driver incompatibility issues that are unresolved (note: the README reports CUDA driver issues motivated the TensorFlow-CPU build).
- You need real-time or streaming inference rather than batch processing of complete MGF files.

## Inputs

- MGF file (GNPS-style spectral data)
- input directory path (host machine)
- output directory path (host machine)
- cpu_threads parameter (integer, optional)

## Outputs

- predicted SMILES structures (text output in output directory)
- inference log or report (optional)

## How to apply

First, pull or load the delser292/mass2smiles:final Docker container (or build from the Dockerfile in Zenodo 14778327). Prepare an input directory containing your GNPS-style MGF files and designate an output directory for predicted SMILES structures. Mount both directories as volumes when running the container. If using the TensorFlow-CPU build, instantiate the InferenceModel with a configurable cpu_threads parameter (e.g., cpu_threads=128) to tune CPU core allocation for your hardware. Execute the container with the mounted paths and MGF filename, then collect the predicted SMILES output files from the mounted output directory.

## Related tools

- **Docker** (container runtime for reproducible isolation and deployment of the Mass2SMILES inference engine with pre-configured dependencies) — https://www.docker.com
- **delser292/mass2smiles:final** (containerized Mass2SMILES model with TensorFlow-CPU or GPU inference backend) — https://zenodo.org/records/7883491
- **TensorFlow** (deep learning framework underlying the Mass2SMILES transformer model; TensorFlow-CPU build is used to avoid CUDA driver incompatibilities)
- **Python** (scripting language for the Mass2SMILES inference pipeline (mass2smiles_transformer.py)) — https://github.com/volvox292/mass2smiles

## Examples

```
docker run -v c:/your_path/to_the_folder/mass2smiles/:/app mass2smiles:transformer_v1 conda run -n tf python app/mass2smiles_transformer.py your_mgf_file.mgf /app
```

## Evaluation signals

- Output directory contains one or more SMILES structure files corresponding to each input MGF file (1:1 mapping).
- Predicted SMILES strings are valid (match SMILES grammar and can be parsed by chemistry libraries like RDKit).
- Actual CPU thread count observed during inference execution matches or is ≤ the configured cpu_threads parameter (verification via system monitoring or container logs).
- Inference completes without Docker runtime errors or OOM (out-of-memory) exceptions.
- Output file timestamps are later than container execution start time, confirming fresh inference rather than cached results.

## Limitations

- CUDA driver incompatibilities motivated the TensorFlow-CPU build, resulting in slower inference compared to GPU execution; the article notes 'inference speed is highly improved' only when GPU is available and properly configured.
- The container requires valid directory mount paths; misconfigured host paths will cause runtime failures or produce empty output directories.
- No changelog is available; version pinning and reproducibility tracking across updates (e.g., between Zenodo 7883491 and 14778327) may be unclear.
- MGF files must follow GNPS-style format conventions; non-standard or malformed spectra may cause silent failures or degraded prediction quality.

## Evidence

- [readme] Spectral data can be provided as MGF files (GNPS-syle) and model inference is most effciently performed via the provided docker container.: "Spectral data can be provided as MGF files (GNPS-syle) and model inference is most effciently performed via the provided docker container."
- [readme] the container is available as tarball in supplementary or via docker pull delser292/mass2smiles:final: "the container is available as tarball in supplementary or via docker pull delser292/mass2smiles:final"
- [intro] InferenceModel accepts a configurable cpu_threads parameter to adjust CPU cores used during inference: "The InferenceModel accepts a configurable cpu_threads parameter (e.g., cpu_threads=128) to adjust the number of CPU cores used during inference"
- [readme] You need to point to your input and output dir, now the mass2smiles model is built into the container.: "You need to point to your input and output dir, now the mass2smiles model is built into the container."
- [readme] the cddd does not seem to work on newer cuda drivers, therefore it is build using tensorflow cpu: "the cddd does not seem to work on newer cuda drivers, therefore it is build using tensorflow cpu"
