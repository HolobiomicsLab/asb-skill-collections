---
name: cheminformatics-database-querying
description: Use when you have a list of identified or suspected chemical compound
  names (e.g., from GC-MS Match.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - ChemmineR
  - fmcsR
  - webchem
  - R
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- To perform the chemical structure matches and summarize atomic features, uafR taps
  into an amazing set of cheminformatics packages -- [ChemmineR]
- uafR taps into an amazing set of cheminformatics packages -- [ChemmineR](https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html),
  [fmcsR]
- uafR taps into an amazing set of cheminformatics packages -- [ChemmineR](https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html),
  [fmcsR](https://bioconductor.org/packages/release/bioc
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

# cheminformatics-database-querying

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Query structural and categorical metadata for chemical compounds by name against integrated cheminformatics databases and libraries, using exact mass and functional group data to classify compounds and retrieve bioactivity or occurrence information. This skill bridges mass spectrometry peak identification with chemical property lookups and structural matching.

## When to use

Apply this skill when you have a list of identified or suspected chemical compound names (e.g., from GC-MS Match.Factor hits or a query set) and need to enrich them with structural properties (molecular weight, ring count, functional groups), categorical affiliations (presence in PubChem reactive groups, LOTUS natural products, KEGG bioactivities, FEMA flavor database, or FDA/SPL registry), or best-match classification against a user-defined type library using structural similarity (FMCS score >0.95). Use it after spreadOut() and mzExacto() have prepared and extracted your compound candidates.

## When NOT to use

- Your input compound identifiers are already standardized InChI or SMILES strings rather than common chemical names — use direct structure-based tools instead.
- You require real-time or custom-threshold structural matching beyond the pre-integrated FMCS score >0.95 threshold — categorate() applies a fixed matching pipeline.
- Your query list contains only mass spectrometry peaks or m/z values without compound name assignments — use mzExacto() first to resolve names before querying databases.

## Inputs

- query_chemicals (character vector of compound names)
- chem_library (optional data frame of reference chemical groups/types, wide or long format)
- input_format parameter ('wide' for data frame columns as groups, or 'long' for vectors)

## Outputs

- categorate() output table: rows = query chemicals, columns = query name, matched type/group, matched compound identifier (CMP identifier or 'No')
- exactoThese() subset: filtered character vector of chemical names meeting Database, FMCS property, or Library criteria

## How to apply

Load your query chemical names as a character vector (e.g., c('Linalool', 'Methyl Salicylate')) and optionally a reference chemical library (chem_library) formatted as a data frame with compound type groups (wide format) or individual vectors (long format). Call categorate(query_chemicals, chem_library, input_format = 'wide') to invoke ChemmineR and fmcsR for structural matching via webchem, which queries PubChem, LOTUS, KEGG, FEMA, and FDA/SPL to return a categorized table. Each row reports the query chemical name, matched type/group (or 'No' if no structural match ≥0.95 found), and matched compound identifier (e.g., 'CMP2'). Filter results using exactoThese() with subsetBy parameters ('Database', 'FMCS', or 'Library') and subsetArgs (e.g., 'reactives', 'FEMA', 'MW', 'Rings', 'Groups', 'Atoms', 'NCharges') to subset for downstream mass spectrometry re-querying with mzExacto().

## Related tools

- **ChemmineR** (Performs structural similarity searches and cheminformatics property calculations for compound matching within categorate()) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **fmcsR** (Computes flexible maximum common substructure (FMCS) scores to rank structural matches between query chemicals and reference library compounds) — https://bioconductor.org/packages/release/bioc/html/fmcsR.html
- **webchem** (Queries PubChem, LOTUS, KEGG, FEMA, and FDA/SPL databases to retrieve categorical and bioactivity metadata for matched compounds) — https://cran.r-project.org/web/packages/webchem/index.html
- **R** (Execution environment for categorate() and exactoThese() workflow functions)

## Examples

```
query_chemicals = c("Linalool", "Methyl Salicylate", "Limonene"); chem_library = data.frame(cbind(GroupA = c("Guaiacol", "Ethyl heptanoate"), GroupB = c("Aspirin", "alpha-Pinene"))); query_categorated = categorate(query_chemicals, chem_library, input_format = "wide")
```

## Evaluation signals

- All query chemical names appear in the output rows; no queries are silently dropped.
- Matched compound identifiers (CMP1, CMP2, etc., or 'No') are present in output and correspond to entries in the input chem_library or database.
- Best-match structural scores (if reported) are ≥0.95, confirming FMCS threshold compliance.
- exactoThese() subsets reduce the chemical list deterministically: Database='FEMA' returns only chemicals marked as flavor/odor in FEMA, FMCS='MW' filters by molecular weight, Library='GroupB' returns only chemicals from that reference group.
- Spot-check a few output rows against PubChem or LOTUS database entries (via browser) to confirm chemical name resolution and property accuracy.

## Limitations

- categorate() is restricted to compounds resolvable by webchem to PubChem, LOTUS, KEGG, FEMA, or FDA/SPL; obscure or proprietary compounds may return 'No match'.
- Structural matching threshold (FMCS >0.95) is fixed in the uafR implementation and cannot be tuned without code modification.
- Performance degrades with very large query lists (>1000 compounds) due to network calls to external databases; batch processing or caching is not documented.
- Categorical affiliations (e.g., 'reactive', 'natural product', 'FDA approved') reflect database state at query time and may become stale if databases are not regularly updated.

## Evidence

- [methods] categorate() function and structural matching: "`categorate()` is an overpowered function that accesses a broad array of categorical data for searched chemicals."
- [other] FMCS structural matching score threshold: "The categorate() function, when applied under structural-matching conditions restricted to 4 chemical type sets, produces a best-match table that correctly identifies compound classifications (e.g.,"
- [methods] Database sources integrated into categorate(): "Reactive Groups from [PubChem](https://pubchem.ncbi.nlm.nih.gov/), natural products occurrences from [LOTUS](https://lotus.naturalproducts.net/), bioactivites and risk categories from the Kyoto"
- [readme] exactoThese() subsetting by database or structural property: "these_chems = exactoThese(query_categorated, subsetBy = "Database", subsetArgs = "FEMA"); these_chems = exactoThese(query_categorated, subsetBy = "FMCS", subsetArgs = "MW", subsetArgs2 = "Between","
- [readme] Input format and library structure for categorate(): "query_chemicals = c("Linalool", "Methyl Salicylate", "Limonene", "alpha-Thujene"); chem_library = data.frame(cbind(GroupA, GroupB)); query_categorated = categorate(query_chemicals, chem_library,"
- [methods] ChemmineR, fmcsR, and webchem tool integration: "uafR taps into an amazing set of cheminformatics packages -- [ChemmineR](https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html), [fmcsR](https://bioconductor.org/packages/release/bioc"
