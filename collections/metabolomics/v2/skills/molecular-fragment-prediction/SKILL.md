---
name: molecular-fragment-prediction
description: Use when when you have an experimental tandem mass spectrum (m/z peaks and intensities) and a chemical formula, and need to identify the true molecular structure from a candidate library (e.g., PubChem).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - ICEBERG
  - coleygroup/ms-pred
  - PubChem
  - MAGMa
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c04654
  title: ICEBERG / fragmentation graph generation
evidence_spans:
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

# molecular-fragment-prediction

## Summary

Predict tandem mass spectra at the level of molecular fragments by learning to infer collision-induced dissociation (CID) breakage events and reconstruct their fragmentation graphs. This enables ranking of candidate molecular structures against experimental spectra.

## When to use

When you have an experimental tandem mass spectrum (m/z peaks and intensities) and a chemical formula, and need to identify the true molecular structure from a candidate library (e.g., PubChem). Fragment-level prediction is particularly valuable when structural isomers share the same molecular formula but differ in fragmentation behavior.

## When NOT to use

- Input spectrum comes from soft ionization (ESI, APCI) without collision energy annotation — ICEBERG requires CID tandem MS data with known collision energy
- Candidate library is extremely small (<10 candidates) — fragment-level ranking is most beneficial when discriminating among many structurally similar isomers
- Chemical formula is unknown or ambiguous — the model requires exact formula match before ranking candidates

## Inputs

- experimental tandem mass spectrum (m/z peaks and intensities, typically in .mgf or .hdf5 format)
- chemical formula (molecular composition, e.g., C₆H₁₂O₆)
- candidate structure library (SMILES strings and InChI keys, e.g., from PubChem)
- pretrained ICEBERG model weights (fragment generator and intensity predictor checkpoints)

## Outputs

- ranked list of candidate structures (sorted by cosine similarity or retrieval score)
- predicted fragment m/z values for each candidate
- predicted intensity values for each fragment ion
- top-1 and top-k retrieval accuracy metrics
- fragmentation graph (DAG) showing breakage events for each candidate

## How to apply

Train or use a pretrained ICEBERG model that learns two coupled components: (1) a fragment generator that predicts which molecular substructures will break under CID collision energy, represented as a directed acyclic graph (DAG) of fragmentation events, and (2) an intensity predictor that estimates relative peak heights for each predicted fragment ion. For each candidate structure, run the model to predict its fragment-level spectrum, then compare predicted peaks (m/z and intensity) to observed experimental peaks using cosine similarity or ranking metrics. Score candidates by ranking accuracy (top-1, top-5) or retrieval recall. Contrastive finetuning on large structural libraries (e.g., PubChem via InChI keys) improves generalization to out-of-training structures.

## Related tools

- **ICEBERG** (Core model for fragment-level spectrum prediction and candidate ranking; available via WebUI without GPU requirement) — http://iceberg-ms.mit.edu/
- **coleygroup/ms-pred** (Repository containing ICEBERG implementation, training pipelines, and structural elucidation demo notebook) — https://github.com/coleygroup/ms-pred
- **PubChem** (Candidate structure library queried by chemical formula to retrieve all isomeric structures for ranking)
- **MAGMa** (Algorithm used during ICEBERG training to annotate substructures and label fragmentation breakage events (DAG construction))

## Examples

```
python notebooks/iceberg_2025_biorxiv/iceberg_demo_pubchem_elucidation.ipynb (or via WebUI at http://iceberg-ms.mit.edu/ by entering chemical formula and experimental mass spectrum to retrieve ranked candidates)
```

## Evaluation signals

- Top-1 retrieval accuracy: the ground-truth structure ranks first in the predicted list (aim: ≥40% for NIST'20 [M+H]+ dataset)
- Top-k recall: percentage of test queries where correct structure appears in top-k predictions
- Cosine similarity between predicted and experimental fragment spectra: higher similarity indicates better match
- Peak intensity prediction error: MAE or RMSE between predicted and observed fragment ion intensities
- Fragmentation graph validity: DAG contains plausible neutral losses and m/z transitions consistent with known chemistry

## Limitations

- Requires pretrained model weights (NIST'20 license required for full accuracy; MassSpecGym weights available but with lower curation quality)
- Performance degrades for molecules with many isomers sharing identical fragmentation patterns
- Collision energy must be known and annotated in training data; transfer across different CE values not guaranteed
- Computational cost scales with candidate library size (hours to days for millions of PubChem structures on standard GPU)
- Fragment generator may over- or under-predict breakage sites if training data lacks diversity in molecular scaffolds

## Evidence

- [other] ICEBERG predicts spectra at the level of molecular fragments, enabling spectrum-based ranking of PubChem candidates: "ICEBERG predicts spectra at the level of molecular fragments, enabling spectrum-based ranking of PubChem candidates."
- [other] Run ICEBERG's ranking algorithm to score each candidate structure against the experimental spectrum by predicting fragment-level spectra and comparing to observed peaks: "Run ICEBERG's ranking algorithm to score each candidate structure against the experimental spectrum by predicting fragment-level spectra and comparing to observed peaks."
- [readme] ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor."
- [readme] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] To train ICEBERG, we must annotate substructures and create a labeled dataset over the breakage process, which we do with the MAGMa algorithm: "To train ICEBERG, we must annotate substructures and create a labeled dataset over the breakage process, which we do with the MAGMa algorithm."
