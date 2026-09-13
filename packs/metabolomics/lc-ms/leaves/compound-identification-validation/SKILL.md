---
name: compound-identification-validation
description: Use when when you have an unknown MS/MS spectrum (in .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - rdkit
  - PyTorch
  - PyTorch Geometric
  - matchms
  - Python
  - conda
  - pip
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-identification-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate compound identifications by cross-modal retrieval of MS/MS spectra against a molecular structure library using contrastive spectral-structural embeddings. This skill enables ranking and confidence scoring of candidate structures matched to an unknown mass spectrum.

## When to use

When you have an unknown MS/MS spectrum (in .mgf format with precursor m/z and fragment peaks) and a reference library of candidate molecular structures (SMILES or SDF format), and need to identify the most likely compound(s) by computing similarity between the spectrum's learned embedding and all candidate structure embeddings in a unified feature space.

## When NOT to use

- Input spectrum is already annotated or known; this skill is for unknown compound identification only.
- Reference library is empty or contains no structures within ±10 ppm of the precursor mass; no candidates will pass mass filtering.
- Collision energy of the query spectrum is unknown and differs substantially from the model's training energy level; score accuracy will degrade without multi-energy weighting.

## Inputs

- MS/MS spectrum in .mgf format with precursor m/z and fragment ion peaks
- Reference library of molecular structures in SMILES or SDF format with associated neutral mass
- Pretrained CSU-MS2 model checkpoint (model.pth) and configuration file (config.yaml)
- Precursor m/z value from spectrum metadata

## Outputs

- Ranked list of candidate molecular structures (SMILES)
- Cosine similarity scores for each candidate (0–1 range)
- Top-k matches (default k=100) with confidence scores
- CSV file with columns: smiles, score

## How to apply

Load a pretrained CSU-MS2 model (config.yaml and model.pth checkpoint) and instantiate ModelInference. Preprocess the query spectrum (normalize, handle metadata). Encode the query spectrum into the embedding space using ms2_encode(). Extract candidate structures from a reference library filtered by precursor mass (within ±10 ppm tolerance is typical). Encode each candidate SMILES string into the embedding space using get_feature(). Compute cosine similarity between the query spectrum embedding and all candidate structure embeddings. Rank candidates by descending similarity score and return top-k results (typically 100) with confidence scores. The rationale is that contrastively trained embeddings align spectral and structural feature spaces such that true matches have higher cosine similarity than false matches.

## Related tools

- **matchms** (Load and preprocess MS/MS spectra from .mgf files; normalize peak intensities and metadata) — https://matchms.readthedocs.io/en/latest/
- **rdkit** (Parse SMILES strings and molecular structures; compute molecular properties (neutral mass, fingerprints); validate structure validity) — https://rdkit.org/
- **PyTorch** (Implement the neural encoder for MS/MS spectra and contrastive loss during model training; inference with pretrained weights) — https://pytorch.org/
- **PyTorch Geometric** (Build graph neural network encoder for molecular structures; convert SMILES to graph representations (nodes=atoms, edges=bonds)) — https://pytorch-geometric.readthedocs.io/en/latest/

## Examples

```
config_path = "/model/low_energy/checkpoints/config.yaml"; model_inference = ModelInference(config_path=config_path, pretrain_model_path="/model/low_energy/checkpoints/model.pth", device="cpu"); ms_feature = model_inference.ms2_encode(ms_list[i:i+1]); indice, score, candidate = get_topK_result(library=smiles_list, ms_feature=ms_feature, smiles_feature=smiles_feature, topK=100)
```

## Evaluation signals

- Cosine similarity scores are in [0, 1] range and sum of top-k scores is monotonically decreasing.
- True known compound (if available) ranks in top-k results with high confidence score; compare rank and score to ground truth annotation.
- Mass filter correctly excludes candidates outside ±10 ppm window of precursor m/z; verify reference_library after mass_search contains only relevant structures.
- Output CSV has non-null SMILES strings and numeric scores for each row; no NaN or infinity values.
- Inference latency is consistent across multiple spectra; check model device is set correctly (cpu vs gpu) and batch encoding is efficient.

## Limitations

- Model performance depends on collision energy; single energy-level models may give low scores for spectra acquired at different energies. Use search_user_defined_library.py with weighted multi-energy models for improved robustness across collision energies.
- Reference library must have accurate neutral mass annotations; mass filtering step relies on precursor m/z metadata quality.
- Contrastively trained embeddings may show lower separation for isomeric or near-isobaric compounds that share similar fragmentation patterns.
- Model was trained on specific MS/MS datasets; generalization to novel compound classes or instruments outside training domain is not explicitly characterized.

## Evidence

- [other] CSU-MS2 implements contrastive spectral-structural unification to enable cross-modal retrieval, unifying MS/MS spectra and molecular structures for compound identification.: "CSU-MS2 implements contrastive spectral-structural unification to enable cross-modal retrieval, unifying MS/MS spectra and molecular structures for compound identification."
- [other] Encode query spectra and candidate molecular structures into the learned embedding space. Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings. Rank candidates by similarity score and output ranked retrieval results with top-k matches and confidence scores.: "Encode query spectra and candidate molecular structures into the learned embedding space. Compute cosine similarity between query spectrum embeddings and all candidate structure embeddings. Rank"
- [readme] Searching in a smiles library with search_library.py function. users Users can load the different collision energy level model according to the collision energy setting, or load three energy level models, and use the weighted scores of different energy levels as the final score: "load the different collision energy level model according to the collision energy setting, or load three energy level models, and use the weighted scores of different energy levels as the final score"
- [other] Preprocess spectra and convert molecular structures to graph representations using rdkit and PyTorch Geometric.: "Preprocess spectra and convert molecular structures to graph representations using rdkit and PyTorch Geometric."
- [readme] spectrum = spectrum_processing(spectrum); ms_feature = model_inference.ms2_encode(ms_list[i:i+1]); query_ms = float(spectrum.metadata['precursor_mz'])-1.008; search_res=search_structure_from_mass(reference_library, query_ms, 10): "spectrum = spectrum_processing(spectrum); ms_feature = model_inference.ms2_encode(ms_list[i:i+1]); query_ms = float(spectrum.metadata['precursor_mz'])-1.008;"
