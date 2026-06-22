---
name: background-reference-set-construction
description: Use when when preparing to perform pathway enrichment analysis on metabolomics data, you need a background-reference file that maps metabolic pathways to their constituent metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - R
  - KEGG
  - KEGGREST
  - enrichmet
  - BiocFileCache
  - R (readr, readxl, dplyr)
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed through a single R function call
- curated KEGG data for enrichment using Fisher's Exact Test
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enrichmet_cq
    doi: 10.1101/2025.08.28.672951v2
    title: EnrichMET
  dedup_kept_from: coll_enrichmet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.08.28.672951v2
  all_source_dois:
  - 10.1101/2025.08.28.672951v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# background-reference-set-construction

## Summary

Construction of a curated pathway-to-metabolite reference mapping file that defines the background universe of metabolites and their pathway memberships for statistical enrichment testing. This reference set is essential for Fisher's exact test-based pathway enrichment, where it serves as the null hypothesis denominator.

## When to use

When preparing to perform pathway enrichment analysis on metabolomics data, you need a background-reference file that maps metabolic pathways to their constituent metabolites. This is required before executing Fisher's exact test enrichment, particularly when working with KEGG pathways or other curated pathway databases and you do not already have a pre-constructed, pathway-indexed metabolite set.

## When NOT to use

- You already possess a pre-validated and organism-specific pathway-metabolite reference and do not need to rebuild or update it.
- Your analysis uses non-pathway-based enrichment (e.g., gene ontology, disease associations) that require different reference structures.
- Input metabolites use non-standardized or proprietary identifiers without a documented mapping to KEGG or other curated databases.

## Inputs

- Pathway database (KEGG, manually curated, or Zenodo-hosted)
- Metabolite identifier mapping (KEGG IDs, HMDB IDs, or other standardized codes)
- Optional: raw metabolite list to validate identifier compatibility

## Outputs

- PathwayVsMetabolites data.frame or CSV file with columns: Pathway, Metabolites
- Validated pathway-metabolite index suitable for Fisher's exact test background
- Metadata on pathway counts, metabolite coverage, and filtered pathway set

## How to apply

Obtain or construct a PathwayVsMetabolites file in tabular format (CSV or data.frame) with two columns: Pathway (pathway identifiers or names) and Metabolites (comma-separated KEGG IDs or other metabolite identifiers). If using KEGG, retrieve pathway-to-metabolite mappings via the KEGGREST R package or download curated human-specific mappings from Zenodo (zenodo.org/records/17819145). Ensure metabolite identifiers in this reference match those used in your input metabolite list. Perform basic quality checks: verify that min_pathway_occurrence (e.g., ≥2 metabolites per pathway) and min_metabolite_occurrence (e.g., ≥1) thresholds are met to avoid spurious or uninformative pathway entries. This reference set then becomes the fixed background against which observed metabolites are tested using Fisher's exact test.

## Related tools

- **KEGGREST** (Programmatic retrieval of KEGG pathway-to-metabolite mappings via REST API)
- **enrichmet** (Integrates constructed reference set and executes Fisher's exact test enrichment against it) — https://github.com/biodatalab/enrichmet
- **BiocFileCache** (Caching downloaded reference files (e.g., from Zenodo) for reproducibility and offline use)
- **R (readr, readxl, dplyr)** (Loading, validating, and reformatting pathway-metabolite mappings into analysis-ready data structures)

## Examples

```
# Load human pathway-metabolite reference from Zenodo
library(readr)
PathwayVsMetabolites <- read_csv('https://zenodo.org/api/records/17819145/files/human_pathway.csv/content')
# Validate and filter: keep pathways with ≥2 metabolites
PathwayVsMetabolites <- PathwayVsMetabolites %>% filter(!is.na(Pathway) & !is.na(Metabolites))
```

## Evaluation signals

- PathwayVsMetabolites table contains no missing values in Pathway or Metabolites columns and each metabolite identifier is standardized and consistent with input metabolite list.
- Pathway filtering meets min_pathway_occurrence and min_metabolite_occurrence thresholds; pathway counts and metabolite coverage align with documentation.
- Cross-validation: all input metabolites appear in at least one pathway entry (or justified exclusion is documented); no metabolite identifiers in the reference are orphaned or malformed.
- File format validation: CSV or R data.frame loads without parsing errors; row/column structure matches expected schema for downstream Fisher's exact test.
- Reproducibility check: construction workflow (KEGGREST query parameters, Zenodo version tag, filtering thresholds) is fully documented and re-running produces identical results.

## Limitations

- Reference sets are static snapshots; KEGG and other curated databases are updated periodically, so pathway-metabolite assignments may become stale or incomplete over time.
- Metabolite identifier standardization is critical; mismatches between reference identifiers and input identifiers (e.g., KEGG vs. HMDB vs. PubChem) cause spurious null enrichment results.
- Background reference quality directly impacts Fisher's exact test validity; highly incomplete or biased pathway coverage introduces systematic errors in p-value estimation.
- The README notes 'No changelog found', indicating limited version tracking for the reference files, which may complicate reproducibility if external references (Zenodo, KEGG) are updated.

## Evidence

- [readme] This file defines the mapping between metabolic pathways and their associated metabolites and serves as the background reference for the Fisher exact test used during enrichment: "This file defines the mapping between metabolic pathways and their associated metabolites and serves as the background reference for the Fisher exact test used during enrichment"
- [intro] curated human specific pathway to metabolite mappings are periodically updated and made available on Zenodo: "curated human specific pathway to metabolite mappings are periodically updated and made available on Zenodo"
- [intro] pathway to metabolite mappings are obtained from the KEGG resource using the KEGGREST package: "pathway to metabolite mappings are obtained from the KEGG resource using the KEGGREST package"
- [intro] enrichmet integrates fgsea for fast MetSEA, igraph for topology-based metrics, and curated KEGG data for enrichment using Fisher's Exact Test: "enrichmet integrates fgsea for fast MetSEA, igraph for topology-based metrics, and curated KEGG data for enrichment using Fisher's Exact Test"
- [intro] Filter pathways using min_pathway_occurrence parameter (min_pathway_occurrence = 2) and Filter metabolites using min_metabolite_occurrence parameter (min_metabolite_occurrence = 1): "Filter pathways using min_pathway_occurrence parameter and Filter metabolites using min_metabolite_occurrence parameter"
