---
name: feature-matrix-assembly
description: Use when when you have a set of chemical structures (SMILES, SDF, mol,
  mol2, or hin files) and need to convert them into a tabular feature representation
  for retention time prediction, metabolite annotation, or other quantitative structure–property
  modeling tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - alvaDesc
  - RDKit
  - cmmrt build_data.py
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity,
  and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt_cq
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-022-00613-8
  all_source_dois:
  - 10.1186/s13321-022-00613-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-matrix-assembly

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assemble a unified feature matrix combining molecular descriptors and fingerprints from chemical structure input, creating a row-per-molecule table ready for machine learning model training. This skill bridges molecular representation generation and downstream regression or classification workflows.

## When to use

When you have a set of chemical structures (SMILES, SDF, mol, mol2, or hin files) and need to convert them into a tabular feature representation for retention time prediction, metabolite annotation, or other quantitative structure–property modeling tasks. Use this skill when you require both physicochemical descriptors (topological, structural) and fingerprints (MACCS166, Extended Connectivity, Path) in a single consolidated table.

## When NOT to use

- Input is already a feature matrix or pre-computed descriptor/fingerprint table; skip to model training.
- Your workflow uses only fingerprints or only descriptors; use the individual generation functions instead.
- You require custom descriptor sets not available in the standard alvaDesc configuration (e.g., quantum-mechanical properties or proprietary descriptors).
- Input molecules contain structures that alvaDesc cannot parse (e.g., invalid SMILES, disconnected fragments, or reactive intermediates).

## Inputs

- Chemical structure file(s) in SMILES, SDF, mol, mol2, or hin format
- Molecular dataset metadata (e.g., PubChem IDs, InChI, or direct SMILES strings)
- alvaDesc software instance configured with descriptor and fingerprint calculation parameters

## Outputs

- Unified feature matrix (CSV or tabular file): rows = molecules, columns = 5666 descriptors + 2214 fingerprints
- Row identifiers (molecule names, PubChem IDs, or SMILES strings)
- Column metadata mapping descriptor/fingerprint indices to names

## How to apply

Load molecular structures from your input collection (METLIN SMRT, PubChem-indexed SDF files, or direct SMILES strings). Configure alvaDesc to compute 5,666 molecular descriptors across physicochemical, topological, and structural categories, and 2,214 fingerprints using MACCS166, Extended Connectivity Fingerprints (ECFP), and Path Fingerprints (PFP) algorithms. Execute alvaDesc in batch mode on all molecules to generate both descriptor and fingerprint vectors. Horizontally concatenate descriptor and fingerprint columns into a single matrix with shape [n_molecules × (5666 descriptors + 2214 fingerprints)], ensuring row–column alignment by molecule identifier. Export the complete feature matrix as CSV or tabular format with molecule identifiers as row labels and feature names as column headers. Verify that all molecules from input have corresponding rows and that no NaN or sparse regions exist in the output table before passing to machine learning model training.

## Related tools

- **alvaDesc** (Core tool for batch computation of 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, ECFP, PFP) from chemical structures) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative or complementary fingerprint generation; featured in notebooks for training DNNs with RDKit fingerprints) — https://github.com/rdkit/rdkit
- **cmmrt build_data.py** (Python utility functions to orchestrate alvaDesc processing, fingerprint/descriptor vector generation, and matrix export) — https://github.com/constantino-garcia/cmmrt/blob/main/cmmrt/rt/build_data_cmm.py

## Examples

```
python -c "from cmmrt.rt.build_data_cmm import generate_vector_fps_descs; aDesc = init_alvadesc(); matrix = generate_vector_fps_descs(aDesc, chemicalStructureFile='molecules.sdf', fingerprint_types=('ECFP', 'MACCSFP', 'PFP'), descriptors=True); import pandas as pd; pd.DataFrame(matrix).to_csv('feature_matrix.csv', index=False)"
```

## Evaluation signals

- Output matrix dimensions match expected shape: n_molecules rows and exactly 5666 + 2214 = 7880 feature columns (or documented subset).
- No missing values (NaN) or sparse/zero-only columns in descriptor or fingerprint sections; all alvaDesc computations completed successfully.
- Row identifiers are unique and traceable back to input structures; 1:1 correspondence between input molecules and output rows verified.
- Fingerprint columns contain binary or integer fingerprint bit patterns consistent with MACCS166, ECFP, or PFP specifications; descriptor columns contain numeric values within expected physicochemical ranges (e.g., molecular weight, logP).
- Downstream machine learning model training converges and produces retention time predictions with reported accuracy (e.g., median absolute error ≤ 40 s on SMRT test set) consistent with paper benchmarks.

## Limitations

- alvaDesc is commercial software under license; availability and cost may restrict reproducibility and portability across computational environments.
- Fingerprint and descriptor computation is deterministic but assumes molecular structure quality and completeness; invalid or ambiguous SMILES/structures will fail or produce spurious features.
- The 5,666 descriptors and 2,214 fingerprints are computationally dense; feature matrix memory footprint and I/O overhead scale linearly with dataset size (e.g., 80,038 molecules in SMRT produce ~600 MB+ table).
- No built-in feature selection or dimensionality reduction; high-dimensional output may require downstream filtering or regularization in machine learning models to avoid overfitting, especially on small training sets.
- Feature matrix validity depends on correct alvaDesc configuration; misconfigured descriptor/fingerprint algorithms or batch mode errors will propagate silently into downstream models.

## Evidence

- [other] The feature generation pipeline uses alvaDesc to generate 5,666 molecular descriptors and 2,214 fingerprints: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [other] Combine descriptor and fingerprint outputs into a unified feature matrix: "Combine descriptor and fingerprint outputs into a unified feature matrix with rows=molecules and columns=descriptors+fingerprints"
- [other] Export the complete feature matrix as a CSV or tabular file ready for downstream machine learning: "Export the complete feature matrix as a CSV or tabular file ready for downstream machine learning model training"
- [other] Batch mode execution on all molecules to generate both descriptor and fingerprint sets: "Execute alvaDesc in batch mode on all molecules to generate both descriptor and fingerprint sets"
- [readme] Python utility functions for fingerprint/descriptor vector generation and matrix assembly: "generate_vector_fps_descs(aDesc, chemicalStructureFile, fingerprint_types = ("ECFP", "MACCSFP", "PFP"), descriptors = True) generates both the the descriptors and the fingerprints"
- [intro] Feature matrix used for training machine learning regressors on retention time data: "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
