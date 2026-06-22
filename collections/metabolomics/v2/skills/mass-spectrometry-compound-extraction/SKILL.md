---
name: mass-spectrometry-compound-extraction
description: Use when you have a preprocessed GC-MS dataset (from spreadOut) with standardized column names (Compound.Name, Component.RT, Base.Peak.MZ, Component.Area, Match.Factor) and a specific list of chemical compounds you want to extract and aggregate across multiple sample runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - R
  - mzExacto
  - spreadOut
  - categorate
  - exactoThese
  - ChemmineR
  - webchem
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

# mass-spectrometry-compound-extraction

## Summary

Extract m/z, retention time, match factor, and peak area values for a set of known query chemicals from preprocessed GC-MS data by searching an advanced dictionary keyed on compound names and spectral signatures. This skill bridges the transition from raw mass spectrometry output to compound-level tabular data suitable for downstream chemical classification and risk assessment.

## When to use

You have a preprocessed GC-MS dataset (from spreadOut) with standardized column names (Compound.Name, Component.RT, Base.Peak.MZ, Component.Area, Match.Factor) and a specific list of chemical compounds you want to extract and aggregate across multiple sample runs. Apply this skill when you need to pull out exact mass, retention time, best match factor, and area for known query chemicals rather than filtering by match factor threshold alone.

## When NOT to use

- Your input is raw .CSV from GC-MS instrument without spreadOut preprocessing — use spreadOut first to normalize column names and structure.
- You want to filter compounds by Match Factor threshold (e.g., > 80) rather than by exact chemical identity — use filter on Match.Factor column instead.
- You need to perform chemical classification or subsetting by molecular weight, functional groups, or database membership — use categorate and exactoThese for that purpose.

## Inputs

- standard_spread object (output from spreadOut function)
- query_chemicals: character vector of compound names

## Outputs

- dataframe with rows = query chemicals, columns = Compound, Mass, RT, Best Match (Match Factor), and per-sample area values

## How to apply

Load the preprocessed standard_spread object (output from spreadOut), which contains matrices of compound names, retention times, match factors, m/z values, exact masses, areas, and nested webInfo for published chemical identifiers. Define query_chemicals as a character vector of compound names (e.g., 'Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'). Execute mzExacto(standard_spread, query_chemicals) to search the spread dictionary and extract all matching samples that contain these chemicals, using retention time and published m/z peaks for precise identification. The function returns a single dataframe where rows correspond to the query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each sample (e.g., Std_soln_00, Std_soln_07, Std_soln_00a). The aggregation uses all published names and top m/z peaks to ensure robust matching across multiple hits per chemical per sample.

## Related tools

- **spreadOut** (Preprocesses raw GC-MS .CSV input, normalizing column names and sorting by retention time and published m/z peaks to create the standard_spread object required as input to mzExacto) — https://github.com/castratton/uafR
- **categorate** (Downstream enrichment of extracted compounds with categorical data (reactive groups, molecular properties, database presence) to enable fine-grained subsetting) — https://github.com/castratton/uafR
- **exactoThese** (Subset and filter categorated compounds by molecular weight range, database membership, or chemical descriptors (rings, groups, atoms, charges) to refine query_chemicals before or after mzExacto extraction) — https://github.com/castratton/uafR
- **ChemmineR** (Underlying cheminformatics package integrated into uafR for chemical structure and property queries)
- **webchem** (Underlying package for accessing PubChem and other public chemical databases to enrich query_chemicals with published identifiers and properties)

## Examples

```
input_spread = spreadOut(input_dat)
query_chemicals = c("Linalool", "Methyl Salicylate", "Limonene", "alpha-Thujene")
input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- Output dataframe has exactly as many rows as there are query_chemicals (no missing or duplicate compounds unless multiple m/z peaks exist for a single compound).
- All query_chemicals appear in the Compound column of the output; compounds not found in standard_spread are either absent from output or explicitly marked as NA/not found.
- Match Factor values in output are non-missing and within expected range (0–100); any flagged as low (e.g., < 65) are inspected for potential false positives.
- Retention time and m/z values match expected literature values or instrument calibration for each compound; gross outliers indicate data quality issues or mismatched identifications.
- Area values are positive numbers (no negative or zero areas except where genuinely absent in the source data); aggregation across multiple sample runs is consistent and traceable.

## Limitations

- Requires strict input column naming (Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, Match.Factor); datasets with non-standard columns will fail or require manual preprocessing.
- Relies on exact or fuzzy matching of query_chemicals names against Compound.Name in the input; spelling variations, case sensitivity, or synonym differences may cause missed extractions.
- If the same compound appears multiple times in a single sample (different retention times, m/z peaks, or Match Factors), the function aggregates them; the user must verify which aggregation strategy (best match, mean, all) is appropriate for downstream use.
- No changelog documented in repository; stability and backward compatibility of function signature or output format across versions are unclear.

## Evidence

- [methods] mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals: "mzExacto() collects the same information for a set of query chemicals and uses it to precisely search the advanced dictionary for samples that have those chemicals"
- [methods] The first step in the process is to convert the raw input to a format that downstream functions can work with. spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses): "spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses)"
- [methods] aggregation (using all published names and top m/z peaks) of sample portions that describe a chemical: "aggregation (using all published names and top m/z peaks) of sample portions that describe a chemical"
- [other] Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each sample (Std_soln_00, Std_soln_07, Std_soln_00a).: "Return a single dataframe where rows correspond to the four query chemicals and columns include Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each"
- [readme] The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor': "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"
