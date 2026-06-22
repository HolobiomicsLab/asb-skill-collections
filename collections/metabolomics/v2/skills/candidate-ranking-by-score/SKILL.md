---
name: candidate-ranking-by-score
description: 'Use when you have a query mass spectrum and a set of candidate molecular structures, and you need to prioritize candidates by their likelihood of matching the query. Typical triggers include: (1) you have computed or extracted spectral features (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - Python 3.11.7
  - MVP (MultiView Projection)
  - PyTorch Geometric
  - DGL (Deep Graph Library)
  - RDKit
  - Streamlit
  - MassSpecGym
derived_from:
- doi: 10.1101/2025.11.12.688047v1
  title: MVP
evidence_spans:
- 'python_version: 3.11.7'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mvp_cq
    doi: 10.1101/2025.11.12.688047v1
    title: MVP
  dedup_kept_from: coll_mvp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.11.12.688047v1
  all_source_dois:
  - 10.1101/2025.11.12.688047v1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# candidate-ranking-by-score

## Summary

Rank a set of molecular candidates against a query mass spectrum by computing cross-view similarity scores using MultiView Projection (MVP), then sorting candidates by aggregated scores to identify the most likely molecular matches. This skill is essential for MS/MS annotation workflows where multiple candidate structures must be prioritized for a given experimental spectrum.

## When to use

Apply this skill when you have a query mass spectrum and a set of candidate molecular structures, and you need to prioritize candidates by their likelihood of matching the query. Typical triggers include: (1) you have computed or extracted spectral features (e.g., binned m/z intensities or subformula labels) and molecular descriptors (e.g., fingerprints, graph embeddings); (2) you want a ranked list with quantitative similarity scores rather than a binary classification; (3) the candidates have already been pre-filtered by mass or other coarse criteria and now require fine-grained scoring.

## When NOT to use

- Your candidates have not been pre-filtered or feature-extracted; perform data preprocessing (subformula assignment, fingerprint computation, consensus spectra generation) first.
- You only have the raw spectrum without precomputed spectral features or molecular descriptors; this skill requires all input views to be computed in advance.
- Your query spectrum or candidates are in unprocessed raw format (e.g., vendor .raw files); use appropriate data conversion and peak-picking tools before applying MVP.

## Inputs

- Query mass spectrum (query_spectrum: TSV or structured format with m/z, intensity pairs or subformula labels)
- Candidate molecular structures (candidates_mass.json: list of SMILES or molecular graphs with identifiers)
- Precomputed spectral features for query (fingerprints or consensus spectra file)
- Precomputed spectral features for candidates (fingerprints or consensus spectra files)
- Precomputed molecular descriptors for candidates (DGL/PyTorch Geometric graph embeddings or molecular fingerprints)
- Trained MVP model weights (checkpoint from pretrained model or custom training)

## Outputs

- Ranked candidate list (JSON or TSV): each candidate with its identifier, aggregated similarity score, and rank position
- Similarity score matrix (optional): pairwise cross-view scores for downstream analysis
- Structured output file: candidate rank, molecular identifier, aggregated MVP score, individual view contributions

## How to apply

Load the query spectrum and candidate molecular structures into memory alongside their precomputed spectral features (binned spectra or formSpec subformula labels) and molecular views (fingerprints, graph embeddings from DGL/PyTorch Geometric). Apply the MVP model's MultiView Projection layer to compute cross-view similarity scores between the query spectrum and each candidate, aggregating scores across all view pairs. Rank candidates by their aggregated similarity scores in descending order. Export the ranked candidate list with scores to a structured output file (JSON or TSV). The quality of ranking depends on the fidelity of input feature extraction and the MVP model's learned projections; verify by checking that top-ranked candidates have chemically plausible spectral fragmentation patterns relative to the query.

## Related tools

- **MVP (MultiView Projection)** (Core model for computing cross-view similarity scores and ranking candidates; encapsulates the learned projection layers trained on MassSpecGym) — https://github.com/HassounLab/MVP
- **PyTorch Geometric** (Graph neural network library used to compute and embed molecular graph descriptors as one view for MVP)
- **DGL (Deep Graph Library)** (Graph neural network library for computing molecular graph embeddings and spectral graph representations)
- **RDKit** (Cheminformatics toolkit for computing molecular fingerprints and descriptors from SMILES/molecular structures)
- **Streamlit** (Web application framework for interactive visualization and ranking results in the MVP application interface)
- **MassSpecGym** (Source dataset and preprocessing utilities for training and evaluating MVP on standardized MS/MS spectra and candidates) — https://github.com/pluskal-lab/MassSpecGym

## Examples

```
python test.py --param_pth params_binnedSpec.yaml
```

## Evaluation signals

- Top-ranked candidates have chemical structures consistent with expected fragmentation patterns for the query spectrum (manual inspection or expert validation).
- Aggregated similarity scores are in a plausible range (e.g., 0–1 or normalized scale); verify no score is NaN or degenerate.
- Rank order is monotonically decreasing by similarity score (no ties or reversals unless explicitly handled by tiebreaker logic).
- Output file is valid JSON/TSV with all required fields (rank, candidate_id, similarity_score) and row count matches input candidate set.
- Reproducibility check: running the same query + candidate set with the same MVP model weights produces identical ranked output (deterministic seeding).

## Limitations

- MVP ranking quality is bounded by the quality of precomputed spectral features and molecular descriptors; poor feature extraction (e.g., missed peaks or incorrect subformula labels) will degrade ranking.
- The pretrained MVP model is trained on MassSpecGym dataset; performance on spectra from different instruments, ionization modes, or chemical domains may degrade.
- MVP does not account for prior probabilities, chemical prevalence, or biological context; all ranking is driven solely by spectral-molecular similarity scores.
- Computational cost scales with the number of candidates and complexity of molecular graphs; very large candidate sets (>10,000) may require batching or approximation.

## Evidence

- [intro] MVP can be used to rank a set of molecular candidates given a spectrum.: "MVP can be used to rank a set of molecular candidates given a spectrum"
- [other] The ranking workflow extracts spectral features and molecular descriptors, applies MultiView Projection to compute cross-view similarity, ranks by aggregated scores, and exports results.: "Extract or compute spectral features and molecular descriptors (views) for both query and candidates. 3. Apply MultiView Projection to compute cross-view similarity scores between the query spectrum"
- [readme] Data preprocessing supports both formSpec (with subformula labels) and binnedSpec input formats, with precomputed fingerprints and consensus spectra.: "If using formSpec, compute subformula labels. 2. Run our preprocess code to obatain fingerprints and consensus spectra files"
- [readme] The pretrained model is used by modifying configuration files with dataset paths and running the test script.: "You can use our pretrained model (on MassSpecGym) to rank molecular candidates by providing the spectra data and a list of candidates. After prepping your data, modify the params_binnedSpec.yaml or"
- [readme] MVP is trained on MassSpecGym dataset; users can download preprocessed files or preprocess their own data.: "Our model is trained on MassSpecGym dataset. Follow their instruction to download the spectra and candidate dataset."
