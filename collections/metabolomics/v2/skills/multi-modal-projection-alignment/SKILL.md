---
name: multi-modal-projection-alignment
description: Use when you have a mass spectrum and a set of candidate molecular structures, and need to rank candidates by their likelihood of matching the query spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - Python 3.11.7
  - DGL
  - PyTorch
  - RDKit
  - PyTorch Geometric
  - MassSpecGym
  - MVP (HassounLab)
derived_from:
- doi: 10.1101/2025.11.12.688047v1
  title: MVP
evidence_spans:
- 'python_version: 3.11.7'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mvp_cq
    doi: 10.1101/2025.11.12.688047v1
    title: MVP
  dedup_kept_from: coll_mvp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.11.12.688047v1
  all_source_dois:
  - 10.1101/2025.11.12.688047v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-modal-projection-alignment

## Summary

MultiView Projection (MVP) aligns spectral features and molecular descriptors across multiple feature spaces to compute cross-view similarity scores for ranking molecular candidates against a query mass spectrum. This skill is essential when you need to match an unknown spectrum to a set of candidate molecules by aggregating evidence from both spectral and structural representations.

## When to use

Apply this skill when you have a mass spectrum and a set of candidate molecular structures, and need to rank candidates by their likelihood of matching the query spectrum. Specifically, use MVP when your input includes both spectral data (binned or subformula-annotated) and candidate molecules, and you want a ranked list with aggregated cross-modal similarity scores rather than single-modality matching.

## When NOT to use

- Input spectrum is from a well-characterized compound already in a reference library (direct database lookup is faster and more reliable).
- Candidate pool is very small (<5 molecules) or you only have structural similarity without spectral features (use single-modality matching instead).
- Input data lacks preprocessing (fingerprints, consensus spectra, or subformula labels); MVP requires precomputed multi-view features.

## Inputs

- query mass spectrum (TSV or JSON format, optionally with subformula annotations)
- candidate molecular structures (SMILES or molecular graphs)
- precomputed spectral features (fingerprints, consensus spectra, subformula labels)

## Outputs

- ranked candidate list with aggregated similarity scores
- structured output file (JSON or TSV) mapping candidates to scores

## How to apply

Load the query spectrum and candidate molecular structures into memory. Extract or compute spectral features (via binned spectra or subformula labels) and molecular descriptors (fingerprints, graph representations) to create separate views. Apply MultiView Projection to compute cross-view similarity scores between the query spectrum's spectral view and each candidate's molecular view. Aggregate similarity scores across views (the pretrained model on MassSpecGym learns this aggregation). Rank candidates by their aggregated scores in descending order. The rationale is that consensus across independent feature spaces reduces false positives and leverages complementary structural and spectral information.

## Related tools

- **DGL** (Graph neural network library for encoding molecular structures as views)
- **PyTorch** (Deep learning framework for training and inference of MVP model)
- **RDKit** (Molecular toolkit for computing fingerprints and molecular descriptors from SMILES)
- **PyTorch Geometric** (Graph neural network library for molecular graph representations)
- **MassSpecGym** (Reference dataset for pretraining the MVP model on standardized spectra and candidates) — https://github.com/pluskal-lab/MassSpecGym
- **MVP (HassounLab)** (Core implementation of MultiView Projection algorithm for spectra annotation) — https://github.com/HassounLab/MVP

## Examples

```
python test.py --param_pth params_binnedSpec.yaml
```

## Evaluation signals

- Ranked output contains all input candidates with no duplicates or missing entries.
- Aggregated similarity scores are normalized (e.g., in [0, 1]) and sorted in descending order.
- Top-ranked candidate's true molecular identity (if known) appears in top-k results (k typically 1–10 depending on candidate pool size).
- Cross-view scores show expected correlation with spectral and structural similarity (candidates with both high spectral and structural similarity score higher than those with only one).
- Output file schema matches expected format (JSON/TSV with candidate ID, structure, and score fields).

## Limitations

- MVP requires precomputed spectral features (subformula labels or consensus spectra) and molecular descriptors (fingerprints, graphs); raw spectra and SMILES alone are insufficient without preprocessing.
- Performance is trained on MassSpecGym dataset; may not generalize well to spectra from different instruments, ionization modes, or chemical domains not well represented in training data.
- Ranking quality depends on candidate pool composition; if true match is not in the candidate set, MVP will rank the closest incorrect candidate highest.

## Evidence

- [intro] MVP can be used to rank a set of molecular candidates given a spectrum.: "MVP can be used to rank a set of molecular candidates given a spectrum"
- [readme] MultiView Projection (MVP) aligns spectral and molecular views for annotation.: "This repository provides the implementation of MultiView Projection (MVP). MVP can be used to rank a set of molecular candidates given a spectrum."
- [other] Workflow requires spectral feature extraction and molecular descriptor computation.: "Extract or compute spectral features and molecular descriptors (views) for both query and candidates"
- [other] Cross-view similarity scores are aggregated and ranked.: "Apply MultiView Projection to compute cross-view similarity scores between the query spectrum and each candidate. Rank candidates by their aggregated similarity scores in descending order."
- [readme] Data preprocessing includes fingerprints, consensus spectra, and subformula labels.: "We include sample subformula, fingerprint, and consensus spectra data in `../data/sample/`."
- [readme] Model is pretrained on MassSpecGym dataset.: "You can use our pretrained model (on MassSpecGym) to rank molecular candidates by providing the spectra data and a list of candidates."
