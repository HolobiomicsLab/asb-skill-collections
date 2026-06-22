---
name: metabolite-pathway-association-mapping
description: Use when you have a list of metabolite names or identifiers detected in your samples and need to assign them to known metabolic pathways before computing pathway dysregulation scores, performing pathway-level machine learning, or conducting metabolite-pathway regression analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
  tools:
  - Lilikoi v2.0
  - R
  - HMDB (Human Metabolome Database)
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

# metabolite-pathway-association-mapping

## Summary

Transform individual metabolite identifiers (names or masses) into a standardized metabolite-pathway association table that maps each metabolite to one or more canonical metabolic pathways. This is a prerequisite step for pathway-level analysis in personalized metabolomics studies.

## When to use

You have a list of metabolite names or identifiers detected in your samples and need to assign them to known metabolic pathways before computing pathway dysregulation scores, performing pathway-level machine learning, or conducting metabolite-pathway regression analysis.

## When NOT to use

- Your metabolites are already pre-mapped to pathways in a curated database and require no conversion.
- You are working with a non-standard organism or custom metabolite nomenclature not covered by Lilikoi's embedded or linked databases.
- Your analysis goal is sample-level classification or prognosis without pathway-level aggregation; metabolite-level features may suffice.

## Inputs

- List or vector of metabolite names (string identifiers)
- Sample metabolite abundance data (optional, for validation context)

## Outputs

- Metabolite-pathway association table (rows: metabolites; columns: pathway assignments)
- Standardized metabolite identifiers (e.g., HMDB IDs)

## How to apply

Use Lilikoi's lilikoi.MetaTOpathway function to convert metabolite names to standardized identifiers (such as HMDB IDs) and retrieve their pathway assignments from a curated metabolite-pathway database. The function outputs a table with metabolite identifiers as rows and pathway annotations as columns (or a lookup structure). This association table becomes the reference used downstream by lilikoi.PDSfun (for dysregulation scoring), lilikoi.meta_path (for regression), and lilikoi.KEGGplot (for visualization). The conversion ensures consistency across the analysis pipeline and enables aggregation of metabolite-level measurements into pathway-level features.

## Related tools

- **Lilikoi v2.0** (R package providing lilikoi.MetaTOpathway function for metabolite name-to-pathway conversion and lilikoi.PDSfun for downstream pathway dysregulation scoring) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment in which Lilikoi v2.0 executes the metabolite-pathway mapping workflow)
- **HMDB (Human Metabolome Database)** (Referenced database providing standardized metabolite identifiers and pathway annotations used by lilikoi.MetaTOpathway)

## Examples

```
convertResults=lilikoi.MetaTOpathway('name'); Metabolite_pathway_table = convertResults$table; head(Metabolite_pathway_table)
```

## Evaluation signals

- Output table has no null or unmapped metabolites; all input metabolite names resolve to standardized identifiers (e.g., HMDB IDs).
- Pathway annotations are non-empty for >95% of metabolites; the table is sparse but complete (no column of all zeros).
- Downstream lilikoi.PDSfun executes without errors, confirming that the table structure and metabolite identifiers are compatible.
- Spot-check: manually verify that 2–3 known metabolites (e.g., glucose, pyruvate, lactate) are assigned to expected pathways (e.g., Glycolysis, TCA cycle).
- Table dimensions are consistent with input metabolite count and the expected size of the organism's metabolic network (e.g., hundreds of metabolites × dozens of pathways for human data).

## Limitations

- Lilikoi's metabolite name conversion is limited to metabolites in curated pathway databases (primarily human metabolism); rare, novel, or organism-specific metabolites may not be mapped.
- Metabolite name ambiguity (e.g., common chemical names vs. IUPAC nomenclature) can lead to incorrect or missed mappings; standardized nomenclature (e.g., HMDB IDs) is recommended as input.
- The association table is static at the time of analysis; updates to pathway annotations or database content do not propagate automatically.

## Evidence

- [readme] Transform the metabolite names to the HMDB ids using Lilikoi MetaTOpathway function: "Transform the metabolite names to the HMDB ids using Lilikoi MetaTOpathway function"
- [other] For each pathway, extract the subset of metabolites assigned to that pathway.: "For each pathway, extract the subset of metabolites assigned to that pathway."
- [intro] Lilikoi v2 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression: "Lilikoi v2 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression."
- [other] Organize scores into a matrix with samples as rows and pathways as columns, generating the PDSmatrix output.: "Organize scores into a matrix with samples as rows and pathways as columns"
