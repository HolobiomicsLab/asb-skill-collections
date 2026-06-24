---
name: metabolite-annotation-mapping
description: Use when you have a MultiAssayExperiment object with metabolite measurements
  (assay slot) and basic rowData (e.g., metabolite names or mass-to-charge ratios),
  but lack standardized chemical identifiers or pathway assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDiff
  - R
  - WGCNA
  - Small Molecular Pathway Database (SMPDB)
  - MultiAssayExperiment
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
- install.packages("WGCNA")
- The core concept of the so called "weighted" correlation analysis by Langfelder
  and Horvarth
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty344
  all_source_dois:
  - 10.1093/bioinformatics/bty344
  - 10.1158/0008-5472.can-14-1490
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-annotation-mapping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Retrieve and map standardized metabolite identifiers (HMDB, KEGG, ChEBI) to pathway and chemical annotations from external databases (SMPDB). This enriches rowData in a MultiAssayExperiment object with biochemical context, enabling downstream pathway-level analysis and metabolite classification.

## When to use

You have a MultiAssayExperiment object with metabolite measurements (assay slot) and basic rowData (e.g., metabolite names or mass-to-charge ratios), but lack standardized chemical identifiers or pathway assignments. Use this skill before performing correlation network analysis, module identification, or pathway enrichment to ground metabolites in SMPDB, KEGG, or HMDB nomenclature.

## When NOT to use

- Metabolite rowData already contains curated pathway or functional annotations from a prior annotation step.
- The input identifiers (KEGG, HMDB, ChEBI) are absent or unmapped; SMPDB annotation will fail silently or return sparse results.
- You require real-time pathway databases or organism-specific pathway context not available in SMPDB.

## Inputs

- MultiAssayExperiment object with metabolite assay and rowData
- rowData columns containing KEGG, HMDB, or ChEBI identifiers (or NA if absent)

## Outputs

- MultiAssayExperiment object with enriched rowData
- Annotated rowData table with SMPDB pathway, SUB_PATHWAY, and chemical metadata columns

## How to apply

Load the MultiAssayExperiment object and invoke the get_SMPDBanno function, specifying which rowData columns contain KEGG IDs, HMDB IDs, and/or ChEBI IDs (e.g., column_kegg_id=6, column_hmdb_id=7, column_chebi_id=NA). The function queries the Small Molecular Pathway Database (SMPDB) to retrieve pathway annotations and chemical metadata for each metabolite. The enriched object is returned with additional annotation columns in rowData (e.g., SUB_PATHWAY, pathway names, chemical class). Verify that the returned rowData contains non-null pathway entries for the majority of metabolites and that SUB_PATHWAY entries can be extracted for module naming or pathway stratification in downstream steps.

## Related tools

- **MetaboDiff** (Provides the get_SMPDBanno function to retrieve SMPDB annotations and enrich rowData.) — https://github.com/andreasmock/MetaboDiff
- **Small Molecular Pathway Database (SMPDB)** (External database queried by get_SMPDBanno to supply metabolite pathway, chemical class, and functional annotations.)
- **MultiAssayExperiment** (Bioconductor container class that stores metabolite assays and rowData; enriched by annotation mapping.)

## Examples

```
met <- get_SMPDBanno(met, column_kegg_id=6, column_hmdb_id=7, column_chebi_id=NA)
```

## Evaluation signals

- rowData contains new non-null columns for SUB_PATHWAY, pathway names, or other SMPDB metadata post-annotation.
- Percentage of metabolites with assigned SUB_PATHWAY entries is ≥80% (or visibly higher than pre-annotation).
- Module naming downstream (e.g., in WGCNA workflow) successfully uses most abundant SUB_PATHWAY per module, indicating annotations are populated.
- No warnings or silent failures (NA returns) for metabolites with valid KEGG/HMDB/ChEBI IDs in the input.
- Annotated metabolites can be grouped and stratified by pathway in exploratory plots (e.g., heatmaps, correlation networks).

## Limitations

- Annotation coverage depends on SMPDB database completeness; metabolites with rare or novel identifiers may remain unmapped.
- SMPDB queries require valid, standardized KEGG, HMDB, or ChEBI identifiers in rowData; incorrect or obsolete IDs will yield null or erroneous mappings.
- The function is synchronous and may be slow for large metabolite tables (>1000 metabolites) due to repeated database lookups.
- SMPDB annotations are organism-agnostic; human-specific pathway context is not guaranteed for non-human datasets.

## Evidence

- [methods] Metabolite annotation can be retrieved from the Small Molecular Pathway Database (SMPDB) if HMDB, KEGG or ChEBI ids are part of the rowData object: "Metabolite annotation can be retrieved from the Small Molecular Pathway Database (SMPDB) if HMDB, KEGG or ChEBI ids are part of the rowData object"
- [methods] The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis.: "The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis."
- [other] For each module, identify the most abundant SUB_PATHWAY annotation and assign module names accordingly.: "For each module, identify the most abundant SUB_PATHWAY annotation and assign module names accordingly."
- [readme] The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements.: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
