---
name: compound-identifier-aggregation
description: Use when you have metabolomics results from multiple studies with compound
  identifiers in heterogeneous formats (names, InChI strings, SMILES, ChEBI/KEGG/HMDB
  codes) and need to merge datasets for vote-counting or meta-analysis. Apply this
  skill before computing consensus measures (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - amanida
  - webchem
  - PubChem
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted
  meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions
  for computing a weighted meta-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Compound Identifier Aggregation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Harmonize and deduplicate metabolite compound identifiers across multiple studies by converting diverse ID formats (chemical name, InChI, InChIKey, SMILES) to a common standard (PubChem ID) and detecting duplicates. This enables meaningful meta-analysis by ensuring each metabolite is counted only once across study results.

## When to use

You have metabolomics results from multiple studies with compound identifiers in heterogeneous formats (names, InChI strings, SMILES, ChEBI/KEGG/HMDB codes) and need to merge datasets for vote-counting or meta-analysis. Apply this skill before computing consensus measures (e.g., vote-counting or weighted p-value combination) to avoid artificially inflating sample size or misattributing results to distinct metabolites.

## When NOT to use

- Identifiers are already standardized to a single namespace (e.g., all KEGG IDs or all PubChem IDs with no aliases) — check_names will still work but adds unnecessary latency.
- Your compound list is already deduplicated and you are only performing within-study analysis (not cross-study meta-analysis); identifier harmonization is critical only for multi-study consensus.
- Internet access to PubChem is unavailable; webchem queries will fail and check_names cannot complete.

## Inputs

- Harmonized metabolite dataset (CSV, XLS, or TXT) with columns: compound identifier (any format), p-value or trend label, fold-change, study sample size (N), and bibliographic reference
- Pre-loaded amanida data frame from amanida_read() with mode='quan' or mode='qual'

## Outputs

- Deduplicated amanida data frame with PubChem IDs, duplicate flags, and harmonized compound records
- Compound descriptor table (optional, if comp.inf=T) including PubChem ID, molecular formula, molecular weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, and Drugbank identifiers

## How to apply

Use the amanida `check_names` function on your harmonized dataset (loaded via `amanida_read` with columns: identifier, p-value or trend label, fold-change, study size N, and reference). The function queries PubChem via the `webchem` package to convert all identifiers to PubChem IDs, then automatically detects and flags duplicates. Set `comp.inf = T` in subsequent analysis to retrieve and attach molecular descriptors (formula, weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank) to each deduplicated record. This transformation ensures downstream vote-counting and meta-analysis operate on a single, standardized compound namespace.

## Related tools

- **amanida** (R package providing check_names() function for PubChem ID conversion and duplicate detection, and amanida_read() for loading harmonized datasets) — https://github.com/mariallr/amanida
- **webchem** (R package queried by amanida's check_names to retrieve and convert compound identifiers to PubChem IDs)
- **PubChem** (Public chemical compound database serving as the standard namespace for identifier conversion and metadata retrieval)

## Examples

```
datafile <- amanida_read(input_file, mode = "quan", coln = c("Compound Name", "P-value", "Fold-change", "N total", "References"), separator=";"); datafile <- check_names(datafile)
```

## Evaluation signals

- All identifiers in the output are in PubChem ID format (numeric); no heterogeneous ID formats remain.
- Duplicate compound records are flagged and consolidated; the number of unique compounds in the output matches the expected deduplicated count.
- When comp.inf=T, each record includes non-null molecular formula, weight, and cross-database identifiers (KEGG, ChEBI, HMDB); missing descriptors indicate PubChem lookup failure for that compound.
- Comparison of pre- and post-harmonization record counts shows expected reduction; no data loss for non-duplicate records.
- Subsequent vote-counting or meta-analysis results are reproducible across runs (same deduplicated set produces same consensus votes or p-values).

## Limitations

- PubChem database coverage is incomplete for rare or novel compounds; identifiers without PubChem matches are dropped or retained as-is, reducing harmonization completeness.
- Identical chemical structures with different stereochemistry or ionization states may map to distinct PubChem IDs, causing artificial splitting rather than merging; manual review of flagged duplicates is recommended.
- webchem queries depend on internet connectivity and PubChem API availability; high-throughput queries may be rate-limited or fail transiently.
- Only identifier formats supported by PubChem and webchem (chemical name, InChI, InChIKey, SMILES) are reliably converted; proprietary or institutional metabolite codes may not harmonize.

## Evidence

- [intro] Identifier conversion and deduplication process: "The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature, PubChem ID. Then duplicates are searched"
- [intro] check_names function purpose and usage: "Before the meta-analysis the IDs can be checked using public databases information. The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common"
- [intro] Compound descriptor retrieval with comp.inf parameter: "If you select the option `comp.inf = T` the package will retrieve the PubChem ID from the ID using `webchem`. Results will return the following information: PubChem ID, Molecular Formula, Molecular"
- [intro] Metadata output from identifier harmonization: "Results will return the following information: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank"
- [readme] Integration with downstream meta-analysis workflow: "In this step you will obtain an S4 object with two tables: adapted meta-analysis acces by `amanida_result@stat` [, when] Selecting the option `comp.inf = T` the package need the previous use of"
