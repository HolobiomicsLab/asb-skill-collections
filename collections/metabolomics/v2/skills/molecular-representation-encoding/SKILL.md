---
name: molecular-representation-encoding
description: Use when when you have a molecular target compound defined by SMILES,
  InChI, or chemical formula and need to feed it into a pretrained spectrum prediction
  model (ICEBERG or SCARF) to generate tandem mass spectra or conduct structural elucidation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - ms-pred
  - ICEBERG WebUI
  - ICEBERG
  - SCARF
  - PubChem
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular representation encoding

## Summary

Convert molecular identity (SMILES, InChI, or chemical formula) into a neural network-compatible format that enables downstream tandem mass spectrum prediction. This encoding step is essential for initializing fragment-level or formula-level mass spectrum generators.

## When to use

When you have a molecular target compound defined by SMILES, InChI, or chemical formula and need to feed it into a pretrained spectrum prediction model (ICEBERG or SCARF) to generate tandem mass spectra or conduct structural elucidation. Use this skill when the molecular input is unprocessed and the prediction model requires a consistent vector or embedding representation.

## When NOT to use

- Input is already a tandem mass spectrum (m/z and intensity pairs) — use spectrum comparison or retrieval instead.
- Molecular structure is incomplete or malformed (invalid SMILES or InChI) — encoding will fail; validate chemical identity first.
- Target is to compare experimental spectra directly without molecular information — use spectral matching rather than encoding.

## Inputs

- SMILES string
- InChI string
- Chemical formula
- Pretrained ICEBERG model weights (PyTorch checkpoint)
- Pretrained SCARF model weights (PyTorch checkpoint)

## Outputs

- Learned molecular embedding / latent representation
- Model input tensor with compatible shape for downstream prediction heads
- Fragment-level or formula-level encoded representation (model-dependent)

## How to apply

Load the molecular input (SMILES, InChI, or chemical formula) into the ms-pred environment. Initialize the ICEBERG or SCARF model with pretrained weights (from the ms-pred repository or downloaded weights trained on NIST'20 or MassSpecGym datasets). Pass the molecular representation through the encoder component of the neural network to generate a learned latent representation. The choice between ICEBERG and SCARF depends on prediction granularity: ICEBERG produces fragment-level predictions suitable for detailed structural elucidation, while SCARF produces chemical formula–level predictions for faster inference. Validate the encoding by confirming the model accepts the input without shape errors and produces a fixed-dimensional embedding compatible with downstream intensity prediction or retrieval modules.

## Related tools

- **ICEBERG** (Neural network model that encodes molecular inputs and generates fragment-level tandem mass spectrum predictions via learned graph breakage events) — https://github.com/coleygroup/ms-pred
- **SCARF** (Alternative spectrum prediction model that encodes molecular inputs and generates formula-level (rather than fragment-level) predictions autoregressively) — https://github.com/coleygroup/ms-pred
- **ms-pred** (Python package and repository containing implementations of ICEBERG, SCARF, and baseline models with pretrained checkpoints and training pipelines) — https://github.com/coleygroup/ms-pred
- **ICEBERG WebUI** (Web interface for structural elucidation that encodes molecular inputs and ranks candidates from PubChem without requiring GPU or local installation) — http://iceberg-ms.mit.edu/
- **PubChem** (Database of molecular structures and chemical formulas used to populate candidate libraries for retrieval-based structural elucidation after encoding)

## Examples

```
python src/ms_pred/dag_pred/predict_smis.py --smiles 'CC(C)Cc1ccc(cc1)C(C)C(O)=O' --model-config configs/iceberg/iceberg_elucidation.yaml --output predictions.json
```

## Evaluation signals

- Encoded representation has expected dimensionality (e.g., 256 or 512 for typical GNN/FFN encoders); check model config or checkpoint metadata.
- Model forward pass completes without shape mismatch or NaN errors; confirm by running a single test molecule through the encoder.
- Encoded vectors from chemically similar molecules cluster together in embedding space (inspect via t-SNE or cosine similarity matrix).
- Downstream intensity prediction or retrieval module accepts the encoded representation without input validation failures.
- Consistent encoding of the same molecular input across repeated runs (deterministic behavior when model is in eval mode).

## Limitations

- ICEBERG and SCARF require pretrained weights; training from scratch demands two GPUs with ≥24 GB RAM and NIST'20 or MassSpecGym datasets with manual annotation (MAGMa substructure labeling for ICEBERG). Public weights are available only for MassSpecGym (smaller, less curated) or require NIST'20 license.
- Encoding assumes valid, chemically sensible molecular inputs; malformed SMILES, InChI, or chemical formulas will cause encoding to fail or produce meaningless embeddings.
- Fragment-level encoding (ICEBERG) predicts spectra only for collision energies and ionization modes seen during training; out-of-distribution collision energies or rare ion types may degrade prediction accuracy.
- Model embeddings are black-box learned representations and do not expose interpretable chemical features; retrieval and ranking depend on learned similarity, not explicit chemical rules.
- CPU-only inference is feasible but slow; GPU recommended for batch encoding of large molecular libraries.

## Evidence

- [other] Load molecular input (SMILES, InChI, or chemical formula) for the target compound.: "Load molecular input (SMILES, InChI, or chemical formula) for the target compound."
- [other] Initialize the ICEBERG model with pretrained weights from the ms-pred repository.: "Initialize the ICEBERG model with pretrained weights from the ms-pred repository."
- [other] Pass the molecular representation through the ICEBERG neural network to generate fragment-level predictions.: "Pass the molecular representation through the ICEBERG neural network to generate fragment-level predictions."
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/! By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [readme] Or you can download the weights trained on the MassSpecGym dataset, publicly available via Dropbox.: "Or you can download the weights trained on the MassSpecGym dataset, publicly available via Dropbox."
- [readme] CPU-only inference is also feasible if you set cuda_devices: None.: "CPU-only inference is also feasible if you set cuda_devices: None."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG.: "You need two GPUs with at least 24GB RAM to train ICEBERG."
