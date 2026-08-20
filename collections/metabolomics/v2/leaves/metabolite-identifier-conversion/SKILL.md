---
name: metabolite-identifier-conversion
description: Use when your metabolomics dataset contains metabolite identifiers in
  multiple formats (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Lilikoi v2.0
  - R
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification,
  in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis
  in R programming environment.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lilikoi_v2_0_cq
    doi: 10.1093/gigascience/giaa162
    title: Lilikoi V2.0
  dedup_kept_from: coll_lilikoi_v2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa162
  all_source_dois:
  - 10.1093/gigascience/giaa162
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-identifier-conversion

## Summary

Convert metabolite identifiers in heterogeneous formats (names, KEGG IDs, HMDB IDs, PubChem IDs) into a unified metabolite-pathway mapping table using Lilikoi's MetaTOpathway function. This skill is essential when ingesting metabolomics datasets with mixed or non-canonical metabolite naming schemes before pathway analysis.

## When to use

Your metabolomics dataset contains metabolite identifiers in multiple formats (e.g., metabolite names, KEGG IDs, HMDB IDs, PubChem IDs) and you need to map them to canonical identifiers and their associated KEGG/pathway annotations for downstream pathway analysis, classification, or visualization. This is the first transformation step after loading raw metabolite data.

## When NOT to use

- Your metabolite identifiers are already in a standardized canonical format (e.g., all HMDB IDs) and pre-mapped to pathways; conversion would be redundant.
- Your analysis does not require pathway annotation or KEGG membership; you only need metabolite identity standardization for statistical analysis.
- The metabolite names in your dataset are non-standard abbreviations or custom codes not resolvable against the 100k reference database.

## Inputs

- metabolomics dataset with metabolite identifiers (CSV format)
- metabolite identifier format specification (string: 'name', 'KEGG_ID', 'HMDB_ID', or 'PubChem_ID')

## Outputs

- Metabolite_pathway_table (data frame with metabolite ID and KEGG pathway assignment columns)

## How to apply

Load your metabolomics data (e.g., plasma_breast_cancer.csv with metabolite IDs and identifiers) into R. Call lilikoi.MetaTOpathway() with the identifier format as a parameter (e.g., 'name' for metabolite names). The function matches metabolite standard names against a 100k reference database using exact matching; when no direct hit is found, it applies fuzzy matching to identify the closest matching canonical metabolite name. The output is a Metabolite_pathway_table with columns for metabolite ID and assigned KEGG pathway annotations. Inspect the resulting table for the proportion of successfully converted metabolites and any unmatched entries, which should be reviewed for data quality or manual curation.

## Related tools

- **Lilikoi v2.0** (Performs metabolite identifier conversion via MetaTOpathway function using fuzzy matching against 100k reference database) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment for loading data, executing lilikoi functions, and exporting Metabolite_pathway_table)

## Examples

```
convertResults=lilikoi.MetaTOpathway('name'); Metabolite_pathway_table = convertResults$table; head(Metabolite_pathway_table)
```

## Evaluation signals

- Conversion success rate: proportion of input metabolites matched to canonical identifiers (target: >90% for well-characterized datasets like plasma metabolomics)
- No duplicate entries in Metabolite_pathway_table; each metabolite ID maps to exactly one pathway or a consistent set of pathways
- Spot-check: verify that known metabolites (e.g., glucose, lactate, pyruvate) are correctly assigned to expected pathways
- Presence of NA or unmapped values should be documented and reviewed; if >10%, investigate data quality or format specification mismatch
- Output table schema invariant: contains at minimum 'Metabolite_ID' and 'Pathway' columns with no structural nulls in key fields

## Limitations

- Fuzzy matching relies on string similarity; highly abbreviated or proprietary metabolite names may not resolve correctly.
- The reference database contains ~100k metabolites; rare or recently discovered metabolites may not be present, resulting in unmapped entries.
- Metabolites with multiple biochemical roles may be assigned to a single dominant pathway; pathway ambiguity is not flagged.
- No changelog available to track updates to the reference database or fuzzy matching algorithm across Lilikoi versions.

## Evidence

- [other] The MetaTOpathway function performs ID conversion by matching metabolite standard names against a 100k database, and applies fuzzy matching to find closest matches when no direct hits are found: "The MetaTOpathway function performs ID conversion by matching metabolite standard names against a 100k database, and applies fuzzy matching to find closest matches when no direct hits are found,"
- [readme] convertResults=lilikoi.MetaTOpathway('name'); Metabolite_pathway_table = convertResults$table: "# Transform the metabolite names to the HMDB ids using Lilikoi MetaTOpathway function
convertResults=lilikoi.MetaTOpathway('name')
Metabolite_pathway_table = convertResults$table"
- [intro] Lilikoi v2 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression: "Lilikoi v2.0 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression."
- [readme] dt <- lilikoi.Loaddata(file=system.file("extdata", "plasma_breast_cancer.csv", package = "lilikoi")): "dt <- lilikoi.Loaddata(file=system.file("extdata", "plasma_breast_cancer.csv", package = "lilikoi"))"
