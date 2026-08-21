---
name: cross-view-similarity-scoring
description: Use when you have an experimental mass spectrum (query) and a set of
  molecular candidate structures, and you need to rank the candidates by how well
  their predicted spectral features match the query spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3765
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Python 3.11.7
  - MVP (MultiView Projection)
  - PyTorch / PyTorch Geometric
  - RDKit
  - DGL (Deep Graph Library)
  - MassSpecGym
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-view-similarity-scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply MultiView Projection (MVP) to compute cross-view similarity scores between a query spectrum and molecular candidate structures, enabling ranking of candidates by aggregated similarity. This skill is essential when you need to match an experimental mass spectrum against a library of putative molecular structures.

## When to use

Use this skill when you have an experimental mass spectrum (query) and a set of molecular candidate structures, and you need to rank the candidates by how well their predicted spectral features match the query spectrum. Specifically applicable to MS/MS annotation tasks where spectral feature extraction and multi-view molecular descriptors are available.

## When NOT to use

- Input spectra lack preprocessing or feature extraction (e.g., raw, unnormalized m/z–intensity pairs without binning or consensus spectral computation)
- Candidate structures are not available or only partial structural information exists
- Query spectrum is of insufficient quality or too sparse to extract reliable spectral features

## Inputs

- Query mass spectrum (TSV or JSON format with m/z and intensity pairs)
- Candidate molecular structures (SMILES strings or molecular identifiers in JSON format)
- Spectral features extracted from query (binned spectra or formula-based subformula labels)
- Molecular descriptors for candidates (fingerprints, graph representations, or consensus spectra)

## Outputs

- Ranked candidate list with aggregated cross-view similarity scores
- Structured output file (e.g., JSON or TSV) mapping candidates to scores in descending order

## How to apply

Load the query spectrum and candidate molecular structures into memory. Extract or compute spectral features (e.g., binned spectra or formula-based spectral representations) from the query and molecular descriptors (views) from each candidate using preprocessing steps such as subformula assignment (if using formSpec) or binning (if using binnedSpec). Apply the MultiView Projection method to compute pairwise cross-view similarity scores between the query spectrum and each candidate by comparing their feature representations across views. Aggregate the similarity scores for each candidate and rank them in descending order. Export the ranked candidate list with their aggregated similarity scores to a structured output file.

## Related tools

- **MVP (MultiView Projection)** (Core implementation for computing cross-view similarity scores and ranking molecular candidates against query spectra) — https://github.com/HassounLab/MVP
- **PyTorch / PyTorch Geometric** (Neural network and graph neural network backend for learning multi-view feature representations)
- **RDKit** (Molecular structure parsing and fingerprint/descriptor computation)
- **DGL (Deep Graph Library)** (Graph representation and message-passing for molecular candidate encoding)
- **MassSpecGym** (Source dataset for training and evaluation of ranking models) — https://github.com/pluskal-lab/MassSpecGym

## Examples

```
python test.py --param_pth params_binnedSpec.yaml
```

## Evaluation signals

- Ranked candidate list contains all input candidates with no duplicates and scores in descending order
- Similarity scores fall within the expected range (e.g., [0, 1] or normalized equivalents) for the chosen cross-view similarity metric
- Top-ranked candidate matches the ground-truth annotation (if available) or aligns with manual spectral interpretation
- Ranking is stable across repeated runs with the same inputs
- Output file is valid JSON/TSV with required fields (candidate_id, score, rank) and no missing or malformed entries

## Limitations

- MVP requires preprocessed spectral features and molecular descriptors; raw spectra must first undergo binning or subformula assignment
- Performance depends on the quality of candidate structure set; missing or incorrect structures will not rank correctly
- Model trained on MassSpecGym may not generalize well to spectra from different ionization methods or mass analyzers outside the training distribution
- Computational cost scales with the number of candidates; large-scale rankings may require batching or model optimization

## Evidence

- [readme] MVP can be used to rank a set of molecular candidates given a spectrum.: "MVP can be used to rank a set of molecular candidates given a spectrum."
- [other] Extract or compute spectral features and molecular descriptors (views) for both query and candidates.: "Extract or compute spectral features and molecular descriptors (views) for both query and candidates."
- [other] Apply MultiView Projection to compute cross-view similarity scores between the query spectrum and each candidate.: "Apply MultiView Projection to compute cross-view similarity scores between the query spectrum and each candidate."
- [readme] If using formSpec, compute subformula labels: "If using formSpec, compute subformula labels"
- [readme] Run our preprocess code to obatain fingerprints and consensus spectra files: "Run our preprocess code to obatain fingerprints and consensus spectra files"
- [other] Rank candidates by their aggregated similarity scores in descending order.: "Rank candidates by their aggregated similarity scores in descending order."
