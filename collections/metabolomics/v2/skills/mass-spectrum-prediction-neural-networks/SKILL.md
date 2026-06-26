---
name: mass-spectrum-prediction-neural-networks
description: Use when when you have molecular structures (SMILES, InChI, or chemical
  formula) and need to predict their tandem mass spectra for structural elucidation
  or compound ranking against databases. Use SCARF when operating at the chemical
  formula level;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - ICEBERG
  - SCARF
  - MassFormer
  - PubChem
  - MAGMa algorithm
  techniques:
  - LC-MS
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

# mass-spectrum-prediction-neural-networks

## Summary

Use neural network models (ICEBERG, SCARF, or MassFormer) to predict tandem mass spectra from molecular structures, enabling in silico spectrum generation for structure elucidation and compound identification without experimental measurement.

## When to use

When you have molecular structures (SMILES, InChI, or chemical formula) and need to predict their tandem mass spectra for structural elucidation or compound ranking against databases. Use SCARF when operating at the chemical formula level; use ICEBERG when you need fragment-level prediction and higher retrieval accuracy (40% top-1 on NIST'20 [M+H]+). Choose this skill when experimental spectra are unavailable or when you need rapid in silico screening before experimental confirmation.

## When NOT to use

- Input molecules contain rare functional groups or heavy elements not represented in the NIST'20 or MassSpecGym training sets; model generalization to unseen chemistry is limited.
- You require predictions at a specific collision energy not present in training data; models are trained on collision energy-annotated spectra and do not generalize well to out-of-distribution energies.
- Your workflow demands real-time prediction on millions of compounds; inference latency and GPU memory constraints may be prohibitive without distributed computing.

## Inputs

- Molecular structures (SMILES strings, InChI, or chemical formula)
- Pre-trained model weights (checkpoint files) from ms-pred repository
- Configuration YAML file specifying model architecture and hyperparameters
- Optional collision energy annotations (for context-aware prediction)

## Outputs

- Predicted tandem mass spectra (peak lists with m/z and intensity values)
- Subformula-to-fragment assignments (for SCARF)
- Fragment graph and breakage annotations (for ICEBERG)
- Structured spectrum table (m/z, intensity, fragment identity)

## How to apply

Load molecular input as SMILES, InChI, or chemical formula and convert to model-compatible tensors. Initialize the chosen model (ICEBERG, SCARF, or MassFormer) with pre-trained weights from the ms-pred repository. Execute forward inference to generate spectrum predictions, which include peak m/z values and intensities (ICEBERG/MassFormer) or subformula-level intensities (SCARF). For SCARF, subformulae are assigned to fragments via the MAGMa algorithm during preprocessing (assign_subformulae.py). Parse output into structured format (peak list with m/z and intensity pairs, optionally with fragment/subformula annotations). Adjust batch_size and num_workers based on GPU RAM (batch_size=8, num_workers=6 for 8GB GPU; batch_size=8, num_workers=12 for 24GB GPU); CPU-only inference is feasible by setting cuda_devices to None.

## Related tools

- **ICEBERG** (Fragment-level tandem mass spectrum predictor; infers breakage events and reconstructs fragment graphs for high-accuracy structural elucidation; accessible via WebUI without GPU) — https://github.com/coleygroup/ms-pred
- **SCARF** (Subformula-classification spectrum predictor; performs autoregressive reconstruction of fragmentations at chemical formula level) — https://github.com/coleygroup/ms-pred
- **MassFormer** (Graph Transformer baseline for tandem mass spectrum prediction from molecular structure) — https://github.com/coleygroup/ms-pred
- **PubChem** (Database of molecular candidates for retrieval-based ranking and structural elucidation; formula and InChIKey mappings used for contrastive training)
- **MAGMa algorithm** (Assigns subformulae and annotates substructures in preprocessing; required for SCARF training data preparation) — https://github.com/coleygroup/ms-pred

## Examples

```
python src/ms_pred/dag_pred/predict_smis.py --config configs/iceberg/iceberg_elucidation.yaml --input molecules.smi --output predictions.pkl
```

## Evaluation signals

- Top-k retrieval accuracy: rank predicted spectrum against PubChem candidate library and measure top-1, top-5, top-10 correct structure retrieval rate
- Cosine similarity between predicted and experimental spectra: compute spectral dot product normalized by L2 norms; typical thresholds ≥0.7 for high-quality matches
- Fragment/subformula assignment correctness: verify that predicted m/z peaks correspond to valid molecular fragments or subformulae by cross-referencing structure
- Inference stability: repeat predictions on identical inputs and confirm deterministic output (or document stochastic variance if sampling is used)
- Batch processing validation: confirm that model batch predictions match single-sample predictions element-wise (no accumulation artifacts)

## Limitations

- NIST'20 dataset is commercial and requires purchase; publicly available MassSpecGym training weights show lower accuracy due to less manual curation and quality control compared to NIST'20.
- Model generalization is constrained to collision energies and ionization modes represented in training data; out-of-distribution collision energies or adducts ([M+Na]+, [M-H]−) may yield degraded predictions.
- Substructure annotation via MAGMa is computationally expensive (several hours even when parallelized) for large libraries; preprocessing time scales with dataset size.
- GPU memory requirements are substantial (minimum 24GB RAM for ICEBERG training); smaller GPUs require aggressive batch size reduction which may affect convergence and final model quality.
- SCARF operates at chemical formula level, losing fragment-level structural detail; ICEBERG provides higher top-1 retrieval accuracy (40% on NIST'20 [M+H]+) but requires more computational resources.

## Evidence

- [other] SCARF is a spectrum predictor model that operates by performing subformula classification to autoregressively reconstruct fragmentations and predict tandem mass spectra at the chemical formula level.: "SCARF is a spectrum predictor model that operates by performing subformula classification to autoregressively reconstruct fragmentations and predict tandem mass spectra at the chemical formula level."
- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [other] Initialize the SCARF model with pre-trained weights from the ms-pred repository.: "Initialize the SCARF model with pre-trained weights from the ms-pred repository."
- [other] Execute forward inference pass through SCARF to generate subformula-level spectrum predictions for each molecule.: "Execute forward inference pass through SCARF to generate subformula-level spectrum predictions for each molecule."
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/. By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem. No GPU is required.: "You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/. By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from"
- [readme] When you have a GPU with smaller RAM, set smaller numbers for batch_size and num_workers to fit the model into GPU RAM (batch_size: 8, num_workers: 6 tested on NVIDIA RTX 4070M 8GB; batch_size: 8, num_workers: 12 tested on NVIDIA RTX A5000 24GB). CPU-only inference is also feasible if you set cuda_devices: None.: "When you have a GPU with smaller RAM, set smaller numbers for batch_size and num_workers to fit the model into GPU RAM (batch_size: 8, num_workers: 6 tested on NVIDIA RTX 4070M 8GB; batch_size: 8,"
- [readme] MassSpecGym has undergone less manual curation and quality control compared to NIST, and the results of new predictions will be different.: "MassSpecGym has undergone less manual curation and quality control compared to NIST, and the results of new predictions will be different."
- [readme] Data should then be assigned to subformulae files using data_scripts/forms/assign_subformulae.py, which will preprocess the data.: "Data should then be assigned to subformulae files using data_scripts/forms/assign_subformulae.py, which will preprocess the data."
- [readme] Making formula subsets takes longer (on the order of several hours, even parallelized) as it requires converting each molecule in PubChem to a mol / InChI.: "Making formula subsets takes longer (on the order of several hours, even parallelized) as it requires converting each molecule in PubChem to a mol / InChI."
