---
name: chemical-similarity-metrics-evaluation
description: Use when after training a sequence-to-sequence decoder that reconstructs
  SMILES strings from fixed-size embeddings (e.g., from MS/MS spectra), use this skill
  to measure reconstruction fidelity on held-out test embeddings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0154
  tools:
  - RDKit
  - PyTorch
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s42004-023-00932-3
  title: Spec2Mol
evidence_spans:
- Processing of the chemical data is based on the [RDKit](https://www.rdkit.org/)
  software.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spec2mol_cq
    doi: 10.1038/s42004-023-00932-3
    title: Spec2Mol
  dedup_kept_from: coll_spec2mol_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42004-023-00932-3
  all_source_dois:
  - 10.1038/s42004-023-00932-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-similarity-metrics-evaluation

## Summary

Evaluate decoder reconstruction quality by measuring exact-match accuracy and Tanimoto similarity between reconstructed SMILES strings and reference molecules. This skill quantifies how faithfully a decoder has recovered molecular structure from a latent embedding.

## When to use

After training a sequence-to-sequence decoder that reconstructs SMILES strings from fixed-size embeddings (e.g., from MS/MS spectra), use this skill to measure reconstruction fidelity on held-out test embeddings. Apply when you need to validate that the decoder has learned a meaningful mapping from continuous embeddings back to discrete molecular graphs.

## When NOT to use

- Decoder has not been trained yet—evaluate only after training is complete and weights are frozen.
- Input embeddings are from the training set rather than held-out test data—this will inflate metrics and obscure generalization.
- Reference SMILES strings are not in canonical form—non-canonical forms of the same molecule will be marked as mismatches.

## Inputs

- Trained decoder PyTorch model checkpoint
- Test set of encoder-produced embeddings (fixed-size vectors)
- Reference SMILES strings for test molecules
- SMILES tokenizer configuration

## Outputs

- Exact-match accuracy (fraction of predictions matching reference SMILES exactly)
- Per-molecule Tanimoto similarity scores
- Aggregated test set metrics (mean Tanimoto, accuracy)

## How to apply

Run inference on the trained decoder using held-out test embeddings to generate predicted SMILES strings. For each prediction, compute two metrics: (1) exact-match accuracy—a binary indicator of whether the predicted SMILES is character-for-character identical to the reference SMILES—and (2) Tanimoto similarity, which measures structural overlap by comparing the binary fingerprints of reconstructed and reference molecules computed via RDKit. Report both metrics aggregated over the test set. Use canonical SMILES representations to ensure consistent string comparison. Tanimoto similarity captures partial credit for chemically plausible but non-identical reconstructions, whereas exact-match reveals whether the decoder recovered the precise target structure.

## Related tools

- **RDKit** (Decodes predicted SMILES strings to molecular graphs and computes Tanimoto fingerprint similarity) — https://www.rdkit.org/
- **PyTorch** (Loads trained decoder model and executes inference on test embeddings)

## Evaluation signals

- Exact-match accuracy is typically non-zero; a completely random decoder would score near 0% unless the dataset is very small or SMILES diversity is limited.
- Mean Tanimoto similarity is substantially higher than exact-match accuracy, reflecting partial credit for structurally similar but non-identical reconstructions.
- Tanimoto scores fall in the range [0, 1]; any value outside this range indicates an error in fingerprint computation or similarity calculation.
- Predictions can be re-encoded via RDKit without error (valid SMILES); invalid SMILES strings indicate decoder failure to respect syntax constraints.
- Aggregated metrics on the test set should be stable when computed in multiple runs if the model is deterministic; high variance may indicate overfitting or data leakage.

## Limitations

- Exact-match accuracy is a strict metric and may underestimate decoder competence; isomeric SMILES (different string representations of the same molecule) are marked as failures.
- Tanimoto similarity depends on RDKit fingerprint choice (e.g., Morgan, ECFP); results may vary if fingerprint type is not specified or documented.
- The evaluation assumes that reference SMILES are correct and in canonical form; errors or inconsistencies in reference data will confound results.
- Reconstruction of very large or rare molecular scaffolds may have low accuracy due to limited training data, even if the decoder is well-trained.
- No changelog or versioning information is available for the Spec2Mol repository, making reproducibility across versions uncertain.

## Evidence

- [other] Evaluate decoder on held-out test embeddings by measuring exact-match accuracy and Tanimoto similarity of reconstructed vs. reference molecules: "Evaluate decoder on held-out test embeddings by measuring exact-match accuracy and Tanimoto similarity of reconstructed vs. reference molecules (decoded via RDKit)."
- [readme] The decoder reconstructs the molecular structure, in a SMILES format, given the embedding that the encoder generates.: "The decoder reconstructs the molecular structure, in a SMILES format, given the embedding that the encoder generates."
- [other] Train the decoder end-to-end using cross-entropy loss on SMILES token prediction, with teacher forcing during training.: "Train the decoder end-to-end using cross-entropy loss on SMILES token prediction, with teacher forcing during training."
- [readme] Processing of the chemical data is based on the RDKit software.: "Processing of the chemical data is based on the [RDKit](https://www.rdkit.org/) software."
- [other] Prepare SMILES tokenizer and target SMILES string dataset, converting molecules to canonical SMILES format using RDKit.: "Prepare SMILES tokenizer and target SMILES string dataset, converting molecules to canonical SMILES format using RDKit."
