---
name: pubchem-cross-reference-lookup
description: 'Use when you have metabolite or compound identifiers in mixed formats (chemical name, InChI, InChIKey, SMILES) across multiple studies or datasets and need to: (1) unify them to a single canonical identifier (PubChem ID) for deduplication, (2) detect and resolve duplicate entries that differ only.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0533
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0602
  tools:
  - R
  - webchem
  - PubChem
  - amanida
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted meta-analysis in R
- the package will retrieve the PubChem ID from the ID using `webchem`
- all ids are converted to a unique one, in this case the PubChem ID
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pubchem-cross-reference-lookup

## Summary

Convert heterogeneous chemical identifiers (chemical names, InChI, InChIKey, SMILES) into a unified PubChem ID and retrieve standardized compound descriptors. This skill enables harmonization of metabolite nomenclature across multi-study datasets, essential for meta-analysis where identifier format inconsistency would otherwise prevent duplicate detection and comparison.

## When to use

Apply this skill when you have metabolite or compound identifiers in mixed formats (chemical name, InChI, InChIKey, SMILES) across multiple studies or datasets and need to: (1) unify them to a single canonical identifier (PubChem ID) for deduplication, (2) detect and resolve duplicate entries that differ only in identifier format, or (3) retrieve standardized compound properties (Molecular Formula, Molecular Weight, ChEBI, KEGG, HMDB, DrugBank cross-references) to enrich metadata before quantitative meta-analysis.

## When NOT to use

- Input identifiers are already unified to a single format (e.g., all PubChem IDs or all SMILES strings) with no duplicates detected — direct deduplication by exact string match is more efficient.
- Your dataset consists only of gene or protein identifiers, not chemical compounds — PubChem is a chemical structure database and will not resolve biological macromolecule identifiers.
- Internet connectivity to PubChem is unavailable or blocked; the webchem query step will fail without network access to the PubChem REST API.

## Inputs

- Data frame or table with metabolite identifiers in any of: chemical name, InChI, InChIKey, SMILES format
- Associated metadata columns (p-value, fold-change, study size N, bibliographic reference)
- File path to input dataset (csv, xls/xlsx, or txt)

## Outputs

- Harmonized metabolite table with PubChem ID as canonical identifier
- Deduplicated metabolite list (one record per unique PubChem ID)
- Optionally: enriched compound descriptor table (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank)

## How to apply

Load your metabolite table (with columns for identifier, p-value, fold-change, study size N, and reference) using the amanida_read function in R, specifying mode='quan' or 'qual'. Pass the resulting data frame to the check_names function, which invokes the webchem R package to query PubChem for each identifier format, returning the corresponding PubChem ID and optionally retrieving associated descriptors (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank). The function flags duplicate PubChem IDs across the full dataset; retain the first occurrence of each unique PubChem ID and remove redundant entries. Set comp.inf=TRUE in compute_amanida if you want to combine this harmonization with downstream meta-analysis in a single pipeline.

## Related tools

- **webchem** (R package that queries PubChem REST API to convert chemical identifiers (name, InChI, InChIKey, SMILES) to PubChem ID and retrieve compound metadata)
- **amanida** (R package providing check_names and compute_amanida functions to orchestrate identifier harmonization, duplicate detection, and subsequent weighted meta-analysis) — https://github.com/mariallr/amanida
- **PubChem** (Public chemistry database and REST API queried by webchem to standardize identifiers and retrieve compound descriptors) — https://pubchem.ncbi.nlm.nih.gov

## Examples

```
datafile <- amanida_read('metabolites.csv', mode='quan', coln=c('Compound Name', 'P-value', 'Fold-change', 'N total', 'References'), separator=';'); datafile_harmonized <- check_names(datafile)
```

## Evaluation signals

- All input identifiers are successfully mapped to a non-null PubChem ID; rows with failed lookups are logged.
- Duplicate detection: verify that identical PubChem IDs resulting from different input formats are flagged and consolidated to a single record.
- Retrieved compound descriptors (Molecular Formula, Molecular Weight, InChIKey, cross-references) match expected values for known reference compounds (e.g., glucose, alanine) when manually validated against PubChem web interface.
- Row count decreases from input to output proportional to the number of duplicates detected; no metabolites are lost unless they failed the PubChem lookup.
- The final harmonized table has no missing PubChem ID values in the canonical identifier column; all retained rows are paired with valid cross-references to KEGG, ChEBI, HMDB, or Drugbank.

## Limitations

- Identifier lookup success depends on exact string matching or PubChem's internal fuzzy-matching logic; minor typos, non-standard chemical nomenclature, or misspelled names may result in failed or incorrect lookups.
- PubChem does not cover all metabolites, especially rare or newly synthesized compounds; identifiers not in PubChem will be unresolved and excluded from the harmonized dataset.
- Cross-reference completeness varies by compound: not all PubChem IDs have entries in all secondary databases (KEGG, ChEBI, HMDB, Drugbank), so enriched descriptors may be incomplete.
- The method assumes that distinct identifiers pointing to the same PubChem ID represent the same metabolite; isomers or stereoisomers with identical PubChem IDs but different chemical significance in context will be incorrectly merged.

## Evidence

- [other] The identifier harmonization is implemented via the check_names function, which searches chemical identifiers in PubChem format (chemical name, InChI, InChIKey, SMILES) using the webchem package to convert them to PubChem ID: "The identifier harmonization is implemented via the check_names function, which searches chemical identifiers in PubChem format (chemical name, InChI, InChIKey, SMILES) using the webchem package to"
- [intro] The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature, PubChem ID. Then duplicates are searched: "The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature, PubChem ID. Then duplicates are searched"
- [readme] If you select the option `comp.inf = T` the package will retrieve the PubChem ID from the ID using `webchem`. Results will return the following information: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank.: "If you select the option `comp.inf = T` the package will retrieve the PubChem ID from the ID using `webchem`. Results will return the following information: PubChem ID, Molecular Formula, Molecular"
- [other] Search for and identify duplicate entries by comparing retrieved PubChem IDs across the full dataset. Retain unique PubChem IDs and remove redundant entries, preserving one record per unique metabolite.: "Search for and identify duplicate entries by comparing retrieved PubChem IDs across the full dataset. Retain unique PubChem IDs and remove redundant entries, preserving one record per unique"
- [readme] Before the meta-analysis the IDs can be checked using public databases information. The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature using `webchem` package.: "Before the meta-analysis the IDs can be checked using public databases information. The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common"
