---
name: tandem-ms-spectral-data-interpretation
description: Use when you have untargeted MS2 spectral data in MS2MP-compatible format
  and need to assign KEGG pathway annotations to spectra without spectral library
  matching or manual compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MS2MP
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c06875
  title: MS2MP
evidence_spans:
- MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly
  from untargeted tandem mass spectrometry(MS2)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c06875
  all_source_dois:
  - 10.1021/acs.analchem.4c06875
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-ms-spectral-data-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply deep learning-based MS2MP framework to predict KEGG metabolic pathways directly from untargeted tandem mass spectrometry (MS2) spectra without requiring prior compound identification. This skill bridges the gap between raw spectral data and functional pathway annotation by leveraging pre-trained neural networks.

## When to use

You have untargeted MS2 spectral data in MS2MP-compatible format and need to assign KEGG pathway annotations to spectra without spectral library matching or manual compound identification. Use this when your analysis goal is pathway-level functional interpretation rather than individual metabolite structure elucidation.

## When NOT to use

- Input is already annotated with confident compound identifications; use targeted quantification or structure-based pathway mapping instead.
- MS2 spectra are from highly unusual or non-standard ionization methods not represented in MS2MP training data.
- Your system cannot meet minimum hardware requirements (16 GB RAM, 256 GB disk space).

## Inputs

- untargeted MS2 spectra (in MS2MP-compatible format)
- spectrum identifiers or run metadata
- pre-trained MS2MP model weights (from repository)

## Outputs

- spectrum-to-KEGG pathway prediction table (spectrum ID × pathway annotation)
- confidence scores or prediction probabilities (if model outputs them)

## How to apply

First, verify that your MS2 spectral input data conforms to MS2MP's required file structure and validates spectral data integrity (m/z values, intensity distributions, spectrum metadata). Load the pre-trained MS2MP deep learning model from the official repository. Run MS2MP inference on the prepared MS2 input to generate KEGG pathway predictions for each spectrum, specifying batch processing parameters if available. Parse and structure the model output into a labeled table mapping spectrum identifiers to their corresponding KEGG pathway predictions. Validate output by checking that all input spectra received predictions and that pathway annotations fall within expected KEGG categories for your sample type.

## Related tools

- **MS2MP** (Deep learning framework for inference of KEGG pathway predictions from MS2 spectral feature vectors) — https://github.com/ucasaccn/MS2MP

## Evaluation signals

- All input spectra receive a KEGG pathway prediction; no spectra are dropped or marked as 'no prediction'.
- Predicted pathways are valid KEGG identifiers and match expected metabolic categories for your sample matrix (e.g., amino acid or lipid metabolism for biological samples).
- Output table structure is consistent: each row represents one spectrum, columns include spectrum ID and pathway annotation with no missing values in the pathway field.
- Inference completes within a reasonable time frame relative to the number of spectra and your system hardware (benchmark against documented runtime on similar configurations).
- When rerun on the same input data, predictions are identical (model inference is deterministic).

## Limitations

- MS2MP predictions are pathway-level; they do not provide individual compound structure or exact mass assignments.
- Model performance depends on training data composition; spectra from underrepresented ionization methods or novel compounds may receive low-confidence or erroneous predictions.
- Minimum 16 GB RAM and 256 GB disk space required; high-confidence performance demonstrated on systems with 64–128 GB RAM.
- Pre-trained model is fixed; retraining or fine-tuning on custom MS2 datasets is not addressed in the framework documentation.

## Evidence

- [readme] MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly from untargeted tandem mass spectrometry(MS2).: "MS2MP is a novel deep learning-based framework for KEGG pathway prediction directly from untargeted tandem mass spectrometry(MS2)."
- [readme] Minimum hardware requirements are 16 GB memory and 256 GB disk space, with tested configurations on Intel Iris Xe and NVIDIA RTX 4090 systems.: "We recommend that MS2MP should run in a computer with at least 16 G of memory and 256 G of disk space."
- [other] Workflow steps include data preparation, model loading, inference execution, and output structuring.: "1. Prepare MS2 input data in the format required by MS2MP (verify file structure and spectral data integrity). 2. Load the pre-trained MS2MP deep learning model from the repository. 3. Run MS2MP"
- [readme] Demonstrated compatibility on systems with Intel Core i7-12700 CPU with 128 GB memory and AMD Ryzen 9 9950X CPU with 64 GB memory.: "We have demonstrated the program's usability on two computers with the following configurations: 1): GPU: Intel® Iris® Xe graphics, CPU: Intel® Core™ i7-12700, Running memory: 128 G, Disk space: 1 T;"
