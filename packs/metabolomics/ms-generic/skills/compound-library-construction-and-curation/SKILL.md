---
name: compound-library-construction-and-curation
description: Use when when you have a set of query chemicals (e.g., ethyl hexanoate, methyl salicylate, octanal, undecane) and need to evaluate them against reference compound categories, or when you want to restrict structural matching to specific compound type sets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
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

# compound-library-construction-and-curation

## Summary

Assemble and organize chemical reference libraries (e.g., GroupA, GroupB, or restricted type sets) as data structures for downstream structural matching and categorical enrichment. This skill ensures that query chemicals can be accurately matched against well-curated compound sets using cheminformatics tools.

## When to use

When you have a set of query chemicals (e.g., ethyl hexanoate, methyl salicylate, octanal, undecane) and need to evaluate them against reference compound categories, or when you want to restrict structural matching to specific compound type sets (e.g., Type A–E chemical sets) rather than uncontrolled libraries. Use this skill before calling categorate() or mzExacto() to ensure the reference library is correctly formatted and semantically organized.

## When NOT to use

- If your reference library is already pre-matched and indexed externally (e.g., linked to a public database like PubChem or KEGG without need for local curation).
- If you are only interested in mass spectrometry peak matching without structural classification; use mzExacto() directly on unsorted input instead.
- If your query chemicals are already fully annotated with database identifiers (e.g., CAS numbers, InChI keys) and do not require structural similarity matching.

## Inputs

- list of query chemical names (character vector or from CSV Compound.Name column)
- reference compound groups (named character vectors, e.g., GroupA, GroupB)
- compound type sets (Type A–E chemical sets or equivalent restricted library)
- input data frame with columns: Compound.Name, Match.Factor (optional for pre-filtering)

## Outputs

- structured reference library data frame (wide format with group/type columns)
- best-match table showing query chemical name, matched type/group, and compound identifier (CMP1, CMP2, etc., or 'No' for no match)
- structural match scores (>0.95 threshold for reliable matches)
- curated query_chemicals vector ready for downstream analysis via exactoThese() or mzExacto()

## How to apply

Structure your reference compounds into named groups (e.g., GroupA, GroupB) and combine them into a data frame with `input_format = 'wide'` for use with the categorate() function. Load both the query chemical list and the restricted type library as R data structures. Ensure library columns correspond to chemical type categories and contain verified compound identifiers or names. Pass the curated library to categorate() along with your query chemicals; the function will then perform structural matching via ChemmineR and fmcsR to return a best-match table. Verify that match scores exceed 0.95 for reliable classifications and that output identifiers (e.g., 'CMP1', 'CMP2', 'No match') are consistent with your library schema.

## Related tools

- **ChemmineR** (Provides structural matching and cheminformatics data access for compound classification within the library) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **fmcsR** (Computes flexible maximum common substructure (FMCS) matches to calculate structural similarity scores between query and library compounds) — https://bioconductor.org/packages/release/bioc/html/fmcsR.html
- **webchem** (Retrieves and enriches chemical metadata (names, properties, database identifiers) for library compounds) — https://cran.r-project.org/web/packages/webchem/index.html
- **R** (Data frame construction, library organization, and automation of workflow)

## Examples

```
query_chemicals = c("Linalool", "Methyl Salicylate", "Limonene", "alpha-Thujene"); GroupA = c("Guaiacol", "Tridecane", "Ethyl heptanoate", "Caffeine"); GroupB = c("2-Aminothiazole", "Aspirin", "Octanoic acid", "alpha-Pinene", "Toluene"); chem_library = data.frame(cbind(GroupA, GroupB)); query_categorated = categorate(query_chemicals, chem_library, input_format = "wide")
```

## Evaluation signals

- Best-match table returns compound identifiers (CMP1, CMP2, etc.) for all query chemicals; 'No' entries indicate compounds without matches above the 0.95 score threshold.
- Structural match scores for high-confidence matches (e.g., ethyl hexanoate → CMP2) are ≥0.95 and consistent across repeated runs.
- Library data frame schema validates: correct column names (group/type labels), no missing values in reference compound names, and wide format compatible with categorate().
- Query chemical names are normalized (case, whitespace, synonym resolution) and successfully resolve to library entries or return explicit 'No match' rather than errors.
- Downstream exactoThese() and mzExacto() calls execute without data type mismatches or missing column errors, confirming library structure is consumable by downstream functions.

## Limitations

- Structural matching is restricted to chemical type sets defined by the library; compounds outside these sets will not be matched even if similar compounds exist elsewhere.
- Match scores >0.95 may be unattainable for highly dissimilar or novel query compounds, resulting in false 'No match' designations.
- Library curation is manual; typos or synonym variations in compound names can prevent correct matching (e.g., 'Methyl Salicylate' vs. 'Methyl salicylate').
- The wide-format data frame input_format may become unwieldy with many type sets or large libraries; performance and memory usage are not characterized in the article.

## Evidence

- [readme] Library structure and matching: "GroupA = c("Guaiacol", "Tridecane", "Ethyl heptanoate", "Caffeine"); GroupB = c("2-Aminothiazole", "Aspirin", "Octanoic acid", "alpha-Pinene", "Toluene"); chem_library = data.frame(cbind(GroupA,"
- [methods] categorate() function and best-match output: "The categorate() function, when applied under structural-matching conditions restricted to 4 chemical type sets, produces a best-match table that correctly identifies compound classifications (e.g.,"
- [methods] Workflow: loading and passing libraries to categorate(): "Load the query chemical list (Ethyl hexanoate, Methyl salicylate, Octanal, Undecane) and the restricted type library (Type A–E chemical sets) as R data structures. Call categorate() on the query"
- [methods] Match score threshold and output schema: "Extract the best-match results, which identify the highest-scoring structural match (match score >0.95) within each type set for each query chemical"
- [methods] Tool integration for structural matching: "uafR taps into an amazing set of cheminformatics packages -- ChemmineR, fmcsR, webchem"
- [readme] categorate() function purpose: "categorate() is an overpowered function that accesses a broad array of categorical data for searched chemicals"
