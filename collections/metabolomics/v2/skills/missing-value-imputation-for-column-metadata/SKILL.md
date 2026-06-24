---
name: missing-value-imputation-for-column-metadata
description: Use when when preparing raw HPLC column parameter arrays for featurization
  into feature vectors for retention time prediction models. Specifically apply this
  skill when column metadata contains empty strings (indicating missing diameter or
  pH values) or non-standard string encodings (e.g., '2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - NumPy
  - pandas
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

# missing-value-imputation-for-column-metadata

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Handles missing or malformed values in HPLC column metadata prior to featurization by converting empty strings to numeric zeros and standardizing non-standard parameter encodings. This ensures complete, parseable feature vectors for downstream machine learning of retention times across different chromatographic methods.

## When to use

When preparing raw HPLC column parameter arrays for featurization into feature vectors for retention time prediction models. Specifically apply this skill when column metadata contains empty strings (indicating missing diameter or pH values) or non-standard string encodings (e.g., '2.7 spp' or '2.6 spp' for Tanaka parameters) that would cause parsing errors or inconsistent normalization during one-hot encoding and numerical feature scaling.

## When NOT to use

- Input column metadata is already fully populated with no missing values or non-standard encodings — skip directly to one-hot encoding and normalization.
- Tanaka parameters or other numerical fields are already in native floating-point or integer format — no string replacement step is needed.
- The use case explicitly requires preservation of missing values as NaN for downstream imputation methods (e.g., KNN imputation or matrix factorization) rather than zero-filling.

## Inputs

- raw column_params array (list or numpy array) containing categorical features (company, USP), numerical features (length, diameter, temperature, flow rate, dead time, pH values), and Tanaka parameter block
- column metadata indices indicating which positions contain diameter (3), pH_B (20), and Tanaka parameters (84:92)

## Outputs

- cleaned column_params array with empty strings replaced by 0 and Tanaka parameter strings ('2.7 spp', '2.6 spp') replaced by float 2.7
- intermediate Python variables (e.g., diameter, pH_B, tanaka_params) ready for downstream normalization and concatenation into feature vectors

## How to apply

Inspect the raw column_params array for empty strings in metadata fields known to be frequently missing (diameter at index 3, pH_B at index 20). Replace any empty string with the numeric zero value using conditional checks (e.g., `if column_params[3] == ''`, assign 0). For Tanaka parameter blocks (indices 84:92), scan for string entries matching '2.7 spp' or '2.6 spp' and replace them with the float value 2.7 using list comprehension or conditional replacement. Apply these transformations before concatenating features into the combined HSM/Tanaka feature array, ensuring all numerical fields are floating-point or integer types rather than strings, and all Tanaka parameters are standardized to a single numeric representation for consistent gradient slope calculation downstream.

## Related tools

- **NumPy** (Conditional array manipulation via np.where for converting additive flags to binary and handling missing values; array indexing for diameter and pH field access)
- **pandas** (Optional: reading and validating column metadata from CSV or structured formats before imputation)

## Examples

```
```python
import numpy as np
# Given raw column_params list with empty strings
column_params[3] = '' if column_params[3] == '' else column_params[3]
column_params[3] = 0 if column_params[3] == '' else float(column_params[3])
column_params[20] = 0 if column_params[20] == '' else float(column_params[20])
tanaka_params = [2.7 if p in ['2.7 spp', '2.6 spp'] else float(p) for p in column_params[84:92]]
```
```

## Evaluation signals

- All empty strings in diameter (index 3) and pH_B (index 20) fields are replaced with numeric 0; verify via `isinstance(column_params[3], (int, float))` and `column_params[3] == 0`.
- All Tanaka parameter entries matching '2.7 spp' or '2.6 spp' (indices 84:92) are replaced with float 2.7; verify via `all(isinstance(p, float) for p in column_params[84:92])` and no remaining string entries.
- Downstream normalization step (e.g., `diameter / some_scale`) succeeds without TypeError, confirming all fields are numeric.
- Concatenated feature vector has expected shape after imputation, matching the sum of one-hot encoding dimensions (company + USP + solvent A + solvent B + additives) plus normalized continuous features plus Tanaka parameters.
- No NaN or inf values appear in the final feature array after imputation and normalization; verify via `np.isfinite(feature_array).all()`.

## Limitations

- Assumes that missing diameter and pH_B values should be represented as 0, which may not reflect the true physical measurement; domain experts should validate whether zero-filling is more appropriate than other imputation strategies (e.g., column-wise mean) for downstream model performance.
- Hard-coded replacement of '2.7 spp' and '2.6 spp' with exactly 2.7 does not distinguish between the two original encodings; if the distinction is semantically meaningful, this approach loses information.
- Empty strings are identified via exact string comparison (`== ''`); if missing values are encoded as 'NA', 'N/A', 'null', or None objects, the detection logic will fail and require additional conditional branches.
- The skill does not validate whether zero is a physically plausible value for diameter or pH in the context of HPLC columns; a zero pH or zero diameter could introduce downstream model artifacts.

## Evidence

- [results] Handling missing values by converting empty strings to 0 for diameter and pH_B: "Handling missing values by converting empty strings to 0 for diameter and pH_B  [section=results; evidence='if column_params[3] == '': diameter = 0 if column_params[20] == '': pH_B = 0']"
- [results] Tanaka parameter string cleaning procedure: "Clean Tanaka parameter vector by replacing '2.7 spp' or '2.6 spp' entries with 2.7 float value."
- [results] Tanaka parameters located within column_params array: "extracting Tanaka parameters from column_params[84:92] and computing gradient slopes (s1, s2, s3)"
- [results] Missing value replacement is prerequisite to feature concatenation: "Concatenate all encoded features (company, USP, solvents, additives, normalized numericals) into HSM parameter block (indices 0–91) and append cleaned Tanaka vector (indices 92+) into a single"
- [results] Diameter and pH_B location within metadata structure: "Parse input column_params array containing company name, USP designation, length, diameter, particle size, temperature, flow rate, dead time, solvent A/B identities, additive flags, pH values, and"
