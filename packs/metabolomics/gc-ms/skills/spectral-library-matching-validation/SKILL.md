---
name: spectral-library-matching-validation
description: Use when you have GC-MS data preprocessed into a structured spread format and need to confirm that a set of known or suspected compounds are correctly identified in your samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzExacto
  - spreadOut
  - exactoThese
  - categorate
  - ChemmineR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-matching-validation

## Summary

Validate and extract mass spectrometry compound identifications by searching preprocessed spectral libraries for known query chemicals using retention time, m/z values, and match factor thresholds. This skill ensures that retrieved compound metadata (m/z, RT, match factor, area) meets quality standards before downstream analysis.

## When to use

Apply this skill when you have GC-MS data preprocessed into a structured spread format and need to confirm that a set of known or suspected compounds are correctly identified in your samples. Use it after initial peak detection and compound assignment, particularly when match factors vary across replicates or when you need to aggregate fragmented peak calls for the same chemical across multiple sample files.

## When NOT to use

- Input data lacks strict column names (Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor) — preprocessing will fail.
- Query chemical names do not match published compound names in the spectral library — no matches will be returned.
- Match factors are consistently below 60–65 across all samples — suggests poor quality peak detection and identifications should not be trusted for downstream analysis.

## Inputs

- GC-MS data .CSV file with required columns: Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor
- preprocessed spread object (output from spreadOut())
- query_chemicals: character vector of known compound names

## Outputs

- validated dataframe with rows corresponding to query chemicals and columns: Compound, Mass (exact mass), RT (retention time), Best Match (match factor), area values per sample

## How to apply

First, prepare your raw GC-MS .CSV file using spreadOut(), which organizes retention times, m/z values, match factors, and areas into an indexed dictionary structure. Then define your query_chemicals as a character vector of compound names you wish to validate (e.g., c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane')). Execute mzExacto(spread_object, query_chemicals) to search the spread dictionary and extract all matching instances, which uses published m/z peaks and retention times for precise identification. The function returns a consolidated dataframe where rows are compounds and columns are Compound name, exact Mass, RT, Best Match (match factor value), and area for each sample. Evaluate match factor values—typically requiring Match.Factor ≥ 65–80 as a quality cutoff—to decide which identifications are reliable. If a compound appears in multiple samples or with multiple peaks, mzExacto aggregates them using all published names and top m/z peaks to yield a single consensus row per chemical.

## Related tools

- **spreadOut** (prepares raw GC-MS .CSV data into indexed dictionary structure with retention times, m/z, match factors, and area matrices for downstream spectral library searching) — https://github.com/castratton/uafR
- **mzExacto** (searches preprocessed spread dictionary to extract and consolidate m/z, retention time, match factor, and area data for query chemicals across multiple samples) — https://github.com/castratton/uafR
- **exactoThese** (subsets validated compound lists by chemical properties (molecular weight, functional groups, ring count) or database membership (LOTUS, FEMA, KEGG, FDA/SPL) after mzExacto returns results) — https://github.com/castratton/uafR
- **categorate** (enriches validated compounds with cheminformatics metadata (reactive groups, SMILES, molecular properties) and database cross-references for post-validation filtering) — https://github.com/castratton/uafR
- **R** (primary execution environment for all uafR functions)
- **ChemmineR** (underlying cheminformatics package for compound structure and property queries in enrichment workflows)

## Examples

```
input_spread = spreadOut(input_dat); query_chemicals = c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'); input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- Output dataframe has exactly one row per query chemical and one column per sample, with no missing compounds unless they truly absent from input spread.
- All Match.Factor values in output are ≥ 65 (or your chosen threshold), and Match.Factor ≥ 80 for high-confidence identifications.
- Retention time values are consistent across replicates of the same chemical (within ~0.1 min), indicating stable chromatography and correct peak aggregation.
- Base.Peak.MZ values match published exact masses within 5 ppm tolerance (or instrument-specific mass accuracy spec) for each compound.
- Area values are positive and non-zero for all sample columns; if a compound is absent from a sample, area should be NA or 0 (not negative or corrupted).

## Limitations

- Requires exact chemical name matches between query vector and compound names in spectral library—synonyms or spelling variants will not be retrieved.
- Match factor threshold is user-specified; no automated decision rule is provided for which cutoff is appropriate, and threshold choice may be instrument- or method-dependent.
- If the same compound elutes at multiple retention times (e.g., geometric isomers or co-elution with contaminants), mzExacto may aggregate them into a single row, losing information about structural or chemical distinctions.
- Performance depends on quality of initial peak detection and compound assignment in the input .CSV file; garbage input yields garbage output even if mzExacto executes without error.
- No changelog documented in repository, limiting ability to track function behavior changes or bug fixes across versions.

## Evidence

- [methods] mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals: "mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals"
- [other] Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each sample: "Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each"
- [methods] spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses): "spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses)"
- [readme] The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order."
- [methods] aggregation (using all published names and top m/z peaks) of sample portions that describe a chemical: "aggregation (using all published names and top m/z peaks) of sample portions that describe a chemical"
- [methods] query_chems = standard_dat$Compound.Name[standard_dat$Match.Factor >= 65]: "query_chems = standard_dat$Compound.Name[standard_dat$Match.Factor >= 65]"
