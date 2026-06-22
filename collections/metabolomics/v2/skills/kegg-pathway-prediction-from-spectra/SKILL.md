---
name: kegg-pathway-prediction-from-spectra
description: Use when you have untargeted MS2 spectral data (in MS2MP-compatible format) and need to assign KEGG pathway annotations to unknown metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MS2MP
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
  - build: coll_ms2mp_cq
    doi: 10.1021/acs.analchem.4c06875
    title: MS2MP
  dedup_kept_from: coll_ms2mp_cq
schema_version: 0.2.0
---

# kegg-pathway-prediction-from-spectra

## Summary

Use MS2MP, a deep learning framework, to predict KEGG metabolic pathways directly from untargeted tandem mass spectrometry (MS2) spectra. This skill enables high-throughput functional annotation of unknown metabolites without requiring extensive spectral libraries or manual curation.

## When to use

You have untargeted MS2 spectral data (in MS2MP-compatible format) and need to assign KEGG pathway annotations to unknown metabolites. Apply this skill when you want to infer metabolic context and functional roles of detected compounds directly from their fragmentation patterns, particularly in discovery metabolomics workflows where pathway-level interpretation is the goal rather than compound identification alone.

## When NOT to use

- Input spectra are already annotated with high-confidence compound or pathway assignments via alternative methods (e.g., database matching); MS2MP adds processing overhead without new value.
- MS2 data do not conform to MS2MP's required input format or lack the spectral quality needed for deep learning inference (e.g., extremely sparse, low m/z resolution, or missing intensity information).
- Your system does not meet minimum hardware requirements (≥16 GB running memory, ≥256 GB disk space); MS2MP will fail or produce unreliable results under resource constraints.

## Inputs

- MS2 spectral data in MS2MP-compatible format with verified file structure and spectral integrity
- Spectrum identifiers (unique labels for each MS2 spectrum)
- Pre-trained MS2MP deep learning model checkpoint

## Outputs

- Labeled table mapping spectrum identifiers to predicted KEGG pathways
- Pathway predictions for each spectrum (one or more pathway assignments per spectrum)

## How to apply

First, verify that your MS2 input data conform to MS2MP's required file structure and that spectral data integrity is preserved (check for expected m/z ranges, intensity distributions, and header metadata). Load the pre-trained MS2MP deep learning model from the official repository. Run MS2MP inference on your MS2 dataset; the framework processes each spectrum through its learned representations to generate pathway predictions. Parse the model's raw predictions into a labeled output table linking each spectrum identifier to its predicted KEGG pathway(s). Validate that output records are complete (no missing spectrum IDs or pathways) and that confidence scores (if provided) fall within expected ranges [0–1].

## Related tools

- **MS2MP** (Deep learning framework for KEGG pathway prediction from MS2 spectra; processes spectral data through pre-trained neural network to generate pathway annotations) — github.com/ucasaccn/MS2MP

## Evaluation signals

- All input spectra have corresponding output pathway predictions (no missing records in output table).
- Predicted pathway identifiers conform to KEGG nomenclature (valid KEGG pathway IDs present in output).
- Inference completes without out-of-memory errors or hardware-related crashes on systems meeting or exceeding stated minimum requirements (16 GB memory, 256 GB disk).
- Output table schema is consistent: each row contains spectrum ID, pathway ID(s), and any confidence/probability scores in expected numeric ranges.
- Spot-check: manually inspect 5–10 predictions by comparing predicted pathway(s) against spectral fragmentation patterns and known metabolite databases to verify biological plausibility.

## Limitations

- MS2MP requires substantial computational resources (minimum 16 GB running memory and 256 GB disk space); systems below these thresholds will fail or produce degraded results.
- The framework's predictions are contingent on the quality and completeness of the training data; pathways underrepresented in the training set may be predicted with lower accuracy.
- MS2MP outputs pathway-level annotations, not compound identifications; multiple different compounds can map to overlapping pathways, so pathway prediction alone does not uniquely identify metabolites.
- Pre-trained model compatibility may be limited to specific MS2 acquisition parameters (e.g., ionization method, collision energy, m/z range) used during training; spectra from different instrumental configurations may yield less reliable predictions.

## Evidence

- [intro] MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly from untargeted tandem mass spectrometry(MS2).: "MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly from untargeted tandem mass spectrometry(MS2)."
- [readme] Minimum hardware recommendations and tested configurations.: "We recommend that MS2MP should run in a computer with at least 16 G of memory and 256 G of disk space."
- [readme] Demonstrated hardware configurations for running MS2MP.: "We have demonstrated the program's usability on two computers with the following configurations: 1): GPU: Intel® Iris® Xe graphics, CPU: Intel® Core™ i7-12700, Running memory: 128 G, Disk space: 1 T;"
- [other] Workflow step: prepare MS2 input data.: "Prepare MS2 input data in the format required by MS2MP (verify file structure and spectral data integrity)."
- [other] Workflow step: parse model predictions.: "Parse and structure the model predictions into a labeled output table with spectrum identifiers and corresponding KEGG pathway predictions."
