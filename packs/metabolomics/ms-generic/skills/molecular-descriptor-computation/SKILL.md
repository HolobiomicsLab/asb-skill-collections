---
name: molecular-descriptor-computation
description: Use when when you have a query mass spectrum and a set of candidate molecular structures (as SMILES or 2D/3D coordinates), and you need to prepare them for cross-view similarity comparison or machine learning-based ranking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3694
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  tools:
  - Python 3.11.7
  - RDKit
  - DGL (Deep Graph Library)
  - PyTorch Geometric
  - data_preprocess.py
  - subformula_assign.py
  techniques:
  - mass-spectrometry
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

# molecular-descriptor-computation

## Summary

Compute spectral features and molecular descriptors (views) from query spectra and candidate molecular structures to enable multi-view similarity scoring in mass spectrometry annotation. This is a prerequisite feature engineering step for ranking molecular candidates against experimental spectra.

## When to use

When you have a query mass spectrum and a set of candidate molecular structures (as SMILES or 2D/3D coordinates), and you need to prepare them for cross-view similarity comparison or machine learning-based ranking. Typical trigger: before applying MultiView Projection to score candidates against an experimental spectrum.

## When NOT to use

- If descriptors are already precomputed and stored; skip directly to similarity scoring.
- If your spectrum is unlabeled or lacks sufficient peak information for feature extraction (descriptor quality will degrade).
- If candidate structures are incomplete or malformed (SMILES parsing will fail); validate molecular structure data first.

## Inputs

- Query mass spectrum (TSV or JSON format with m/z and intensity pairs)
- Candidate molecular structures (SMILES strings or molecular property JSON)
- Spectrum type parameter (formSpec or binnedSpec)
- Optional: subformula labels and assignment directory (if using formSpec)

## Outputs

- Spectral feature vectors (consensus spectra, subformula encodings)
- Molecular descriptor files (fingerprints, DGL/PyG graph objects)
- Preprocessed dataset in structured format (pickle/HDF5) ready for ranking

## How to apply

Load the query spectrum and candidate molecular structures into memory. Extract or compute spectral features (e.g., binned spectra, subformula labels, consensus spectra) and molecular descriptors (e.g., fingerprints, graph representations via DGL/PyG) for both query and candidates. The choice of descriptor type depends on your spectrum representation mode: use formSpec with subformula assignment and consensus spectra, or use binnedSpec with fingerprints. Preprocess using the provided data_preprocess.py script, which handles both modes. Store outputs (fingerprints, consensus spectra files) in structured format for downstream similarity computation.

## Related tools

- **RDKit** (Parse SMILES strings and compute molecular fingerprints and descriptors)
- **DGL (Deep Graph Library)** (Construct and encode molecular graph representations from candidate structures)
- **PyTorch Geometric** (Alternative framework for molecular graph encoding and feature extraction)
- **data_preprocess.py** (MVP-provided preprocessing script to compute fingerprints and consensus spectra from raw spectra and candidates) — github.com/HassounLab/MVP
- **subformula_assign.py** (MVP utility to assign subformula labels for formSpec mode preprocessing) — github.com/HassounLab/MVP

## Examples

```
python data_preprocess.py --spec_type binnedSpec --dataset_pth ../data/sample/data.tsv --candidates_pth ../data/sample/candidates_mass.json --output_dir ../data/sample/
```

## Evaluation signals

- Fingerprint and descriptor files are successfully generated and match expected dimensions (e.g., fingerprint bit length, descriptor count).
- Consensus spectra or subformula encodings are non-null and contain expected range of values (e.g., normalized intensity 0–1, valid subformula indices).
- Preprocess script runs without errors and outputs all intermediate files (fingerprints, consensus spectra) to the specified output directory.
- Molecular structures parse without exception and yield valid SMILES representations (RDKit canonicalization should succeed).
- Descriptor outputs align in count and order with input candidate set (one descriptor row per candidate molecule).

## Limitations

- Descriptor quality depends on input spectrum peak labeling and resolution; low-quality spectra yield poor features.
- RDKit may fail to parse invalid or non-standard SMILES; input validation required.
- Subformula assignment (formSpec mode) is limited to max 60 formulae per spectrum and may be computationally expensive for large candidate sets.
- Graph-based descriptors (DGL/PyG) require valid 2D/3D molecular coordinates; invalid or missing structures will cause preprocessing to fail.

## Evidence

- [other] Extract or compute spectral features and molecular descriptors (views) for both query and candidates.: "Extract or compute spectral features and molecular descriptors (views) for both query and candidates."
- [readme] We provide sample spectra data and candidates in `data/sample`. For preprocessing: 1. If using formSpec, compute subformula labels 2. Run our preprocess code to obatain fingerprints and consensus spectra files: "We provide sample spectra data and candidates in `data/sample`. For preprocessing: 1. If using formSpec, compute subformula labels 2. Run our preprocess code to obatain fingerprints and consensus"
- [readme] python data_preprocess.py --spec_type binnedSpec --dataset_pth ../data/sample/data.tsv --candidates_pth  ../data/sample/candidates_mass.json --output_dir ../data/sample/: "python data_preprocess.py --spec_type binnedSpec --dataset_pth ../data/sample/data.tsv --candidates_pth  ../data/sample/candidates_mass.json --output_dir ../data/sample/"
- [readme] Key packages - dgl - pytorch - rdkit - pytorch-geometric: "Key packages - dgl - pytorch - rdkit - pytorch-geometric"
- [readme] We include sample subformula, fingerprint, and consensus spectra data in `../data/sample/`.: "We include sample subformula, fingerprint, and consensus spectra data in `../data/sample/`."
