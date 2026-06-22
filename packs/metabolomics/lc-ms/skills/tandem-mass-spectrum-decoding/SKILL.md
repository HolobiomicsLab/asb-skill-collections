---
name: tandem-mass-spectrum-decoding
description: Use when when you have raw predictions from a trained fragment generation or intensity prediction neural network model and need to convert those predictions into a standard spectrum file format (m/z–intensity pairs) for comparison against experimental spectra or for structural elucidation workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - ms-pred
  - ICEBERG WebUI
  - ICEBERG
  - ms-pred repository
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans:
- github.com__samgoldman97__ms-pred
- You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_fragmentation_graph_generation_cq
    doi: 10.1021/acs.analchem.3c04654
    title: ICEBERG / fragmentation graph generation
  dedup_kept_from: coll_iceberg_fragmentation_graph_generation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04654
  all_source_dois:
  - 10.1021/acs.analchem.3c04654
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-mass-spectrum-decoding

## Summary

Decode neural network outputs from mass spectrum prediction models (e.g., ICEBERG) into structured tandem mass spectra by converting predicted fragment tokens and intensity scores into m/z and intensity pairs. This skill bridges learned molecular fragmentation predictions and interpretable experimental spectrum formats.

## When to use

When you have raw predictions from a trained fragment generation or intensity prediction neural network model and need to convert those predictions into a standard spectrum file format (m/z–intensity pairs) for comparison against experimental spectra or for structural elucidation workflows. Specifically triggered when ICEBERG or similar models output fragment tokens and intensity logits that require post-processing into spectrum coordinates.

## When NOT to use

- Input is experimental (measured) spectrum data — no decoding needed; import directly.
- Only chemical formula predictions are required; use SCARF instead, which predicts at formula level without fragment decoding.
- Model outputs are already in m/z–intensity format — decoding is redundant.

## Inputs

- Fragment generation model predictions (token logits or argmax predictions)
- Intensity predictor model outputs (per-fragment intensity scores)
- Model vocabulary mapping (fragment tokens to molecular structures or m/z values)
- Pretrained ICEBERG model weights (gen_ckpt and inten_ckpt)

## Outputs

- Tandem mass spectrum (m/z and intensity pairs)
- Structured spectrum file (MGF, SDF, or JSON format)
- Spectrum object suitable for retrieval or comparison against PubChem candidates

## How to apply

After running inference on the trained fragment generator (which predicts molecular fragments via a DAG model) and intensity predictor (which scores those fragments), decode the model outputs by: (1) converting predicted fragment token IDs back to molecular structures or m/z values using the model's vocabulary; (2) retrieving the corresponding predicted intensities from the intensity model output; (3) pairing each decoded m/z with its intensity score; (4) filtering or thresholding low-confidence predictions if needed; (5) formatting the m/z–intensity pairs into a structured spectrum object or MGF/SDF file. The decoding step is essential because ICEBERG predicts at fragment-level granularity (not just chemical formula), requiring explicit reconstruction of the fragmentation graph into observable m/z values.

## Related tools

- **ICEBERG** (Fragment-level tandem mass spectrum prediction model whose outputs are decoded into spectrum format by this skill) — https://github.com/coleygroup/ms-pred
- **ms-pred repository** (Provides training, inference, and decoding utilities for spectrum prediction and reconstruction) — https://github.com/coleygroup/ms-pred
- **ICEBERG WebUI** (Web interface that abstracts spectrum decoding and ranking against PubChem candidates) — http://iceberg-ms.mit.edu/

## Examples

```
python src/ms_pred/dag_pred/predict_smis.py --input_smiles 'CCO' --gen_ckpt models/gen.pt --inten_ckpt models/inten.pt --output_spectrum spectrum.json
```

## Evaluation signals

- Decoded spectrum contains non-empty list of m/z–intensity pairs with positive, finite values.
- m/z values fall within expected range for molecular ion and fragment ions (e.g., 50–500 m/z for small molecules).
- Intensity values sum to a normalized total (e.g., sum = 1.0 or max = 100) as per spectrum file format convention.
- Decoded spectrum can be compared against experimental spectra using spectral similarity metrics (e.g., cosine similarity > 0.5 indicates reasonable decoding).
- Spectrum structure is compatible with retrieval pipeline and ranks candidate molecules from PubChem as expected.

## Limitations

- Decoding quality depends on model accuracy; poor fragment or intensity predictions will yield uninformative spectra.
- Fragment vocabulary size and coverage determine whether predicted fragments can be mapped to valid m/z values; out-of-vocabulary predictions may be dropped or cause decoding errors.
- ICEBERG predictions are trained on collision-energy-annotated spectra (NIST'20 only); transferring to other collision energies or ionization modes without retraining may degrade decoding fidelity.
- The decoding process assumes a single ionization mode and adduct type; multi-adduct scenarios require separate model runs and post-hoc merging.
- GPU memory constraints during inference (especially on small GPUs) may require batch size reduction, affecting throughput.

## Evidence

- [other] Pass the molecular representation through the ICEBERG neural network to generate fragment-level predictions. Decode model outputs to construct predicted tandem mass spectrum (m/z and intensity pairs).: "Pass the molecular representation through the ICEBERG neural network to generate fragment-level predictions. Decode model outputs to construct predicted tandem mass spectrum"
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula"
- [readme] This repository contains implementations for the following spectrum simulator models predicting molecular tandem mass spectra from molecules: ICEBERG: [Inferring CID by Estimating Breakage Events and Reconstructing their Graphs]: "spectrum simulator models predicting molecular tandem mass spectra from molecules: ICEBERG"
- [readme] An example of how to use ICEBERG for structural elucidation campaigns can be found at notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb: "An example of how to use ICEBERG for structural elucidation campaigns can be found at notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb"
- [readme] Get pretrained ICEBERG model weights. You can either train the model by yourself; Or if you have an NSIT'20 license (or newer), you can email the maintainer with a proof of license; Or you can download the weights trained on the MassSpecGym dataset: "Get pretrained ICEBERG model weights. You can either train the model by yourself"
