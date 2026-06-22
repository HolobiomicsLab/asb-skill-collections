---
name: tanaka-physicochemical-descriptor-handling
description: Use when you have raw HPLC column metadata arrays containing Tanaka parameter blocks that will be fed into a featurizer for machine learning on retention times. Tanaka parameters are present but may contain string artifacts ('2.7 spp', '2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - NumPy
  - pandas
  - Graphormer
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

# tanaka-physicochemical-descriptor-handling

## Summary

Extract, clean, and integrate Tanaka physicochemical parameters (indices 84–92 of column metadata arrays) into combined feature vectors for HPLC method-independent retention time prediction. Handles malformed entries ('2.7 spp', '2.6 spp') and computes gradient slope features (s1, s2, s3) needed by graph transformer models.

## When to use

You have raw HPLC column metadata arrays containing Tanaka parameter blocks that will be fed into a featurizer for machine learning on retention times. Tanaka parameters are present but may contain string artifacts ('2.7 spp', '2.6 spp') instead of float values, or may need gradient slope computation from chromatographic timing data. Use this skill when building feature vectors that must combine physicochemical descriptors with HSM parameter blocks for method-agnostic (reverse phase and HILIC) retention modeling.

## When NOT to use

- Tanaka parameters are already known to be clean floats with no string artifacts and your model does not require gradient slope features—use direct feature concatenation instead.
- Column metadata does not include indices 84–92 (e.g., older or non-HPLC datasets without Tanaka parameters)—this skill will fail on incomplete arrays.
- Your retention time model is method-specific (single chromatographic mode) and does not need method-independent feature blending; simpler physicochemical encodings may suffice.

## Inputs

- column_params: numpy array or list of length ≥92, containing company name, USP code, length, diameter, particle size, temperature, flow rate, dead time, solvent identities, additive flags, pH values, and Tanaka parameter vector at indices 84–92
- chromatographic gradient table: (t1, B1), (t2, B2), (t3, B3) tuples or arrays defining time points (min) and %B organic phase
- predefined company, USP, and solvent lists for one-hot encoding of HSM parameter block

## Outputs

- combined_feature_array: concatenated numpy array merging one-hot-encoded HSM block (indices 0–91) with cleaned and slope-augmented Tanaka vector (indices 92+), dtype float or mixed int/float
- gradient_slope_features: three-element array [s1, s2, s3] representing temporal rate of change of organic phase composition

## How to apply

Extract the Tanaka parameter vector from fixed indices 84–92 of the column_params array. Iterate through the vector and replace any entries marked '2.7 spp' or '2.6 spp' with the float value 2.7, converting remaining entries to float. In parallel, compute three gradient slope features from the chromatographic gradient table: s1 = (B2 − B1) / (t2 − t1), s2 = (B3 − B2) / (t3 − t2), and s3 = (B3 − B1) / (t3 − t1), where B_i and t_i are %B mobile phase and time at gradient points i. Concatenate the cleaned Tanaka vector (now indices 92+) with the HSM parameter block (indices 0–91, containing one-hot-encoded categoricals and normalized numericals) into a single combined feature array using np.concatenate. Validate that all Tanaka entries are float type and lie in expected physicochemical ranges before passing to the graph transformer model.

## Related tools

- **NumPy** (Array indexing, slicing, type conversion, and concatenation for extracting Tanaka blocks and building combined feature arrays)
- **Graphormer** (Graph transformer model that consumes the combined feature vectors (HSM + cleaned Tanaka parameters) to predict retention times across HPLC methods) — https://github.com/microsoft/Graphormer
- **Graphormer-RT** (Extension of Graphormer providing pre-trained models and example scripts for HPLC retention time prediction, including featurize_column workflow) — https://github.com/HopkinsLaboratory/Graphormer-RT

## Examples

```
tanaka_params = [2.7 if p == '2.7 spp' or p == '2.6 spp' else float(p) for p in column_params[84:92]]; s1 = (B2 - B1) / (t2 - t1); feature_array = np.concatenate([hsm_block, tanaka_params])
```

## Evaluation signals

- All entries in the cleaned Tanaka vector are float type (np.dtype('float64') or equivalent); no string artifacts remain.
- Tanaka entries marked '2.7 spp' or '2.6 spp' are replaced with 2.7; all others convert to float without exception.
- Gradient slopes s1, s2, s3 are finite positive or negative values (not NaN or inf) and have plausible magnitude (typically 0–100 %B/min for HPLC).
- Combined feature array length equals HSM block size (92) plus length of Tanaka vector (typically 8–10 elements); concatenation is axis=0 with no shape mismatches.
- Feature array can be passed directly to Graphormer model without dtype or shape errors; comparison against known retention time test set yields expected model output format.

## Limitations

- The string replacement rule ('2.7 spp' → 2.7) is specific to this dataset (RepoRT); other sources may use different artifact strings requiring custom handling.
- Gradient slope computation assumes exactly three time points (t1, t2, t3) and corresponding %B values; datasets with non-uniform or missing gradient points require interpolation or filtering.
- No automatic validation that Tanaka parameters lie in known physicochemical ranges; out-of-range values (e.g., negative or >10) will pass through unchanged and may degrade model predictions.
- Indices 84–92 are hardcoded; if column metadata array structure changes (e.g., additional fields inserted), this skill will extract wrong indices without warning.

## Evidence

- [results] extracting Tanaka parameters from column_params[84:92] and computing gradient slopes (s1, s2, s3): "extracting Tanaka parameters from column_params[84:92] and computing gradient slopes (s1, s2, s3)"
- [results] tanaka_params = [2.7 if param == '2.7 spp' else param for param in tanaka_params]; tanaka_params = [2.7 if param == '2.6 spp' else param for param in tanaka_params]: "tanaka_params = [2.7 if param == '2.7 spp' else param for param in tanaka_params]
tanaka_params = [2.7 if param == '2.6 spp' else param for param in tanaka_params]"
- [results] s1 = (B2 - B1) / (t2 - t1); s2 = (B3 - B2) / (t3 - t2); s3 = (B3 - B1) / (t3 - t1): "s1 = (B2 - B1) / (t2 - t1)
s2 = (B3 - B2) / (t3 - t2)
s3 = (B3 - B1) / (t3 - t1)"
- [results] concatenating integer encodings (categorical + additive presence flags) with float encodings (normalized continuous features and physicochemical parameters): "concatenating integer encodings (categorical + additive presence flags) with float encodings (normalized continuous features and physicochemical parameters)"
- [readme] Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github with additional usage examples: "Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github"
