---
name: multi-source-metabolite-resolution
description: Use when you have metabolite identifiers sourced from a single metabolome database (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - devtools
  - MetaFetcheR
derived_from:
- doi: 10.1101/2021.02.28.433248v2
  title: MetaFetcheR
evidence_spans:
- MetaFetcheR is implemented in R
- library(devtools)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metafetcher_cq
    doi: 10.1101/2021.02.28.433248v2
    title: MetaFetcheR
  dedup_kept_from: coll_metafetcher_cq
schema_version: 0.2.0
---

# multi-source-metabolite-resolution

## Summary

Link and resolve metabolite identifiers across five major metabolome databases (HMDB, ChEBI, PubChem, KEGG, LipidMaps) to standardize metabolite representation and eliminate cross-database identifier ambiguity. Use this skill when you have metabolite IDs from one database and need unified identifiers or annotations from multiple sources.

## When to use

You have metabolite identifiers sourced from a single metabolome database (e.g., HMDB accessions, PubChem CIDs, KEGG compound IDs) and need to map them to corresponding identifiers in other major metabolome databases, or you are aggregating metabolite data from multiple studies/platforms and require a canonical cross-database linkage index to resolve ID conflicts and standardize annotation.

## When NOT to use

- Input metabolites are already pre-linked to a single canonical identifier system (e.g., you only need HMDB-to-HMDB validation, not cross-database mapping).
- Your metabolites originate from databases not supported by MetaFetcheR (e.g. specialized lipid databases, plant metabolomes, or non-standard compound collections not indexed in HMDB, ChEBI, PubChem, KEGG, or LipidMaps).
- You require real-time or streaming ID resolution; MetaFetcheR uses a static internal index and may not reflect very recent database updates.

## Inputs

- metabolite identifiers (as vector or table column: HMDB accessions, ChEBI IDs, PubChem CIDs, KEGG compound IDs, or LipidMaps entries)
- source database label for each identifier (e.g. 'HMDB', 'PubChem', 'KEGG')
- R data frame or list of IDs and source labels

## Outputs

- CSV file with one row per input metabolite
- columns: source_id, source_database, hmdb_ids, chebi_ids, pubchem_ids, kegg_ids, lipidomaps_ids (or equivalent schema)
- resolved cross-database metabolite ID mapping table

## How to apply

Load your metabolite identifiers and their source database into R. Call MetaFetcheR's core mapping function, which queries the package's internal cross-database linkage index covering HMDB, ChEBI, PubChem, KEGG, and LipidMaps. The function resolves each input ID against all target databases and returns a single aggregated output table with one row per input metabolite. For each row, retain the source ID and source database, then populate columns for each target database's resolved IDs. Export the mapping table as CSV. Success is indicated when all input IDs produce at least one resolved target ID (or a clear null if no match exists), and the output table has a consistent schema across all rows.

## Related tools

- **MetaFetcheR** (R package that hosts the core cross-database metabolite ID linkage index and mapping function) — https://github.com/komorowskilab/MetaFetcheR
- **devtools** (R package dependency for installing MetaFetcheR from GitHub)
- **R** (runtime environment and language for executing MetaFetcheR mapping functions)

## Examples

```
library(devtools); install_github("shizidushu/hfun","komorowskilab/metafetcher"); library(metafetcher); mapping_result <- metafetcher_resolve(ids = c('HMDB0000001', 'HMDB0000002'), source_db = 'HMDB'); write.csv(mapping_result, 'metabolite_mapping.csv', row.names=FALSE)
```

## Evaluation signals

- All input metabolite IDs produce at least one resolved target ID in the output, or are explicitly marked as unresolved (null/NA); no silent failures.
- Output CSV schema is consistent: one row per input metabolite, source_id and source_database always populated, target database columns present (even if empty for some rows).
- Cross-database consistency check: if an input ID resolves to a target ID in database X, querying that target ID as a new input should return the original input ID in the source database column (bidirectional linkage).
- No duplicate rows per input metabolite; each input ID appears exactly once in the output.
- All resolved IDs conform to the expected format for their database (e.g. HMDB IDs match pattern HMDB####, PubChem CIDs are integers, KEGG IDs match C##### format).

## Limitations

- MetaFetcheR supports only five metabolome databases (HMDB, ChEBI, PubChem, KEGG, LipidMaps); metabolites from other specialized or emerging databases will not be resolved.
- The internal cross-database linkage index is static and may lag behind live database updates; newly curated metabolites or recent ID changes may not be reflected.
- Ambiguous or incorrect source database labels in the input will cause resolution failures; the user must ensure accurate source database annotation.
- No changelog provided in the repository; users cannot easily track which versions of the underlying databases are included in a given package release.

## Evidence

- [other] MetaFetcheR supports resolving IDs for five metabolome databases: "MetaFetcheR supports resolving IDs for five metabolome databases: Human Metabolome Database (HMDB), Chemical Entities of Biological Interest (ChEBI), PubChem, Kyoto Encyclopedia of Genes and Genomes"
- [other] workflow: call core mapping function and aggregate results: "Call the MetaFetcheR core mapping function to resolve input IDs against the package's internal cross-database linkage index (HMDB, ChEBI, PubChem, KEGG, LipidMaps). 3. Aggregate resolved identifiers"
- [readme] designed to link metabolites IDs from different databases: "An R package designed to link metabolites IDs from different Metabolome databases with eachother in a step to resolve ambiguity and standardize metabolites representation and annotation."
- [other] export mapping table as CSV: "Export the mapping table as a CSV file with one row per input metabolite and columns for each database's resolved IDs."
- [readme] installation via devtools: "library(devtools) install_github("shizidushu/hfun","komorowskilab/metafetcher")"
