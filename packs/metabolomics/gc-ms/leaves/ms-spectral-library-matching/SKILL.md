---
name: ms-spectral-library-matching
description: 'Use when when you have a GC-MS dataset (CSV with columns: Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor) and a known set of target chemicals you wish to locate and extract with their spectral match quality and quantitation.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - spreadOut()
  - mzExacto()
  - spreadOut
  - mzExacto
  - Agilent Unknowns Analysis
  techniques:
  - GC-MS
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- Modern programming languages allow even complex workflows to be automated
- Modern programming languages allow even complex workflows to be automated.
- The first step in the process is to convert the raw input to a format that downstream functions can work with. `spreadOut()` prepares the read in .CSV for intelligent ***sorting*** (using retention
- '`mzExacto()` collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals.'
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

# ms-spectral-library-matching

## Summary

Match query chemicals against GC-MS sample data by comparing retention times, exact masses, and compound names to identify and extract best-match factors and quantified area values. This skill automates the lookup and validation of reference compounds in mass spectrometry datasets.

## When to use

When you have a GC-MS dataset (CSV with columns: Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor) and a known set of target chemicals you wish to locate and extract with their spectral match quality and quantitation. Use this when you need to reproduce reported match factors and area values for reference compounds across multiple sample solutions.

## When NOT to use

- Input CSV lacks required column names (Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor) — use data reformatting or validation skill first.
- Query chemicals are not known a priori and you only want to extract all peaks above a certain match factor threshold — use alternative filtering or discovery workflows instead.
- GC-MS data is in a non-standard format (e.g., raw binary, mzML, NetCDF) — convert to CSV with required columns first.

## Inputs

- GC-MS dataset CSV file (with required columns: Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor)
- Character vector of query chemical names (e.g., c('Ethyl hexanoate', 'Methyl salicylate'))

## Outputs

- Dataframe with columns: Compound name, exact Mass, RT, Best Match factor, area values per sample file
- Numeric match factor values and corresponding quantitative area measurements for each matched compound and sample

## How to apply

First, load the raw GC-MS CSV and apply spreadOut() to convert it into a structured list indexed by retention time and mass, with aggregation across all published chemical names and top m/z peaks. Create a query chemical list as a character vector (e.g., c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane')). Apply mzExacto() to the spreadOut output and query list; it searches the aggregated dictionary by comparing retention times, exact masses, and all published names against sample data. Extract the resulting dataframe containing Compound name, exact Mass, RT, Best Match factor (numeric; typically >89 for high-confidence matches), and area values per sample file. Validate that the returned match factors and areas correspond to expected published reference values within acceptable analytical variance.

## Related tools

- **spreadOut** (Converts raw GC-MS CSV input into a structured list indexed by retention time and mass, with aggregation by published chemical names and top m/z peaks) — https://github.com/castratton/uafR
- **mzExacto** (Searches the spreadOut-aggregated dictionary against query chemicals by comparing retention times, exact masses, and all published names to extract best-match factors and area values) — https://github.com/castratton/uafR
- **Agilent Unknowns Analysis** (Recommended software for generating input data in the default CSV format with required column names) — https://www.agilent.com/cs/library/usermanuals/public/G3335-901
- **R** (Programming environment for executing spreadOut(), mzExacto(), and validation workflows)

## Examples

```
input_spread = spreadOut(input_dat); query_chemicals = c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'); input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- Returned match factor values for reference compounds match published expected values (e.g., Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68) within analytical precision
- Area values returned for each compound and sample file are numerically consistent with input CSV and do not contain NaN or missing values for matched compounds
- All queried chemicals that exist in the input dataset are returned; no expected matches are missing or dropped
- Match factor values are numeric, typically >89 for high-confidence library matches, and fall within the expected range 0–100
- Output dataframe contains exactly the required columns (Compound name, exact Mass, RT, Best Match factor, area per sample) with no structural errors

## Limitations

- Query chemicals must be spelled and formatted to match published chemical names in the input dataset; name normalization is not automatic.
- Input CSV must have exact column names in no particular order; even minor variations will cause parsing failure.
- Match factor threshold (e.g., >89) and retention time tolerance are not user-configurable in the documented workflow; threshold is applied post-hoc via subsetting.
- Performance and accuracy depend on quality of underlying Agilent Unknowns Analysis output and correctness of the spectral library used by that software.
- Does not handle isomeric or isobaric compounds that may have identical retention times and masses; returns best single match.

## Evidence

- [readme] The first step in the process is to convert the raw input to a format that downstream functions can work with. `spreadOut()` prepares the read in .CSV for intelligent ***sorting*** (using retention times and published masses) then ***aggregation***: "The first step in the process is to convert the raw input to a format that downstream functions can work with. `spreadOut()` prepares the read in .CSV for intelligent ***sorting*** (using retention"
- [readme] `mzExacto()` collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals.: "`mzExacto()` collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals."
- [readme] ***aggregation*** (using all published names and top m/z peaks) of sample portions that describe a chemical: "***aggregation*** (using all published names and top m/z peaks) of sample portions that describe a chemical"
- [readme] The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order."
- [other] Validate that reported best-match factors (Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68) and area values match the computed output.: "Validate that reported best-match factors (Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68) and area values match the computed output."
