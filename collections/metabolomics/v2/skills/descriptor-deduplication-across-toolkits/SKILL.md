---
name: descriptor-deduplication-across-toolkits
description: Use when when computing molecular descriptors from SMILES strings using both RDKit and mordred libraries simultaneously, and you need to combine their outputs into a single feature matrix without redundant features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - mordred
  - NumPy
  - pandas
  - RDKit
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- import mordred from mordred import Calculator, descriptors
- import numpy as np
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphormer_rt_cq
    doi: 10.1021/acs.analchem.4c05859
    title: Graphormer-RT
  dedup_kept_from: coll_graphormer_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05859
  all_source_dois:
  - 10.1021/acs.analchem.4c05859
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# descriptor-deduplication-across-toolkits

## Summary

Remove redundant molecular descriptors that exist in both RDKit and mordred libraries, retaining only the RDKit version to create a unified, non-redundant descriptor feature set for machine learning. This deduplication step is essential when combining multiple descriptor calculation toolkits to avoid feature duplication and reduce dimensionality in molecular featurization pipelines.

## When to use

When computing molecular descriptors from SMILES strings using both RDKit and mordred libraries simultaneously, and you need to combine their outputs into a single feature matrix without redundant features. Specifically, apply this skill after calculating descriptors from both libraries but before concatenating them into a unified feature array for downstream machine learning tasks.

## When NOT to use

- Input is already a single-source descriptor matrix (only RDKit or only mordred, not both) — deduplication is unnecessary
- Downstream analysis requires traceability of descriptor source or comparison of toolkit-specific outputs — concatenating deduplicated descriptors may obscure source provenance
- Memory or storage constraints do not permit retaining both RDKit and mordred descriptors in any form — use only one toolkit instead

## Inputs

- SMILES strings (input molecular identifiers)
- RDKit descriptor array (NumPy array of descriptor values computed by RDKit)
- mordred descriptor array (NumPy array of descriptor values computed by mordred Calculator)
- Descriptor name lists from both RDKit and mordred libraries

## Outputs

- Deduplicated mordred descriptor indices or array
- Unified descriptor feature matrix (concatenated RDKit + non-duplicate mordred descriptors)
- Descriptor name mapping (list of final descriptor identifiers post-deduplication)

## How to apply

After calculating descriptor sets from both RDKit (using RDKit's descriptor module) and mordred (using mordred's Calculator with the full descriptor set), identify descriptors that appear in both libraries by name. Remove the mordred versions of these duplicate descriptors using a deduplication function (e.g., `remove_mordred_duplicates`), keeping only the RDKit versions since RDKit descriptors are the preferred source. This approach preserves chemical information coverage while eliminating collinearity and reducing memory footprint. The rationale is that RDKit is the more established and widely validated toolkit in cheminformatics; retaining its descriptors prevents potential method-specific bias from mordred while maintaining comprehensive molecular property coverage. Finally, concatenate the retained RDKit descriptors with the deduplicated (non-duplicate) mordred descriptors into a single feature matrix.

## Related tools

- **RDKit** (Computes molecular descriptors from SMILES; serves as the preferred descriptor source for deduplicated features)
- **mordred** (Computes alternative set of molecular descriptors; sources are filtered to remove duplicates of RDKit descriptors)
- **NumPy** (Handles array manipulation, concatenation, and storage of descriptor matrices in .npz compressed format)
- **pandas** (Optional: facilitates descriptor metadata management and export to .csv/.txt formats for validation)

## Examples

```
cleared_mordred_descriptors, duplicate_indices = remove_mordred_duplicates(mordred_descriptors_array, rdkit_descriptors_array); final_features = np.concatenate([rdkit_descriptors_array, cleared_mordred_descriptors], axis=1)
```

## Evaluation signals

- Verify that the output descriptor count equals (unique RDKit descriptors) + (non-duplicate mordred descriptors) — check no descriptors appear twice
- Confirm all RDKit descriptor names are present in the final deduplicated list and all mordred names in the final list have no RDKit counterpart by exact string matching
- Validate output array shape: rows = number of molecules, columns = count of unique descriptors across both libraries
- Check that deduplicated mordred descriptor indices match expected positions after removal (e.g., if 50 of 500 mordred descriptors are duplicates, retain 450)
- Spot-check a sample of deduplicated descriptor values to ensure they match the original RDKit and mordred arrays at their respective source indices

## Limitations

- Duplicate detection relies on exact name string matching; descriptors with similar names but different calculations (e.g., 'NumRotatableBonds' vs 'RotatableBonds') may not be identified as duplicates
- Retaining only RDKit versions of duplicates assumes RDKit implementations are correct and comparable; this assumption may fail if RDKit and mordred use different normalization or calculation logic for the same descriptor
- No mechanism is provided in the article to handle conflicting or discrepant descriptor values if both libraries produce different results for the same molecular property
- The deduplication function (`remove_mordred_duplicates`) implementation details are not fully specified, leaving interpretation of matching logic to the practitioner

## Evidence

- [results] Calculate RDKit descriptors using RDKit's descriptor module. 3. Calculate mordred descriptors using the mordred Calculator with the full descriptor set. 4. Remove mordred descriptors that duplicate RDKit descriptors using remove_mordred_duplicates function.: "Calculate RDKit descriptors using RDKit's descriptor module. 3. Calculate mordred descriptors using the mordred Calculator with the full descriptor set. 4. Remove mordred descriptors that duplicate"
- [results] The Calc_Descriptors routine retrieves descriptor names from both RDKit and mordred libraries, removes duplicate descriptors that exist in both libraries (keeping RDKit versions), and combines them with extra custom headers to create a unified descriptor feature set: "removes duplicate descriptors that exist in both libraries (keeping RDKit versions), and combines them with extra custom headers to create a unified descriptor feature set"
- [results] Removal of Mordred descriptors that duplicate RDKit descriptors  [section=results; evidence='cleared_mordred_descriptors, duplicate_indeces = remove_mordred_duplicates(cleared_mordred_descriptors, rdkit_descriptors)']: "cleared_mordred_descriptors, duplicate_indeces = remove_mordred_duplicates(cleared_mordred_descriptors, rdkit_descriptors)"
- [results] Concatenate RDKit and deduplicated mordred descriptor arrays into a single feature matrix.: "Concatenate RDKit and deduplicated mordred descriptor arrays into a single feature matrix."
