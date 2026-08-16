---
name: chromatographic-retention-time-matching
description: Use when you have GC-MS data with multiple replicate injections or samples, need to identify a predefined set of query chemicals by name, and want to consolidate all instances of those chemicals (which may appear with varying match factors or peak areas across different samples or injection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0628
  tools:
  - R
  - mzExacto
  - spreadOut
  techniques:
  - GC-MS
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- any software or utility that generates the necessary information can be used with simple modifications
- any software or utility that generates the necessary information can be used with simple modifications (e.g. changing the column names)
- mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_claw_mrm_cq
    doi: 10.1021/acs.analchem.4c05039
    title: CLAW-MRM
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

# chromatographic-retention-time-matching

## Summary

A GC-MS data processing skill that uses retention time (RT) and published m/z peaks to precisely identify and match query chemicals within preprocessed mass spectrometry datasets. This skill enables unambiguous chemical identification by aggregating multiple detection instances across samples that share matching retention times and mass spectral signatures.

## When to use

Apply this skill when you have GC-MS data with multiple replicate injections or samples, need to identify a predefined set of query chemicals by name, and want to consolidate all instances of those chemicals (which may appear with varying match factors or peak areas across different samples or injection replicates) into a single searchable result. Use it after raw .CSV data has been loaded and preprocessed via spreadOut() to organize retention times and m/z values.

## When NOT to use

- Input data lacks the required column names (Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor); preprocess or reformat first.
- Query chemicals are unknown or you need to discover dominant peaks without a predefined list; use filter-by-match-factor instead.
- You want to subset results by molecular weight, database presence, or chemical structure; use exactoThese() for fine-grained filtering after mzExacto().

## Inputs

- preprocessed standard_spread list object (output from spreadOut())
- character vector of query chemical names

## Outputs

- dataframe with rows corresponding to query chemicals and columns: Compound, Mass, RT, Best Match (match factor), and area values per sample

## How to apply

First, prepare your input by loading a .CSV file with mandatory columns: Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, and Match.Factor, then call spreadOut() to create a structured list object containing matrices of compound names, retention times, match factors, m/z values, exact masses, areas, and nested metadata. Define your query_chemicals as a character vector of compound names (e.g., c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane')). Call mzExacto(spread_object, query_chemicals) to search the preprocessed dictionary and extract all matching samples. The function aggregates results using all published names and top m/z peaks, returning a single dataframe where rows are the query chemicals and columns include Compound, Mass (exact mass), RT, Best Match (match factor), and area values for each sample. The retention time matching ensures that different detections of the same chemical across samples are correctly consolidated rather than treated as separate entities.

## Related tools

- **spreadOut** (Converts raw .CSV input into structured spread dictionary format with organized retention times and published masses for downstream matching) — https://github.com/castratton/uafR
- **mzExacto** (Core function that searches the spread dictionary using retention time and m/z peak matching to extract and aggregate all instances of query chemicals across samples) — https://github.com/castratton/uafR
- **R** (Execution environment for spreadOut(), mzExacto(), and downstream analysis)

## Examples

```
input_spread = spreadOut(input_dat); query_chemicals = c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'); input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- Output dataframe has exactly as many rows as query chemicals supplied; missing or extra rows indicate incomplete matching.
- All retained rows have non-NA values for RT, Best Match (match factor), and Mass columns; NAs suggest failed lookups.
- Retention times within a row are consistent across samples (allow ±0.1–0.3 min tolerance per instrument calibration); large discrepancies suggest incorrect consolidation.
- Best Match (match factor) values are ≥65 if filtering was applied upstream, or reflect the highest match factor among replicates of the same chemical.
- Area values scale reasonably with known sample concentrations or injection volumes; anomalously large/small values may indicate data entry or matching errors.

## Limitations

- Matching depends entirely on retention time and published m/z peak accuracy; incorrect or missing RT values in the input will cause failed matches.
- Chemical name spelling and formatting must match the dictionary exactly; typos or alternative nomenclature will not be found.
- The function assumes retention times are sufficiently distinct across query chemicals; co-eluting compounds may be incorrectly aggregated if their m/z peaks overlap significantly.
- Match factor filtering (e.g., ≥65) may be too permissive or strict depending on instrument tuning and library quality; manual review of lower-confidence hits is recommended.
- No changelog available in the repository; behavior changes across versions are not documented.

## Evidence

- [methods] spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses): "spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses)"
- [methods] mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals: "mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals"
- [other] Load the pre-processed standard_spread list object (output from spreadOut()) containing matrices of compound names, retention times, match factors, m/z values, exact masses, areas, and nested webInfo: "Load the pre-processed standard_spread list object (output from spreadOut()) containing matrices of compound names, retention times, match factors, m/z values, exact masses, areas, and nested webInfo"
- [other] Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each sample: "Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each"
- [methods] aggregation (using all published names and top m/z peaks) of sample portions that describe a chemical: "aggregation (using all published names and top m/z peaks) of sample portions that describe a chemical"
- [readme] The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor': "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"
