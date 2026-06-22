---
name: contrastive-learning-for-cross-modal-retrieval
description: Use when you have paired MS/MS spectra and molecular structures (SMILES or SDF format) and need to perform compound identification by retrieving the correct structure for an unknown spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - rdkit
  - PyTorch
  - PyTorch Geometric
  - matchms
  - Python
  - conda
  - pip
  - Distributed Data Parallel (DDP)
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01594
  title: CSU-MS2
evidence_spans:
- '- [rdkit](https://rdkit.org/)'
- '- [pytorch](https://pytorch.org/)'
- '- [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/)'
- '- [matchms](https://matchms.readthedocs.io/en/latest/)'
- '- [python3](https://www.python.org/)'
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_csu_ms2_cq
    doi: 10.1021/acs.analchem.5c01594
    title: CSU-MS2
  dedup_kept_from: coll_csu_ms2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01594
  all_source_dois:
  - 10.1021/acs.analchem.5c01594
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# contrastive-learning-for-cross-modal-retrieval

## Summary

Train contrastive embeddings to align MS/MS spectral and molecular structural feature spaces, enabling cross-modal retrieval where query spectra are matched against candidate structures via cosine similarity in a learned unified embedding space. This skill is essential when compound identification requires matching raw mass spectrometry data directly against molecular structure libraries without intermediate feature engineering.

## When to use

Apply this skill when you have paired MS/MS spectra and molecular structures (SMILES or SDF format) and need to perform compound identification by retrieving the correct structure for an unknown spectrum. The skill is particularly valuable when traditional spectral library matching fails due to data heterogeneity, instrument variation, or insufficient reference spectra at specific collision energies.

## When NOT to use

- Input spectra are already assigned to known compounds; use for unknowns only.
- Molecular structure library is very small (<100 candidates); simpler spectral matching is more efficient.
- Spectra lack sufficient fragment information or precursor mass metadata; contrastive matching requires quality spectral features.

## Inputs

- MS/MS spectrum data (MGF format)
- Molecular structure library (SMILES or SDF format)
- Training dataset of paired MS/MS spectra and structures

## Outputs

- Ranked list of candidate structures with cosine similarity scores
- Top-k matched compounds with confidence scores
- Trained contrastive embedding model checkpoint

## How to apply

Load MS/MS spectra (MGF format) and molecular structures (SMILES/SDF) using matchms and rdkit. Preprocess spectra (normalize, remove noise) and convert structures to graph representations using rdkit and PyTorch Geometric. Train a siamese-style contrastive model using PyTorch on pairs of spectra and structures, minimizing a contrastive loss that pushes matching pairs together and non-matching pairs apart in embedding space. Encode query spectra and candidate structures into the learned embedding space. Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings, then rank candidates by similarity score and output top-k matches with confidence scores. Optionally, weight predictions from multiple collision-energy-specific models to improve robustness.

## Related tools

- **rdkit** (Convert SMILES/SDF molecular structures to graph representations and compute structural features) — https://rdkit.org/
- **PyTorch** (Define and train the contrastive siamese embedding model with siamese-style loss function) — https://pytorch.org/
- **PyTorch Geometric** (Implement graph neural network layers for encoding molecular structures into embeddings) — https://pytorch-geometric.readthedocs.io/en/latest/
- **matchms** (Load, preprocess, and normalize MS/MS spectrum data from MGF format) — https://matchms.readthedocs.io/en/latest/
- **Distributed Data Parallel (DDP)** (Enable multi-GPU and multi-node parallel training of the contrastive model)

## Examples

```
python -m pip install -r requirements.txt; conda create --name CSU-MS2 python=3.8.18; python CSU-MS2/run.py main(rank=0, world_size=1, num_gpus=1, rank_is_set=False, ds_args={}); python search_library.py --config_path model/low_energy/checkpoints/config.yaml --model_path model/low_energy/checkpoints/model.pth --spectrum_file query.mgf --library reference_library.csv
```

## Evaluation signals

- Top-k retrieval accuracy: percentage of queries where ground-truth structure appears in top-1, top-5, or top-10 ranked results.
- Cosine similarity distribution: embedding space should exhibit high similarity (>0.8) for true matches and low similarity (<0.3) for decoys.
- Ranked retrieval metrics (MRR, NDCG): mean reciprocal rank and normalized discounted cumulative gain should improve with training epochs.
- Cross-modal consistency: re-encoding the same spectrum or structure should produce nearly identical embeddings (cosine similarity ≈ 1.0).
- Mass filtering sanity check: retrieved candidates should cluster near the query precursor mass (within specified tolerance) before similarity ranking.

## Limitations

- Model performance depends critically on training dataset size and quality; limited or biased training data may yield poor generalization to novel spectra.
- Collision energy mismatch between query spectrum and training data degrades retrieval accuracy; multiple collision-energy-specific models or weighted ensemble approaches are recommended.
- Computational cost scales with library size; searching millions of structures may require indexing or approximate nearest-neighbor methods.
- Embedding space may not capture all structural isomers; structures with identical fragment patterns but different connectivity may receive high similarity scores incorrectly.

## Evidence

- [other] CSU-MS2 implements contrastive spectral-structural unification to enable cross-modal retrieval, unifying MS/MS spectra and molecular structures for compound identification.: "CSU-MS2 implements contrastive spectral-structural unification to enable cross-modal retrieval"
- [other] Train contrastive embeddings using PyTorch and PyTorch Geometric to align spectral and structural feature spaces via a siamese-style loss function.: "Train contrastive embeddings using PyTorch and PyTorch Geometric to align spectral and structural feature spaces via a siamese-style loss function"
- [other] Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings.: "Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings"
- [other] Preprocess spectra and convert molecular structures to graph representations using rdkit and PyTorch Geometric.: "Preprocess spectra and convert molecular structures to graph representations using rdkit and PyTorch Geometric"
- [readme] users Users can load the different collision energy level model according to the collision energy setting, or load three energy level models, and use the weighted scores of different energy levels as the final score: "load the different collision energy level model according to the collision energy setting, or load three energy level models, and use the weighted scores"
- [readme] We developed a method named CSU-MS2 to cross-modal match MS/MS spectra against molecular structures for compound identification.: "We developed a method named CSU-MS2 to cross-modal match MS/MS spectra against molecular structures for compound identification"
