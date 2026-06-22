---
name: metabolite-quantification-accuracy-assessment
description: Use when you have executed mzExacto() on a preprocessed GC-MS dataset and need to verify that the returned dataframe correctly matches query chemicals to their m/z peaks, retention times, and quantitative measurements (area values).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - R
  - mzExacto
  - spreadOut
  - categorate
  - Agilent Unknowns Analysis
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-quantification-accuracy-assessment

## Summary

Validate that a mass spectrometry data extraction function (mzExacto) correctly retrieves m/z values, retention times, match factors, and peak areas for known query chemicals by comparing extracted dataframe outputs against expected compound identifiers and retention time/m/z reference standards. This skill ensures quantification accuracy before downstream chemical categorization or database lookups.

## When to use

Apply this skill when you have executed mzExacto() on a preprocessed GC-MS dataset and need to verify that the returned dataframe correctly matches query chemicals to their m/z peaks, retention times, and quantitative measurements (area values). Use it as a quality-control checkpoint after spreadOut() preprocessing but before categorate() or exactoThese() subsetting, especially when match factors vary widely (e.g., 62–98%) across replicates or when multiple standard solutions (Std_soln_00, Std_soln_07, Std_soln_00a) are being interrogated simultaneously.

## When NOT to use

- Input CSV has not been preprocessed by spreadOut() — this skill assumes a structured 'spread' dictionary object, not raw Unknowns Analysis output.
- Query chemicals are not known or predefined — this skill is for targeted validation, not exploratory discovery of all compounds in the dataset.
- Match.Factor filtering has already been applied upstream — if you have already subsetted to Match.Factor > 80, validation of lower-confidence hits will be incomplete.

## Inputs

- standard_spread object (output from spreadOut() function)
- query_chemicals character vector (e.g., c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'))

## Outputs

- mzExacto output dataframe with columns: Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values per sample

## How to apply

Define a set of known query chemicals (e.g., Ethyl hexanoate, Methyl salicylate, Octanal, Undecane) that are present in your preprocessed standard_spread object. Execute mzExacto(standard_spread, query_chemicals) to extract a dataframe with rows for each query chemical and columns for Compound name, exact Mass, RT (retention time), Best Match (match factor), and area values per sample. Verify correctness by checking: (1) all query chemicals appear as rows in the output; (2) retention times and m/z values match published reference values in the advanced dictionary; (3) Match.Factor values are ≥65 (typical minimum threshold for GC-MS compound identification); (4) area values are non-zero and numerically consistent across replicate standards; (5) no unexpected NAs or duplicates are introduced. The rationale is that mzExacto() searches the spread dictionary using retention time and published m/z peaks for precise identification, so validation ensures the search logic correctly aggregated multi-peak and multi-file sample portions that describe each chemical.

## Related tools

- **spreadOut** (Preprocesses raw CSV input and constructs the standard_spread dictionary object required as input to mzExacto; prepares data for intelligent sorting by retention time and published masses) — https://github.com/castratton/uafR
- **mzExacto** (Core function that collects m/z, retention time, match factor, and area information for query chemicals by searching the advanced dictionary for matching samples) — https://github.com/castratton/uafR
- **categorate** (Downstream function that accesses categorical data for searched chemicals; used after mzExacto validation to enrich results with database membership and structural properties) — https://github.com/castratton/uafR
- **Agilent Unknowns Analysis** (Recommended software for generating the raw CSV input in default format with required column names (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name))
- **R** (Programming environment for executing spreadOut(), mzExacto(), and validation checks on the output dataframe)

## Examples

```
input_spread = spreadOut(input_dat); query_chemicals = c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'); input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- All four query chemicals appear as rows in the mzExacto output dataframe with no missing or duplicate entries.
- Retention time (RT) values for each compound are consistent (within ±0.01 min) across replicate standard solutions (Std_soln_00, Std_soln_07, Std_soln_00a).
- Base.Peak.MZ (m/z) values match published reference values or previously validated peaks for each compound (e.g., Methyl salicylate at m/z 120.00).
- Match.Factor values are ≥65 for all query chemicals; inspect outliers <70 as potential ambiguous identifications.
- Area values are non-zero, positive numbers; absence of NAs in the output dataframe indicates complete aggregation of sample portions from the advanced dictionary.

## Limitations

- mzExacto requires query chemicals to be spelled exactly as they appear in the Compound.Name column of the input dataset; name mismatches will result in silent loss of records.
- Match.Factor threshold (65 or higher) is a heuristic; compounds below this threshold may be true positives but are typically filtered; validation should inspect any below-threshold results independently.
- The skill validates presence and consistency of output structure but does not independently verify that the m/z or RT values are scientifically correct; cross-reference with external MS libraries (e.g., NIST, PubChem) is recommended for novel compounds.
- Aggregation of multi-peak and multi-file sample portions relies on the accuracy of the advanced dictionary; incorrect dictionary entries will propagate into mzExacto results.

## Evidence

- [other] Does the mzExacto() function correctly retrieve m/z, retention time, match factor, and area values for a set of known query chemicals from mass spectrometry data?: "Does the mzExacto() function correctly retrieve m/z, retention time, match factor, and area values for a set of known query chemicals from mass spectrometry data?"
- [methods] mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals: "mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals"
- [other] Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each sample: "Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each"
- [methods] Query.Factor filtering with query_chems = standard_dat$Compound.Name[standard_dat$Match.Factor >= 65]: "query_chems = standard_dat$Compound.Name[standard_dat$Match.Factor >= 65]"
- [methods] The first step in the process is to convert the raw input to a format that downstream functions can work with. spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses): "spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses)"
- [methods] aggregation (using all published names and top m/z peaks) of sample portions that describe a chemical: "aggregation (using all published names and top m/z peaks) of sample portions that describe a chemical"
