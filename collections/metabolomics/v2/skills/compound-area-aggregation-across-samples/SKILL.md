---
name: compound-area-aggregation-across-samples
description: Use when you have a GC-MS dataset with multiple sample files (e.g., Std_soln_00, Std_soln_07, Std_soln_00a) where the same chemical is detected in different runs with varying Match.Factor scores, and you need to consolidate area values by compound identity rather than by individual peak detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - R
  - spreadOut()
  - mzExacto()
  - Agilent Unknowns Analysis
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Compound Area Aggregation Across Samples

## Summary

Aggregates chromatographic peak areas for the same compound across multiple GC-MS sample files by matching on retention time, exact mass, and published chemical names. This skill normalizes and combines area measurements for a single compound detected in replicate or related samples, enabling comparative analysis of compound abundances.

## When to use

You have a GC-MS dataset with multiple sample files (e.g., Std_soln_00, Std_soln_07, Std_soln_00a) where the same chemical is detected in different runs with varying Match.Factor scores, and you need to consolidate area values by compound identity rather than by individual peak detection. This is essential before quantitative comparison or validation of compound abundances across replicates.

## When NOT to use

- Your input is already a pre-aggregated feature table or peak matrix organized by compound-sample pairs; aggregation has already been performed.
- You are working with single-sample data or do not have replicate/multi-file samples to consolidate.
- Your dataset lacks standardized chemical nomenclature or does not include retention time and m/z metadata required for compound matching across files.

## Inputs

- GC-MS output CSV file with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name
- List of query chemical names (string vector)
- Optional Match.Factor threshold (numeric, e.g., >80 or >89) for pre-filtering compounds

## Outputs

- Aggregated dataframe with columns: Compound name, exact Mass, RT, Best Match factor, area values per sample file
- Structured list (spreadOut object) with sorted and aggregated sample portions by compound identity

## How to apply

Load your GC-MS .CSV file (with required columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) into R using read.csv(). Apply spreadOut() to convert raw input into a structured list that sorts by retention times and published masses, then aggregates sample portions using all published names and top m/z peaks as matching criteria. This groups multiple detections of the same chemical across files. Query your compounds of interest using mzExacto() on the spreadOut output, which searches the advanced dictionary and returns a dataframe containing compound name, exact mass, RT, best-match factor, and area values organized by sample file. Validate that area values are correctly consolidated for each compound-sample pair and that Match.Factor thresholds (if applied beforehand) are preserved.

## Related tools

- **spreadOut()** (Converts raw GC-MS CSV input into sorted and aggregated list structure using retention times, published masses, and all chemical names for intelligent grouping of sample portions by compound identity) — https://github.com/castratton/uafR
- **mzExacto()** (Searches the aggregated dictionary (spreadOut output) for query chemicals and extracts consolidated area values and match factors per compound-sample pair) — https://github.com/castratton/uafR
- **R** (Programming environment for automating the aggregation workflow and data manipulation)
- **Agilent Unknowns Analysis** (Recommended software for generating GC-MS output in the default CSV format with correct column names required for aggregation) — https://www.agilent.com/cs/library/usermanuals/public/G3335-901

## Examples

```
input_spread = spreadOut(input_dat); input_exacto = mzExacto(input_spread, c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'))
```

## Evaluation signals

- Verify that all detections of the same compound (e.g., Methyl salicylate) across different sample files (Std_soln_00, Std_soln_07, Std_soln_00a) are grouped into a single row per sample with distinct area values.
- Confirm that reported best-match factors match expected values (e.g., Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68) and are preserved in the output.
- Check that retention times and exact masses for aggregated compound entries remain consistent and match published chemical metadata.
- Validate that the output dataframe has one row per compound-sample combination with no duplicate entries for the same compound in the same file.
- Ensure that area values are correctly matched to their source sample files (File.Name column) and are not conflated across different samples.

## Limitations

- Aggregation accuracy depends on the quality and consistency of chemical nomenclature in the Compound.Name column; variations in spelling or naming conventions may prevent correct matching.
- Retention time and exact mass matching may fail if GC-MS instruments have not been properly calibrated or if published reference m/z values differ significantly from observed values.
- Match.Factor scores below threshold (if pre-filtering is applied) will be excluded, potentially discarding weak but valid detections; threshold selection requires domain knowledge.
- The approach assumes that a single chemical produces a single dominant peak per sample; isomers or co-eluting compounds with identical or near-identical m/z and RT may be incorrectly aggregated.

## Evidence

- [readme] The first step in the process is to convert the raw input to a format that downstream functions can work with. `spreadOut()` prepares the read in .CSV for intelligent ***sorting*** (using retention times and published masses) then ***aggregation***: "The first step in the process is to convert the raw input to a format that downstream functions can work with. `spreadOut()` prepares the read in .CSV for intelligent ***sorting*** (using retention"
- [methods] ***aggregation*** (using all published names and top m/z peaks) of sample portions that describe a chemical: "***aggregation*** (using all published names and top m/z peaks) of sample portions that describe a chemical"
- [methods] `mzExacto()` collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals.: "`mzExacto()` collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals."
- [other] Extract the resulting dataframe containing Compound name, exact Mass, RT, Best Match factor, and area values per sample (Std_soln_00, Std_soln_07, Std_soln_00a).: "Extract the resulting dataframe containing Compound name, exact Mass, RT, Best Match factor, and area values per sample (Std_soln_00, Std_soln_07, Std_soln_00a)."
- [other] Validate that reported best-match factors (Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68) and area values match the computed output.: "Validate that reported best-match factors (Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68) and area values match the computed output."
