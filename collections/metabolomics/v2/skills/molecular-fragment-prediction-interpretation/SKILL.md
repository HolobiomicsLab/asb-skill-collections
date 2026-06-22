---
name: molecular-fragment-prediction-interpretation
description: Use when you have an experimental tandem mass spectrum (collision energy annotated) and a known molecular formula or candidate structure list, and you need to rank or discriminate between isomeric or isobaric candidates by comparing predicted fragment-level spectral patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - ICEBERG WebUI
  - PubChem
  - ICEBERG
  - MAGMa
  - SCARF
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- You can run ICEBERG structural elucidation easily at http://iceberg-ms.mit.edu/
- By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
---

# molecular-fragment-prediction-interpretation

## Summary

Predict and interpret fragment-level tandem mass spectra for organic molecules using neural graph models trained on experimental collision-induced dissociation data. This skill enables structural elucidation by ranking candidate structures from PubChem based on similarity between predicted and experimental fragment spectra.

## When to use

You have an experimental tandem mass spectrum (collision energy annotated) and a known molecular formula or candidate structure list, and you need to rank or discriminate between isomeric or isobaric candidates by comparing predicted fragment-level spectral patterns. Particularly valuable when the experimental spectrum is complex or when database matching alone is insufficient.

## When NOT to use

- Input is a low-resolution or uncalibrated spectrum with poor mass accuracy (>5 ppm drift); fragment mass prediction relies on accurate m/z values.
- Candidate library is limited to a single structure or fewer than 5 candidates; ranking skill is most valuable when discriminating among multiple isomers.
- Experimental spectrum is from electron ionization (EI) or other fragmentation mode not covered by the training data (NIST'20 and MassSpecGym are primarily [M+H]+ collision-induced dissociation); model performance degrades on out-of-distribution fragmentation modes.

## Inputs

- experimental tandem mass spectrum (m/z × intensity pairs, preferably with collision energy annotation)
- molecular formula (string, e.g., 'C6H12O6')
- candidate structure list (SMILES or InChI strings, e.g., from PubChem)
- mass spectrometry file format (mzML, mgf, or HDF5 spectrum dataset)

## Outputs

- ranked candidate structure list with similarity scores
- predicted fragment graph (breakage events and subgraph masses)
- predicted fragment-level spectrum (m/z × predicted intensity pairs)
- per-candidate similarity metric (e.g., cosine similarity to experimental spectrum)

## How to apply

Encode the molecular structure (SMILES or InChI) using a graph neural network to predict a fragment graph, representing molecular breakage events and their connectivity. For each candidate structure, score the predicted fragment masses and intensities against the experimental spectrum using spectral similarity metrics (e.g., cosine similarity). Rank candidates by similarity score. The model is trained to predict spectra at the molecular fragment level rather than at the formula level, allowing discrimination between structural isomers. For best performance, ensure experimental spectra have collision energy annotations and use pretrained weights from NIST'20 or MassSpecGym datasets; CPU-only inference is feasible for smaller batches. Compare top-ranked predictions against reference spectra when available to validate ranking quality.

## Related tools

- **ICEBERG** (Fragment graph generator and intensity predictor; core model for predicting fragment-level tandem mass spectra from molecular structures and ranking candidates) — https://github.com/coleygroup/ms-pred
- **ICEBERG WebUI** (No-GPU web interface for structural elucidation; accepts chemical formula and experimental spectrum, queries PubChem, and returns ranked candidates without local setup) — http://iceberg-ms.mit.edu/
- **PubChem** (Source database of candidate structures matched by molecular formula for retrieval and ranking)
- **MAGMa** (Algorithm for annotating substructures and labeling molecular breakage process to generate training data for fragment graph models)
- **SCARF** (Alternative baseline model predicting spectra at formula level rather than fragment level; included for comparison)

## Examples

```
jupyter notebook notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb
```

## Evaluation signals

- Top-1 retrieval accuracy: verify that the correct isomer (if known) ranks first or within top-k (benchmark: 40% top-1 on NIST'20 [M+H]+)
- Spectral similarity distribution: predicted spectrum cosine similarity to experimental spectrum should be substantially higher for correct candidate than for decoys
- Fragment mass accuracy: predicted major fragments should match observed m/z peaks within ±0.01 Da (or per-dataset mass tolerance)
- Rank stability: repeat prediction on same spectrum should produce identical or near-identical ranking (deterministic for non-stochastic models)
- Hit rate on held-out test set: if ground truth structure is known, record whether it appears in top-k ranked list (k=1, 5, 10)

## Limitations

- Requires pretrained model weights (NIST'20 licensed or MassSpecGym public); training from scratch demands two GPUs with ≥24 GB RAM each and ~1 week per dataset
- Performance is biased toward [M+H]+ collision-induced dissociation spectra; other ionization modes and fragmentation energies are not well represented in training data
- Fragment prediction inherits errors from the graph neural network encoder; molecules with rare or unusual connectivity patterns may produce poor-quality fragment graphs
- Retrieval performance degrades when candidate library is very large (>100k compounds) or when no candidates match the experimental fragmentation pattern
- Web UI does not support GPU-accelerated batch processing; single-spectrum queries take ~30–60 seconds

## Evidence

- [readme] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.: "By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem."
- [readme] No GPU is required.: "No GPU is required to run ICEBERG structural elucidation via the WebUI."
- [other] ICEBERG predicts fragment-level mass spectra for each candidate and ranks them by similarity to the experimental spectrum.: "ICEBERG predicts fragment-level mass spectra for each candidate and ranks them by similarity to the experimental spectrum."
- [readme] ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor.: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor."
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset.: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
