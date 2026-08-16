---
name: binary-additive-flag-encoding
description: Use when constructing HPLC column feature vectors from raw metadata that
  includes additive composition flags (e.g., presence/absence or concentration of
  formic acid, acetic acid, TFA, or phosphoric acid in mobile phase eluents A and
  B).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - NumPy
  - pandas
  - Graphormer-RT
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
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

# binary-additive-flag-encoding

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Converts HPLC eluent additive presence flags (formic acid, acetic acid, trifluoroacetic acid, phosphoric acid) into binary indicators (0 or 1) for use in chromatographic column feature vectors. This encoding enables machine learning models to incorporate categorical additive composition information into method-independent retention time prediction.

## When to use

Apply this skill when constructing HPLC column feature vectors from raw metadata that includes additive composition flags (e.g., presence/absence or concentration of formic acid, acetic acid, TFA, or phosphoric acid in mobile phase eluents A and B). Use it as part of the featurize_column workflow when preparing inputs for graph transformer models of retention times across different chromatographic methods (reverse phase, HILIC).

## When NOT to use

- Input already contains normalized or pre-encoded additive features (e.g., one-hot encoded individual additive types).
- Additive information is missing or not part of the column metadata structure.
- The analysis goal does not require categorical mobile phase composition (e.g., purely molecular descriptor–based models without method parameters).

## Inputs

- column_params array (raw HPLC metadata including additive A and B flags at defined indices)
- additive presence values (numeric or string representation: 0, non-zero number, or empty string)

## Outputs

- binary additive flag vector (numpy array of 0/1 integers for additive A presence)
- binary additive flag vector (numpy array of 0/1 integers for additive B presence)
- concatenated integer encoding block including company, USP, solvent, and additive binary flags

## How to apply

Extract additive presence values from the column_params array (indices corresponding to additive A and B flags). Apply np.where to convert all non-zero additive values to 1, leaving zeros unchanged: `add_A_vals = np.where(add_A_vals != 0, 1, add_A_vals)` and `add_B_vals = np.where(add_B_vals != 0, 1, add_B_vals)`. This creates binary (0/1) presence indicators regardless of the original representation (e.g., concentration units, empty strings). Concatenate the resulting binary vectors into the integer encoding block (indices 0–91) of the HSM parameter block, keeping them separate from float-valued normalized features and physicochemical parameters (Tanaka/HSMB blocks).

## Related tools

- **NumPy** (Implements np.where conditional logic for binary conversion of additive flags; performs array concatenation of integer encodings)
- **Graphormer-RT** (Consumes the featurized column vectors (including binary additive encodings) as input to graph transformer model for retention time prediction) — https://github.com/HopkinsLaboratory/Graphormer-RT

## Examples

```
import numpy as np
add_A_vals = np.array([0.1, 0, 0.05])
add_B_vals = np.array([0, 0, 0.02])
add_A_binary = np.where(add_A_vals != 0, 1, add_A_vals)
add_B_binary = np.where(add_B_vals != 0, 1, add_B_vals)
int_encodings = np.concatenate([company, USP, solv_A, solv_B, add_A_binary, add_B_binary])
```

## Evaluation signals

- Output binary vectors contain only 0 and 1 values; no other integers or floats present.
- Length of additive flag vectors matches expected dimensions (typically 1 per eluent A/B or per additive type depending on metadata structure).
- Concatenated int_encodings block maintains correct index alignment: company one-hot, USP one-hot, solvent A/B one-hot, then additive A/B binary flags, with no gaps or overlaps.
- Non-zero input additive values (e.g., 0.1%, 0.05 M, any concentration > 0) all map to 1; zero and empty string values map to 0.
- Featurized column vectors produce consistent retention time predictions when fed to trained Graphormer-RT models, indicating successful integration with downstream graph transformer.

## Limitations

- Binary encoding loses quantitative information about additive concentration, which may be relevant for fine-grained retention prediction in some methods.
- Empty string handling converts to 0 globally; if empty strings represent 'unknown' rather than 'absent', this may introduce systematic bias.
- The encoding assumes all additive columns share the same presence/absence semantics; heterogeneous metadata (e.g., some columns using concentration, others using boolean flags) must be normalized before conversion.
- No validation that additive flags are semantically consistent with mobile phase solvent identity (e.g., phosphoric acid often used in aqueous eluents); misalignment is not detected by the encoding step itself.

## Evidence

- [results] Conversion of additive values to binary (0 or 1) by checking if non-zero: "add_A_vals = np.where(add_A_vals != 0, 1, add_A_vals)
add_B_vals = np.where(add_B_vals != 0, 1, add_B_vals)"
- [results] Additive flags are part of the integer encoding block concatenated with one-hot categorical features: "int_encodings = np.concatenate([[-2],company, USP, solv_A, solv_B, add_A_vals,"
- [results] Handling missing values by converting empty strings to 0 for additive-adjacent features: "Handling missing values by converting empty strings to 0 for diameter and pH_B"
- [results] Additive metadata is extracted from column parameters as part of featurization workflow: "Featurization of HPLC column parameters including diameter, particle size, temperature, flow rate, dead time, solvent composition, pH, and Tanaka/HSMB physicochemical parameters"
- [results] Binary additive encodings are concatenated into the HSM parameter block used by retention time model: "concatenating integer encodings (categorical + additive presence flags) with float encodings (normalized continuous features and physicochemical parameters)"
