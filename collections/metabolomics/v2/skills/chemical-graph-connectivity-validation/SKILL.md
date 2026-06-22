---
name: chemical-graph-connectivity-validation
description: Use when after a machine learning model has generated predicted molecular structures (connectivity graphs and molecular formulas) from 1D NMR spectra. Use it to quantify accuracy on a held-out test set, measure degradation when applying the model beyond its training scope (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_3520
  tools:
  - NMR2Struct model (transformer + CNN architecture)
  - PubChem or equivalent chemical database
  - NMR spectrum simulation or database retrieval tool
  techniques:
  - NMR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-graph-connectivity-validation

## Summary

Validate predicted molecular connectivity graphs against ground-truth structures by comparing bond topology, atom composition, and structural invariants. This skill is essential when assessing whether a structure prediction model (such as NMR2Struct) has correctly recovered the connectivity of a molecule from spectroscopic data.

## When to use

Apply this skill after a machine learning model has generated predicted molecular structures (connectivity graphs and molecular formulas) from 1D NMR spectra. Use it to quantify accuracy on a held-out test set, measure degradation when applying the model beyond its training scope (e.g., molecules >19 heavy atoms), and identify failure modes in structure recovery.

## When NOT to use

- Input NMR spectra are 2D (COSY, HSQC, HMBC) rather than 1D — the framework is designed for 1D ¹H and ¹³C only.
- Ground-truth connectivity is unavailable or ambiguous — validation requires unambiguous reference structures.
- Model has not been trained or fine-tuned; applying validation before model development is premature.

## Inputs

- Pretrained or fine-tuned NMR2Struct model checkpoint (transformer + CNN architecture)
- 1D ¹H and/or ¹³C NMR spectra (simulated, experimental, or database-retrieved)
- Ground-truth molecular structures (connectivity graphs, SMILES, or MOL files)
- Test set molecules with metadata: molecular formula, heavy atom count, IUPAC name or identifier

## Outputs

- Top-1, top-3, top-5 structure recovery accuracy metrics (fraction or percentage)
- Accuracy comparison report: in-scope (≤19 heavy atoms) vs. out-of-scope (>19 heavy atoms) baseline
- Error distribution and failure mode analysis (categorized errors, confidence score distributions)
- Summary report quantifying absolute and relative accuracy degradation

## How to apply

Load the ground-truth molecular connectivity graph (typically as SMILES, MOL file, or graph representation) for each test molecule. Compare the model's predicted connectivity graph to the ground-truth by checking that atoms, bonds, and bond orders match. Compute top-k structure recovery accuracy (fraction of predictions where the top-1, top-3, or top-5 ranked predictions match ground-truth connectivity). Organize results by molecule size (e.g., ≤19 vs. >19 heavy atoms) to detect performance degradation. Document absolute and relative accuracy loss, categorize errors by failure mode (e.g., incorrect bond placement, wrong atom type), and flag any systematic patterns that suggest out-of-scope generalization failure.

## Related tools

- **NMR2Struct model (transformer + CNN architecture)** (End-to-end deep learning model for predicting molecular structure from 1D NMR spectra; generates predicted connectivity graphs and molecular formulas that are compared against ground truth)
- **PubChem or equivalent chemical database** (Source for retrieving or constructing held-out test sets of molecules beyond training scope (>19 heavy atoms) with ground-truth connectivity information)
- **NMR spectrum simulation or database retrieval tool** (Generates or retrieves 1D ¹H and/or ¹³C NMR spectra for each test molecule to feed through the model)

## Evaluation signals

- Top-1 accuracy on in-scope test molecules (≤19 heavy atoms) matches or exceeds the reported baseline from the article.
- Top-k accuracy (k=1,3,5) metrics are computed and reported separately to show ranking quality of predictions.
- Quantified degradation in accuracy for out-of-scope molecules (>19 heavy atoms) relative to in-scope baseline is documented with absolute and relative loss percentages.
- Confidence score distributions are examined: predictions ranked by score should show higher accuracy in top-ranked predictions; low-confidence predictions should correlate with errors.
- Error categories are documented (e.g., wrong bond order, incorrect atom type, missing bonds) to identify systematic failure modes rather than random errors.

## Limitations

- Model effectiveness is bounded to molecules with up to 19 heavy atoms; generalization to larger molecules is uncharacterized and likely degraded.
- Validation requires ground-truth connectivity, which may be expensive or unavailable for large out-of-scope molecules.
- Structure recovery accuracy depends heavily on input NMR spectrum quality (resolution, noise); poor spectra may artificially depress accuracy metrics.
- The framework predicts molecular structure (formula and connectivity) from 1D NMR alone, which may be inherently ambiguous for certain compound classes (e.g., isomers with identical 1D spectra).

## Evidence

- [other] The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized.: "The framework's demonstrated effectiveness is bounded to molecules with up to 19 heavy atoms, establishing a known performance limit beyond which generalization is uncharacterized."
- [other] Compute top-1, top-3, and top-5 structure recovery accuracy (fraction of predictions matching ground-truth connectivity).: "compute top-1, top-3, and top-5 structure recovery accuracy (fraction of predictions matching ground-truth connectivity)"
- [other] Compare out-of-scope accuracy metrics against the reported in-scope baseline (molecules ≤19 heavy atoms) and quantify the absolute and relative degradation.: "Compare out-of-scope accuracy metrics against the reported in-scope baseline (molecules ≤19 heavy atoms) and quantify the absolute and relative degradation"
- [intro] we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra: "a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
- [intro] We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
