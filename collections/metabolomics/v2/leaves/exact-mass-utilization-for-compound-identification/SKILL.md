---
name: exact-mass-utilization-for-compound-identification
description: Use when you have a GC-MS dataset in CSV format with retention times,
  base peak m/z values, component areas, and compound names, and you need to identify
  whether specific query chemicals are present in your samples and retrieve their
  -match factors (scoring the confidence of the spectral match) and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - spreadOut()
  - mzExacto()
  - Agilent Unknowns Analysis
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- Modern programming languages allow even complex workflows to be automated
- Modern programming languages allow even complex workflows to be automated.
- The first step in the process is to convert the raw input to a format that downstream
  functions can work with. `spreadOut()` prepares the read in .CSV for intelligent
  ***sorting*** (using retention
- '`mzExacto()` collects the same information for a set of query chemicals and uses
  it to precisely search the advanced dictionary for samples that have those chemicals.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_uafr_cq
    doi: 10.1371/journal.pone.0306202
    title: uafr
  dedup_kept_from: coll_uafr_cq
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

# exact-mass-utilization-for-compound-identification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill applies exact mass matching and retention time correlation to identify compounds in GC-MS datasets by comparing measured m/z values and retention times against reference chemical metadata. It is used to validate analytical results and retrieve match factors and area quantifications for target compounds from mass spectrometry samples.

## When to use

You have a GC-MS dataset in CSV format with retention times, base peak m/z values, component areas, and compound names, and you need to identify whether specific query chemicals are present in your samples and retrieve their best-match factors (scoring the confidence of the spectral match) and quantitative area values. This is particularly valuable when you want to reproduce published analytical results or verify the presence of known reference compounds with high confidence (e.g., Match.Factor > 89).

## When NOT to use

- Your CSV input is missing any of the required column names (Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor) — the function will fail or produce incorrect results.
- Your query chemicals are not properly spelled or do not exist in the reference metadata that spreadOut() aggregates — mzExacto() will not find matches.
- You are attempting to identify unknown compounds without a curated list of expected chemical names — use categorate() and exactoThese() instead to discover and filter candidate chemicals by database membership or structural properties.

## Inputs

- CSV file with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name
- spreadOut() output (structured list of aggregated sample portions organized by retention time and chemical metadata)
- query_chemicals vector (character vector of compound names to search for)

## Outputs

- mzExacto() dataframe with columns: Compound name, exact Mass, RT, Best Match factor, area values per sample
- Match factor values (0–100 scale, where >89 indicates high-confidence spectral match)
- Component.Area quantifications per sample for matched compounds

## How to apply

First, load your GC-MS CSV file into R and apply spreadOut() to convert the raw input into a structured list that sorts by retention times and published m/z values, then aggregates sample portions that describe each chemical using all published chemical names and top m/z peaks. Next, define your query_chemicals as a vector of compound names (e.g., c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane')). Apply mzExacto() to the spreadOut output and query list; this function searches the aggregated dictionary by comparing retention times, exact masses, and all published chemical names against your sample data. Extract the resulting dataframe containing Compound name, exact Mass, RT, Best Match factor, and area values per sample. Finally, validate your results by comparing the computed best-match factors and area values against published or expected reference values.

## Related tools

- **spreadOut()** (Prepares raw GC-MS CSV data by sorting by retention times and published masses, then aggregates sample portions using all published chemical names and top m/z peaks to create the structured input for mzExacto()) — https://github.com/castratton/uafR
- **mzExacto()** (Core matching function that collects chemical metadata for query compounds and precisely searches the aggregated dictionary by comparing retention times, exact masses, and published chemical names against sample data to return best-match factors and area values) — https://github.com/castratton/uafR
- **R** (Programming environment for implementing the workflow and accessing the uafR package functions)
- **Agilent Unknowns Analysis** (Recommended software for generating GC-MS data in the required CSV format with correct column names) — https://www.agilent.com/cs/library/usermanuals/public/G3335-901

## Examples

```
input_spread = spreadOut(input_dat); query_chemicals = c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'); input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- Best-match factors for reference compounds fall within expected ranges (e.g., Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68) when compared against published values.
- Area values returned for each compound and sample match or closely approximate expected quantifications from the original analytical report.
- All query chemicals are present in the output dataframe with Match.Factor values; absence indicates unsuccessful matching.
- Retention times in the output dataframe align with known retention times for the reference compounds (confirming correct compound identification, not just m/z match).
- No missing or NULL values in the Best Match factor or area value columns for successfully matched compounds.

## Limitations

- Match success depends critically on the quality and completeness of chemical name metadata in the reference data; misspelled or missing synonyms will prevent identification.
- The function is designed for GC-MS data; applicability to other mass spectrometry methods (LC-MS, MALDI, etc.) or retention-time-independent workflows is unknown.
- Match factors are derived from spectral library comparisons and do not provide structural confirmation; a high match factor indicates good agreement with a library spectrum but does not guarantee chemical identity in the absence of orthogonal validation (e.g., standards, alternative ionization methods).
- The CSV input must strictly conform to column name and data format requirements; missing or misnamed columns will cause function failure.

## Evidence

- [methods] mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals.: "`mzExacto()` collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals."
- [methods] The first step in the process is to convert the raw input to a format that downstream functions can work with. `spreadOut()` prepares the read in .CSV for intelligent sorting (using retention times and published masses) then aggregation (using all published names and top m/z peaks) of sample portions that describe a chemical.: "prepares the read in .CSV for intelligent ***sorting*** (using retention times and published masses) then ***aggregation*** (using all published names and top m/z peaks) of sample portions that"
- [other] The research question validates four reference compounds (Ethyl hexanoate, Methyl salicylate, Octanal, Undecane) with best-match factors (Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68).: "reported best-match factors (Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68) and area values match the computed output"
- [readme] The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'.: "The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"
- [readme] In the README example, the user applies mzExacto() directly to spreadOut() output with a query_chemicals vector to extract specific compounds.: "input_spread = spreadOut(input_dat); query_chemicals = c("Linalool", "Methyl Salicylate", "Limonene", "alpha-Thujene"); input_exacto = mzExacto(input_spread, query_chemicals)"
