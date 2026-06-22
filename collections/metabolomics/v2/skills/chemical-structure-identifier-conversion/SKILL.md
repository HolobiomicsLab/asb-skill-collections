---
name: chemical-structure-identifier-conversion
description: Use when when you have a metabolomic dataset with heterogeneous chemical identifiers (names, InChI strings, InChIKeys, or SMILES) and need a single canonical identifier per metabolite to enable comparison across studies, detect redundant entries, or link to external chemical databases for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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
---

# Chemical Structure Identifier Conversion

## Summary

Convert multiple chemical identifier formats (chemical name, InChI, InChIKey, SMILES) into a standardized PubChem ID nomenclature, detect duplicates, and optionally retrieve enriched metabolite descriptors (Molecular Formula, Molecular Weight, cross-database IDs) from public repositories.

## When to use

When you have a metabolomic dataset with heterogeneous chemical identifiers (names, InChI strings, InChIKeys, or SMILES) and need a single canonical identifier per metabolite to enable comparison across studies, detect redundant entries, or link to external chemical databases for enrichment.

## When NOT to use

- Identifiers are already standardized to a single format (e.g., all are PubChem IDs or all are KEGG compound codes) and no cross-database linking is needed.
- Input contains only qualitative trend data without identifiers that can be resolved to chemical structures (e.g., free-text compound descriptions or proprietary internal codes with no public database entry).
- PubChem is temporarily unavailable or network access is restricted; the webchem query step will fail and cannot be retried without external connectivity.

## Inputs

- Metabolite identifier table (CSV, XLS, XLSX, or TXT format)
- Columns: identifier (chemical name, InChI, InChIKey, or SMILES), p-value, fold-change, study size (N), reference

## Outputs

- Harmonized metabolite table with PubChem ID as canonical identifier
- Duplicate flag or removal log
- Enriched compound descriptor table (if comp.inf=TRUE): PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank cross-references

## How to apply

Load metabolite identifiers from a CSV/XLS/XLSX/TXT table using amanida_read with columns in order: identifier, p-value (for quantitative) or trend (for qualitative), fold-change/reference, study size, and reference. Call check_names to query each identifier format against PubChem via the webchem R package, which returns the corresponding PubChem ID. Compare PubChem IDs across the full dataset to identify and flag duplicates—retain one record per unique PubChem ID and remove redundant entries. Optionally set comp.inf=TRUE to retrieve additional descriptors (Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank) for each harmonized compound. The harmonized output table uses PubChem ID as the canonical identifier and serves as the input for downstream meta-analysis.

## Related tools

- **amanida** (R package providing check_names and amanida_read functions for identifier harmonization and metabolite merging) — https://github.com/mariallr/amanida
- **webchem** (R package used by check_names to query PubChem and convert chemical identifiers to PubChem IDs)
- **PubChem** (Public chemical database queried via webchem to resolve identifiers and retrieve compound descriptors)

## Examples

```
datafile <- amanida_read("compounds.csv", mode="quan", c("Compound Name", "P-value", "Fold-change", "N total", "References"), separator=";"); datafile <- check_names(datafile, comp.inf=TRUE)
```

## Evaluation signals

- All input identifiers (name, InChI, InChIKey, SMILES) are mapped to a valid PubChem ID; no unmapped identifiers remain unless they genuinely have no PubChem entry.
- Duplicate PubChem IDs are identified and flagged; only one record per unique PubChem ID is retained in the output.
- Harmonized output table has no missing PubChem ID values in the canonical identifier column.
- If comp.inf=TRUE, enriched descriptor columns (Molecular Formula, Molecular Weight, cross-database IDs) are populated and consistent with PubChem records for spot-checked compounds.
- Row count decreases after deduplication; the number of unique PubChem IDs equals the final output table row count.

## Limitations

- Identifiers not present in PubChem (e.g., novel or proprietary compounds, metabolites with incomplete chemical characterization) cannot be resolved and must be manually curated or excluded.
- Query success depends on internet connectivity and PubChem availability; transient network failures or service downtime will interrupt conversion.
- Ambiguous or misspelled chemical names may resolve to incorrect PubChem IDs; manual verification of results is recommended, especially for rare or structurally similar compounds.
- The webchem package may return multiple matches for a single identifier; the check_names function's behavior in resolving such ambiguities is not fully specified in the documentation.

## Evidence

- [other] The identifier harmonization is implemented via the check_names function, which searches chemical identifiers in PubChem format (chemical name, InChI, InChIKey, SMILES) using the webchem package to convert them to PubChem ID, then checks for duplicates.: "The identifier harmonization is implemented via the check_names function, which searches chemical identifiers in PubChem format (chemical name, InChI, InChIKey, SMILES) using the webchem package to"
- [readme] The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature, PubChem ID. Then duplicates are searched: "The IDs in format chemical name, InChI, InChIKey, and SMILES are searched in PubChem to transform all into a common nomenclature using `webchem` package."
- [readme] Selecting the option `comp.inf = T` the package need the previous use of `check_names`. Then using PubChem ID duplicates are checked. Results are returned including the following information: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank.: "Results are returned including the following information: PubChem ID, Molecular Formula, Molecular Weight, SMILES, InChIKey, KEGG, ChEBI, HMDB, Drugbank."
- [other] Load metabolite identifiers (chemical names, InChI, InChIKey, SMILES) from input table using amanida_read function in R. Query PubChem via the webchem R package to convert each identifier format to a corresponding PubChem ID.: "Load metabolite identifiers (chemical names, InChI, InChIKey, SMILES) from input table using amanida_read function in R. Query PubChem via the webchem R package to convert each identifier format to a"
- [other] Search for and identify duplicate entries by comparing retrieved PubChem IDs across the full dataset. Retain unique PubChem IDs and remove redundant entries, preserving one record per unique metabolite.: "Search for and identify duplicate entries by comparing retrieved PubChem IDs across the full dataset. Retain unique PubChem IDs and remove redundant entries, preserving one record per unique"
