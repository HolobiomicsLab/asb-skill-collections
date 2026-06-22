---
name: mass-spectrometry-library-curation
description: Use when when preprocessing a public MS/MS spectral library (e.g., GNPS) for machine learning and you discover discrepancies between expected and observed compound counts after filtering by instrument type, or when a known instrument metadata issue (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - msfiddle
  - FIDDLE
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-library-curation

## Summary

Curate and filter tandem mass spectrometry (MS/MS) spectral libraries by applying instrument-specific metadata constraints (e.g., allowlist fixes) and re-splitting datasets to obtain reproducible training/test compound counts. This skill ensures that instrumental biases are corrected before model development or validation.

## When to use

When preprocessing a public MS/MS spectral library (e.g., GNPS) for machine learning and you discover discrepancies between expected and observed compound counts after filtering by instrument type, or when a known instrument metadata issue (e.g., missing instrument category codes) has been identified in the raw data.

## When NOT to use

- Input spectral library is already pre-filtered and validated by the source provider with published instrument mappings and no known metadata issues.
- The analysis goal is method development on a single instrument type where instrument-specific biases are intentional (e.g., building an Orbitrap-only predictor); in this case, skip allowlist curation and use the raw library as-is.
- Instrument metadata is absent or cannot be reliably mapped to standard categories; curation may introduce false negatives or require manual review that is not feasible at scale.

## Inputs

- Raw GNPS public spectral library (MGF format with TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY fields)
- Instrument metadata mapping or configuration file
- Instrument allowlist rules (e.g., JSON or YAML defining which instruments map to which categories)

## Outputs

- Curated spectral dataset (MGF or CSV) with corrected instrument annotations
- Training set compound list with verified count
- Test set compound list with verified count
- Audit report documenting allowlist changes and their effect on dataset composition

## How to apply

Load the raw GNPS spectral dataset and its associated instrument metadata using msfiddle or the FIDDLE preprocessing pipeline. Identify and apply the necessary instrument allowlist configuration updates—for example, adding missing instrument identifiers like 'ftms' to the gnps_orbitrap category if high-resolution Orbitrap spectra are being incorrectly filtered out. Re-run the dataset filtering and train/test splitting logic with the corrected allowlist. Extract and verify the resulting compound counts for training and test sets (e.g., comparing against reported baseline values of 28,751 training and 3,195 test compounds for the Orbitrap dataset). If counts match the expected split, the instrument metadata fix is confirmed; if not, investigate whether additional instrument codes or filtering rules are missing.

## Related tools

- **msfiddle** (CLI and Python API for loading spectral data, applying filtering rules, and splitting datasets according to instrument allowlist configuration) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Full research codebase providing dataset preprocessing, filtering, and train/test split logic with configurable instrument allowlist rules) — https://github.com/JosieHong/FIDDLE

## Examples

```
msfiddle --test_data /path/to/gnps_raw.mgf --config_path /path/to/config_orbitrap_updated.yml --result_path /path/to/curated_output.csv --device 0
```

## Evaluation signals

- Training set compound count matches expected value (e.g., 28,751 for corrected Orbitrap dataset).
- Test set compound count matches expected value (e.g., 3,195 for corrected Orbitrap dataset).
- No spectra from excluded instrument types remain in the filtered dataset; spot-check a sample of spectra to verify PRECURSOR_TYPE field matches the allowlist.
- Before/after dataset size comparison shows a measurable change when the allowlist fix is applied, confirming that the instrument metadata correction affected filtering logic.
- Train/test split ratio is consistent with documented baseline (e.g., ~90% / ~10% or similar proportions reported in the paper).

## Limitations

- The provided article and README do not explicitly document the instrument allowlist fix methodology or the full set of instrument codes and mappings; practitioners must inspect the FIDDLE source code (config files and preprocessing scripts) to identify the exact allowlist structure and which codes were added or corrected.
- Curation success depends on the reliability of instrument metadata in the source library; if instrument type annotations are missing, ambiguous, or incorrectly assigned in the raw data, filtering will fail to detect and correct them.
- The expected dataset split counts (28,751 training, 3,195 test) are specific to the Orbitrap dataset with the 'ftms' allowlist fix; other instruments or datasets will have different thresholds, and applying this skill to new datasets requires re-establishing baseline expectations.

## Evidence

- [other] Does applying the updated instrument allowlist fix (adding 'ftms' to gnps_orbitrap) to the dataset result in the reported training and test split counts of 28,751 and 3,195 compounds respectively?: "Does applying the updated instrument allowlist fix (adding 'ftms' to gnps_orbitrap) to the dataset result in the reported training and test split counts of 28,751 and 3,195 compounds respectively?"
- [other] Load the raw GNPS spectral dataset and instrument metadata used in FIDDLE preprocessing. Update the instrument allowlist configuration to include 'ftms' in the gnps_orbitrap category.: "Load the raw GNPS spectral dataset and instrument metadata used in FIDDLE preprocessing. Update the instrument allowlist configuration to include 'ftms' in the gnps_orbitrap category."
- [other] Re-run the dataset filtering and splitting logic with the updated allowlist using msfiddle.: "Re-run the dataset filtering and splitting logic with the updated allowlist using msfiddle."
- [readme] CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle): "CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)"
- [readme] The required MGF fields are `TITLE`, `PRECURSOR_MZ`, `PRECURSOR_TYPE`, and `COLLISION_ENERGY`: "The required MGF fields are `TITLE`, `PRECURSOR_MZ`, `PRECURSOR_TYPE`, and `COLLISION_ENERGY`"
