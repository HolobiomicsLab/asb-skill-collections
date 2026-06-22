---
name: batch-structure-processing
description: Use when you have a collection of 100+ molecules in SMILES, SDF, MOL, or MOL2 format and need to compute a unified feature representation combining physicochemical descriptors and structural fingerprints for downstream machine learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0306
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0092
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
---

# batch-structure-processing

## Summary

Batch processing of chemical structures through alvaDesc to generate standardized molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path) for large molecular datasets. This skill is essential for preparing feature matrices for machine learning models in retention time prediction and metabolite annotation workflows.

## When to use

Apply this skill when you have a collection of 100+ molecules in SMILES, SDF, MOL, or MOL2 format and need to compute a unified feature representation combining physicochemical descriptors and structural fingerprints for downstream machine learning. Specifically useful when training regressors for retention time prediction or when performing cross-method projection of chromatographic data.

## When NOT to use

- Input is already a pre-computed feature table or descriptor matrix — skip directly to feature selection or model training.
- Molecules are very small organic compounds (< 10 atoms) or simple salts where fingerprint diversity is minimal; descriptors alone may be sufficient.
- You require real-time or streaming structure processing rather than batch; alvaDesc batch mode is optimized for offline processing of entire datasets at once.

## Inputs

- SMILES strings or chemical structure files (SDF, MOL, MOL2, HIN format)
- Molecular dataset metadata (pubchem IDs, inchi identifiers, or direct structure representations)
- alvaDesc software configuration or command-line parameters

## Outputs

- Unified feature matrix (CSV or tabular format): rows = molecules, columns = 5,666 descriptors + 2,214 fingerprints
- Individual descriptor vector file (5,666 features per molecule)
- Individual fingerprint vector file (2,214 features per molecule: MACCS166, ECFP, PFP concatenated)

## How to apply

Load your molecular structures (SMILES or SDF files) into alvaDesc and configure batch processing to compute both descriptor and fingerprint sets simultaneously. Configure alvaDesc to generate 5,666 molecular descriptors across physicochemical, topological, and structural categories, and 2,214 fingerprints using MACCS166, Extended Connectivity, and Path Fingerprint algorithms. Execute batch mode processing on all molecules to generate feature vectors, then concatenate descriptor and fingerprint outputs row-wise (molecules × features) into a unified CSV feature matrix. Export as tabular format with molecules as rows and all descriptors+fingerprints as columns. Validate that the resulting feature matrix has no missing values and contains the expected column counts (5,666 + 2,214 = 7,880 features) before passing to machine learning training.

## Related tools

- **alvaDesc** (Batch computation of 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) from chemical structure files) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative open-source option for fingerprint generation (ECFP, MACCSFP, PFP equivalents) as demonstrated in training notebooks)
- **cmmrt/build_data.py** (Python utility functions for orchestrating batch fingerprint and descriptor generation; wraps alvaDesc API calls) — https://github.com/constantino-garcia/cmmrt/blob/master/cmmrt/rt/build_data_cmm.py

## Examples

```
from cmmrt.rt.build_data import generate_vector_fps_descs; features = generate_vector_fps_descs(aDesc, chemicalStructureFile='molecules.sdf', fingerprint_types=('ECFP', 'MACCSFP', 'PFP'), descriptors=True)
```

## Evaluation signals

- Feature matrix shape is (N_molecules, 7880) where N_molecules matches input dataset size and 7880 = 5,666 descriptors + 2,214 fingerprints.
- No NaN or missing values in descriptor or fingerprint columns; all 80,038 molecules (or input count) have complete feature vectors.
- Fingerprint vectors are binary or count-valued (MACCS166 bits, ECFP/PFP counts) and descriptor vectors are floating-point physicochemical properties; verify column data types are consistent with expected ranges.
- CSV export has valid tabular structure with headers matching descriptor names and fingerprint type identifiers (e.g., 'MACCS_bit_1', 'ECFP_count', 'PFP_count').
- Downstream machine learning model can ingest the feature matrix without shape or dtype errors; fingerprint-only models show comparable or superior retention time prediction error (mean absolute error ≤ 50 s) compared to descriptor-only baseline.

## Limitations

- alvaDesc is commercial software requiring a license; open-source alternatives (RDKit) produce similar but not identical fingerprints and may differ in descriptor coverage.
- Batch processing speed and memory overhead scale linearly with dataset size; METLIN SMRT (80,038 molecules) requires significant computational resources and wall-clock time.
- Fingerprint generation is deterministic but depends on exact alvaDesc version and configuration; minor software updates may produce slightly different bit patterns or counts, affecting reproducibility.
- The skill assumes input structures are valid and properly formatted; malformed SMILES or corrupted SDF files will cause alvaDesc to skip or error on individual molecules, reducing feature matrix row count.

## Evidence

- [intro] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [intro] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [other] Configure alvaDesc to compute 5,666 molecular descriptors across physicochemical, topological, and structural categories: "Configure alvaDesc to compute 5,666 molecular descriptors across physicochemical, topological, and structural categories"
- [other] Combine descriptor and fingerprint outputs into a unified feature matrix with rows=molecules and columns=descriptors+fingerprints: "Combine descriptor and fingerprint outputs into a unified feature matrix with rows=molecules and columns=descriptors+fingerprints"
- [readme] To train your own model or to predict the RT of your own set of compounds it is necessary to generate the fingerprints using alvaDesc software: "To train your own model or to predict the RT of your own set of compounds it is necessary to generate the fingerprints using alvaDesc software"
- [readme] The function generate_vector_fps_descs(aDesc, chemicalStructureFile, fingerprint_types = ("ECFP", "MACCSFP", "PFP"), descriptors = True) generates both the the descriptors and the fingerprints: "The function generate_vector_fps_descs(aDesc, chemicalStructureFile, fingerprint_types = ("ECFP", "MACCSFP", "PFP"), descriptors = True) generates both the the descriptors and the fingerprints"
