---
name: metabolite-identifier-cross-mapping
description: Use when when you have metabolite identifiers from one or more metabolome databases and need to resolve them to equivalent identifiers in other databases, or when standardizing metabolite representation across multi-source metabolomic datasets where compounds may be annotated using different.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3375
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

# metabolite-identifier-cross-mapping

## Summary

MetaFetcheR is an R package that resolves and links metabolite identifiers across five major metabolome databases (HMDB, ChEBI, PubChem, KEGG, LipidMaps) to standardize metabolite annotation and resolve ambiguity in compound identity across data sources.

## When to use

When you have metabolite identifiers from one or more metabolome databases and need to resolve them to equivalent identifiers in other databases, or when standardizing metabolite representation across multi-source metabolomic datasets where compounds may be annotated using different database identifiers.

## When NOT to use

- Input metabolite identifiers are already standardized to a single database and no cross-database linking is needed.
- Metabolites originate from databases not supported by MetaFetcheR (only HMDB, ChEBI, PubChem, KEGG, LipidMaps are supported).
- High-throughput ID resolution is required on datasets > package scaling capacity; consider batch processing or alternative APIs.

## Inputs

- metabolite identifier list (vector or data frame column)
- source database name (HMDB, ChEBI, PubChem, KEGG, or LipidMaps)
- R environment with MetaFetcheR package loaded

## Outputs

- cross-database metabolite mapping table (data frame)
- CSV export with columns: source_id, source_database, hmdb_id, chebi_id, pubchem_id, kegg_id, lipidmaps_id

## How to apply

Load metabolite identifiers and their source database into R. Call MetaFetcheR's core mapping function, which queries an internal cross-database linkage index spanning HMDB, ChEBI, PubChem, KEGG, and LipidMaps. The function resolves each input ID against all supported target databases in parallel. Aggregate the resolved identifiers from all target databases into a single output table, preserving the source ID, source database, and all resolved target IDs with their corresponding databases. Export the mapping table as CSV with one row per input metabolite and columns for each database's resolved IDs, enabling downstream analysis with standardized compound identifiers.

## Related tools

- **R** (execution environment for MetaFetcheR package)
- **devtools** (R package dependency manager used to install MetaFetcheR from GitHub)
- **MetaFetcheR** (core mapping engine implementing cross-database metabolite ID resolution) — https://github.com/komorowskilab/MetaFetcheR

## Examples

```
library(devtools); install_github("komorowskilab/metafetcher"); library(MetaFetcheR); result <- map_metabolites(metabolite_ids = c("HMDB0000001", "HMDB0000002"), source_db = "HMDB"); write.csv(result, "metabolite_mapping.csv", row.names=FALSE)
```

## Evaluation signals

- All input metabolite IDs successfully matched to at least one target database without missing values in output table.
- Resolved IDs conform to the formatting and namespace conventions of their respective databases (e.g., HMDB IDs start with HMDB, ChEBI IDs are numeric).
- No duplicate rows per input metabolite; one-to-one mapping from source ID to resolved ID set is preserved.
- Cross-validation: spot-check resolved IDs by querying source databases directly to confirm identity equivalence.
- Output CSV structure matches expected schema: source_id, source_database, and one column per target database with null values for unresolved IDs.

## Limitations

- MetaFetcheR currently supports only five metabolome databases; metabolites from other sources or custom databases cannot be resolved.
- Resolution success depends on completeness and currency of the internal cross-database linkage index; newly added metabolites or IDs may not be immediately available.
- No changelog is available, limiting awareness of index updates or changes to ID mappings between versions.

## Evidence

- [other] MetaFetcheR supports resolving IDs for five metabolome databases: Human Metabolome Database (HMDB), Chemical Entities of Biological Interest (ChEBI), PubChem, Kyoto Encyclopedia of Genes and Genomes (KEGG), and Lipidomics Gateway (LipidMaps).: "MetaFetcheR supports resolving IDs for five metabolome databases: Human Metabolome Database (HMDB), Chemical Entities of Biological Interest (ChEBI), PubChem, Kyoto Encyclopedia of Genes and Genomes"
- [other] Call the MetaFetcheR core mapping function to resolve input IDs against the package's internal cross-database linkage index (HMDB, ChEBI, PubChem, KEGG, LipidMaps).: "Call the MetaFetcheR core mapping function to resolve input IDs against the package's internal cross-database linkage index (HMDB, ChEBI, PubChem, KEGG, LipidMaps)."
- [other] Aggregate resolved identifiers from all target databases into a single output table, retaining source ID, source database, and all resolved target IDs and their corresponding databases.: "Aggregate resolved identifiers from all target databases into a single output table, retaining source ID, source database, and all resolved target IDs and their corresponding databases."
- [readme] designed to link metabolites IDs from different Metabolome databases with eachother in a step to resolve ambiguity and standardize metabolites representation and annotation: "An R package designed to link metabolites IDs from different Metabolome databases with eachother in a step to resolve ambiguity and standardize metabolites representation and annotation."
- [readme] MetaFetcheR is implemented in R: "MetaFetcheR is implemented in R"
