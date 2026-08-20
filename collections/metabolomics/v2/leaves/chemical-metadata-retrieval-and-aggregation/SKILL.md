---
name: chemical-metadata-retrieval-and-aggregation
description: Use when after raw GC-MS CSV input has been parsed into separate matrices
  (Component.RT, Base.Peak.MZ, Compound.Name, Match.Factor, Component.Area) and you
  need to enrich sample-level identifications with authoritative chemical properties.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3431
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0821
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

# chemical-metadata-retrieval-and-aggregation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Retrieve published chemical metadata (synonyms, exact molecular mass, top m/z peaks, retention time ranges) from external databases (PubChem, webchem) and aggregate it with GC-MS sample data into a nested, searchable index keyed by compound name. This enables downstream sorting, filtering, and categorization of mass spectrometry detections.

## When to use

Apply this skill after raw GC-MS CSV input has been parsed into separate matrices (Component.RT, Base.Peak.MZ, Compound.Name, Match.Factor, Component.Area) and you need to enrich sample-level identifications with authoritative chemical properties. Use it when the goal is to enable intelligent sorting by retention time and exact mass, aggregate results across multiple chemical names for the same compound, or prepare data for categorical filtering (e.g., by database membership, molecular weight, functional groups).

## When NOT to use

- Input data lacks standardized column names (Component.RT, Base.Peak.MZ, Compound.Name, Match.Factor, File.Name) — preprocessing is required first.
- Compound identifications are unknown or unconfirmed (i.e., only raw MS peaks with no chemical name assigned) — metadata retrieval requires a list of putative compound names to query.
- The goal is to perform de novo structure elucidation or peak deconvolution; this skill assumes compound identities are already proposed and aims only to enrich them with published metadata.

## Inputs

- Raw GC-MS CSV file with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name
- Vector of unique compound names (character vector)
- Web API credentials or local database connections (webchem, PubChem)

## Outputs

- Nested R list object (standard_spread) containing: sample matrices (Compound.Name, Component.RT, Match.Factor, Base.Peak.MZ, Component.Area, each with samples as columns), and webInfo (compound-indexed metadata with published names, top m/z peaks, exact mass, retention time ranges)
- RDS file serialization of standard_spread
- Unique identifier mappings (rtBYmass concatenations)

## How to apply

Query webchem and PubChem APIs for each unique compound name detected in the sample set to retrieve all published synonyms, exact molecular mass, top m/z fragmentation peaks, and literature-reported retention time ranges. Construct a unique identifier for each data point by concatenating retention time and exact mass (rtBYmass) to enable precise matching across samples. Build a nested list structure (webInfo) indexed by compound name, with each entry storing published names, top m/z values, exact mass, and retention time ranges. Aggregate all sample matrices and the metadata list into a single R list object (standard_spread) and serialize as RDS. The key rationale is that published metadata provides a ground-truth chemical signature that transforms sample-level MS peaks (which are instrument- and method-dependent) into compound-centric records suitable for cross-sample aggregation and categorical queries.

## Related tools

- **webchem** (Query PubChem and other chemical databases for exact molecular mass, published synonyms, m/z fragmentation patterns, and retention time metadata for each compound name.) — https://cran.r-project.org/web/packages/webchem/index.html
- **PubChem** (Source database providing published chemical structure data, synonyms, exact masses, and reactive group annotations for compound lookups.) — https://pubchem.ncbi.nlm.nih.gov/
- **ChemmineR** (Bioconductor cheminformatics package for downstream structural analysis, molecular property calculation, and chemical similarity comparisons once metadata is aggregated.) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **R** (Programming language used to coordinate spreadOut() workflow: load CSV, call webchem APIs, build nested data structures, and serialize RDS output.)

## Examples

```
input_spread = spreadOut(read.csv("your/gcms/dataset.csv"))
```

## Evaluation signals

- The webInfo nested list has one entry per unique compound name, each entry contains keys for published_names (character vector of synonyms), top_mz (numeric vector of m/z peaks), exact_mass (single numeric value), and retention_time_range (numeric vector or NA if unavailable).
- All sample matrices (Compound.Name, Component.RT, Match.Factor, Base.Peak.MZ, Component.Area) have identical dimensions: rows = data points, columns = samples, and no NA values are introduced by the query process.
- rtBYmass identifiers are unique across the dataset and correctly concatenate retention time and exact mass with no rounding artifacts or collision.
- RDS serialization completes without error and the deserialized object preserves nested list structure and all numeric precision.
- For a random sample of compound names, manual inspection of the webInfo entries confirms that published_names align with known chemical synonyms and top_mz values correspond to literature fragmentation patterns for that compound.

## Limitations

- webchem API queries may fail or return incomplete metadata for obscure, recently-synthesized, or misspelled compound names; results are only as complete as PubChem coverage.
- Retention time ranges in published literature are often method- and column-specific (GC parameters, column phase) and may not align with the user's instrument or conditions.
- Exact mass precision is sensitive to decimal rounding; if compound name queries return multiple isomers or salts with very similar masses, manual curation may be needed to select the correct record.
- The rtBYmass identifier assumes that retention time and exact mass together uniquely identify a chemical within a sample; in complex mixtures or with poor chromatographic resolution, collisions are possible.
- Aggregation across all published names may conflate different chemical forms (e.g., free acid vs. salt) if PubChem synonyms are broad; filtering by Match.Factor before aggregation can mitigate this.

## Evidence

- [methods] Query webchem and PubChem retrieval: "Query webchem and PubChem via the webchem package to retrieve published chemical metadata for each unique compound name (all published synonyms, top m/z peaks, exact molecular mass, likely retention"
- [methods] rtBYmass identifier construction: "Construct a unique identifier for each data point by concatenating retention time and exact mass (rtBYmass)."
- [methods] webInfo nested list structure: "Build a nested list (webInfo) indexed by compound name, storing all published names, top m/z peaks, exact mass, and published retention time ranges."
- [methods] standard_spread aggregation and serialization: "Aggregate all matrices and the nested metadata list into a single R list object (standard_spread) and serialize as an RDS file."
- [methods] Sorting and aggregation rationale: "spreadOut() prepares the read-in .CSV for intelligent sorting (using retention times and published masses) then aggregation (using all published names and top m/z peaks) of sample portions that"
- [readme] Required input column names: "The column names MUST include: 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name', 'Compound.Name', and 'Match.Factor' in no particular order."
