---
name: molecular-structure-tensor-encoding
description: Use when when you have raw molecular structure representations (SMILES
  strings, InChI notation, or chemical formulas) and need to feed them into a neural
  spectrum prediction model like SCARF or ICEBERG. Apply this skill before any forward
  inference pass through a pre-trained spectrum predictor.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - ms-pred (SCARF model)
  - ms-pred (ICEBERG model)
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans: []
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-tensor-encoding

## Summary

Convert molecular input data (SMILES, InChI, or chemical formula) into model-compatible tensor representations for downstream mass spectrum prediction. This preprocessing step prepares chemical structures for neural network inference by encoding their structural information into fixed-dimensional numerical arrays.

## When to use

When you have raw molecular structure representations (SMILES strings, InChI notation, or chemical formulas) and need to feed them into a neural spectrum prediction model like SCARF or ICEBERG. Apply this skill before any forward inference pass through a pre-trained spectrum predictor.

## When NOT to use

- Input molecules are already in tensor form or pre-encoded numerical format
- The target model accepts raw structure files (e.g., SDF, MOL2) without intermediate encoding
- You are performing structural elucidation via the ICEBERG WebUI, which handles encoding internally

## Inputs

- SMILES strings (molecular structure notation)
- InChI notation (International Chemical Identifier)
- Chemical formulas
- Molecular input data in batch or single-molecule format

## Outputs

- Tensor arrays (model-compatible numerical representations)
- Batch-formatted tensor structures
- Encoded molecular representations suitable for neural network inference

## How to apply

Load molecular input data in SMILES, InChI, or chemical formula format and convert each molecule into a model-compatible tensor representation. The encoding process depends on the specific model's expected input dimensionality and vocabulary: SCARF expects subformula-aware encodings that preserve chemical formula information, while fragment-based models may require molecular graph or SMILES-sequence encodings. Ensure consistent batch formatting and data type (typically float32 for neural networks). Validate tensor shapes match the model's expected input dimensions before passing to the forward pass. The encoded tensors serve as the primary input to the model's inference pipeline.

## Related tools

- **ms-pred (SCARF model)** (Neural spectrum prediction model that accepts encoded tensors as input for subformula-level spectrum generation) — https://github.com/coleygroup/ms-pred
- **ms-pred (ICEBERG model)** (Fragment-level spectrum prediction model that accepts encoded molecular tensors for inference) — https://github.com/coleygroup/ms-pred

## Evaluation signals

- Tensor dimensions match model's expected input shape (no shape mismatch errors during model loading)
- All tensors have uniform batch size and consistent feature dimensions across the dataset
- Numerical values are finite (no NaN or inf) and within expected ranges for molecular descriptors
- Encoded representations preserve structural information sufficient for model to generate chemically valid predictions
- Forward pass executes without runtime errors and produces spectrum predictions of expected dimensionality

## Limitations

- Encoding must be compatible with the specific pre-trained model weights; different model architectures (SCARF vs. ICEBERG) may require different tensor formats
- Chemical formulas alone do not encode stereochemistry or bond information; use SMILES or InChI for structure-sensitive tasks
- Batch encoding assumes homogeneous molecular complexity; very large or atypical molecules may exceed encoding capacity or require special handling

## Evidence

- [other] Load molecular input data (SMILES, InChI, or chemical formula) and prepare as model-compatible tensors.: "Load molecular input data (SMILES, InChI, or chemical formula) and prepare as model-compatible tensors."
- [readme] SCARF predicts spectra at the level of chemical formula: "SCARF predicts spectra at the level of chemical formula"
- [other] Initialize the SCARF model with pre-trained weights from the ms-pred repository. Execute forward inference pass through SCARF to generate subformula-level spectrum predictions: "Initialize the SCARF model with pre-trained weights from the ms-pred repository. Execute forward inference pass through SCARF to generate subformula-level spectrum predictions"
