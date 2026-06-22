---
name: fingerprint-computation-maccs-extended-connectivity-path
description: Use when when you have a set of chemical compounds (as SMILES, mol, SDF, mol2, or hin files) and need to convert their structural information into numerical fingerprint vectors for training machine learning regressors on experimental retention time data or other molecular property prediction tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3344
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

# Fingerprint Computation (MACCS, Extended Connectivity, Path)

## Summary

Generate molecular fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints) from chemical structures using alvaDesc to create a standardized feature representation suitable for machine learning-based retention time prediction and metabolite annotation.

## When to use

When you have a set of chemical compounds (as SMILES, mol, SDF, mol2, or hin files) and need to convert their structural information into numerical fingerprint vectors for training machine learning regressors on experimental retention time data or other molecular property prediction tasks. This skill is essential when fingerprint-based features have been empirically shown to outperform descriptor-only approaches on your target prediction task.

## When NOT to use

- Input is already a precomputed numerical feature matrix or fingerprint table—skip directly to model training.
- Chemical structures are in non-standard or proprietary formats not supported by alvaDesc (e.g., custom binary formats); convert to standard format first.
- You require real-time or streaming fingerprint generation at inference time with strict latency constraints; batch alvaDesc computation is offline and computationally intensive.

## Inputs

- Chemical structure files in SMILES, mol, SDF, mol2, or hin format
- Optionally: CSV with pubchem IDs or INCHI identifiers linked to structure files
- alvaDesc software instance (configured and licensed)

## Outputs

- Fingerprint feature matrix (tabular format: CSV or similar) with rows=molecules, columns=MACCS166 + ECFP + PFP bits
- Concatenated fingerprint string per molecule (ECFP, MACCSFP, PFP sequentially joined)
- Optional: combined descriptor and fingerprint feature matrix if both are computed

## How to apply

Load chemical structures in standardized formats (SMILES, mol, SDF, mol2, or hin) into alvaDesc software. Configure alvaDesc to compute three fingerprint types: MACCS166 (166-bit structural key fingerprints), Extended Connectivity Fingerprints (ECFP), and Path Fingerprints (PFP). Execute alvaDesc in batch mode on all molecules to generate fingerprint bit strings. Concatenate the three fingerprint types sequentially for each molecule, forming feature vectors where each position represents a bit in the combined fingerprint. The resulting feature matrix has rows equal to the number of molecules and columns equal to the total bits across all three fingerprint types (typically ~2,214 features in large datasets like METLIN SMRT with 80,038 molecules). Export to a tabular format (CSV or similar) suitable for downstream machine learning model training. Use fingerprints alone or combined with molecular descriptors depending on validation results—empirical evidence from the cited work suggests fingerprints tend to perform better than descriptors alone for retention time prediction.

## Related tools

- **alvaDesc** (Computes molecular fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) in batch mode from chemical structures) — https://www.alvascience.com/alvadesc/
- **RDKit** (Alternative or complementary fingerprint generation tool (Extended Connectivity fingerprints available via RDKit); referenced as notebook example in cmmrt repository)
- **cmmrt** (Python package implementing the fingerprint generation pipeline and downstream retention time prediction; contains build_data.py functions for alvaDesc orchestration) — https://github.com/constantino-garcia/cmmrt

## Examples

```
from cmmrt.rt.build_data_cmm import generate_vector_fps_descs; fps = generate_vector_fps_descs(aDesc, chemicalStructureFile='compounds.sdf', fingerprint_types=('ECFP', 'MACCSFP', 'PFP'), descriptors=False)
```

## Evaluation signals

- Feature matrix dimensions are consistent: rows = number of input molecules, columns = 2,214 (or documented total for your fingerprint configuration).
- No missing or NaN values in fingerprint vectors; all bits are binary (0 or 1) or integer counts if applicable.
- Fingerprint vectors for identical molecules (or very similar structures) are identical or have high Tanimoto similarity (>0.95 for bit-based fingerprints).
- Downstream machine learning model trained on fingerprints achieves lower mean/median absolute error in retention time prediction compared to descriptors alone (consistent with reported 39.2±1.2 s mean and 17.2±0.9 s median errors as baseline for comparison).
- Output file is readable and parseable (e.g., valid CSV with numeric columns and no malformed entries).

## Limitations

- alvaDesc is proprietary software requiring a license; acquisition and setup are non-trivial and cost money.
- Batch processing latency scales with dataset size; generating fingerprints for 80,038 molecules requires hours of computation.
- Fingerprint representations are fixed-length and may lose information for very large or complex molecules; performance on out-of-distribution structures is not guaranteed.
- Three fingerprint types are concatenated sequentially; correlation between fingerprint types is not explicitly handled, which may lead to redundant features in downstream regression models.
- The workflow assumes input structures are valid and processable; malformed or unusual chemical structures may cause alvaDesc to fail or produce unexpected outputs without clear error messaging.

## Evidence

- [intro] 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software: "5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software"
- [intro] The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better.: "The models were trained using only the descriptors, only the fingerprints, and both types of features simultaneously. Results suggest that fingerprints tend to perform better."
- [intro] We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT): "We have trained state-of-the-art machine learning regressors using the 80,038 experimental RTs from the METLIN small molecule dataset (SMRT)"
- [readme] To train your own model or to predict the RT of your own set of compounds it is necessary to generate the fingerprints using alvaDesc software: "To train your own model or to predict the RT of your own set of compounds it is necessary to generate the fingerprints using alvaDesc software"
- [readme] generate_vector_fingerprints(aDesc, chemicalStructureFile = None, smiles = None) generates the fingerprints used in the CMM RT model. This function processes an instance of the alvaDesc software, and the input file path representing the compound of interest in the format SMILES, mol, SDF, mol2 or hin.: "the input file path representing the compound of interest in the format SMILES, mol, SDF, mol2 or hin"
- [readme] It returns a string formed the values of the ECFP, MACCSFP and PFP fingerprints sequentially joint.: "It returns a string formed the values of the ECFP, MACCSFP and PFP fingerprints sequentially joint."
