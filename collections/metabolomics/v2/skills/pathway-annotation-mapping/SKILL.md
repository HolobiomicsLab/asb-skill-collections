---
name: pathway-annotation-mapping
description: Use when you have a metabolomics dataset with metabolite identifiers in mixed formats (e.g., common names, KEGG accessions, HMDB IDs) and need to assign each metabolite to its canonical pathway(s) before performing pathway-level classification, feature selection, or prognosis modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0602
  tools:
  - Lilikoi v2.0
  - R
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis in R programming environment.
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

# pathway-annotation-mapping

## Summary

Map metabolite identifiers in heterogeneous formats (names, KEGG IDs, HMDB IDs, PubChem IDs) to unified pathway annotations using fuzzy matching against a canonical metabolite database. This skill produces a structured metabolite-pathway table required for downstream pathway-level analysis and prognosis modeling.

## When to use

You have a metabolomics dataset with metabolite identifiers in mixed formats (e.g., common names, KEGG accessions, HMDB IDs) and need to assign each metabolite to its canonical pathway(s) before performing pathway-level classification, feature selection, or prognosis modeling. This is the mandatory normalization step before lilikoi.PDSfun (pathway derangement score computation) or lilikoi.featuresSelection can be applied.

## When NOT to use

- Metabolite identifiers are already mapped to KEGG pathway IDs with 100% confidence — direct use as Metabolite_pathway_table is more efficient.
- Input is already a pathway derangement score (PDS) matrix or a feature-selected pathway matrix — this skill is for identifier-to-pathway conversion only, not for PDS computation or downstream feature selection.
- Metabolite identifiers are in a custom proprietary nomenclature with no mapping to HMDB, KEGG, or PubChem — fuzzy matching may fail to find valid pathway assignments.

## Inputs

- Metabolomics dataset with metabolite identifiers (CSV or R data.frame)
- Metabolite identifier format specifier (string: 'name', 'KEGG', 'HMDB', 'PubChem')
- Lilikoi v2.0 package with bundled ~100k metabolite reference database

## Outputs

- Metabolite_pathway_table (data.frame with columns: metabolite ID, canonical name, pathway assignment)
- Conversion metadata (match confidence, fuzzy match distance if applicable)

## How to apply

Load your metabolomics data using lilikoi.Loaddata() to extract the metabolite identifier column and metadata. Call lilikoi.MetaTOpathway() with the identifier format type (e.g., 'name' for metabolite common names) as the argument. The function matches identifiers against a ~100k canonical metabolite database; when no direct match is found, it applies fuzzy matching to identify the closest matches. The function returns a structured Metabolite_pathway_table with metabolite ID and pathway assignment columns. Verify output by inspecting the head() of the table to confirm all metabolites received pathway assignments and that pathway names are recognized KEGG pathway terms.

## Related tools

- **Lilikoi v2.0** (Hosts the MetaTOpathway function for metabolite identifier conversion and the reference metabolite-pathway database (100k entries)) — https://github.com/lanagarmire/lilikoi2
- **R** (Execution environment for Lilikoi v2.0 and data manipulation (dplyr, data.table))

## Examples

```
dt <- lilikoi.Loaddata(file=system.file("extdata", "plasma_breast_cancer.csv", package = "lilikoi")); convertResults=lilikoi.MetaTOpathway('name'); Metabolite_pathway_table = convertResults$table; head(Metabolite_pathway_table)
```

## Evaluation signals

- All metabolites in the input dataset receive pathway assignments (zero unmapped entries or explicit 'NA' entries flagged and reviewed)
- Pathway names in Metabolite_pathway_table match known KEGG pathway nomenclature (e.g., 'Pyruvate Metabolism', 'Citric Acid Cycle'); spot-check 5–10 rows against KEGG database
- Fuzzy-matched metabolites (distance > threshold) are logged with match confidence scores; inspect these to confirm semantic similarity (e.g., 'pyruvate' matched to 'pyruvic acid')
- Metabolite_pathway_table schema is consistent: no missing columns, no inconsistent data types, metabolite ID column has no duplicates or whitespace artifacts
- Downstream lilikoi.PDSfun() executes without error on Metabolite_pathway_table, indicating pathway annotations are in the expected format

## Limitations

- Fuzzy matching relies on string similarity and may produce false positives for metabolites with similar names but different biochemical roles; manual review of fuzzy matches is recommended.
- The ~100k metabolite reference database is static (version bundled with Lilikoi v2.0); newly discovered metabolites or recently curated HMDB/KEGG entries may not be present.
- One-to-many metabolite-pathway relationships are supported but may complicate downstream pathway feature selection if a metabolite participates in multiple pathways.
- Performance degrades if input dataset contains a high proportion of non-standard or proprietary metabolite identifiers that do not match any of the supported formats (KEGG, HMDB, PubChem, or common names).

## Evidence

- [other] MetaTOpathway function performs ID conversion by matching metabolite standard names against a 100k database, and applies fuzzy matching to find closest matches when no direct hits are found, producing a Metabolite_pathway_table output.: "The MetaTOpathway function performs ID conversion by matching metabolite standard names against a 100k database, and applies fuzzy matching to find closest matches when no direct hits are found,"
- [readme] The README workflow showing MetaTOpathway usage with the 'name' format specifier.: "# Transform the metabolite names to the HMDB ids using Lilikoi MetaTOpathway function
convertResults=lilikoi.MetaTOpathway('name')
Metabolite_pathway_table = convertResults$table"
- [intro] Lilikoi v2.0 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression.: "Lilikoi v2.0 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression."
- [readme] The README example showing the full workflow from data loading through MetaTOpathway to downstream PDSfun.: "# Transform metabolites into pathway using pathtracer algorithm
PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)"
- [readme] The README states the package is a modern comprehensive tool for metabolomics analysis.: "Lilikoi v2 is a modern, comprehensive package to enable metabolomics analysis in R programming environment."
