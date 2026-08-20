---
name: database-integration-and-linkage
description: Use when you have a list of metabolite identifiers sourced from one metabolome
  database (e.g., HMDB IDs, PubChem CIDs) and need to map them to equivalent identifiers
  in other databases for data integration, cross-referencing, or standardization in
  downstream metabolomics analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
  tools:
  - R
  - devtools
  - MetaFetcheR
  license_tier: open
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

# Cross-database metabolite identifier linking and resolution

## Summary

MetaFetcheR links metabolite identifiers across five major metabolome databases (HMDB, ChEBI, PubChem, KEGG, LipidMaps) to resolve ID ambiguity and standardize metabolite representation. This skill is essential when working with metabolomic data where the same chemical entity may be referenced by different identifiers in different public repositories.

## When to use

You have a list of metabolite identifiers sourced from one metabolome database (e.g., HMDB IDs, PubChem CIDs) and need to map them to equivalent identifiers in other databases for data integration, cross-referencing, or standardization in downstream metabolomics analysis.

## When NOT to use

- Input metabolites are already represented as chemical structures (SMILES, InChI, or molecular formulas) rather than database-specific identifiers.
- Target analysis requires only metabolites from a single database with no cross-database validation or integration needed.
- Input IDs are from metabolome databases not supported by MetaFetcheR (currently limited to HMDB, ChEBI, PubChem, KEGG, LipidMaps).

## Inputs

- Metabolite identifier list (e.g., vector or data frame in R)
- Source database name (HMDB, ChEBI, PubChem, KEGG, or LipidMaps)
- Input metabolite identifiers (database-specific IDs)

## Outputs

- Cross-database mapping table (data frame or CSV)
- Columns: source ID, source database, resolved target IDs per database
- One row per input metabolite with all resolved identifiers

## How to apply

Load metabolite identifiers and their source database into R. Call the MetaFetcheR core mapping function, which resolves input IDs against an internal cross-database linkage index covering HMDB, ChEBI, PubChem, KEGG, and LipidMaps. The function returns a table where each row represents one input metabolite with columns containing the source ID, source database, and all resolved target IDs paired with their corresponding target databases. Aggregate the resolved identifiers into a single output table and export as CSV. Verify that all input metabolites received mapping attempts and that the output contains one row per input metabolite with consistent database naming conventions across rows.

## Related tools

- **MetaFetcheR** (R package implementing cross-database metabolite ID mapping and resolution via internal linkage index) — https://github.com/komorowskilab/MetaFetcheR
- **devtools** (R package installation and development utilities for loading MetaFetcheR from GitHub)

## Examples

```
library(devtools); install_github("shizidushu/hfun","komorowskilab/metafetcher"); library(MetaFetcheR); mapped_ids <- metafetcher_map(input_ids, source_db="HMDB", target_dbs=c("ChEBI","PubChem","KEGG","LipidMaps")); write.csv(mapped_ids, "metabolite_mapping.csv", row.names=FALSE)
```

## Evaluation signals

- All input metabolites appear in the output table with exactly one row per input metabolite.
- Output columns include source ID, source database, and at least one resolved target database ID for each row.
- No missing values or null entries in the source ID and source database columns.
- Resolved target IDs are consistent with expected format for their declared target database (e.g., HMDB IDs follow HMDB001234 format).
- CSV export is well-formed with consistent column headers and no dropped rows or truncated values.

## Limitations

- MetaFetcheR currently supports only five metabolome databases; identifiers from other repositories cannot be resolved.
- Mapping success depends on the completeness of the internal cross-database linkage index, which may not capture all metabolites or recent database updates.
- Some metabolites may have no mappings to certain target databases if they are not represented or linked in the underlying index.
- The README notes no changelog is available, so version-specific behavior and index update frequency are not documented.

## Evidence

- [readme] An R package designed to link metabolites IDs from different Metabolome databases with eachother in a step to resolve ambiguity and standardize metabolites representation and annotation.: "An R package designed to link metabolites IDs from different Metabolome databases with eachother in a step to resolve ambiguity and standardize metabolites representation and annotation."
- [other] MetaFetcheR supports resolving IDs for five metabolome databases: Human Metabolome Database (HMDB), Chemical Entities of Biological Interest (ChEBI), PubChem, Kyoto Encyclopedia of Genes and Genomes (KEGG), and Lipidomics Gateway (LipidMaps).: "MetaFetcheR supports resolving IDs for five metabolome databases: Human Metabolome Database (HMDB), Chemical Entities of Biological Interest (ChEBI), PubChem, Kyoto Encyclopedia of Genes and Genomes"
- [other] Call the MetaFetcheR core mapping function to resolve input IDs against the package's internal cross-database linkage index (HMDB, ChEBI, PubChem, KEGG, LipidMaps).: "Call the MetaFetcheR core mapping function to resolve input IDs against the package's internal cross-database linkage index (HMDB, ChEBI, PubChem, KEGG, LipidMaps)."
- [other] Aggregate resolved identifiers from all target databases into a single output table, retaining source ID, source database, and all resolved target IDs and their corresponding databases.: "Aggregate resolved identifiers from all target databases into a single output table, retaining source ID, source database, and all resolved target IDs and their corresponding databases."
- [other] Export the mapping table as a CSV file with one row per input metabolite and columns for each database's resolved IDs.: "Export the mapping table as a CSV file with one row per input metabolite and columns for each database's resolved IDs."
