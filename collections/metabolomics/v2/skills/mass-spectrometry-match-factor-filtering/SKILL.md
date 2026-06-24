---
name: mass-spectrometry-match-factor-filtering
description: Use when you have a GC-MS dataset with a Match.Factor column (output
  from Agilent Unknowns Analysis or equivalent) and need to retain only high-confidence
  compound identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3370
  tools:
  - R
  - Agilent Unknowns Analysis
  - uafR
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with
  simple modifications
- any software or utility that generates the necessary information can be used with
  simple modifications (e.g. changing the column names)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_uafr
    doi: 10.1371/journal.pone.0306202
    title: uafr
  dedup_kept_from: coll_uafr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pone.0306202
  all_source_dois:
  - 10.1371/journal.pone.0306202
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-match-factor-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply quality-based thresholds to GC-MS compound identifications by filtering on Match.Factor scores, a library-matching metric that ranges from 0–100. This skill enables reproducible subsetting of compound lists at standardized quality cutoffs (e.g., ≥65, ≥80, ≥90) to balance detection sensitivity against false-positive risk.

## When to use

Use this skill when you have a GC-MS dataset with a Match.Factor column (output from Agilent Unknowns Analysis or equivalent) and need to retain only high-confidence compound identifications. Apply it when you want to compare how compound counts and identity certainty vary across multiple quality thresholds, or when downstream analysis (e.g., cheminformatics lookups, chemical categorization) requires pre-filtering to high-confidence hits.

## When NOT to use

- Input data lacks a Match.Factor column or equivalent library-match quality metric.
- You have already manually curated or pre-filtered the compound list and need only to extract a subset by name, not by quality score.
- Match.Factor values are not on a 0–100 scale or have not been validated as comparable across your sample set.

## Inputs

- CSV file with columns: Compound.Name, Match.Factor, Component.RT, Base.Peak.MZ, Component.Area, File.Name
- One or more numeric threshold values (e.g., 65, 80, 90)

## Outputs

- Filtered list of unique Compound.Name values per threshold condition
- Summary CSV table: threshold value (column 1) vs. count of unique compounds retained (column 2)

## How to apply

Load the GC-MS data (CSV format with required columns: Compound.Name, Match.Factor, and others such as Component.RT, Base.Peak.MZ, Component.Area, File.Name) into R. Define multiple Match.Factor threshold values (e.g., ≥65, ≥80, ≥90) based on your confidence requirements and the expected false-positive rate at each level. For each threshold, apply a logical filter to the Match.Factor column and retain the unique Compound.Name values that meet or exceed that threshold. Count the number of unique compounds passing each threshold condition. Construct a summary table with one row per threshold showing the threshold value and corresponding compound count, then save to CSV. The rationale: Match.Factor is a normalized library-match score where higher values indicate better spectral correspondence; thresholds are typically selected to balance sensitivity (retaining true positives) against specificity (excluding ambiguous or low-confidence identifications).

## Related tools

- **R** (Environment for loading CSV, applying logical filters to Match.Factor column, aggregating unique compounds, and writing summary tables.)
- **Agilent Unknowns Analysis** (Recommended software for generating GC-MS output in the standard format with correct Match.Factor column naming and values.)
- **uafR** (R package that wraps Match.Factor filtering and downstream cheminformatics workflows (spreadOut, mzExacto, categorate, exactoThese functions).) — https://github.com/castratton/uafR

## Examples

```
query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor >= 80]; summary_table = data.frame(Threshold = c(65, 80, 90), Count = c(length(unique(input_dat$Compound.Name[input_dat$Match.Factor >= 65])), length(unique(input_dat$Compound.Name[input_dat$Match.Factor >= 80])), length(unique(input_dat$Compound.Name[input_dat$Match.Factor >= 90])))); write.csv(summary_table, 'match_factor_summary.csv', row.names = FALSE)
```

## Evaluation signals

- Verify that the number of retained compounds decreases monotonically as the Match.Factor threshold increases (e.g., count at ≥90 ≤ count at ≥80 ≤ count at ≥65).
- Check that all Compound.Name values in the filtered output have Match.Factor values ≥ the stated threshold (no false negatives in the filter logic).
- Confirm the summary table has exactly three rows (or one per threshold tested) with no missing or null entries.
- Validate that unique compound counts match manual spot-checks on the input data for at least one threshold.
- Ensure CSV output is properly formatted with consistent column names and no trailing whitespace or encoding artifacts.

## Limitations

- Match.Factor is specific to library-based GC-MS identification; unknown or novel compounds without library matches cannot be filtered by this metric.
- Optimal threshold values are context-dependent and may vary by instrument calibration, reference library version, and analyte class; no universal cutoff is recommended.
- Filtering on Match.Factor alone does not account for retention-time matching, abundance anomalies, or co-elution artifacts that may indicate false positives.
- The skill assumes strict column naming (Compound.Name, Match.Factor) as enforced by Agilent Unknowns Analysis; datasets from other instruments or formats may require preprocessing.

## Evidence

- [other] How many query chemicals are retained in the standard_data.csv compound list when applying Match.Factor filter thresholds of ≥65, ≥80, and ≥90?: "How many query chemicals are retained in the standard_data.csv compound list when applying Match.Factor filter thresholds of ≥65, ≥80, and ≥90?"
- [other] Match.Factor filtering can be applied to standard_data.csv at multiple threshold levels (≥65, ≥80, ≥90) to subset the compound list based on matching quality criteria.: "Match.Factor filtering can be applied to standard_data.csv at multiple threshold levels (≥65, ≥80, ≥90) to subset the compound list based on matching quality criteria."
- [other] Apply three independent filters: Match.Factor >= 65, Match.Factor >= 80, and Match.Factor >= 90, retaining unique compound names for each filter.: "Apply three independent filters: Match.Factor >= 65, Match.Factor >= 80, and Match.Factor >= 90, retaining unique compound names for each filter."
- [readme] The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order."
- [methods] query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]: "query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]"
- [methods] The recommended software for generating the necessary data in the default format (i.e. with correct column names) is Unknowns Analysis: "The recommended software for generating the necessary data in the default format (i.e. with correct column names) is Unknowns Analysis"
