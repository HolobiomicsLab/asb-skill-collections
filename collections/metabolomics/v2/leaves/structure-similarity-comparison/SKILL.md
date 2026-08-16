---
name: structure-similarity-comparison
description: Use when after executing a molecular structure prediction model on spectroscopic
  input data and obtaining predicted molecular structures in a standardized format
  (e.g., SMILES, MOL, SDF).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_3318
  tools:
  - MultiModalSpectralTransformer
  - RDKit
  techniques:
  - NMR
  license_tier: open
derived_from:
- doi: 10.1002/ange.202517611
  title: MMST
evidence_spans:
- github.com/mpriessner/MultiModalSpectralTransformer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mmst_cq
    doi: 10.1002/ange.202517611
    title: MMST
  dedup_kept_from: coll_mmst_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/ange.202517611
  all_source_dois:
  - 10.1002/ange.202517611
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# structure-similarity-comparison

## Summary

Compare predicted molecular structures against reference outputs using structural similarity metrics or exact-match validation to assess prediction accuracy. This skill evaluates whether a transformer-based spectroscopic model has correctly inferred molecular connectivity and stereochemistry from multimodal spectra (NMR, HSQC, COSY, IR).

## When to use

After executing a molecular structure prediction model on spectroscopic input data and obtaining predicted molecular structures in a standardized format (e.g., SMILES, MOL, SDF). The input should include both predicted structures and reference (ground-truth) structures from the same dataset or validation set. Use this skill to quantify prediction accuracy before deployment or publication.

## When NOT to use

- Predicted structures have not yet been generated or are in an incompatible format (e.g., raw model embeddings rather than chemical structure notation).
- Reference structures are unavailable or not aligned with the predicted set (e.g., different dataset or incompletely labeled validation data).
- The goal is to evaluate model performance on a held-out test set without ground truth; use ablation studies or cross-validation instead.

## Inputs

- Predicted molecular structures (SMILES strings, MOL files, or SDF format from model output)
- Reference molecular structures (ground-truth SMILES, MOL, or SDF from validation dataset)
- Mapping between predicted and reference structures (indices, identifiers, or pairing metadata)

## Outputs

- Per-structure similarity scores (numeric values, typically 0–1 range)
- Exact-match binary flags (true/false for each structure pair)
- Comparison report documenting prediction accuracy metrics and structural discrepancies
- Flagged failures or low-similarity cases for manual inspection

## How to apply

Load predicted molecular structures and reference structures into a comparison framework. Apply structural similarity metrics (e.g., Tanimoto similarity on molecular fingerprints, graph isomorphism checks, or SMILES canonicalization matching) to compute pairwise similarity scores. For exact-match validation, perform atom-by-atom and bond-by-atom topological comparison using chemistry libraries (e.g., RDKit). Aggregate per-structure similarity scores into a comparison report documenting prediction accuracy (e.g., percentage of structures matching above a threshold, mean similarity score) and flag structural discrepancies (missing atoms, incorrect stereochemistry, wrong connectivity). The rationale is that high similarity or exact matches indicate the model has learned spectroscopic-to-structure mappings correctly; low similarity or failures reveal systematic errors in the model or particular spectral modality weaknesses.

## Related tools

- **MultiModalSpectralTransformer** (Generates predicted molecular structures from spectroscopic modalities; outputs are passed to comparison step.) — https://github.com/mpriessner/MultiModalSpectralTransformer
- **RDKit** (Computes molecular fingerprints, similarity metrics (Tanimoto), graph isomorphism checks, and canonicalization for structural comparison.)

## Evaluation signals

- Exact-match rate: percentage of predicted structures that match reference structures exactly (100% similarity or canonical SMILES equality).
- Mean and median similarity scores across all structure pairs; scores > 0.85–0.90 typically indicate good prediction performance.
- Distribution of discrepancies: identify systematic errors (e.g., consistently missed functional groups, incorrect stereochemistry) by analyzing low-similarity outliers.
- Per-modality accuracy: stratify comparison by input spectroscopic modality (NMR vs. IR vs. HSQC+COSY) to diagnose which modalities contribute to errors.
- Reproducibility: verify that comparison metrics are deterministic and independent of structure ordering or SMILES canonicalization rules.

## Limitations

- Structural similarity metrics are sensitive to molecular fingerprint choice and threshold selection; identical molecules may yield different similarity scores depending on the algorithm (Tanimoto, Dice, overlap) and bit-length.
- SMILES canonicalization and stereochemical representation vary across chemistry software; canonical SMILES matching may fail even for identical structures if generated by different tools.
- Exact-match validation assumes ground-truth reference structures are correctly labeled and complete; errors in reference data will inflate failure rates.
- The skill does not distinguish between minor structural variations (e.g., tautomers, regioisomers) that may be chemically distinct but highly similar; domain expertise is needed to interpret borderline cases.
- Computational cost scales with dataset size; comparing large structure libraries (>10k compounds) may require distributed or approximate similarity methods.

## Evidence

- [full_text] Compare predicted structures against reference outputs using structural similarity metrics or exact-match validation.: "Compare predicted structures against reference outputs using structural similarity metrics or exact-match validation."
- [full_text] Retrieve reference molecular structure predictions from the GitHub repository or Zenodo deposits.: "Retrieve reference molecular structure predictions from the GitHub repository or Zenodo deposits."
- [full_text] Generate a comparison report documenting prediction accuracy and any structural discrepancies.: "Generate a comparison report documenting prediction accuracy and any structural discrepancies."
- [readme] MultiModalSpectralTransformer is a transformer-based architecture that integrates various spectroscopic modalities (NMR, HSQC, COSY, IR) for automated molecular structure prediction: "MultiModalSpectralTransformer is a transformer-based architecture that integrates various spectroscopic modalities (NMR, HSQC, COSY, IR) for automated molecular structure prediction"
