---
name: multi-format-identifier-harmonization
description: Use when you have metabolomics datasets from multiple studies that use different chemical identifier formats (names, InChI, InChIKey, SMILES), and you need to merge them for meta-analysis or cross-study comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - R
  - webchem
  - amanida
  - PubChem
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted meta-analysis in R
- the package will retrieve the PubChem ID from the ID using `webchem`
- This vignette illustrates `Amanida` R package, which contains a collection of functions for computing a weighted meta-analysis
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

# Multi-Format Identifier Harmonization

## Summary

Converts heterogeneous chemical identifiers (chemical names, InChI, InChIKey, SMILES) into a unified PubChem ID nomenclature and detects duplicate entries across metabolomics datasets. This standardization enables reliable comparison and meta-analysis of results from multiple independent studies.

## When to use

Apply this skill when you have metabolomics datasets from multiple studies that use different chemical identifier formats (names, InChI, InChIKey, SMILES), and you need to merge them for meta-analysis or cross-study comparison. Specifically, use it before computing weighted meta-analysis to ensure that the same metabolite is not counted multiple times under different identifier representations.

## When NOT to use

- Input identifiers are already standardized to a single namespace (e.g., all already PubChem IDs or all already KEGG accessions) — direct deduplication may be simpler.
- Chemical identifiers are proprietary or from closed databases not indexed by PubChem (e.g., in-house compound codes) — PubChem lookup will fail.
- Network connectivity to PubChem or webchem services is unavailable — the function requires live database queries.

## Inputs

- Metabolite identifier table (csv/txt/xls/xlsx) with columns: identifier (chemical name, InChI, InChIKey, or SMILES), p-value, fold-change, study size (N), reference
- R data frame loaded via amanida_read() function with mode='quan' or mode='qual'

## Outputs

- Harmonized metabolite table with PubChem ID as canonical identifier
- Duplicate detection report (identifiers mapping to same PubChem ID)
- Extended compound information table (if comp.inf=TRUE): PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank identifiers

## How to apply

Load your metabolite dataset (csv, xls/xlsx, or txt format) containing identifiers in any of these formats: chemical name, InChI, InChIKey, or SMILES. Use the `check_names()` function in the amanida R package, which queries PubChem via the webchem package to convert each identifier to its corresponding PubChem ID. The function then compares retrieved PubChem IDs across the full dataset to identify and flag duplicate entries (same metabolite under different input identifiers). Retain only unique PubChem IDs, preserving one canonical record per metabolite. Optionally enable `comp.inf = TRUE` to retrieve additional standardized descriptors (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank) from PubChem to enrich the harmonized table.

## Related tools

- **webchem** (R package that queries PubChem API to retrieve PubChem IDs and compound metadata from chemical identifiers (names, InChI, InChIKey, SMILES))
- **amanida** (R package containing check_names() function for identifier harmonization and compute_amanida() for subsequent weighted meta-analysis) — https://github.com/mariallr/amanida
- **PubChem** (Public chemical compound database (upstream data source) providing canonical PubChem IDs and cross-referenced identifiers (KEGG, ChEBI, HMDB, Drugbank)) — https://pubchem.ncbi.nlm.nih.gov/

## Examples

```
library(amanida)
coln = c("Compound Name", "P-value", "Fold-change", "N total", "References")
input_file <- system.file("extdata", "dataset2.csv", package = "amanida")
datafile <- amanida_read(input_file, mode = "quan", coln, separator=";")
datafile <- check_names(datafile)
```

## Evaluation signals

- All input identifiers successfully resolved to PubChem IDs with no null/NA values (except genuinely unmatchable identifiers, which should be logged separately).
- Duplicate detection: verify that metabolites with the same PubChem ID but different input identifier formats are correctly flagged and consolidated to a single record.
- Cross-reference validation: randomly sample 5–10 harmonized records and manually verify on PubChem that the assigned PubChem ID, Molecular Formula, and InChIKey match the original compound.
- Dataset size check: harmonized table row count ≤ original table row count (should equal original if no duplicates exist; should be less if duplicates were merged).
- Schema compliance: output table includes mandatory columns (PubChem ID, original identifier, reference) plus optional columns if comp.inf=TRUE (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank).

## Limitations

- PubChem coverage is not exhaustive; rare or very recently synthesized metabolites may not have a PubChem entry, causing lookup failure. These identifiers must be handled separately (e.g., manual curation or retention as unmapped entries).
- Identifier format ambiguity: a chemical name like 'glucose' may match multiple PubChem entries (e.g., different stereoisomers or salt forms). The webchem query may return the first match or require disambiguation; verify results in ambiguous cases.
- Network-dependent: the function requires live internet connectivity to PubChem; offline or air-gapped environments cannot use this skill without local database mirroring.
- InChI and SMILES are sensitive to formatting variations (whitespace, stereochemistry notation); malformed or non-standard representations in the input may fail to match even if the chemical is in PubChem.
- Missing data handling: the amanida_read() function ignores rows with missing identifier values during import, so sparse or incomplete identifier columns will silently lose data.

## Evidence

- [intro] check_names_function_and_purpose: "The identifier harmonization is implemented via the check_names function, which searches chemical identifiers in PubChem format (chemical name, InChI, InChIKey, SMILES) using the webchem package to"
- [intro] harmonization_workflow_steps: "Query PubChem via the webchem R package to convert each identifier format to a corresponding PubChem ID. 3. Search for and identify duplicate entries by comparing retrieved PubChem IDs across the"
- [intro] optional_compound_descriptors: "If you select the option `comp.inf = T` the package will retrieve the PubChem ID from the ID using `webchem`. Results will return the following information: PubChem ID, Molecular Formula, Molecular"
- [readme] supported_identifier_formats: "The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature using `webchem` package."
- [readme] check_names_usage_in_amanida: "Before the meta-analysis the IDs can be checked using public databases information. The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common"
- [intro] missing_data_filter: "missing data is ignored"
