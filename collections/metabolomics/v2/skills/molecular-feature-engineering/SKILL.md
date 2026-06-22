---
name: molecular-feature-engineering
description: Use when you have a set of chemical structures (small molecules, metabolites, or drug-like compounds) represented as SMILES, SDF, mol, InChI, or mol2 files, and you need to train a machine learning model to predict a molecular property (e.g., retention time, solubility, binding affinity).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3577
  tools:
  - alvaDesc
  - RDKit
  - build_data.py (cmmrt package)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-feature-engineering

## Summary

Generate a unified feature matrix of molecular descriptors and fingerprints from chemical structures (SMILES, SDF, mol, or InChI) using alvaDesc, enabling downstream machine learning model training for tasks such as retention time prediction. This skill bridges structural chemistry input to quantitative feature space suitable for regression or classification.

## When to use

You have a set of chemical structures (small molecules, metabolites, or drug-like compounds) represented as SMILES, SDF, mol, InChI, or mol2 files, and you need to train a machine learning model to predict a molecular property (e.g., retention time, solubility, binding affinity). You do not yet have a feature matrix; raw structures must be converted to numerical descriptors and/or fingerprints.

## When NOT to use

- Input is already a feature table or descriptor matrix—skip directly to model training.
- Chemical structures are too large or complex for alvaDesc to process (e.g., macromolecules, polymers, or proteins); use protein-specific featurization tools instead.
- Fingerprint diversity or descriptor interpretability is the primary goal rather than predictive performance; consider dimensionality reduction or feature selection after generation.

## Inputs

- chemical structure file (SMILES string, SDF file, mol file, InChI, or mol2 format)
- molecule identifier (e.g., PubChem ID, custom ID)
- list or batch of molecules (≥1 compound; tested on 80,038 molecules in source study)

## Outputs

- molecular descriptor matrix (rows=molecules, columns=5,666 descriptor features)
- molecular fingerprint matrix (rows=molecules, columns=2,214 fingerprint features from MACCS166, ECFP, PFP)
- unified feature matrix (rows=molecules, columns=5,666 descriptors + 2,214 fingerprints concatenated)
- CSV or tabular file ready for machine learning model training

## How to apply

Load the molecular dataset (e.g., 80,038 molecules from METLIN SMRT) and configure alvaDesc to compute both molecular descriptors (5,666 features across physicochemical, topological, and structural categories) and multiple fingerprint types (MACCS166, Extended Connectivity Fingerprints/ECFP, and Path Fingerprints/PFP). Execute alvaDesc in batch mode on all molecules, then combine descriptor and fingerprint outputs into a single feature matrix with rows representing molecules and columns representing the concatenated descriptor and fingerprint values. The resulting matrix can be used to train machine learning regressors; empirical evidence from the source paper shows that fingerprints tend to outperform descriptors alone, though both can be combined. Export the final feature matrix as a CSV or tabular format compatible with downstream machine learning libraries.

## Related tools

- **alvaDesc** (Computes molecular descriptors (5,666 features) and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints; 2,214 total) from chemical structures in batch mode) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative fingerprint generation tool used in supplementary notebooks (train_with_rdkit.ipynb) as an open-source option for ECFP, MACCS, and path-based fingerprints) — https://github.com/rdkit/rdkit
- **build_data.py (cmmrt package)** (Provides Python functions generate_vector_fingerprints() and generate_vector_fps_descs() to integrate alvaDesc processing, handle SMILES/structure file input, and format fingerprint and descriptor outputs for CMM-RT model training) — https://github.com/constantino-garcia/cmmrt

## Examples

```
from cmmrt.rt.build_data_cmm import generate_vector_fps_descs; aDesc_instance = initialize_alvadesc(); features = generate_vector_fps_descs(aDesc_instance, chemicalStructureFile='molecules.sdf', fingerprint_types=('ECFP', 'MACCSFP', 'PFP'), descriptors=True)
```

## Evaluation signals

- Feature matrix dimensions match expected output: rows = number of input molecules; columns = 5,666 descriptors + 2,214 fingerprints (or subset thereof if only descriptors or only fingerprints are used).
- No missing or NaN values in the feature matrix; all molecules processed successfully by alvaDesc.
- Fingerprint features are binary or count-valued (MACCS166, ECFP, PFP); descriptor features are continuous numerical values.
- CSV export is parseable and compatible with downstream machine learning libraries (e.g., scikit-learn, TensorFlow).
- Downstream model trained on the feature matrix achieves reported baseline performance (e.g., mean absolute error ≤ 39.2 s for retention time prediction on SMRT) or comparable to prior published benchmarks.

## Limitations

- alvaDesc is proprietary and requires a commercial license; open-source alternatives (RDKit) are available but may produce different descriptor/fingerprint values and dimensionality.
- Batch processing time scales with dataset size; the source study processed 80,038 molecules but does not report runtime or memory requirements for larger datasets.
- Combined descriptor + fingerprint matrices are high-dimensional (7,880 features); dimensionality reduction or feature selection may be necessary for sparse datasets or interpretability.
- Fingerprints are lossy representations and may not capture all structural nuances; the source paper shows fingerprints outperform descriptors alone for retention time prediction but generalization to other molecular properties is not guaranteed.
- Chemical structures must be valid and parseable by alvaDesc; malformed SMILES, incomplete stereochemistry, or unusual valence states may cause processing failures.

## Evidence

- [other] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [other] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [other] The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better.: "The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better."
- [readme] To train your own model or to predict the RT of your own set of compounds it is necessary to generate the fingerprints using alvaDesc software (under license, check alvadesc software).: "To train your own model or to predict the RT of your own set of compounds it is necessary to generate the fingerprints using alvaDesc software"
- [readme] the function generate_vector_fps_descs(aDesc, chemicalStructureFile, fingerprint_types = ("ECFP", "MACCSFP", "PFP"), descriptors = True) generates both the the descriptors and the fingerprints. It contains the descriptors values value by value and the ECFP, MACCSFP and PFP fingerprints andsequentially joint.: "the function generate_vector_fps_descs(aDesc, chemicalStructureFile, fingerprint_types = ("ECFP", "MACCSFP", "PFP"), descriptors = True) generates both the the descriptors and the fingerprints"
