---
name: chemical-type-classification-and-annotation
description: Use when after identifying query chemicals from GC-MS data (via Match.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - ChemmineR
  - fmcsR
  - webchem
  - R
  - uafR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-type-classification-and-annotation

## Summary

Classify and annotate query chemicals against a user-defined or restricted library of compound type categories using structural matching and categorical database lookups. This skill identifies best-matching compound types for GC-MS detected chemicals and enriches them with cross-database metadata (PubChem, LOTUS, KEGG, FEMA, FDA/SPL).

## When to use

Apply this skill after identifying query chemicals from GC-MS data (via Match.Factor filtering or manual selection) and you need to: (1) assign each query chemical to a best-matching type category within a restricted compound library, or (2) annotate query chemicals with categorical attributes (reactive groups, natural product occurrence, bioactivity, flavor/odor designation, or FDA/SPL presence) to enable downstream filtering or prioritization.

## When NOT to use

- Query chemicals are already structurally classified or annotated within your own internal taxonomy and re-annotation against external categories is not required.
- Input data lacks standardized chemical names; categorate() relies on exact or fuzzy name matching to public databases via webchem and will fail or produce spurious matches on malformed, proprietary, or non-standard chemical identifiers.
- The chemical library is empty, malformed (missing column names or type groupings), or incompatible with wide-format input_format='wide' specification.

## Inputs

- vector of query chemical names (character vector, e.g., c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'))
- chemical library data.frame (wide format: columns = type sets, rows = compound identifiers or chemical names)
- optional: pre-filtered GC-MS compound list (Compound.Name column with Match.Factor >= user-defined threshold, e.g., 70–80)

## Outputs

- categorate() best-match table (data.frame): rows = query chemicals, columns = type categories and compound identifiers (CMP1, CMP2, etc.) or 'No' for unmatched
- enriched annotation data.frame: includes categorical attributes (reactive groups, LOTUS membership, KEGG bioactivity, FEMA flavor code, FDA/SPL status) for each query chemical
- subset vectors (character): output from exactoThese() for downstream m/z extraction via mzExacto()

## How to apply

Pass a vector of query chemical names (e.g., c('Linalool', 'Methyl Salicylate', 'Limonene')) and a structured chemical library (as an R data.frame with compounds grouped by type or category) to the categorate() function with input_format='wide'. The function accesses ChemmineR and fmcsR to perform structural matching via flexible maximum common substructure (FMCS) scoring, returning a best-match table that identifies the highest-scoring structural match (typically Match.Factor >0.95) within each type set for each query chemical. For each chemical, categorate() queries PubChem (reactive groups), LOTUS (natural products), KEGG (bioactivities), FEMA (flavor/odor), and FDA/SPL (regulatory status) via webchem, producing a data.frame where rows are query chemicals and columns represent categorical membership or best-matching type identifier (e.g., 'CMP1', 'CMP2', 'GroupA', or 'No' for no match). Use exactoThese() downstream to subset the categorated results by Database, FMCS structural properties (MW, rings, groups, atoms, charges), or Library group assignment.

## Related tools

- **ChemmineR** (Performs cheminformatics analysis and structural comparisons; core engine for FMCS matching in categorate()) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **fmcsR** (Computes flexible maximum common substructure (FMCS) similarity scores between query and library chemicals; returns Match.Factor-like scores for type assignment) — https://bioconductor.org/packages/release/bioc/html/fmcsR.html
- **webchem** (Queries PubChem, LOTUS, KEGG, FEMA, and FDA/SPL databases to retrieve categorical metadata (reactive groups, natural products, bioactivities, flavor, regulatory status) for annotating query chemicals) — https://cran.r-project.org/web/packages/webchem/index.html
- **R** (Execution environment and host language for categorate(), exactoThese(), and data manipulation)
- **uafR** (Package containing categorate() and exactoThese() functions for chemical classification and downstream subsetting workflows) — https://github.com/castratton/uafR

## Examples

```
query_chemicals = c("Linalool", "Methyl Salicylate", "Limonene"); GroupA = c("Guaiacol", "Tridecane", "Ethyl heptanoate"); GroupB = c("2-Aminothiazole", "Aspirin", "Octanoic acid"); chem_library = data.frame(cbind(GroupA, GroupB)); query_categorated = categorate(query_chemicals, chem_library, input_format = "wide")
```

## Evaluation signals

- Best-match table contains exactly one row per query chemical and at most one assigned type (CMP identifier, GroupA/B label, or 'No') per type set; no duplicates or NA values in the best-match column.
- Each matched compound has a structural Match.Factor or FMCS score >0.95 (or user-specified threshold); verify scores in the output data.frame or by inspecting categorate() intermediate outputs.
- Cross-database annotation columns (Database, reactive_groups, LOTUS, KEGG, FEMA, FDA_SPL) are populated (non-empty) for chemicals successfully queried to external databases; missing annotations align with known database coverage gaps (e.g., very novel or highly proprietary compounds may return 'NA' or 'Unknown').
- Downstream exactoThese() subsetting on categorate() output (e.g., subsetBy='Database', subsetArgs='FEMA') returns a non-empty vector of chemical names matching the requested criteria; vector length is consistent with library composition.
- mzExacto() successfully extracts m/z peaks and retention times for chemicals returned by exactoThese(query_categorated, ...) with no errors or missing values in the input_exacto output table.

## Limitations

- categorate() relies on exact or fuzzy name matching via webchem; synonym variants, abbreviations, or IUPAC/common name discrepancies may cause database query failures, leading to missing or incorrect annotations.
- Structural matching (FMCS) assumes input chemical library compounds have associated SMILES or structure formats; if library compounds lack chemical structure data, fmcsR cannot compute similarity scores and categorate() will default to 'No' match.
- Match.Factor and FMCS thresholds (>0.95) are heuristic; chemicals with borderline similarity (0.85–0.95) may be excluded from classification even if chemically related. Users should validate threshold choice against domain knowledge.
- External database queries (PubChem, LOTUS, KEGG, FEMA, FDA/SPL) are network-dependent and subject to rate limits, API availability, and version drift; outdated or temporarily unavailable databases will produce 'NA' or stale annotation values.
- categorate() output is deterministic only if chemical library and query list are stable; adding or reordering library compounds or query chemicals will alter best-match assignments due to FMCS pairwise scoring.

## Evidence

- [other] categorate() function correctly match chemical compounds to their best-matching compound type categories: "The categorate() function, when applied under structural-matching conditions restricted to 4 chemical type sets, produces a best-match table that correctly identifies compound classifications (e.g.,"
- [methods] categorate() accesses categorical data from multiple databases: "`categorate()` is an overpowered function that accesses a broad array of categorical data for searched chemicals."
- [methods] categorate() uses ChemmineR, fmcsR, and webchem for structural matching: "Call categorate() on the query chemicals, passing the restricted library to access structural match data via ChemmineR, fmcsR, and webchem."
- [readme] exactoThese() enables subsetting of categorate() output by database, FMCS properties, or library group: "these_chems = exactoThese(query_categorated, subsetBy = "Database", subsetArgs = "FEMA")
these_chems = exactoThese(query_categorated, subsetBy = "FMCS", subsetArgs = "MW", subsetArgs2 = "Greater"
- [methods] External databases queried include PubChem, LOTUS, KEGG, FEMA, FDA/SPL: "Reactive Groups from [PubChem](https://pubchem.ncbi.nlm.nih.gov/), natural products occurrences from [LOTUS](https://lotus.naturalproducts.net/), bioactivites and risk categories from the Kyoto"
- [readme] categorate() with wide-format input: "query_categorated = categorate(query_chemicals, chem_library, input_format = "wide")"
