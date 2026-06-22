---
name: kegg-database-querying
description: Use when you have identified two or more organisms (via their KEGG organism codes, e.g., 'hsa' for Homo sapiens) and need to retrieve their complete metabolic pathway and reaction datasets as a prerequisite for network reconstruction or comparative metabolic analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0224
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0585
  tools:
  - MetNet
  - KEGG
  - Java
derived_from:
- doi: 10.1371/journal.pone.0246962
  title: MetNet
evidence_spans:
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG
- MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network
- their metabolic data are retrieved from KEGG and the corresponding networks of metabolic functions are built
- MetNet is a Java tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metnet_cq
    doi: 10.1371/journal.pone.0246962
    title: MetNet
  dedup_kept_from: coll_metnet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pone.0246962
  all_source_dois:
  - 10.1371/journal.pone.0246962
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# KEGG Database Querying

## Summary

Query the KEGG database to retrieve metabolic pathway and reaction data for specified organisms, enabling automated reconstruction of metabolic networks. This skill is essential when you need to programmatically obtain organism-specific metabolic information to build comparative network models.

## When to use

Apply this skill when you have identified two or more organisms (via their KEGG organism codes, e.g., 'hsa' for Homo sapiens) and need to retrieve their complete metabolic pathway and reaction datasets as a prerequisite for network reconstruction or comparative metabolic analysis. Use it specifically when organism identifiers are available and the downstream goal is to build structural or functional representations of metabolic networks.

## When NOT to use

- When metabolic network data has already been retrieved and stored locally; querying again would be redundant and inefficient.
- When working with custom or non-KEGG metabolic databases; this skill is KEGG-specific and cannot be applied to other pathway databases without adaptation.
- When only a small subset of hand-curated reactions is needed; full KEGG queries retrieve comprehensive data that may exceed the scope of focused studies.

## Inputs

- organism identifiers (KEGG codes, e.g., 'hsa', 'ptr')
- KEGG database connection or API endpoint
- configuration file specifying organisms and pathways (e.g., organismList.txt, pathwayList.txt)

## Outputs

- metabolic pathway data per organism (pathway IDs, definitions, associated reactions)
- metabolic reaction data per organism (reaction equations, enzyme IDs, stoichiometric coefficients)
- organism-specific metabolic data records ready for network reconstruction

## How to apply

Load organism identifiers (KEGG codes) from a configuration file such as organismList.txt. Query the KEGG database programmatically to retrieve metabolic pathway and reaction data for each selected organism. The retrieved data should include pathway definitions, reaction stoichiometry, and enzyme associations. Validate that all expected pathways and reactions for each organism have been successfully retrieved before proceeding to network reconstruction. The query results form the raw input layer that will be passed to network topology builders (e.g., MetNet) to generate structural and functional network representations. Ensure that the KEGG version and query parameters are consistent across all organisms being compared to maintain comparability.

## Related tools

- **MetNet** (Java tool that consumes KEGG metabolic data queried by this skill to automatically reconstruct metabolic network topology and functional representations) — https://github.com/simeoni-biolab/MetNet
- **KEGG** (Source database from which metabolic pathway and reaction data are retrieved via programmatic queries)

## Examples

```
java -jar MetNet.jar hsa ptr set
```

## Evaluation signals

- Verify that the number of retrieved pathways and reactions per organism matches expected counts from KEGG documentation or a manual spot check.
- Confirm that all organism identifiers in the input list were successfully queried and no organisms were skipped or failed silently.
- Validate that reaction data includes required fields: reaction equations, enzyme EC numbers, and stoichiometric coefficients.
- Check that retrieved data for two organisms can be independently passed to MetNet for network reconstruction without schema errors.
- Ensure query timestamps and KEGG version metadata are recorded to enable reproducibility and version tracking across comparative analyses.

## Limitations

- KEGG data quality and completeness varies by organism; less-studied organisms may have incomplete pathway annotations.
- KEGG is a commercial and subscription-based resource for some use cases; access restrictions or rate limits may apply depending on usage context.
- The retrieved data reflects KEGG's current curation state; pathway and reaction annotations are periodically updated, so reproducibility of results from different KEGG versions may differ.
- Organism selection is constrained to organisms present in KEGG; custom or newly sequenced organisms not yet in the database cannot be queried directly.

## Evidence

- [other] Query KEGG database to retrieve metabolic pathway and reaction data for each of the two organisms.: "Query KEGG database to retrieve metabolic pathway and reaction data for each of the two organisms"
- [readme] Load organism identifiers from organismList.txt and pathwayList.txt configuration files.: "organismList.txt : configuration file containing the list of organisms available in KEGG"
- [other] MetNet automatically reconstructs metabolic networks by retrieving metabolic data from KEGG for two organisms selected by the user.: "MetNet automatically reconstructs metabolic networks by retrieving metabolic data from KEGG for two organisms selected by the user"
- [readme] MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG.: "MetNet is a Java tool that makes it possible to automatically reconstruct the metabolic network of two organisms selected in KEGG"
- [readme] Please ensure that the configuration files organismList.txt and pathwayList.txt are in the tool's directory.: "Please ensure that the configuration files organismList.txt and pathwayList.txt are in the tool's directory"
