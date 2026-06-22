---
name: hplc-column-parameter-normalization
description: Use when when you have raw HPLC column specifications from RepoRT or similar metadata repositories and need to prepare them as input features for machine learning models. Apply this skill before featurizing molecular structures or training graph transformers for retention time prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3375
  tools:
  - NumPy
  - pandas
  - Graphormer-RT
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# HPLC Column Parameter Normalization

## Summary

Normalizes raw HPLC column metadata (length, temperature, pH) and encodes categorical column features (company, USP type, solvents, additives) into a unified numeric feature vector combining HSM parameter blocks with Tanaka physicochemical parameters. This standardization enables method-independent retention time prediction across reverse-phase and HILIC chromatography.

## When to use

When you have raw HPLC column specifications from RepoRT or similar metadata repositories and need to prepare them as input features for machine learning models. Apply this skill before featurizing molecular structures or training graph transformers for retention time prediction. Trigger: column_params array contains mixed types (strings for company/USP/solvents, floats for length/temp/pH, and Tanaka parameter vectors).

## When NOT to use

- Input is already a featurized array (e.g., already one-hot encoded and normalized); re-normalizing will corrupt the feature space.
- Column metadata is incomplete or missing critical fields (e.g., no solvent identities, no Tanaka parameters); handle as separate data quality issue before applying this skill.
- You are working with a custom proprietary column encoding scheme that does not align with RepoRT structure; adapt the index positions and lookup lists first.

## Inputs

- column_params array (NumPy 1D or list): raw HPLC column metadata including company name (string), USP code (string), length (float), diameter (float or empty string), particle size (float), temperature (float), flow rate (float), dead time (float), HPLC type (string), solvent A identity (string: h2o/meoh/acn/Other), solvent B identity (string), additive A/B flags (int), pH_A/B (float or empty string), gradient time/B% points (time1–4, grad1–4 as floats), and Tanaka parameter vector (indices 84:92, mixed float/string)
- company list (list of strings): predefined reference list of column manufacturers for one-hot encoding
- USP list (list of strings): predefined reference list of USP column types for one-hot encoding
- solvent list (list of strings): predefined reference list ['h2o', 'meoh', 'acn', 'Other'] for solvent identity encoding

## Outputs

- featurized column array (NumPy 1D ndarray, float64): concatenated feature vector with structure [int_encodings (company one-hot + USP one-hot + solvent_A one-hot + solvent_B one-hot + additive_A binary + additive_B binary), normalized_numericals (length/250, temp/100, pH_A/14, pH_B/14), tanaka_params (8 floats), gradient_slopes (s1, s2, s3)]; total length ~110–120 elements depending on company/USP list sizes
- metadata dictionary (optional): mapping of feature indices to names for downstream interpretation

## How to apply

Parse the column_params array containing 92+ elements: company name, USP designation, physical dimensions, temperature, flow rate, dead time, solvent A/B identities, additive flags, pH values, and Tanaka parameter indices [84:92]. (1) One-hot encode categorical features (company, USP type, solvent A/B each as 0/1 binary vectors) using predefined lookup lists. (2) Convert additive presence flags (additive A and B) to binary using np.where(value != 0, 1, 0). (3) Normalize numerical features by dividing length by 250, temperature by 100, and pH values by 14 to bring them into comparable ranges. (4) Clean Tanaka parameters [84:92] by replacing string values like '2.7 spp' or '2.6 spp' with float 2.7, and handle missing values by converting empty strings to 0 for diameter and pH_B. (5) Extract and compute gradient slope features (s1, s2, s3) from B and t parameters if present. (6) Concatenate all encoded features (integer one-hots + additive flags, then float normalized values + Tanaka vector) into a single NumPy array via np.concatenate, producing indices 0–91 (HSM block) and 92+ (Tanaka/gradient slopes).

## Related tools

- **NumPy** (Array concatenation, one-hot encoding via indexing, element-wise normalization (division), np.where for binary conversion, and creation of feature vectors)
- **pandas** (Optional: loading column metadata from CSV/TSV or pickle files (e.g., RepoRT metadata tables) prior to parsing into column_params array)
- **Graphormer-RT** (Downstream consumption of normalized column feature vectors as input to graph transformer retention time prediction model) — https://github.com/HopkinsLaboratory/Graphormer-RT

## Examples

```
import numpy as np
column_params = ['Waters', 'L1', '150', '2.1', '3.5', '30', '0.3', '0.05', 'RPLC', 'h2o', 'acn', '2', '5', '15', '95', '20', '95', '', '', '3.0', '2.5', '5', '95', '5', '95', 0, 0, 0, 0, 0, 0, 0, 0] + [2.7]*8 + [0.5, 1.2, 0.8]
featurized = featurize_column(column_params, index=0)
print(featurized.shape, featurized.dtype)
```

## Evaluation signals

- Output array length is consistent (e.g., 110–120 elements) and matches expected concatenation: len(company_list) + len(USP_list) + 8 (solvent encoding) + 2 (additives) + 4 (normalized numericals) + 8 (Tanaka) + 3 (slopes).
- All normalized numerical features fall within expected ranges: length ∈ [0, 0.3] (if max column length ~75 mm), temp ∈ [0, 1] (room to elevated temps), pH ∈ [0, 1] (pH 0–14 range).
- One-hot encoded categorical features contain exactly one 1 per category block and the rest 0s (no multi-hot or zero-hot entries).
- Tanaka parameter values are floats without string artifacts; '2.7 spp' and '2.6 spp' entries successfully replaced with 2.7.
- Additive flags are binary (0 or 1 only) and reflect presence/absence; empty or missing values converted to 0 without NaN or None.
- Gradient slope features (s1, s2, s3) computed as (B_later − B_earlier) / (t_later − t_earlier) are finite floats (no division by zero or NaN).

## Limitations

- One-hot encoding assumes company and USP types are known and present in predefined reference lists; unknown categories will cause index errors or silent misalignment if not handled explicitly.
- Normalization by fixed divisors (250, 100, 14) assumes typical HPLC parameter ranges; outlier columns (e.g., ultra-long or sub-ambient temperature) may normalize to out-of-bounds values.
- Missing or inconsistent solvent nomenclature (e.g., 'MeOH' vs. 'meoh' vs. 'methanol') requires case normalization and synonym mapping not detailed in the article.
- Tanaka parameter replacement (2.7 spp → 2.7) loses information about the string marker; no audit trail of which entries were modified.
- Gradient slope calculation (s1, s2, s3) is undefined if time points are identical (t2 = t1, etc.); edge case handling not specified in the workflow.
- No versioning or changelog of feature encoding scheme; future changes to company/USP lists or normalization divisors will break reproducibility unless tracked.

## Evidence

- [results] featurize_column function maps raw column parameters into feature vectors by: (1) one-hot encoding categorical features (company, USP, solvents), (2) normalizing numerical features (length/250, temp/100, pH/14): "featurize_column function maps raw column parameters into feature vectors by: (1) one-hot encoding categorical features (company, USP, solvents), (2) normalizing numerical features (length/250,"
- [results] extracting Tanaka parameters from column_params[84:92] and computing gradient slopes (s1, s2, s3), (4) extracting HSMB parameters from column_params[92:], and (5) concatenating integer encodings (categorical + additive presence flags) with float encodings: "extracting Tanaka parameters from column_params[84:92] and computing gradient slopes (s1, s2, s3), (4) extracting HSMB parameters from column_params[92:], and (5) concatenating integer encodings"
- [results] Clean Tanaka parameter vector by replacing '2.7 spp' or '2.6 spp' entries with 2.7 float value. 8. Handle missing values by converting empty strings to 0 for diameter and pH_B.: "Clean Tanaka parameter vector by replacing '2.7 spp' or '2.6 spp' entries with 2.7 float value. 8. Handle missing values by converting empty strings to 0 for diameter and pH_B."
- [results] def featurize_column(column_params, index): company = one_hot_company(column_params[0]) USP = one_hot_USP(column_params[1]) length = float(column_params[2]) / 250: "def featurize_column(column_params, index): company = one_hot_company(column_params[0]) USP = one_hot_USP(column_params[1]) length = float(column_params[2]) / 250"
- [intro] From Reverse Phase Chromatography to HILIC: Graph Transformers Power Method-Independent Machine Learning of Retention Times: "From Reverse Phase Chromatography to HILIC: Graph Transformers Power Method-Independent Machine Learning of Retention Times"
- [readme] The pickle files (/home/cmkstien/RT_pub/Graphormer_RT/sample_data/HILIC_metadata.pickle, /home/cmkstien/RT_pub/Graphormer_RT/sample_data/RP_metadata.pickle) contain processed column metada generated from RepoRT with the following header: ['company_name', 'usp_code', 'col_length', 'col_innerdiam', 'col_part_size', 'temp', 'col_fl', 'col_dead', 'HPLC_type','A_solv', 'B_solv', 'time1', 'grad1', 'time2', 'grad2', 'time3', 'grad3', 'time4', 'grad4', 'A_pH', 'B_pH']: "The pickle files (/home/cmkstien/RT_pub/Graphormer_RT/sample_data/HILIC_metadata.pickle, /home/cmkstien/RT_pub/Graphormer_RT/sample_data/RP_metadata.pickle) contain processed column metada generated"
