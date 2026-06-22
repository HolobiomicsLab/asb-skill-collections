---
name: molecular-descriptor-generation
description: Use when you have a collection of chemical structures (80,000+ molecules from sources like METLIN SMRT dataset) that need to be converted into numerical feature vectors for machine learning-based retention time (RT) prediction, or when you need to compare descriptor-only, fingerprint-only, and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0250
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_3407
  tools:
  - alvaDesc
  - RDKit
  - cmmrt/build_data.py
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-descriptor-generation

## Summary

Generate a comprehensive feature matrix of molecular descriptors and fingerprints from chemical structures using alvaDesc, enabling machine learning-based molecular property prediction. This skill is essential for converting raw chemical structure data (SMILES, SDF, mol files) into a tabular feature representation suitable for retention time prediction and metabolite annotation.

## When to use

Apply this skill when you have a collection of chemical structures (80,000+ molecules from sources like METLIN SMRT dataset) that need to be converted into numerical feature vectors for machine learning-based retention time (RT) prediction, or when you need to compare descriptor-only, fingerprint-only, and combined feature configurations to identify the best feature set for RT model training.

## When NOT to use

- Input is already a numerical feature table or pre-computed descriptor/fingerprint matrix — skip directly to feature selection or model training.
- Molecules are very large (>1000 atoms) or contain exotic chemistry outside alvaDesc's supported scope — consider alternative cheminformatics tools (RDKit, MOE) for compatibility.
- Real-time prediction is required on individual molecules — pre-compute descriptors/fingerprints in batch mode offline, then load from cache for inference.

## Inputs

- Chemical structure file (SMILES text, SDF, mol, mol2, or hin format)
- List of molecule identifiers (e.g., PubChem IDs, InChI strings)
- alvaDesc software instance (licensed)

## Outputs

- Molecular descriptor matrix (80,038 molecules × 5,666 descriptors)
- Molecular fingerprint matrix (80,038 molecules × 2,214 fingerprints: MACCS166 + ECFP + PFP)
- Unified feature matrix (80,038 molecules × 7,880 combined descriptors+fingerprints, CSV or tabular format)

## How to apply

Load the chemical structure dataset (SMILES or structural file formats: SDF, mol, mol2, hin) into alvaDesc. Configure alvaDesc to compute two parallel feature sets: (1) 5,666 molecular descriptors covering physicochemical, topological, and structural categories, and (2) 2,214 fingerprints using three algorithms (MACCS166, Extended Connectivity Fingerprints/ECFP, and Path Fingerprints/PFP). Execute alvaDesc in batch mode on all molecules to generate both descriptor and fingerprint sets. Combine the output descriptor and fingerprint matrices into a unified feature matrix with rows corresponding to molecules and columns to descriptor+fingerprint features. Export as CSV or tabular format. Note that empirical evidence from the METLIN SMRT training (80,038 molecules) shows fingerprints tend to outperform descriptors alone for RT prediction, so prioritize fingerprint features if computational resources are constrained.

## Related tools

- **alvaDesc** (Batch computation engine for generating 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) from chemical structures in SMILES, SDF, mol, mol2, or hin format) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative open-source cheminformatics library for fingerprint generation (used in train_with_rdkit.ipynb notebook for DNN training))
- **cmmrt/build_data.py** (Python utility module for orchestrating alvaDesc fingerprint and descriptor generation; contains generate_vector_fingerprints() and generate_vector_fps_descs() functions) — https://github.com/constantino-garcia/cmmrt/blob/master/cmmrt/rt/build_data_cmm.py

## Examples

```
from cmmrt.rt.build_data import generate_vector_fps_descs; vector = generate_vector_fps_descs(aDesc, chemicalStructureFile='molecule.sdf', fingerprint_types=('ECFP', 'MACCSFP', 'PFP'), descriptors=True)
```

## Evaluation signals

- Feature matrix dimensions match expected output: rows = input molecule count (e.g., 80,038), columns = 5,666 descriptors + 2,214 fingerprints = 7,880 total.
- Descriptor and fingerprint submatrices are numerically distinct: descriptors contain continuous physicochemical values; fingerprints contain binary or count values (MACCS166, ECFP, PFP).
- No missing values or NaN entries in the unified feature matrix; all 80,038 molecules successfully converted to feature vectors.
- CSV export is valid and parseable; row count matches molecule count; column headers clearly label descriptor/fingerprint type and ID.
- Empirical validation: train ML regressors on fingerprint-only vs. descriptor-only feature sets and confirm fingerprint-only achieves lower mean/median absolute errors than descriptor-only (literature: fingerprints ~39.2±1.2 s MAE vs. higher for descriptors on SMRT).

## Limitations

- alvaDesc is a commercial licensed software; free alternatives (RDKit) have different descriptor/fingerprint catalogs and may not replicate results.
- Batch processing is computationally expensive for very large molecule sets (80,038 molecules × 7,880 features); parallelization and memory management are required.
- Combined descriptor+fingerprint feature matrices are high-dimensional (7,880 features) and prone to overfitting; dimensionality reduction or regularization is recommended before model training.
- Fingerprint generation assumes valid, 2D chemical structures; invalid or incomplete structures may yield missing or zero-valued fingerprints.
- Results are specific to METLIN SMRT dataset (80,038 molecules with experimental RTs); generalization to other molecule sets or RT platforms requires re-training meta-learned projections with ≥10 calibration molecules.

## Evidence

- [intro] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [intro] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [intro] The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better.: "The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better."
- [readme] To train your own model or to predict the RT of your own set of compounds it is necessary to generate the fingerprints using alvaDesc software (under license, check alvadesc software).: "To train your own model or to predict the RT of your own set of compounds it is necessary to generate the fingerprints using alvaDesc software (under license"
- [readme] The function generate_vector_fps_descs(aDesc, chemicalStructureFile, fingerprint_types = ("ECFP", "MACCSFP", "PFP"), descriptors = True) generates both the the descriptors and the fingerprints.: "The function generate_vector_fps_descs(aDesc, chemicalStructureFile, fingerprint_types = ("ECFP", "MACCSFP", "PFP"), descriptors = True) generates both the the descriptors and the fingerprints."
