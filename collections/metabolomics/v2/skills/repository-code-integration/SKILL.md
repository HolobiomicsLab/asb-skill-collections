---
name: repository-code-integration
description: Use when you have identified a published method (e.g., MIST-CF for chemical
  formula ranking from mass spectra) whose source code and trained weights are available
  in a public repository, and you need to apply that method to new experimental data
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0573
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3473
  tools:
  - MIST
  - SCARF
  - MIST-CF
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum
  using an end-to-end energy based modeling approach
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Repository Code Integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate published research code from a versioned repository (clone, install dependencies, instantiate trained models) to enable reproducible application of a computational method on new data. This skill is essential when a research article describes a novel algorithm or model whose implementation is released publicly.

## When to use

You have identified a published method (e.g., MIST-CF for chemical formula ranking from mass spectra) whose source code and trained weights are available in a public repository, and you need to apply that method to new experimental data (e.g., unknown MS/MS spectra) or validate the method's outputs against reference data. The article explicitly names the repository URL and provides setup instructions.

## When NOT to use

- The article does not provide a public repository URL or code is explicitly unavailable (e.g., proprietary or behind access restrictions).
- You require extensive model retraining on custom data and the repository provides only pre-trained weights without training scripts.
- The method has been superseded by a newer version with breaking API changes and you need to reproduce results from the exact paper version.

## Inputs

- GitHub repository URL (e.g., samgoldman97/mist-cf)
- Installation environment specification (environment.yml, requirements.txt)
- Experimental data in expected format (e.g., MGF mass spectrum files, chemical formula strings)
- Pre-trained model checkpoint (downloaded via provided script)
- Configuration YAML file specifying hyperparameters and model settings

## Outputs

- Installed Python package and environment with all dependencies
- Instantiated neural network model loaded from checkpoint
- Model predictions on input data (e.g., ranked chemical formula candidates with scores)
- Validation metrics or comparison statistics (e.g., top-k accuracy, ranking agreement)
- Structured output files (e.g., CSV, JSON) with predictions and metadata

## How to apply

Clone the named repository (e.g., samgoldman97/mist-cf) using git, then follow the repository's documented install sequence (e.g., create a conda environment from environment.yml, install pip requirements, run setup.py develop). Download any required pre-trained model weights or auxiliary tools (e.g., SIRIUS for formula enumeration) using the provided scripts (e.g., quickstart/download_model.sh). Verify the installation by running a quickstart example (e.g., predicting on 10 demo spectra from data/demo_specs.mgf). For your own data, prepare inputs in the expected format (e.g., MGF for mass spectra), then invoke the model's predict script with appropriate configuration. Compare outputs against reference results or expected numerical ranges (e.g., L2 distance < 1e-6 for embedding reproducibility) to confirm correctness.

## Related tools

- **MIST-CF** (Primary formula-transformer model for ranking chemical formula and adduct assignments from tandem MS data without database lookup) — https://github.com/samgoldman97/mist-cf
- **SCARF** (Source of sinusoidal formula embeddings technique adopted by MIST-CF for improved chemical formula representation)
- **SIRIUS** (Auxiliary tool providing dynamic programming formula enumeration (SIRIUS decomp) to generate candidate formulae for a given MS1 mass; integrated into MIST-CF workflow) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST** (Baseline spectrum-transformer architecture for MS annotation that MIST-CF extends with formula-specific components)

## Examples

```
git clone https://github.com/samgoldman97/mist-cf && cd mist-cf && mamba env create -f environment.yml && mamba activate ms-gen && pip install -r requirements.txt && python setup.py develop && bash quickstart/download_model.sh && bash quickstart/run_model.sh
```

## Evaluation signals

- Installation completes without errors; conda environment activates and all imports resolve successfully.
- Quickstart prediction on demo data (e.g., 10 CASMI22 spectra) produces output files with expected schema and no NaN or inf values.
- Embedding vectors match reference outputs from the paper with numerical tolerance (e.g., L2 distance < 1e-6 for sinusoidal embeddings, confirming reproducibility).
- Model predictions on test data fall within reported performance ranges (e.g., top-1 accuracy within ±2% of published results on NPLIB1 test set).
- Output rankings are sensible for known molecular formulae: correct formula ranks in top-k (e.g., top-5) for majority of spectra.

## Limitations

- Pre-trained NIST20-trained models are available only upon request to users with a NIST license; publicly released model (trained on NPLIB1 only) may be less performant on high-resolution Orbitrap data.
- SIRIUS dependency requires download and PATH configuration; non-Linux users must manually obtain and configure the binary from the SIRIUS website.
- Repository code currently supports only positive-mode MS/MS spectra; negative-mode or multi-charge states are not yet handled.
- Setup and data preprocessing pipelines are data-dependent; exact reproduction of paper experiments requires access to proprietary NIST20 dataset in addition to public NPLIB1 subset.

## Evidence

- [readme] Utilizing sinusoidal formula embeddings as developed in our previous work SCARF: "Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF](https://arxiv.org/abs/2303.06470)"
- [readme] Clone repository and run setup: "After git cloning the repository, the enviornment and package can be installed using [Mamba](https://mamba.readthedocs.io/en/latest/installation.html)"
- [readme] Download model and run quickstart: "We have released a trained MIST-CF model (using the public NPLIB1/CANOPUS dataset). This can be downloaded (`quickstart/download_model.sh`) and used to predict a set of 10 spectra from CASMI22"
- [readme] SIRIUS integration and PATH setup: "SIRIUS can be downloaded and moved into a respective folder using the following commands. For non linux based systems, we suggest visiting the [SIRIUS"
- [readme] NIST20 model availability and performance caveat: "Model output will be saved in `quickstart/mist_cf_out/`. This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution"
- [other] Verify embedding reproducibility: "Compare produced embeddings against reference outputs from the MIST-CF repository using numerical tolerance (e.g., L2 distance < 1e-6) to confirm reproducibility."
