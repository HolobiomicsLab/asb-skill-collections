---
name: chemical-identifier-unification
description: 'Use when when you have raw GC-MS output (CSV with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - ChemmineR
  - R
  - webchem
  - PubChem
  techniques:
  - GC-MS
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- To perform the chemical structure matches and summarize atomic features, uafR taps into an amazing set of cheminformatics packages -- [ChemmineR]
- Modern programming languages allow even complex workflows to be automated
- Modern programming languages allow even complex workflows to be automated.
- uafR taps into an amazing set of cheminformatics packages -- [ChemmineR](https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html), [fmcsR](https://bioconductor.org/packages/release/bioc
- '[fmcsR](https://bioconductor.org/packages/release/bioc/html/fmcsR.html), [webchem](https://cran.r-project.org/web/packages/webchem/index.html)'
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

# chemical-identifier-unification

## Summary

Unifies fragmented chemical identifiers across GC-MS samples by querying external chemical databases (PubChem, webchem) to retrieve published synonyms, exact masses, and retention time ranges, then constructs a searchable index keyed by retention-time–mass composites. This enables consistent matching and aggregation of the same chemical across multiple files and detection peaks.

## When to use

When you have raw GC-MS output (CSV with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) containing multiple entries for the same compound under variant names or different m/z peaks, and you need to consolidate them into a unified, queryable chemical inventory before downstream sorting, filtering, or categorical lookup.

## When NOT to use

- Input CSV is already pre-normalized with unique compound identifiers and standardized naming conventions across files.
- Compounds are not in PubChem or webchem (e.g., proprietary unknowns or de novo synthetic compounds); metadata retrieval will fail or return sparse results.
- The workflow requires real-time or streaming processing; RDS serialization introduces latency unsuitable for live data feeds.

## Inputs

- CSV file with mandatory columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name
- PubChem and webchem API access (via R webchem package)

## Outputs

- R list object (standard_spread) containing reshaped matrices for Compound.Name, Component.RT, Match.Factor, Base.Peak.MZ, Component.Area
- Nested metadata list (webInfo) indexed by compound name, storing published synonyms, top m/z peaks, exact mass, retention time ranges
- RDS serialized file of the unified standard_spread object

## How to apply

Load the raw CSV into R via read.csv() and apply spreadOut(), which extracts and reshapes the six required columns into separate matrices (one per metadata type). Query webchem and PubChem programmatically to retrieve all published synonyms, top m/z peaks, exact molecular mass, and literature retention time ranges for each unique Compound.Name entry. Construct a composite unique identifier (rtBYmass) by concatenating retention time and exact mass. Nest all metadata into a single R list indexed by compound name (webInfo), then aggregate all matrices and webInfo into a standard_spread list object and serialize as RDS. This unified structure enables intelligent sorting by retention times and published masses, followed by aggregation using all published names and top m/z peaks to group sample portions describing the same chemical.

## Related tools

- **webchem** (Queries PubChem and external chemical databases to retrieve published synonyms, exact mass, m/z fragments, and retention time metadata for each compound name) — https://cran.r-project.org/web/packages/webchem/index.html
- **ChemmineR** (Provides cheminformatics infrastructure for chemical structure and metadata handling within the uafR pipeline) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **R** (Core programming language for matrix reshaping, list aggregation, and RDS serialization of the unified chemical index)
- **PubChem** (Source database queried via webchem to retrieve published chemical synonyms, exact molecular mass, and fragmentation data) — https://pubchem.ncbi.nlm.nih.gov/

## Examples

```
input_dat = read.csv("gcms_dataset.csv"); input_spread = spreadOut(input_dat)
```

## Evaluation signals

- All six mandatory CSV columns are successfully extracted and reshaped into separate matrices with consistent row/column dimensions (samples as columns, entries as rows).
- No missing or NULL values in the composite rtBYmass identifier; each identifier is unique and deterministic.
- webInfo list contains complete metadata entries for ≥90% of unique Compound.Name values; webchem retrieval failures are logged and traceable.
- The standard_spread RDS object deserializes without corruption and preserves matrix dimensions and nested structure integrity.
- Downstream mzExacto() and categorate() functions execute without type or dimension mismatch errors, confirming proper aggregation.

## Limitations

- Depends on webchem and PubChem API availability and rate limits; queries for large compound sets may timeout or hit quota restrictions.
- Compound names must match PubChem records; misspelled, colloquial, or proprietary names will not retrieve metadata, resulting in sparse or absent entries in webInfo.
- Retention time ranges from literature may not represent the specific GC column, temperature program, or instrument configuration used in the input dataset, risking false aggregation of co-eluting isomers.
- The rtBYmass composite identifier assumes retention time precision; minor instrumental drift or calibration differences may fragment the same chemical across multiple identifiers.

## Evidence

- [other] spreadOut() prepares the read-in CSV for intelligent sorting by retention times and published masses, followed by aggregation using all published names and top m/z peaks to organize sample portions describing a chemical.: "spreadOut() prepares the read in .CSV for intelligent ***sorting*** (using retention times and published masses) then ***aggregation*** (using all published names and top m/z peaks) of sample"
- [other] Extract and reshape Compound.Name, Component.RT, Match.Factor, Base.Peak.MZ, Component.Area columns, each with samples as columns and entries as rows.: "Organize data into separate matrices: extract and reshape Compound.Name, Component.RT, Match.Factor, Base.Peak.MZ, Component.Area columns, each with samples as columns and entries as rows."
- [other] Query webchem and PubChem to retrieve published chemical metadata including all published synonyms, top m/z peaks, exact molecular mass, and likely retention time ranges.: "Query webchem and PubChem via the webchem package to retrieve published chemical metadata for each unique compound name (all published synonyms, top m/z peaks, exact molecular mass, likely retention"
- [other] Construct a unique identifier for each data point by concatenating retention time and exact mass (rtBYmass).: "Construct a unique identifier for each data point by concatenating retention time and exact mass (rtBYmass)."
- [readme] The input .CSV file has strict column name/input data requirements with mandatory columns: Component.RT, Component.Area, Base.Peak.MZ, File.Name, Compound.Name, and Match.Factor.: "The input .CSV file has strict column name/input data requirements. The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"
- [other] Aggregate all matrices and the nested metadata list into a single R list object (standard_spread) and serialize as an RDS file.: "Aggregate all matrices and the nested metadata list into a single R list object (standard_spread) and serialize as an RDS file."
