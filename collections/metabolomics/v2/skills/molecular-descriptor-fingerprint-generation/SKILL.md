---
name: molecular-descriptor-fingerprint-generation
description: Use when you have a collection of chemical structures (SMILES, InChI, SDF, or mol formats) and need to train or apply a machine learning model for retention time prediction or molecular property estimation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3697
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3373
  tools:
  - alvaDesc
  - RDKit
  - cmmrt
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
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
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

# molecular-descriptor-fingerprint-generation

## Summary

Generate molecular descriptors and multiple fingerprint types (MACCS166, Extended Connectivity, Path) from chemical structures using alvaDesc to create feature vectors for machine learning-based retention time prediction and metabolite annotation. This skill bridges molecular structure representation and downstream ML models by systematically computing both handcrafted chemical properties and structural fingerprints.

## When to use

You have a collection of chemical structures (SMILES, InChI, SDF, or mol formats) and need to train or apply a machine learning model for retention time prediction or molecular property estimation. Use this skill when fingerprint-based representations have empirically outperformed descriptor-only features in your domain (as demonstrated in SMRT retention time prediction, where fingerprints achieve lower MAE than descriptors alone), or when you need to generate both descriptor and fingerprint representations to compare their relative predictive power.

## When NOT to use

- Input is already a pre-computed feature table or fingerprint matrix; skip generation and proceed to model training.
- You require real-time inference with sub-millisecond latency; alvaDesc feature generation requires external software licensing and non-negligible compute time per molecule.
- Fingerprint type diversity is not available or your domain requires novel fingerprints not implemented in alvaDesc (e.g., custom pharmacophoric patterns); verify fingerprint availability before committing.

## Inputs

- Chemical structures in SMILES format (string)
- Chemical structures in InChI format (string)
- SDF, mol, mol2, or hin format files
- PubChem ID references (mapped to SDF structures)
- CSV file with compound identifiers and structure representations

## Outputs

- Feature vectors: concatenated ECFP + MACCSFP + PFP fingerprints (2,214 features total)
- Feature vectors: 5,666 molecular descriptors
- Combined feature vectors: descriptors + fingerprints (concatenated)
- alvaDesc-serialized fingerprint/descriptor files for downstream ML training

## How to apply

Load chemical structures in SMILES, InChI, SDF, mol, mol2, or hin format into alvaDesc. Generate the standardized fingerprint set: MACCS166 keys, Extended Connectivity Fingerprints (ECFP), and Path Fingerprints (PFP), alongside 5,666 molecular descriptors. Concatenate fingerprint outputs sequentially (ECFP + MACCSFP + PFP) into a single feature vector per molecule. When comparing feature types, train separate models on (1) descriptors only, (2) fingerprints only, and (3) both concatenated, then evaluate mean and median absolute error across each condition. Fingerprints alone typically yield lower error (mean absolute error ~39.2 s for SMRT) compared to descriptors alone or their combination for chromatographic retention time tasks.

## Related tools

- **alvaDesc** (Primary tool for computing 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) from chemical structures in standard formats (SMILES, InChI, SDF, mol, mol2, hin)) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative fingerprint generation for DNN training; used in cmmrt notebooks to compute fingerprints when alvaDesc licensing is unavailable) — https://www.rdkit.org/
- **cmmrt** (Reference implementation containing build_data.py functions (generate_vector_fingerprints, generate_vector_fps_descs) for orchestrating alvaDesc feature generation and preprocessing for SMRT dataset) — https://github.com/constantino-garcia/cmmrt

## Examples

```
from cmmrt.rt.build_data import generate_vector_fps_descs; aDesc_instance = initialize_alvadesc(); features = generate_vector_fps_descs(aDesc_instance, chemicalStructureFile='compounds.sdf', fingerprint_types=('ECFP', 'MACCSFP', 'PFP'), descriptors=True)
```

## Evaluation signals

- Fingerprint output dimensionality: ECFP + MACCSFP + PFP should total 2,214 features; descriptor vectors should contain exactly 5,666 dimensions.
- Concatenation correctness: verify that combined feature vectors have 2,214 + 5,666 = 7,880 total features when both types are merged.
- No missing or NaN values: 100% completion rate across all molecules in the input set; any failures should be logged and investigated.
- Comparative model performance: fingerprints-only models should achieve mean absolute error ≤39.2±1.2 s and median absolute error ≤17.2±0.9 s on SMRT retention time tasks; descriptors-only should show higher error, validating feature quality.
- Schema compliance: output vectors must be serializable to formats compatible with downstream ML pipelines (NumPy arrays, CSV, HDF5) without dimension mismatch or data loss.

## Limitations

- alvaDesc is commercial software requiring a license; open-source alternatives (RDKit) provide fingerprints but may differ slightly in computed values.
- Fingerprint dimensionality and composition (MACCS166, ECFP, PFP) are fixed by alvaDesc; novel or domain-specific fingerprints require custom implementation.
- Computational cost scales linearly with molecule count; generating 5,666 descriptors + 2,214 fingerprints for 80,038 molecules (SMRT dataset) requires significant compute time not quantified in the article.
- Feature generation assumes valid, well-formed chemical structures; malformed SMILES or InChI inputs will fail silently or produce corrupted feature vectors.
- The standardized fingerprint set was optimized for SMRT retention time prediction; performance on other molecular property prediction tasks (solubility, toxicity, etc.) is untested.

## Evidence

- [readme] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [readme] Results suggest that fingerprints tend to perform better than descriptors alone or combined: "The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better."
- [readme] Mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s achieved with DNN trained on fingerprints: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [readme] Function to generate fingerprints from SMILES or structure files using alvaDesc: "the function generate_vector_fingerprints(aDesc, chemicalStructureFile = None, smiles = None) generates the fingerprints used in the CMM RT model. This function processes an instance of the alvaDesc"
- [readme] Fingerprints concatenated sequentially in specific order for model input: "It returns a string formed the values of the ECFP, MACCSFP and PFP fingerprints sequentially joint."
