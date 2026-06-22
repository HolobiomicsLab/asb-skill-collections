---
name: fingerprint-feature-extraction-retention-time
description: Use when when you have a collection of small molecules with known chemical structures (SMILES, SDF, mol, mol2, or hin format) and need to train or apply a retention time prediction model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3375
  tools:
  - alvaDesc
  - RDKit
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

# fingerprint-feature-extraction-retention-time

## Summary

Generate molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) and descriptors from chemical structures to create feature vectors for retention time prediction models. This skill is essential for preparing molecular input data for machine learning regressors that predict chromatographic retention times.

## When to use

When you have a collection of small molecules with known chemical structures (SMILES, SDF, mol, mol2, or hin format) and need to train or apply a retention time prediction model. The fingerprints and descriptors serve as the feature representation for deep neural networks or other regressors that map molecular properties to experimental retention times on a given chromatographic method.

## When NOT to use

- If you already have pre-computed fingerprint or descriptor matrices for your molecules — re-generating them would be redundant.
- If working with macromolecules (proteins, nucleic acids) — this approach is validated only for small molecules in the METLIN dataset.
- If alvaDesc software is unavailable or licensing restrictions prevent its use — the method is tightly coupled to this proprietary tool.

## Inputs

- Chemical structures in SMILES format (string)
- Chemical structures in SDF/mol/mol2/hin file format
- PubChem identifiers with corresponding structure files
- CSV file with pubchem_id and SMILES or inchi columns

## Outputs

- Fingerprint feature vector (concatenated ECFP, MACCSFP, PFP)
- Molecular descriptor vector (5,666 scalar values)
- Combined feature matrix (fingerprints + descriptors)
- Preprocessed data file ready for machine learning regressor training

## How to apply

Use alvaDesc software to generate three types of molecular features: Extended Connectivity Fingerprints (ECFP), MACCS Keys (MACCSFP), and Path Fingerprints (PFP), alongside 5,666 molecular descriptors. Process chemical structures (provided as SMILES strings, SDF files, or PubChem references) through alvaDesc's feature generation pipeline. Concatenate the resulting fingerprints sequentially to form a unified feature vector for each molecule. This multi-fingerprint approach is chosen because empirical results on the METLIN SMRT dataset (80,038 molecules) show fingerprints outperform descriptors alone or in combination. The concatenated vectors serve as input to regularized deep neural networks with cosine annealing warm restarts for training robust retention time predictors.

## Related tools

- **alvaDesc** (Generates 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) from chemical structures) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative fingerprint generation library; notebooks provided for training DNN with RDKit fingerprints as substitute)

## Examples

```
from cmmrt.rt.build_data_cmm import generate_vector_fps_descs; fingerprints_descriptors = generate_vector_fps_descs(aDesc, chemicalStructureFile='compound.sdf', fingerprint_types=('ECFP', 'MACCSFP', 'PFP'), descriptors=True)
```

## Evaluation signals

- Output feature vectors have expected dimensionality: ECFP + MACCSFP + PFP concatenated, plus 5,666 descriptors when combined mode is used.
- No missing or NaN values in generated fingerprint/descriptor vectors; all molecules produce complete feature representations.
- Fingerprint-only models achieve lower median absolute error (17.2±0.9 s) compared to descriptor-only or mixed approaches on held-out test set.
- Feature matrix dimensions match input molecule count; each molecule yields exactly one feature vector of consistent length.
- Validation against reference results: mean absolute error of 39.2±1.2 s and median absolute error of 17.2±0.9 s achieved when features are used to train the regularized DNN baseline on METLIN SMRT.

## Limitations

- Requires proprietary alvaDesc software (licensed tool); no open-source equivalent with identical fingerprint/descriptor definitions is used in the validation.
- Validated only on small molecules in the METLIN SMRT dataset (80,038 molecules); generalization to other molecular datasets or chromatographic methods not explicitly tested in the feature extraction step.
- Fingerprint generation is computationally expensive at scale; the README notes that complete training requires removing the smoke_test flag to process the full SMRT dataset.
- Feature vectors depend on input chemical structure quality and format; malformed SMILES, missing stereochemistry, or incomplete SDF files may cause generation failures or missing features.

## Evidence

- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [readme] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [readme] The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better.: "The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better."
- [readme] The function generate_vector_fingerprints(aDesc, chemicalStructureFile = None, smiles = None) generates the fingerprints used in the CMM RT model. This function processes an instance of the alvaDesc software, and the input file path representing the compound of interest in the format SMILES, mol, SDF, mol2 or hin.: "the input file path representing the compound of interest in the format SMILES, mol, SDF, mol2 or hin"
- [readme] It generates a file containing the ECFP, MACCSFP and PFP fingerprints sequentially joint for each input compound.: "It generates a file containing the ECFP, MACCSFP and PFP fingerprints sequentially joint for each input compound."
