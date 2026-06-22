---
name: chemical-structure-similarity-matching
description: Use when you have a set of query chemical compounds (as SMILES, names, or ChemMine objects) and a reference library organized into type groups (e.g., Type A–E chemical sets), and you need to assign each query compound to its -matching type based on structural similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - ChemmineR
  - fmcsR
  - webchem
  - R
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- To perform the chemical structure matches and summarize atomic features, uafR taps into an amazing set of cheminformatics packages -- [ChemmineR]
- uafR taps into an amazing set of cheminformatics packages -- [ChemmineR](https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html), [fmcsR]
- uafR taps into an amazing set of cheminformatics packages -- [ChemmineR](https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html), [fmcsR](https://bioconductor.org/packages/release/bioc
- '[fmcsR](https://bioconductor.org/packages/release/bioc/html/fmcsR.html), [webchem](https://cran.r-project.org/web/packages/webchem/index.html)'
- Modern programming languages allow even complex workflows to be automated
- Modern programming languages allow even complex workflows to be automated.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_uafr
    doi: 10.1371/journal.pone.0306202
    title: uafr
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

# chemical-structure-similarity-matching

## Summary

Match query chemical compounds to reference compound type categories using structural similarity scoring via flexmatch common substructure (FMCS) algorithms. This skill identifies best-matching compound classifications when a query set is compared against a restricted type library, returning match scores and compound identifiers for downstream chemical categorization workflows.

## When to use

Apply this skill when you have a set of query chemical compounds (as SMILES, names, or ChemMine objects) and a reference library organized into type groups (e.g., Type A–E chemical sets), and you need to assign each query compound to its best-matching type based on structural similarity. Use it before or after Match.Factor filtering (e.g., Match.Factor ≥ 70–80) to enrich mass spectrometry compound identifications with structural classification. Avoid applying if you are comparing within a single homogeneous set or if you lack a pre-defined reference type library.

## When NOT to use

- Input chemicals are already classified or belong to a single homogeneous type set; use only when multiple non-overlapping type categories exist in the reference library.
- Reference library is undefined, unstructured, or organized only by chemical name without semantic type grouping.
- Query set is empty or contains fewer than 2 chemicals; the skill is designed for batch comparisons across a typed library.

## Inputs

- query_chemicals: character vector of chemical names or identifiers (e.g., c('Linalool', 'Methyl Salicylate', 'Limonene'))
- chem_library: data frame with type-grouped chemicals (wide or long format, columns representing Type A, Type B, etc.)
- input_format: specification of library structure ('wide' for column-based types, or 'long' for tall format)

## Outputs

- best-match table: data frame with columns for query chemical name, assigned type, compound identifier (CMP code or 'No'), and match score
- categorated_result: R data frame object suitable for subsetting and filtering with `exactoThese()`

## How to apply

Load the query chemical list and reference type library (organized as wide or long format data frame) into R. Call the `categorate()` function, passing the query chemical names/identifiers and the type library structure. The function accesses ChemmineR for molecular descriptor computation and fmcsR/webchem for structural matching, returning a best-match table with match scores (typically >0.95 threshold for high-confidence matches) and compound type assignments (e.g., 'CMP1', 'CMP2', or 'No' for no match). Filter the results by match score threshold and optionally subset by Database or FMCS properties (molecular weight, ring count, atom count, charge count) using `exactoThese()` to refine downstream workflows. Validate by confirming that known reference compounds (e.g., ethyl hexanoate) appear with expected type assignments in the output table.

## Related tools

- **ChemmineR** (Provides molecular descriptor extraction and cheminformatics infrastructure for structural comparisons within categorate()) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **fmcsR** (Computes flexmatch common substructure (FMCS) similarity scores for pairwise structural matching within categorate()) — https://bioconductor.org/packages/release/bioc/html/fmcsR.html
- **webchem** (Retrieves chemical property data and external database lookups to support structural matching confidence scoring) — https://cran.r-project.org/web/packages/webchem/index.html
- **R** (Programming environment for automation and orchestration of the categorate() workflow)

## Examples

```
query_chemicals = c('Linalool', 'Methyl Salicylate', 'Limonene'); chem_library = data.frame(cbind(GroupA = c('Guaiacol', 'Ethyl heptanoate'), GroupB = c('Aspirin', 'alpha-Pinene'))); query_categorated = categorate(query_chemicals, chem_library, input_format = 'wide')
```

## Evaluation signals

- Best-match table contains one row per query chemical with non-null type assignment or explicit 'No' entry; no missing rows.
- Match scores in output are numeric, typically ≥0.95 for accepted matches; scores below threshold are documented as unmatched.
- Known reference compounds (e.g., ethyl hexanoate) correctly map to their expected type categories (e.g., 'CMP2' in a specific type) across independent test runs.
- No query chemical is assigned to multiple types in a single run; each receives exactly one best match or 'No' designation.
- Downstream `exactoThese()` subsetting by Database or FMCS properties returns chemical subsets with the correct cardinality and structure.

## Limitations

- Structural matching relies on SMILES or ChemMine-compatible molecular representations; chemicals without valid structures or existing in the library will return 'No match'.
- Match scores and type assignments are sensitive to the reference library composition and type definitions; changing the library may alter assignments for the same query set.
- The match score threshold (>0.95) is empirically tuned; compounds near the threshold boundary may show marginal or inconsistent classification on repeated runs or with library updates.
- Currently tested only on a 4-type set (Type A–E) in the source task; behavior on larger or more complex type hierarchies is not documented.

## Evidence

- [other] The categorate() function, when applied under structural-matching conditions restricted to 4 chemical type sets, produces a best-match table that correctly identifies compound classifications (e.g., CMP2 for ethyl hexanoate).: "produces a best-match table that correctly identifies compound classifications (e.g., CMP2 for ethyl hexanoate)"
- [other] Call categorate() on the query chemicals, passing the restricted library to access structural match data via ChemmineR, fmcsR, and webchem.: "Call categorate() on the query chemicals, passing the restricted library to access structural match data via ChemmineR, fmcsR, and webchem"
- [methods] `categorate()` is an overpowered function that accesses a broad array of categorical data for searched chemicals.: "`categorate()` is an overpowered function that accesses a broad array of categorical data for searched chemicals"
- [methods] uafR taps into an amazing set of cheminformatics packages -- [ChemmineR], [fmcsR], [webchem]: "uafR taps into an amazing set of cheminformatics packages -- [ChemmineR], [fmcsR], [webchem]"
- [readme] query_categorated = categorate(query_chemicals, chem_library, input_format = 'wide'): "query_categorated = categorate(query_chemicals, chem_library, input_format = 'wide')"
- [methods] a useful approach for narrowing the search chemicals for `categorate()` and/or `mzExacto()` is to first subset by match factor: "a useful approach for narrowing the search chemicals for `categorate()` and/or `mzExacto()` is to first subset by match factor"
