---
name: duplicate-record-detection-and-deduplication
description: Use when when merging metabolomic data from multiple studies, you have
  compound identifiers in heterogeneous formats (chemical names, InChI, InChIKey,
  SMILES) and need to detect whether the same compound appears under different representations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  tools:
  - R
  - webchem
  - amanida
  - PubChem
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted
  meta-analysis in R
- the package will retrieve the PubChem ID from the ID using `webchem`
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

# Duplicate Record Detection and Deduplication

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify and remove duplicate metabolite records in a merged dataset by standardizing compound identifiers to a canonical nomenclature (PubChem ID) and comparing them across all entries. This skill ensures each unique metabolite is represented only once before meta-analysis.

## When to use

When merging metabolomic data from multiple studies, you have compound identifiers in heterogeneous formats (chemical names, InChI, InChIKey, SMILES) and need to detect whether the same compound appears under different representations. Apply this skill after data import but before quantitative or qualitative meta-analysis to prevent inflated or conflicting results from the same metabolite.

## When NOT to use

- Input identifiers are already in a single, standardized format (e.g., all entries already use PubChem IDs with no conflicts)—duplicate detection is unnecessary.
- Compounds of interest are not present in PubChem (e.g., novel synthetic compounds, non-standard modifications)—webchem queries will fail or return no match.
- Internet connectivity to PubChem is unavailable or PubChem service is down—identifier harmonization cannot be completed.

## Inputs

- Metabolite identifier table (csv, xls/xlsx, or txt format)
- Columns: compound identifier (chemical name, InChI, InChIKey, or SMILES), p-value, fold-change, study size (N), reference

## Outputs

- Deduplicated metabolite table with harmonized PubChem IDs
- Compound descriptor table (optional) including Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank

## How to apply

Use the amanida R package's `check_names` function to query PubChem via the webchem package, converting all identifier formats (chemical name, InChI, InChIKey, SMILES) to a unique PubChem ID. The function searches each identifier in PubChem and retrieves the canonical PubChem ID. After harmonization, compare PubChem IDs across the full dataset to identify duplicate entries—multiple records sharing the same PubChem ID represent the same metabolite. Retain one record per unique PubChem ID and remove redundant entries. Optionally, retrieve and validate additional compound descriptors (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank) to cross-verify identity. Output a deduplicated identifier table with PubChem ID as the canonical identifier.

## Related tools

- **amanida** (R package providing the check_names function for identifier harmonization and duplicate detection via PubChem queries) — https://github.com/mariallr/amanida
- **webchem** (R package that interfaces with PubChem to retrieve PubChem IDs and compound descriptors from heterogeneous identifier formats)
- **PubChem** (Public chemical database queried via webchem to standardize compound identifiers and retrieve canonical nomenclature and descriptors)

## Examples

```
datafile <- amanida_read('dataset.csv', mode = 'quan', c('Compound Name', 'P-value', 'Fold-change', 'N total', 'References'), separator=','); datafile_clean <- check_names(datafile)
```

## Evaluation signals

- All input identifiers are successfully converted to PubChem IDs; check that no missing values or failed queries remain in the harmonized output.
- The number of unique PubChem IDs is less than or equal to the number of input records, confirming that duplicate detection identified zero or more duplicates.
- Retrieved compound descriptors (Molecular Formula, Molecular Weight, SMILES, InChIKey) are consistent with the PubChem ID assigned; verify by spot-checking a sample of records.
- No two records in the final deduplicated table share the same PubChem ID; this is the primary invariant for deduplication correctness.
- If comp.inf = TRUE, the retrieved KEGG, ChEBI, HMDB, and Drugbank IDs are non-empty for known drugs/metabolites and empty or NA for obscure compounds, indicating valid cross-database retrieval.

## Limitations

- Identifiers not present in PubChem (e.g., proprietary or novel compounds) cannot be harmonized and are skipped or fail silently, leading to loss of data.
- Identical or near-identical compounds with distinct PubChem IDs (e.g., stereoisomers, different salt forms) are treated as separate metabolites; manual curation may be needed.
- Spelling errors, abbreviations, or non-standard nomenclature in input identifiers may not match PubChem entries, resulting in failed queries and duplicates remaining undetected.
- PubChem service latency or downtime can halt the harmonization workflow; no offline fallback is available.
- Webchem queries are rate-limited and time-consuming for large datasets (thousands of records).

## Evidence

- [other] The identifier harmonization is implemented via the check_names function, which searches chemical identifiers in PubChem format (chemical name, InChI, InChIKey, SMILES) using the webchem package to convert them to PubChem ID, then checks for duplicates.: "The identifier harmonization is implemented via the check_names function, which searches chemical identifiers in PubChem format (chemical name, InChI, InChIKey, SMILES) using the webchem package to"
- [intro] The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature, PubChem ID. Then duplicates are searched.: "The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature, PubChem ID. Then duplicates are searched."
- [other] Search for and identify duplicate entries by comparing retrieved PubChem IDs across the full dataset.: "Search for and identify duplicate entries by comparing retrieved PubChem IDs across the full dataset."
- [intro] If you select the option `comp.inf = T` the package will retrieve the PubChem ID from the ID using `webchem`. Results will return the following information: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank.: "If you select the option `comp.inf = T` the package will retrieve the PubChem ID from the ID using `webchem`. Results will return the following information: PubChem ID, Molecular Formula, Molecular"
- [other] Retain unique PubChem IDs and remove redundant entries, preserving one record per unique metabolite.: "Retain unique PubChem IDs and remove redundant entries, preserving one record per unique metabolite."
- [readme] Before the meta-analysis the IDs can be checked using public databases information. The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature using `webchem` package.: "Before the meta-analysis the IDs can be checked using public databases information. The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common"
- [readme] Selecting the option `comp.inf = T` the package need the previous use of `check_names`. Then using PubChem ID duplicates are checked.: "Selecting the option `comp.inf = T` the package need the previous use of `check_names`. Then using PubChem ID duplicates are checked."
