---
name: neural-network-inference-execution
description: Use when you have (1) a molecular structure input in SMILES, InChI, or chemical formula format, (2) a pretrained ICEBERG model checkpoint with fragment generation and intensity prediction weights, and (3) a goal to predict fragmentation patterns and m/z intensities for unknown compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0630
  - http://edamontology.org/topic_3172
  tools:
  - ms-pred
  - ICEBERG WebUI
  - ICEBERG model
  - ms-pred repository
  - PubChem
  techniques:
  - tandem-MS
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

# neural-network-inference-execution

## Summary

Execute a pretrained neural network model on molecular inputs to generate tandem mass spectral predictions at fragment-level granularity. This skill bridges molecular representation encoding and spectrum reconstruction for structural elucidation workflows.

## When to use

Apply this skill when you have (1) a molecular structure input in SMILES, InChI, or chemical formula format, (2) a pretrained ICEBERG model checkpoint with fragment generation and intensity prediction weights, and (3) a goal to predict fragmentation patterns and m/z intensities for unknown compound identification or validation against experimental spectra.

## When NOT to use

- Input is already a complete experimental tandem mass spectrum (inference is unnecessary; use spectral similarity or library matching instead).
- Model weights are not available or not licensed (NIST'20 requires purchase and license verification; MassSpecGym weights are lower-quality alternatives).
- Target compound ionization method or collision energy is fundamentally different from training data (ICEBERG is trained on [M+H]+ ESI-MS/MS; cross-ionization transfer is not validated).

## Inputs

- Molecular structure (SMILES string, InChI, or chemical formula)
- Pretrained ICEBERG model weights (fragment generation checkpoint and intensity prediction checkpoint)
- Configuration file specifying model hyperparameters, batch size, GPU/CPU settings, and output format

## Outputs

- Tandem mass spectrum as (m/z, intensity) pairs
- Structured spectrum file (.mgf, .msp, or .hdf5 format)
- Predicted fragment annotations with molecular substructures

## How to apply

Load the molecular input (SMILES, InChI, or chemical formula) and initialize the ICEBERG model with pretrained weights from the ms-pred repository. Pass the molecular representation through the neural network's fragment generator to predict molecular substructures and breakage patterns, then route those fragments through the intensity predictor to estimate peak intensities. Decode the model's raw outputs into (m/z, intensity) pairs and format them as a structured spectrum file (typically .mgf or .msp). Validate correctness by comparing predicted spectra against experimental reference spectra using spectral similarity metrics (e.g., cosine similarity) or by ranking predicted spectra against known PubChem candidates.

## Related tools

- **ICEBERG model** (Core neural network for fragment-level tandem mass spectrum prediction from molecular inputs) — https://github.com/coleygroup/ms-pred
- **ms-pred repository** (Source repository containing pretrained ICEBERG weights, training scripts, and demo notebooks) — https://github.com/coleygroup/ms-pred
- **ICEBERG WebUI** (GPU-free web interface for running ICEBERG inference without local installation or coding) — http://iceberg-ms.mit.edu/
- **PubChem** (Reference chemical database used to rank predicted spectra against candidate compounds for structural elucidation)

## Examples

```
python src/ms_pred/dag_pred/predict_smis.py --config configs/iceberg/iceberg_elucidation.yaml --input molecules.smiles --output predictions.mgf --cuda_devices 0
```

## Evaluation signals

- Predicted spectrum peaks align with experimental m/z values within instrument mass accuracy tolerance (typically ±5 ppm for high-resolution instruments).
- Spectral similarity (cosine similarity or neutral loss matching) between predicted and experimental spectra exceeds domain-specific threshold (e.g., ≥0.6 for preliminary screening).
- Predicted spectrum ranks known true compound structure in top-N retrieval results when compared against PubChem candidate library (40% top-1 accuracy reported on NIST'20 [M+H]+ dataset).
- Fragment annotations match known fragmentation mechanisms and chemical substructures of the target molecule (validated against mass difference trees or MAGMa-derived fragmentation paths).
- Inference completes within expected runtime (demo notebook runs <2 minutes on NVIDIA RTX 4070M or equivalent; CPU-only inference scales to minutes for single molecules).

## Limitations

- Fragment-level prediction is specific to ICEBERG; SCARF predicts only chemical formula-level fragments and is not interchangeable for this skill.
- Pretrained weights require commercial NIST'20 license (or email license verification); publicly available MassSpecGym weights yield lower-quality predictions due to less rigorous curation.
- Trained exclusively on [M+H]+ ESI-MS/MS with fixed collision energy annotations; generalization to other ionization modes (e.g., [M-H]−, [M+Na]+) or variable collision energies is not validated.
- Inference requires either GPU with ≥8 GB RAM (tested on RTX 4070M) or extended CPU runtime; batch processing may require tuning batch_size and num_workers parameters for memory constraints.
- Model outputs (m/z and intensity pairs) are continuous predictions; post-processing thresholds and peak filtering strategies are user-dependent and not specified in the base model.

## Evidence

- [intro] ICEBERG predicts spectra at the level of molecular fragments: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [other] Initialize model and pass molecular representation through neural network: "Initialize the ICEBERG model with pretrained weights from the ms-pred repository. 3. Pass the molecular representation through the ICEBERG neural network to generate fragment-level predictions."
- [other] Decode outputs to construct predicted tandem mass spectrum: "Decode model outputs to construct predicted tandem mass spectrum (m/z and intensity pairs). 5. Format and export predicted spectrum as a structured spectrum file."
- [readme] WebUI availability and GPU-free inference: "You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/! By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from"
- [readme] Demo runtime and GPU memory requirements: "Running the demo takes <2 minutes with a regular desktop GPU. batch_size: 8, num_workers: 6 tested on NVIDIA RTX 4070M 8GB"
- [readme] Fragment generation and intensity prediction pipeline: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor."
- [other] Load molecular input formats: "Load molecular input (SMILES, InChI, or chemical formula) for the target compound."
- [readme] Top-1 retrieval accuracy benchmark: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
