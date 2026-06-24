---
name: retention-time-and-mass-based-sorting
description: 'Use when you have raw GC-MS output in CSV format (with columns: Component.RT,
  Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3370
  tools:
  - ChemmineR
  - R
  - webchem
  - spreadOut()
  - mzExacto()
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
- The first step in the process is to convert the raw input to a format that downstream
  functions can work with. `spreadOut()` prepares the read in .CSV for intelligent
  ***sorting*** (using retention
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

# retention-time-and-mass-based-sorting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Organize raw GC-MS CSV data by retention time and exact mass to enable intelligent aggregation and downstream chemical matching. This skill prepares unstructured mass spectrometry output into a sortable, queryable artifact indexed by both temporal (RT) and mass-based (m/z) properties.

## When to use

Apply this skill when you have raw GC-MS output in CSV format (with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) and need to organize it for chemical library searching, multi-sample aggregation, or threshold-based filtering before querying against published chemical metadata.

## When NOT to use

- Input CSV is missing required column names (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) — the workflow will fail or produce incorrect indexing.
- Data is already in a pre-aggregated or matrix format without individual sample columns — use only when raw CSV with per-file rows exists.
- Compound names do not match PubChem/webchem nomenclature and no fallback fuzzy matching is configured — metadata enrichment will be incomplete.

## Inputs

- CSV file with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name
- Unique compound names from the input CSV

## Outputs

- R list object (standard_spread) containing: sample-keyed matrices of RT, m/z, match factor, and area; nested list (webInfo) of published metadata per compound
- RDS serialized version of standard_spread for downstream use

## How to apply

Load the raw CSV using R's read.csv() and pass it to spreadOut(), which extracts and reshapes the Component.RT, Base.Peak.MZ, Match.Factor, and Component.Area columns into separate matrices keyed by sample. Simultaneously query webchem and PubChem to retrieve all published synonyms, top m/z peaks, exact molecular mass, and literature retention time ranges for each unique compound name. Create a unique identifier (rtBYmass) by concatenating retention time and exact mass for each data point. Aggregate all matrices and the retrieved metadata into a nested list (webInfo) indexed by compound name, then serialize as an RDS file. This structure enables fast lookup of chemicals by RT+mass and supports subsequent aggregation using all published names and peak data.

## Related tools

- **webchem** (Query PubChem and other chemical databases to retrieve published synonyms, exact masses, top m/z peaks, and retention time ranges for each compound) — https://cran.r-project.org/web/packages/webchem/index.html
- **ChemmineR** (Cheminformatics package integrated into uafR for molecular structure and property analysis) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **R** (Programming environment for data reshaping, matrix operations, and list aggregation)
- **spreadOut()** (Core uafR function that extracts, reshapes, and aggregates MS data matrices and metadata) — https://github.com/castratton/uafR

## Examples

```
input_dat = read.csv("your/gcms/dataset.csv"); input_spread = spreadOut(input_dat)
```

## Evaluation signals

- Output RDS file contains nested list structure with compound names as keys and metadata/matrix subsets as values.
- Each data point has a unique rtBYmass identifier (concatenation of retention time and exact mass) with no duplicates within a sample.
- All six required CSV columns are present in the reshaped matrices (one matrix per column type).
- Published metadata from webchem (synonyms, top m/z, exact mass) matches PubChem records for spot-check compounds.
- Sample-level area values and match factors in output matrices correspond exactly to input CSV rows aggregated by sample.

## Limitations

- Requires exact or near-exact matches between input compound names and PubChem nomenclature; misspellings or regional naming variants will cause metadata lookup failures.
- Retention time ranges from literature may not reflect the specific instrument, column, or program used for the input samples; user should validate RT ranges against empirical data.
- Processing time scales with the number of unique compounds and number of external API queries; large datasets may face rate limiting from PubChem/webchem.
- The rtBYmass identifier assumes RT and mass are sufficient for uniqueness; isomers or compounds with identical RT and base peak m/z will collide.

## Evidence

- [methods] spreadOut() prepares the read in .CSV for intelligent ***sorting*** (using retention times and published masses) then ***aggregation***: "prepares the read in .CSV for intelligent sorting (using retention times and published masses) then aggregation"
- [other] Organize data into separate matrices: extract and reshape Compound.Name, Component.RT, Match.Factor, Base.Peak.MZ, Component.Area columns, each with samples as columns and entries as rows.: "Organize data into separate matrices: extract and reshape Compound.Name, Component.RT, Match.Factor, Base.Peak.MZ, Component.Area columns"
- [other] Query webchem and PubChem via the webchem package to retrieve published chemical metadata for each unique compound name (all published synonyms, top m/z peaks, exact molecular mass, likely retention time ranges).: "Query webchem and PubChem via the webchem package to retrieve published chemical metadata for each unique compound name"
- [other] Construct a unique identifier for each data point by concatenating retention time and exact mass (rtBYmass).: "Construct a unique identifier for each data point by concatenating retention time and exact mass (rtBYmass)"
- [readme] The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order.: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor'"
