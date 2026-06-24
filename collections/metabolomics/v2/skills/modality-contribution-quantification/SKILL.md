---
name: modality-contribution-quantification
description: Use when when you have a trained multitask model that accepts multiple
  input modalities (e.g., 1D NMR spectra in different nuclei or complementary analytical
  techniques) and you need to understand their relative importance for the downstream
  prediction task (e.g., molecular structure elucidation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0611
  tools:
  - convolutional neural network
  - transformer architecture
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmr2struct
    doi: 10.1021/acscentsci.4c01132
    title: NMR2Struct
  dedup_kept_from: coll_nmr2struct
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.4c01132
  all_source_dois:
  - 10.1021/acscentsci.4c01132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# modality-contribution-quantification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify the independent and joint contributions of individual input modalities (e.g., ¹H NMR, ¹³C NMR) to machine learning model performance by running inference under controlled modality conditions and comparing accuracy metrics. This skill reveals which spectroscopic inputs drive predictions and whether synergy exists between combined modalities.

## When to use

When you have a trained multitask model that accepts multiple input modalities (e.g., 1D NMR spectra in different nuclei or complementary analytical techniques) and you need to understand their relative importance for the downstream prediction task (e.g., molecular structure elucidation). Use this skill when the research question targets individual vs. joint contributions rather than model-wide feature importance.

## When NOT to use

- Input is unimodal (only one type of spectrum or input feature available); modality comparison requires at least two independent input streams.
- Model architecture does not support selective input masking or modality-specific inference paths; joint training without modular design prevents clean isolation of contributions.
- Ground-truth labels or test set are incomplete or differ across modality conditions; comparisons require identical molecular references.

## Inputs

- trained NMR2Struct model checkpoint
- test set with molecular structures (ground truth)
- ¹H NMR spectra (1D array or tensor)
- ¹³C NMR spectra (1D array or tensor)
- molecular labels (formula and connectivity as graphs)

## Outputs

- per-modality accuracy metrics (exact-match for formula, graph edit distance or connectivity F1 for structure)
- error distributions by modality
- synergy quantification (combined accuracy − single-modality baseline)
- tabulated results comparing ¹H-only, ¹³C-only, and combined performance

## How to apply

Load the trained model checkpoint and a held-out test set with ground-truth labels and complete spectra for all modalities. Prepare three separate input batches: (1) ¹H NMR only, (2) ¹³C NMR only, and (3) ¹H + ¹³C combined, ensuring identical molecular ground truth across conditions. Run inference on each batch through the convolutional encoder and transformer architecture to generate predictions (molecular formula and connectivity). Compute accuracy metrics independently for each modality—exact-match accuracy for formula and graph edit distance or connectivity F1 for structure—then quantify synergy as (combined accuracy) − max(single-modality accuracy). Tabulate results by modality showing accuracy, error distribution, and performance gaps to isolate each modality's contribution.

## Related tools

- **convolutional neural network** (encoder that processes individual 1D NMR spectra into learned feature representations for each modality before transformer assembly)
- **transformer architecture** (assembles molecular fragments and structure constraints from encoded modality representations into final molecular structure predictions (formula and connectivity))

## Evaluation signals

- Accuracy scores for each modality (¹H only, ¹³C only, combined) are reported with consistent metrics (e.g., exact-match formula accuracy, F1 for connectivity); combined ≥ individual baselines.
- Synergy metric (combined − max(single)) is non-negative and quantifiable; positive values indicate complementary information between modalities.
- Error distributions (e.g., graphs by prediction type, confusion on molecular substructures) are tabulated separately and show different failure modes per modality, supporting claims of independent contributions.
- Test set molecular structures span similar chemical space (heavy atom count, functional group diversity) across all three inference conditions to ensure fair comparison.
- Modality-specific inference batches are constructed identically except for input spectra; no label leakage or batch-composition confounds.

## Limitations

- The framework demonstrates effectiveness on molecules with up to 19 heavy atoms; performance on larger or more complex structures is not characterized.
- Synergy quantification assumes modality independence in training; if the model was pre-trained on combined modalities, isolated single-modality inference may not reflect true independent contributions.
- Exact-match accuracy for molecular formula and graph edit distance are strict metrics; small prediction errors (e.g., connectivity mismatches on peripheral atoms) count as full failures and may not reflect chemical similarity.
- Test set size and chemical diversity directly affect the robustness of per-modality accuracy estimates; small test sets may yield unstable comparisons.

## Evidence

- [other] modality-contribution-quantification: "Prepare three separate input batches: 1H-only spectra, 13C-only spectra, and 1H+13C combined spectra, with identical molecular ground truth labels."
- [intro] multitask framework capability: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
