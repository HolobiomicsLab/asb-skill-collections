---
name: mass-spectrometry-data-formatting
description: 'Use when you have raw GC-MS output exported as CSV (containing columns:
  Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - ChemmineR
  - R
  - webchem
  - Agilent Unknowns Analysis
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
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

# mass-spectrometry-data-formatting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Transform raw GC-MS CSV output into a searchable, nested data structure indexed by compound identity and analytical features. This skill prepares mass spectrometry data for downstream sorting, aggregation, and cheminformatics queries by integrating retention time, m/z peaks, and published chemical metadata.

## When to use

Apply this skill when you have raw GC-MS output exported as CSV (containing columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) and need to enable intelligent filtering by retention time and mass, cross-sample aggregation, or lookup of published chemical synonyms and structural properties before downstream analysis or curation.

## When NOT to use

- Input CSV lacks any of the six required column names (Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name) — preprocessing or reformatting is required before calling spreadOut().
- Compound names are already standardized identifiers or ChEBI/PubChem CIDs — webchem metadata lookup will fail or be redundant.
- Data is already in a preprocessed spread/matrix format — skip directly to mzExacto() or categorate().

## Inputs

- CSV file with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name

## Outputs

- R list object (standard_spread) containing reshaped matrices and nested metadata list (webInfo)
- RDS serialized file for persistence and downstream function compatibility

## How to apply

Load the raw CSV using R's read.csv() and pass it to spreadOut(), which internally: (1) extracts and reshapes the six required columns into separate matrices with samples as columns; (2) queries webchem to retrieve published metadata (all synonyms, top m/z peaks, exact molecular mass, retention time ranges) for each unique Compound.Name; (3) constructs unique identifiers by concatenating retention time and exact mass (rtBYmass); (4) assembles a nested list (webInfo) keyed by compound name, storing all aliases and spectral/physical properties; (5) aggregates all matrices and metadata into a single R list object (standard_spread) and serializes as RDS. This transformation enables subsequent filtering by Match.Factor threshold, sorting by retention times and published masses, and aggregation across sample replicates using all published names and top m/z peaks.

## Related tools

- **webchem** (Retrieves published chemical metadata (synonyms, m/z peaks, molecular mass, retention time ranges) for each detected compound name via PubChem and related chemical databases) — https://cran.r-project.org/web/packages/webchem/index.html
- **ChemmineR** (Provides cheminformatics utilities for structural and property-based queries on the aggregated chemical library) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **R** (Programming language and runtime environment for executing spreadOut() and serializing the output as RDS)
- **Agilent Unknowns Analysis** (Recommended software for generating the input CSV in the default format with correct column names and data types) — https://www.agilent.com/cs/library/usermanuals/public/G3335-901

## Examples

```
input_dat = read.csv('your/gcms/dataset.csv'); input_spread = spreadOut(input_dat)
```

## Evaluation signals

- Verify the output standard_spread list contains exactly six named matrix elements (one per input column) with consistent dimensions: samples as columns, entries as rows.
- Check that webInfo nested list is keyed by unique Compound.Name values and each entry contains published synonyms, top m/z peaks, exact molecular mass, and retention time ranges (non-null).
- Confirm rtBYmass identifiers are unique and follow the format 'retention_time_exact_mass' for each sample–compound combination.
- Validate that the RDS file is readable by R's readRDS() and recreates the standard_spread structure without loss or corruption.
- Spot-check one or two Compound.Name entries in webInfo against PubChem directly to confirm webchem successfully retrieved published data.

## Limitations

- Requires exact or near-exact Compound.Name matching during webchem lookup; poorly formatted or ambiguous chemical names will fail to retrieve metadata or return incorrect entries.
- Depends on external database availability (PubChem, LOTUS, KEGG, FEMA, FDA/SPL); network failures or database downtime will interrupt metadata collection.
- Retention time prediction and m/z peak lists are taken from published databases and may not match the specific GC-MS instrument, column, or method used to generate the input data.
- Large CSV files with hundreds of unique compounds may incur significant API call overhead and latency during webchem metadata retrieval.

## Evidence

- [other] spreadOut() prepares the read-in CSV for intelligent sorting by retention times and published masses, followed by aggregation using all published names and top m/z peaks: "spreadOut() prepares the read in .CSV for intelligent ***sorting*** (using retention times and published masses) then ***aggregation*** (using all published names and top m/z peaks)"
- [readme] The input CSV must have specific column names in no particular order: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order."
- [methods] webchem package is used to query published chemical databases for metadata: "[webchem](https://cran.r-project.org/web/packages/webchem/index.html)"
- [other] The output is a nested list indexed by compound name storing metadata: "Build a nested list (webInfo) indexed by compound name, storing all published names, top m/z peaks, exact mass, and published retention time ranges."
- [other] Output is serialized as RDS for downstream function compatibility: "Aggregate all matrices and the nested metadata list into a single R list object (standard_spread) and serialize as an RDS file."
