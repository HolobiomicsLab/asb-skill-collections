---
name: fragment-level-spectrum-prediction
description: Use when when you have a molecular structure (SMILES, InChI, or chemical formula) and need to predict its tandem mass spectrum for structural elucidation or mass spectrometry validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - ms-pred
  - ICEBERG WebUI
  - ICEBERG
  - ms-pred repository
  - PubChem
  - MAGMa algorithm
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
---

# Fragment-level spectrum prediction

## Summary

Predict tandem mass spectra at molecular fragment granularity by passing molecular representations through a neural network model trained to generate fragment-level m/z and intensity pairs. This approach enables finer structural inference compared to formula-level prediction methods.

## When to use

When you have a molecular structure (SMILES, InChI, or chemical formula) and need to predict its tandem mass spectrum for structural elucidation or mass spectrometry validation. Fragment-level prediction is especially valuable when you need to rank candidate structures against an experimental spectrum or validate a proposed molecular structure, as it provides richer mechanistic information than formula-level approaches.

## When NOT to use

- Input is a chemical formula alone and you need to distinguish isomers or confirm structure—formula-level prediction (SCARF) may be sufficient and faster.
- Experimental spectrum is already obtained and you only need to match it to a library without generating new predictions.
- Training data uses collision energies not in the NIST'20 or MassSpecGym datasets, as model generalization to novel collision regimes is not established.

## Inputs

- Molecular representation (SMILES string, InChI, or chemical formula)
- Pretrained ICEBERG model weights (checkpoint files for fragment generator and intensity predictor)
- Configuration file (YAML) specifying model paths, batch size, GPU/CPU device, and fragment generation thresholds

## Outputs

- Predicted tandem mass spectrum (m/z–intensity pairs in structured format)
- Fragment annotations (which molecular substructures generated each predicted peak)
- Spectrum file (MGF or equivalent format for downstream retrieval/ranking)

## How to apply

Load the molecular input in SMILES, InChI, or chemical formula format. Initialize the ICEBERG model with pretrained weights (available via NIST'20 license, MassSpecGym public weights, or by training from scratch on NIST'20 or MassSpecGym datasets). Pass the molecular representation through the ICEBERG neural network architecture, which comprises a learned fragment generator and an intensity predictor module. The generator predicts which fragments will form (at configurable thresholds controlling fragment quantity), and the intensity predictor estimates their relative abundances. Decode the model outputs to construct m/z and intensity pairs, then format as a structured spectrum file compatible with retrieval against PubChem or other chemical libraries. GPU is optional; CPU-only inference is feasible if needed.

## Related tools

- **ICEBERG** (Core neural network model that predicts fragment-level tandem mass spectra from molecular inputs via a two-stage architecture (fragment generator + intensity predictor)) — https://github.com/coleygroup/ms-pred
- **ICEBERG WebUI** (Browser-based interface for structural elucidation without GPU or code; ranks experimental spectra against PubChem candidates using ICEBERG predictions) — http://iceberg-ms.mit.edu/
- **ms-pred repository** (Source repository containing ICEBERG model implementations, training scripts, configuration templates, and demo notebooks for fragment-level spectrum prediction) — https://github.com/coleygroup/ms-pred
- **PubChem** (Chemical library used to retrieve candidate molecules and rank them via structural elucidation workflow using predicted spectra)
- **MAGMa algorithm** (Annotation tool used during data preparation to label substructures and breakage pathways for ICEBERG training data)

## Examples

```
python notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb
```

## Evaluation signals

- Predicted spectrum exhibits chemically plausible m/z values (within mass tolerance of expected fragment ions from the input molecule)
- Intensity distribution is unimodal or multimodal with peaks corresponding to expected loss patterns and stable fragment ions (e.g., base peak is a known stable cation or neutral loss product)
- Retrieval accuracy: when the predicted spectrum is ranked against a library of candidates, the correct structure ranks in the top-1 (or top-10 for harder cases); on NIST'20 [M+H]+ benchmark, ≥40% top-1 retrieval accuracy indicates model is performing as expected
- Fragment annotations are interpretable: predicted fragments correspond to real chemical substructures (validated against SMILES fragmentation logic) and explain major peaks in the experimental spectrum
- Spectrum file parses without errors and m/z–intensity pairs are ordered monotonically or in expected library format

## Limitations

- Model requires pretrained weights; training from scratch requires NIST'20 (commercial, requires purchase) or MassSpecGym (publicly available but less manually curated than NIST'20); performance is affected by dataset choice.
- Training and full hyperparameter sweeps require two GPUs with ≥24 GB RAM (e.g., NVIDIA A5000); smaller GPUs may require batch size reduction and skipping contrastive finetuning, which degrades performance.
- Generalization to collision energies, ionization modes, or chemical spaces not represented in NIST'20 or MassSpecGym is not established.
- Fragment-level predictions are sensitive to the threshold for controlling the number of fragments generated; insufficient tuning can yield sparse or overpopulated spectra.
- Structural elucidation relies on ranking against a known library (PubChem, NIST); novel compounds not in the library cannot be identified via retrieval.

## Evidence

- [intro] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [other] Load molecular input (SMILES, InChI, or chemical formula) for the target compound. Initialize the ICEBERG model with pretrained weights from the ms-pred repository. Pass the molecular representation through the ICEBERG neural network to generate fragment-level predictions. Decode model outputs to construct predicted tandem mass spectrum (m/z and intensity pairs).: "Load molecular input (SMILES, InChI, or chemical formula) for the target compound. Initialize the ICEBERG model with pretrained weights from the ms-pred repository. Pass the molecular representation"
- [readme] ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor.: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor."
- [intro] No GPU is required to run ICEBERG structural elucidation via the WebUI: "No GPU is required to run ICEBERG structural elucidation via the WebUI"
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development).: "You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development)."
- [readme] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
