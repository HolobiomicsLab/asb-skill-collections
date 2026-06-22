---
name: metabolite-id-normalization
description: Use when you have metabolite identifiers sourced from or annotated against heterogeneous metabolome databases (HMDB, ChEBI, PubChem, KEGG, LipidMaps) and need to resolve ambiguity in metabolite identity, create a unified metabolite reference table, or enable cross-database queries in a metabolomics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3047
  tools:
  - R
  - devtools
  - MetaFetcheR
  - Human Metabolome Database (HMDB)
  - Chemical Entities of Biological Interest (ChEBI)
  - PubChem
  - Kyoto Encyclopedia of Genes and Genomes (KEGG)
  - Lipidomics Gateway (LipidMaps)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2021.02.28.433248v2
  all_source_dois:
  - 10.1101/2021.02.28.433248v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-id-normalization

## Summary

Cross-database metabolite identifier resolution and linking using MetaFetcheR to standardize and disambiguate metabolite representation across HMDB, ChEBI, PubChem, KEGG, and LipidMaps. This skill reconciles fragmented metabolite annotations into a unified reference table, enabling downstream metabolome integration and comparative analysis.

## When to use

Apply this skill when you have metabolite identifiers sourced from or annotated against heterogeneous metabolome databases (HMDB, ChEBI, PubChem, KEGG, LipidMaps) and need to resolve ambiguity in metabolite identity, create a unified metabolite reference table, or enable cross-database queries in a metabolomics workflow.

## When NOT to use

- Your metabolite identifiers are already unified and come from a single, canonical database with no ambiguity.
- You require metabolite structure, chemical properties, or biological pathway information; this skill resolves IDs only, not annotations or chemical descriptors.
- Your metabolite identifiers are from databases not supported by MetaFetcheR (outside HMDB, ChEBI, PubChem, KEGG, LipidMaps).

## Inputs

- metabolite identifier list (e.g. HMDB IDs, ChEBI identifiers, PubChem CIDs)
- source database label for each metabolite (string: 'HMDB', 'ChEBI', 'PubChem', 'KEGG', or 'LipidMaps')
- R environment with MetaFetcheR package loaded

## Outputs

- cross-database metabolite ID mapping table (CSV)
- one row per input metabolite; columns for source ID, source database, and resolved IDs for each of the five target databases
- standardized metabolite reference with disambiguated annotations

## How to apply

Load your metabolite identifiers and their source database into R. Use the MetaFetcheR core mapping function to resolve input IDs against the package's internal cross-database linkage index. The function queries the five supported databases (HMDB, ChEBI, PubChem, KEGG, LipidMaps) and returns all available target IDs for each input metabolite. Aggregate the resolved identifiers into a single output table, preserving the source ID, source database, and all resolved target IDs with their corresponding target database labels. Export the mapping table as a CSV file with one row per input metabolite and columns for each database's resolved IDs. Verify successful resolution by checking that each input metabolite has at least one resolved ID in the target database(s) relevant to your analysis.

## Related tools

- **MetaFetcheR** (R package implementing the cross-database metabolite ID linkage index and resolution function; core execution engine for this skill) — https://github.com/komorowskilab/MetaFetcheR
- **R** (programming environment for loading data, calling MetaFetcheR functions, and exporting results)
- **devtools** (R package dependency for installing MetaFetcheR from GitHub source)
- **Human Metabolome Database (HMDB)** (one of five target metabolome databases for ID resolution)
- **Chemical Entities of Biological Interest (ChEBI)** (one of five target metabolome databases for ID resolution)
- **PubChem** (one of five target metabolome databases for ID resolution)
- **Kyoto Encyclopedia of Genes and Genomes (KEGG)** (one of five target metabolome databases for ID resolution)
- **Lipidomics Gateway (LipidMaps)** (one of five target metabolome databases for ID resolution)

## Examples

```
library(devtools); install_github("shizidushu/hfun","komorowskilab/metafetcher"); library(metafetcher); mapped_ids <- resolve_metabolites(input_ids, source_db="HMDB"); write.csv(mapped_ids, "metabolite_mapping.csv", row.names=FALSE)
```

## Evaluation signals

- All input metabolites have at least one resolved ID in at least one target database (no null mappings for valid inputs).
- Output CSV contains exactly one row per input metabolite with source ID and source database correctly preserved.
- Cross-database links are bidirectional where applicable (e.g., if HMDB ID X maps to ChEBI ID Y, querying Y returns X).
- No duplicate IDs appear in output rows for the same target database (one-to-many resolution is valid; many-to-one duplication indicates mapping error).
- Target database columns are populated only with IDs from their respective databases; no category mismatches or format violations.

## Limitations

- MetaFetcheR supports only five databases (HMDB, ChEBI, PubChem, KEGG, LipidMaps); metabolites not indexed in the package's internal linkage data cannot be resolved.
- Metabolites with no cross-database links (singletons in one database only) will not resolve to other databases; this reflects limitations in the underlying database integration, not failure of the tool.
- The quality and completeness of ID mappings depend on the freshness and accuracy of the internal cross-database linkage index; outdated or misannotated links in source databases will propagate.
- No changelog is available for the package, limiting transparency on version differences and internal linkage data updates.

## Evidence

- [intro] cross-database metabolite resolution: "designed to link metabolites IDs from different Metabolome databases with eachother in a step to resolve ambiguity and standardize metabolites representation and annotation"
- [readme] five supported databases: "Currently the package supports resolving IDs for the following databases: Human Metabolome Database (HMDB), Chemical Entities of Biological Interest (ChEBI), PubChem, Kyoto Encyclopedia of Genes and"
- [other] workflow steps for ID mapping: "Load metabolite identifiers and their source database using R. Call the MetaFetcheR core mapping function to resolve input IDs against the package's internal cross-database linkage index. Aggregate"
- [readme] implementation language: "MetaFetcheR is implemented in R"
- [readme] installation dependency: "library(devtools) install_github("shizidushu/hfun","komorowskilab/metafetcher")"
