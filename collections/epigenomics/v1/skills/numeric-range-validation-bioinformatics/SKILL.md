---
name: numeric-range-validation-bioinformatics
description: Use when after applying a quantitative analysis function (e.g., cooltools.insulation, contact frequency calculations) to Hi-C cooler files or other genomic datasets, validate that the output numeric columns contain values within plausible ranges (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3169
  tools:
  - cooltools
  - cooler
  - pandas
  - pytest
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cooltools
    doi: 10.1371/journal.pcbi.1012067
    title: cooltools
  dedup_kept_from: coll_cooltools
schema_version: 0.2.0
---

# numeric-range-validation-bioinformatics

## Summary

Validate that computed quantitative genomic features (e.g., insulation scores, contact frequencies) fall within mathematically and biologically expected numeric ranges and that derived boolean annotations (e.g., TAD boundary flags) are correctly typed. This skill ensures data integrity and identifies computational or thresholding errors before downstream analysis.

## When to use

After applying a quantitative analysis function (e.g., cooltools.insulation, contact frequency calculations) to Hi-C cooler files or other genomic datasets, validate that the output numeric columns contain values within plausible ranges (e.g., insulation scores as floats, not NaN unless expected; boundary calls as strict boolean 0/1 or True/False) and that no unexpected outliers or type mismatches have been introduced.

## When NOT to use

- Input data are already a quality-controlled, published feature table from a trusted source (e.g., GEO deposit with peer-reviewed validation).
- Analysis goal is exploratory or hypothesis-generating and does not require strict quality gates.
- Numeric values are intentionally sparse or contain expected NaN by design (e.g., regions filtered for low coverage); in such cases, validate sparsity pattern separately rather than enforcing full range.

## Inputs

- pandas DataFrame with computed Hi-C features (insulation scores, contact frequencies, or similar)
- cooler file (HDF5 contact matrix) with bin metadata
- window size parameter (integer, in base pairs) used in feature computation

## Outputs

- validated pandas DataFrame with confirmed dtype and value range integrity
- BED format file with validated boundary annotations (optional)
- validation report or assertion log confirming range and type checks passed

## How to apply

Load the output table (typically as a pandas DataFrame) and inspect the dtype and value ranges of numeric columns. For insulation scores, verify that values are floating-point numbers without unexpected NaN clusters unrelated to low-coverage regions, and that the range is bounded by the definition of the metric (e.g., normalized ratios should not exceed physically plausible limits). For boundary annotations, confirm that is_boundary_* columns are strictly boolean (dtype: bool or int 0/1). Check that row counts match expected bin coordinates and that required columns (e.g., region1, region2, insulation_score, is_boundary_{window}) are all present. Use pandas describe(), dtypes inspection, and assertions on min/max values to programmatically enforce these invariants before exporting to BED or other downstream formats.

## Related tools

- **cooltools** (Computes insulation scores and TAD boundary annotations on Hi-C cooler files; outputs require validation) — https://github.com/open2c/cooltools
- **cooler** (Stores and provides programmatic access to high-resolution Hi-C contact matrices and bin-level metadata) — https://github.com/open2c/cooler
- **pandas** (Provides DataFrame inspection, dtype checking, and range validation via describe(), dtypes, and boolean indexing)
- **pytest** (Framework for writing and running automated unit tests that encode range and type invariants) — https://docs.pytest.org/en/latest

## Examples

```
import pandas as pd; import cooler; c = cooler.Cooler('path/to/file.cool'); insulation = c.attrs.get('insulation'); df = pd.read_csv('insulation_scores.tsv', sep='\t'); assert (df['insulation_score'].dtype == 'float64'), 'dtype mismatch'; assert (df['is_boundary_10000'].isin([0, 1])).all(), 'non-boolean boundary'; assert (df['insulation_score'].min() >= 0), 'negative insulation score'; print('Validation passed')
```

## Evaluation signals

- All numeric columns have correct dtype (e.g., float64 for insulation scores, not object or string).
- Insulation score values fall within expected numeric range (no unexplained infinities, no negative values if metric is normalized positive-definite).
- Boolean boundary annotation columns (is_boundary_*) contain only 0/1 or True/False with no null values unless explicitly masked.
- Row count and bin coordinate ranges match input cooler file dimensions and specified window size.
- Required columns (region1, region2, insulation_score, is_boundary_{window}) are present and non-null.
- No unexpected NaN clusters except in pre-defined low-coverage or edge-bin regions; NaN prevalence is documented.

## Limitations

- Expected range and dtype depend on the specific metric (insulation vs. contact frequency vs. saddle P(s)); validation logic must be customized per metric, not generic.
- Smoothing and derivative functionality in cooltools has an API that is not yet stable, which may affect the numeric output format in future versions.
- Validation cannot distinguish between correct sparse data (expected NaN) and computational errors (unexpected NaN) without domain knowledge of the input cooler and filtering parameters.
- Type checking and range validation are necessary but not sufficient for biological correctness; a value within the numeric range may still be spurious if the underlying Hi-C data are noisy or poorly normalized.

## Evidence

- [other] insulation_score_format_and_range: "Export the insulation score table as a pandas DataFrame containing bin coordinates, insulation score values, and is_boundary_{window} boolean columns."
- [other] validation_checks_on_output: "Verify output file existence, row count, numeric value ranges, and presence of required columns (region1, region2, insulation_score, is_boundary_*)."
- [other] dtype_and_range_assertions: "Validate that insulation scores fall within expected numeric ranges and boundary annotations are boolean."
- [readme] cooltools_computes_quantitative_features: "Cooltools provides computational tools for analyzing high-resolution Hi-C datasets stored in the cooler format, enabling extraction of quantitative genomic features."
