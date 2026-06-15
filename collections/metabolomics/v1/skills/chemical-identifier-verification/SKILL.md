---
name: chemical-identifier-verification
description: Use when when you have a list of chemically known compounds and need to validate that an MS processing pipeline (e.g., mzExacto) correctly retrieves their characteristic m/z, retention time, match factor, and area values from GC-MS data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - R
  - mzExacto
  - spreadOut
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with simple modifications
- any software or utility that generates the necessary information can be used with simple modifications (e.g. changing the column names)
- mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_uafr
    doi: 10.1371/journal.pone.0306202
    title: uafr
  dedup_kept_from: coll_uafr
schema_version: 0.2.0
---

# chemical-identifier-verification

## Summary

Verify that a set of query chemicals can be correctly retrieved and identified from GC-MS data using retention time, m/z peaks, and match factor thresholds. This skill validates whether mass spectrometry search algorithms accurately extract compound-specific metadata (exact mass, retention time, match factor, area) from preprocessed spectral dictionaries.

## When to use

When you have a list of chemically known compounds and need to validate that an MS processing pipeline (e.g., mzExacto) correctly retrieves their characteristic m/z, retention time, match factor, and area values from GC-MS data. Typical scenario: you have 4 standard solutions with known compound identities (e.g., Ethyl hexanoate, Methyl salicylate, Octanal, Undecane) and want to confirm the pipeline extracts matching rows across all samples with consistent match factors ≥65 and correct retention time ordering.

## When NOT to use

- Input data is raw, unprocessed GC-MS CSV without retention time sorting or aggregation by published names and m/z peaks—apply spreadOut() first.
- Query chemicals are unknown or semi-targeted; use Match.Factor filtering (≥65) to generate the chemical list before calling mzExacto().
- Input column names do not match the required schema (Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor)—data preprocessing is required.

## Inputs

- Preprocessed standard_spread object (output from spreadOut()) containing matrices of compound names, retention times, match factors, m/z values, exact masses, areas, and nested webInfo
- Character vector of query chemical names (e.g., c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'))

## Outputs

- Dataframe with rows corresponding to query chemicals and columns: Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each sample

## How to apply

Load preprocessed GC-MS data (output from spreadOut(), which aggregates retention times and published m/z peaks) and define a character vector of known compound names. Execute mzExacto() to search the advanced dictionary for samples containing these chemicals, using retention time and published m/z peaks for precise matching. The function returns a single dataframe where each row corresponds to a query chemical and columns include Compound, exact Mass, RT, Best Match (match factor), and area values for each sample file. Verify correctness by confirming that all query chemicals appear in the output, match factors are consistent with known standards (typically ≥65 for high-confidence matches), retention times are ordered logically, and area values are non-zero and sample-specific.

## Related tools

- **spreadOut** (Preprocesses raw GC-MS CSV into an advanced dictionary structure suitable for chemical searching; aggregates samples by retention time and published m/z peaks) — https://github.com/castratton/uafR
- **mzExacto** (Core function that executes the chemical-identifier-verification workflow; searches the preprocessed dictionary for query chemicals and extracts m/z, retention time, match factor, and area values) — https://github.com/castratton/uafR
- **R** (Statistical and data processing environment in which the uafR package functions are executed)

## Examples

```
input_spread = spreadOut(input_dat)
query_chemicals = c("Ethyl hexanoate", "Methyl salicylate", "Octanal", "Undecane")
input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- All query chemicals appear as rows in the output dataframe; no missing compounds.
- Match factor values are consistent across replicates of the same chemical and meet or exceed the confidence threshold (≥65).
- Retention time values are logically ordered and stable across samples (same compound shows similar RT in different standard solutions).
- Area values are present, non-zero, and sample-specific—different Std_soln files show different area magnitudes for the same compound.
- Exact mass values match published chemical standards for each compound name.

## Limitations

- Requires strict input CSV column naming (Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor); generated or reformatted data may have column name mismatches.
- Performance depends on the quality and completeness of the upstream spreadOut() preprocessing; garbage input produces garbage output.
- Match factors and retention times must be present in the input data; if a query chemical has no matching peaks in the dictionary, it will not appear in the output.
- No changelog documented in the uafR repository, limiting visibility into bug fixes and algorithm changes between versions.

## Evidence

- [other] Load the pre-processed standard_spread list object (output from spreadOut()) containing matrices of compound names, retention times, match factors, m/z values, exact masses, areas, and nested webInfo for published chemical identifiers.: "Load the pre-processed standard_spread list object (output from spreadOut()) containing matrices of compound names, retention times, match factors, m/z values, exact masses, areas, and nested webInfo"
- [other] Execute mzExacto(standard_spread, query_chemicals) to search the spread dictionary and extract matching samples that contain these chemicals, using retention time and published m/z peaks for precise identification.: "Execute mzExacto(standard_spread, query_chemicals) to search the spread dictionary and extract matching samples that contain these chemicals, using retention time and published m/z peaks for precise"
- [other] Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each sample: "Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each"
- [readme] The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order."
- [methods] mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals: "mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals"
