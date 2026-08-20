---
name: data-structure-design-for-spectral-searches
description: Use when you have raw GC-MS output in CSV format with columns Component.RT,
  Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, and File.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - ChemmineR
  - R
  - webchem
  - PubChem
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- To perform the chemical structure matches and summarize atomic features, uafR taps
  into an amazing set of cheminformatics packages -- [ChemmineR]
- Modern programming languages allow even complex workflows to be automated
- Modern programming languages allow even complex workflows to be automated.
- uafR taps into an amazing set of cheminformatics packages -- [ChemmineR](https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html),
  [fmcsR](https://bioconductor.org/packages/release/bioc
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

# data-structure-design-for-spectral-searches

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Design and construct nested data structures that organize raw GC-MS spectral data into searchable indexes keyed by chemical identity, retention time, and exact mass. This skill enables downstream functions to perform rapid intelligent sorting, aggregation, and chemical metadata retrieval across multi-sample datasets.

## When to use

Apply this skill when you have raw GC-MS output in CSV format with columns Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, and File.Name, and you need to prepare the data for chemical searches, sorting by retention time and published masses, or aggregation across multiple samples describing the same chemical.

## When NOT to use

- Input CSV is missing required column names or has incorrect data types for RT, m/z, or mass values
- Data is already in a processed, matrix or feature-table format designed for downstream statistical analysis
- Compound names cannot be reliably matched to PubChem or webchem databases (e.g., proprietary or novel compounds without published metadata)

## Inputs

- CSV file with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name
- PubChem and chemical name registry data (via webchem package queries)

## Outputs

- R list object (standard_spread) containing organized matrices and nested metadata
- RDS serialized file containing the complete spread structure
- rtBYmass unique identifiers (retention time concatenated with exact mass)

## How to apply

Load the raw CSV using R's read.csv() and extract individual columns (Compound.Name, Component.RT, Match.Factor, Base.Peak.MZ, Component.Area) into separate matrices with samples as columns and entries as rows. Query webchem and PubChem via the webchem R package to retrieve published chemical metadata for each unique compound name, including all synonyms, top m/z peaks, exact molecular mass, and retention time ranges. Construct a unique identifier for each data point by concatenating retention time and exact mass (rtBYmass) to enable precise matching. Build a nested R list (webInfo) indexed by compound name, storing published names, top m/z peaks, exact mass, and retention time ranges. Finally, aggregate all matrices and the nested metadata list into a single R list object (standard_spread) and serialize as an RDS file for downstream functions to access.

## Related tools

- **webchem** (Query chemical metadata (synonyms, m/z peaks, exact mass, retention time ranges) from PubChem and published databases for compound name normalization and enrichment) — https://cran.r-project.org/web/packages/webchem/index.html
- **ChemmineR** (Provide cheminformatics functions for chemical structure analysis and data organization within the uafR workflow) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **R** (Core language for automating matrix construction, list aggregation, and RDS serialization of the spread structure)
- **PubChem** (Source database for published chemical metadata (synonyms, molecular properties, spectral peaks) queried via webchem) — https://pubchem.ncbi.nlm.nih.gov/

## Examples

```
input_dat = read.csv("your/gcms/dataset.csv"); input_spread = spreadOut(input_dat)
```

## Evaluation signals

- Verify all six required CSV columns are present and successfully parsed (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name)
- Confirm that each unique compound name was successfully queried in PubChem/webchem and that webInfo contains non-null entries for published synonyms, exact mass, and top m/z peaks
- Check that rtBYmass identifiers are unique per data point and concatenate both retention time and exact mass correctly
- Validate the nested list structure: standard_spread should contain separate matrices for each column plus a webInfo sub-list indexed by compound name
- Verify the RDS file deserializes without error and retains all data types (numeric matrices and character/list metadata)

## Limitations

- Compound name matching to PubChem relies on exact string matching or fuzzy matching via webchem; misspellings, abbreviations, or proprietary names may fail to retrieve metadata
- Retention time ranges from published literature may not match the user's experimental instrument, method, or column type; rtBYmass identifiers are only valid within the context of the user's GC-MS method
- The skill requires internet connectivity to query PubChem and webchem; offline use is not supported
- If multiple compounds have very similar retention times and exact masses, the rtBYmass identifier may not fully disambiguate them; additional orthogonal data (e.g., RI values) may be needed

## Evidence

- [readme] Column requirements and raw input: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order."
- [methods] Core workflow of spreadOut function: "spreadOut() prepares the read in .CSV for intelligent sorting (using retention times and published masses) then aggregation (using all published names and top m/z peaks) of sample portions that"
- [other] Data structure organization into matrices: "Organize data into separate matrices: extract and reshape Compound.Name, Component.RT, Match.Factor, Base.Peak.MZ, Component.Area columns, each with samples as columns and entries as rows."
- [other] Webchem metadata retrieval: "Query webchem and PubChem via the webchem package to retrieve published chemical metadata for each unique compound name (all published synonyms, top m/z peaks, exact molecular mass, likely retention"
- [other] Unique identifier construction: "Construct a unique identifier for each data point by concatenating retention time and exact mass (rtBYmass)."
- [other] Final nested list aggregation: "Aggregate all matrices and the nested metadata list into a single R list object (standard_spread) and serialize as an RDS file."
