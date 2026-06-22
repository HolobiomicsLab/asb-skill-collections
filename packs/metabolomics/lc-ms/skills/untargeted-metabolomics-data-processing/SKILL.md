---
name: untargeted-metabolomics-data-processing
description: Use when you have untargeted MS2 spectral data (from LC-MS/MS or similar instruments) and need to assign metabolic pathway context to detected compounds when standard spectral library matching is unavailable or insufficient.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MS2MP
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.4c06875
  title: MS2MP
evidence_spans:
- MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly from untargeted tandem mass spectrometry(MS2)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_m2s
    doi: 10.1021/acs.analchem.1c03592
    title: m2s
  - build: coll_ms2mp_cq
    doi: 10.1021/acs.analchem.4c06875
    title: MS2MP
  dedup_kept_from: coll_ms2mp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06875
  all_source_dois:
  - 10.1021/acs.analchem.4c06875
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# untargeted-metabolomics-data-processing

## Summary

Process untargeted tandem mass spectrometry (MS2) spectra through a deep learning framework to predict KEGG metabolic pathways directly from spectral data. This skill enables functional annotation of unknown metabolites by leveraging pre-trained models that map MS2 fragmentation patterns to known biochemical pathways.

## When to use

You have untargeted MS2 spectral data (from LC-MS/MS or similar instruments) and need to assign metabolic pathway context to detected compounds when standard spectral library matching is unavailable or insufficient. Apply this skill when your research goal requires connecting individual spectra to KEGG pathway predictions rather than simple compound identification.

## When NOT to use

- Input spectra are from targeted metabolomics experiments where compound identity is already known or constrained to a small validated set.
- Spectral data does not meet MS2MP format requirements or file structure integrity checks fail.
- Available hardware falls below minimum requirements (16 GB RAM, 256 GB disk space).

## Inputs

- MS2 spectral data in MS2MP-compatible format
- Pre-trained MS2MP deep learning model

## Outputs

- Labeled output table with spectrum identifiers and KEGG pathway predictions
- Spectrum-to-pathway mapping

## How to apply

Prepare MS2 spectral input data in the format required by MS2MP, verifying file structure and spectral data integrity. Load the pre-trained MS2MP deep learning model from the official repository. Execute MS2MP inference on the MS2 input data to generate KEGG pathway predictions for each spectrum. Parse and structure the model predictions into a labeled output table mapping spectrum identifiers to their corresponding KEGG pathway assignments. The framework requires a minimum of 16 GB running memory and 256 GB disk space; Intel Iris Xe (with Intel Core i7-12700, 128 GB RAM) or NVIDIA GeForce RTX 4090 (with AMD Ryzen 9 9950X, 64 GB RAM) configurations have been verified as compatible.

## Related tools

- **MS2MP** (Deep learning framework that performs inference on MS2 spectra to predict KEGG pathway assignments) — github.com/ucasaccn/MS2MP

## Evaluation signals

- All input MS2 spectra are successfully loaded and processed without format errors or data integrity failures.
- Output table contains one KEGG pathway prediction per input spectrum with no missing values in the mapping.
- Pathway predictions are drawn from the KEGG database and correspond to known metabolic pathways.
- Model inference completes within expected runtime on verified hardware configurations (Intel Iris Xe or NVIDIA RTX 4090 systems).
- Spectrum identifiers in the output table are consistently mapped to their corresponding input spectra with no duplicates or omissions.

## Limitations

- MS2MP is optimized for untargeted metabolomics and may not perform well on spectra from highly specialized or underrepresented compound classes not well-represented in the training data.
- Prediction accuracy depends on spectral quality; low signal-to-noise spectra or poor fragmentation may yield unreliable pathway assignments.
- The framework requires substantial computational resources; systems with less than 16 GB memory or 256 GB disk space are not supported.
- Output is constrained to KEGG pathway predictions; users cannot predict pathways outside the KEGG database scope.

## Evidence

- [readme] MS2MP requires minimum specifications and tested configurations: "We recommend that MS2MP should run in a computer with at least 16 G of memory and 256 G of disk space."
- [intro] MS2MP is a deep learning framework for pathway prediction from MS2 spectra: "MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly from untargeted tandem mass spectrometry(MS2)."
- [readme] Tested hardware configurations for MS2MP: "GPU: Intel® Iris® Xe graphics; CPU: Intel® Core™ i7-12700; Running memory: 128 G or GPU: NVIDIA® GeForce RTX™ 4090; CPU: AMD Ryzen™ 9 9950X; Running memory: 64 G"
- [other] Workflow for MS2MP inference and output structuring: "Run MS2MP inference on the MS2 input data to generate KEGG pathway predictions for each spectrum. Parse and structure the model predictions into a labeled output table with spectrum identifiers and"
