---
name: module-refactoring-and-legacy-code-removal
description: Use when when a major version release (e.g., v1.x → v2.0.0) deprecates
  a core neural module class, and new equivalent modules must be designed and integrated
  without breaking downstream prediction pipelines. Triggered by breaking changes
  in CHANGELOG or deprecation warnings in model initialization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3673
  tools:
  - FIDDLE
  - msfiddle
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Module Refactoring and Legacy Code Removal

## Summary

Systematically replace deprecated or removed architectural components (e.g., FDRNet) with new module designs that maintain Siamese architecture compatibility and preserve forward-pass semantics. This skill ensures model behavior is preserved during major version transitions while removing technical debt.

## When to use

When a major version release (e.g., v1.x → v2.0.0) deprecates a core neural module class, and new equivalent modules must be designed and integrated without breaking downstream prediction pipelines. Triggered by breaking changes in CHANGELOG or deprecation warnings in model initialization.

## When NOT to use

- Input model is stable and not scheduled for major version release; refactoring introduces unnecessary risk without breaking-change justification.
- Legacy module is still actively used in production and has no direct replacement design; refactoring will create incompatibility with existing checkpoints.
- Downstream consumers (CLI, API, notebooks) have not been updated to handle new output signatures; refactoring must be coordinated with consumer updates.

## Inputs

- Legacy model source code (e.g., containing FDRNet class)
- Atom-count feature vectors (shape: [batch, n_elements])
- Spectrum embeddings (shape: [batch, embedding_dim])
- Model configuration file (e.g., fiddle_tcn_orbitrap.yml)
- Version control history or CHANGELOG documenting removed components

## Outputs

- Refactored model file (e.g., model_tcn.py) with new FormulaEncoder and RescoreHead modules
- Formula embeddings (shape: [batch, 512], L2-normalized)
- Prediction logits (shape: [batch] or [batch, 1])
- Updated module import statements
- Test validation report confirming output shapes and normalization

## How to apply

First, document the removed module's interface (inputs, outputs, tensor shapes, normalization behavior) by inspecting legacy code or version control history. Design replacement modules (e.g., FormulaEncoder, RescoreHead) with matching or enhanced signatures, ensuring they consume the same input types (e.g., atom-count feature vectors) and produce compatible embeddings (e.g., 512-dim L2-normalized tensors). Integrate replacements into the target model file (e.g., model_tcn.py) and verify Siamese architecture compatibility by confirming element-wise operations (e.g., ⊙ product of spectrum and formula embeddings) produce scalar logits. Remove all references to legacy class names in imports and instantiation calls. Validate the refactored forward pass using synthetic tensors with known shapes and normalization properties to confirm output dimensions and normalization match the original behavior.

## Related tools

- **FIDDLE** (Deep learning framework housing the rescore model undergoing Siamese architecture redesign; modules are refactored in this codebase.) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (PyPI package and CLI wrapping FIDDLE; consumes refactored model checkpoints; must be tested to ensure no API breakage after module replacement.) — https://github.com/josiehong/msfiddle

## Examples

```
# In model_tcn.py, after designing FormulaEncoder and RescoreHead:
from fiddle.model_tcn import FormulaEncoder, RescoreHead
encoder = FormulaEncoder(input_dim=20, output_dim=512)
head = RescoreHead(embedding_dim=512)
atom_counts = torch.randn(32, 20)
spec_embedding = torch.randn(32, 512)
formula_emb = encoder(atom_counts)  # shape [32, 512], L2-normalized
logits = head(spec_embedding, formula_emb)  # shape [32, 1]
```

## Evaluation signals

- Forward-pass tensor shapes match expected dimensions (e.g., formula embeddings [batch, 512], logits [batch, 1])
- L2 normalization of formula embeddings confirmed: norm(z_form, dim=1) ≈ 1.0 ± 1e-6 for all batch samples
- Element-wise product (⊙) of spectrum and formula embeddings produces scalar logits without shape mismatch
- No import errors or NameError exceptions when loading refactored model_tcn.py; all legacy class references removed
- Prediction outputs on held-out test spectra from CASMI or EMBL-MCF 2.0 remain within expected accuracy ranges (e.g., top-1 rank match rate ≥ baseline)

## Limitations

- Refactoring assumes replacement modules (FormulaEncoder, RescoreHead) are mathematically equivalent to removed components; if original FDRNet behavior is not fully documented, inference accuracy may drift.
- Existing pre-trained checkpoints from v1.x that reference legacy module names (e.g., FDRNet) are incompatible with refactored code; new v2.0.0 checkpoints must be released separately.
- Integration with downstream tools (BUDDY, SIRIUS) is unaffected by module refactoring, but CLI and Python API tests must still be run to detect silent output format changes.

## Evidence

- [other] The rescore model implements a Siamese architecture that replaces the removed FDRNet class, incorporating a FormulaEncoder to embed atom-count vectors and a RescoreHead that computes element-wise products of spectrum and formula embeddings to generate logits.: "The v2.0.0 rescore model implements a Siamese architecture that replaces the removed FDRNet class, incorporating a FormulaEncoder to embed atom-count vectors and a RescoreHead that computes"
- [other] Design FormulaEncoder as a neural network layer that accepts atom-count feature vectors and produces 512-dimensional embeddings with L2 normalization.: "Design FormulaEncoder as a neural network layer that accepts atom-count feature vectors and produces 512-dimensional embeddings with L2 normalization."
- [other] Design RescoreHead as a module that computes element-wise product (⊙) of spectrum embedding z_spec and formula embedding z_form to produce a scalar logit output.: "Design RescoreHead as a module that computes element-wise product (⊙) of spectrum embedding z_spec and formula embedding z_form to produce a scalar logit output."
- [other] Remove references to the legacy FDRNet class and update module imports.: "Remove references to the legacy FDRNet class and update module imports."
- [readme] Breaking change (v2.0.0): The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md.: "Breaking change (v2.0.0): The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md."
