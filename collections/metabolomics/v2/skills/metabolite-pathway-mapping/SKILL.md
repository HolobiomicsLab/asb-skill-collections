---
name: metabolite-pathway-mapping
description: Use when after metabolite detection and normalization from Metabolomics Workbench format data, when you have a table of metabolite names or identifiers (rows=metabolites, columns=samples) and need to assign pathway membership to compute pathway-level enrichment statistics or visualize.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - Python (pandas, NumPy, SciPy)
  - KEGGREST
  - KEGGgraph
  - pathview
  - MetENP (R package)
  - pandas, dplyr, tidyr
derived_from:
- doi: 10.1101/2020.11.20.391912
  title: MetENP
evidence_spans:
- MetENP
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metenp_cq
    doi: 10.1101/2020.11.20.391912
    title: MetENP
  dedup_kept_from: coll_metenp_cq
schema_version: 0.2.0
---

# metabolite-pathway-mapping

## Summary

Map detected metabolites to pathway and ontology identifiers using cross-reference databases, enabling downstream enrichment analysis and pathway visualization in metabolomics studies. This skill bridges individual metabolite identifications to systems-level pathway context.

## When to use

After metabolite detection and normalization from Metabolomics Workbench format data, when you have a table of metabolite names or identifiers (rows=metabolites, columns=samples) and need to assign pathway membership to compute pathway-level enrichment statistics or visualize metabolite-pathway relationships.

## When NOT to use

- Input metabolites are already annotated with pathway membership and no pathway discovery or re-mapping is needed.
- Metabolite identifiers are unknown or cannot be reliably matched to any reference database (e.g., novel or putative metabolites with no mass match).
- Analysis goal is purely metabolite-level (e.g., classification or clustering) and does not require pathway context or systems-level interpretation.

## Inputs

- Metabolite abundance table (rows=metabolites, columns=samples) in Metabolomics Workbench format
- Normalized metabolite abundances (log-transformed or quantile-normalized)
- Metabolite identifiers (names, KEGG IDs, or RefMet IDs)
- Metabolite-to-pathway cross-reference database (e.g., KEGG, RefMet)

## Outputs

- Annotated metabolite table with pathway identifiers and ontology assignments
- Metabolite-pathway membership matrix
- Pathway information table (pathway IDs, names, reactions, enzymes, genes)
- Pathway network visualization showing metabolite fold-change or abundance patterns

## How to apply

Load the normalized metabolite abundance table and use a metabolite-to-pathway cross-reference database (such as KEGG or RefMet) to map each metabolite identifier to one or more pathway identifiers. For each metabolite, retrieve associated pathway, reaction, enzyme, and gene information. Match metabolites by name, mass, or standardized identifier (e.g., KEGG ID, RefMet ID) against the reference database; resolve ambiguous matches using mass tolerance or manual curation. The output is an annotated metabolite table with pathway assignments that can then be used to compute pathway enrichment scores via Fisher's exact test, hypergeometric test, or rank-based methods, and generate pathway network visualizations showing which metabolites increase or decrease within each pathway.

## Related tools

- **KEGGREST** (Query KEGG database to retrieve pathway, reaction, enzyme, and gene information for mapped metabolites) — https://github.com/Bioconductor/KEGGREST
- **KEGGgraph** (Parse and manipulate KEGG pathway graphs for network-based enrichment and visualization)
- **pathview** (Visualize metabolite abundance or fold-change mapped onto KEGG pathway diagrams)
- **MetENP (R package)** (Comprehensive metabolite enrichment pipeline integrating metabolite-pathway mapping, enrichment scoring, and visualization) — https://github.com/metabolomicsworkbench/MetENP
- **pandas, dplyr, tidyr** (Data manipulation and table joining for metabolite-pathway cross-referencing)

## Examples

```
suppressMessages(library(MetENP)); USER_HOME=Sys.getenv('HOME'); .libPaths(c(paste0(USER_HOME, '/.local/R'), .libPaths())); library('MetENP'); metabolites <- read.csv('metabolite_abundance.csv', row.names=1); mapped <- met_pathways(metabolites, species='hsa'); pathway_info <- pathinfo(mapped)
```

## Evaluation signals

- All metabolites in the input table have been assigned at least one pathway identifier (100% mapping rate, or documented % of unmapped metabolites with justification).
- Pathway assignments are consistent across multiple mapping attempts using the same metabolite identifier and reference database version.
- Pathway network visualization shows expected topology (e.g., connected metabolite–reaction–enzyme–gene subgraphs) and metabolite abundance or fold-change patterns align with known biology in test cases.
- Cross-validation: metabolites known to participate in the same pathway are assigned to the same pathway identifiers; metabolites from different pathways do not overlap.
- Downstream enrichment p-values and adjusted p-values (Benjamini–Hochberg) are computed correctly for pathways with ≥1 mapped metabolites.

## Limitations

- Metabolite mapping accuracy depends on the completeness and currency of the reference database (KEGG, RefMet); novel or recently discovered metabolites may not be present.
- Ambiguous metabolite identifiers (e.g., common names used in multiple species or isomeric metabolites) may map to multiple pathways or incorrect pathways without manual curation.
- Metabolite-pathway relationships are species-specific; cross-species mapping requires species-specific pathway databases and may introduce errors.
- Mass-based matching tolerance (if used) must be chosen carefully to avoid false positives; tight tolerance may miss metabolites with instrument calibration drift.
- Pathway enrichment subsequent to mapping depends on the statistical test chosen; results are sensitive to the multiple-testing correction method and background pathway set.

## Evidence

- [other] Map metabolites to pathway/ontology identifiers using metabolite-to-pathway cross-reference database.: "Map metabolites to pathway/ontology identifiers using metabolite-to-pathway cross-reference database."
- [readme] MetENP is a R package that enables detection of significant metabolites from metabolite information (names or names and concentration along with metadata information) and provides 1. Enrichment score of metabolite class, 2. Maps to pathway of the species of choice, 3. Calculate enrichment score of pathways, 4. Plots the pathways and shows the metabolite increase or decrease 5. Gets gene info, reaction info, enzyme info: "Maps to pathway of the species of choice ... Plots the pathways and shows the metabolite increase or decrease ... Gets gene info, reaction info, enzyme info"
- [readme] MetENP package depends on following Bioconductor packages to function properly: KEGGREST, KEGGgraph, and pathview.: "MetENP package depends on following Bioconductor packages to function properly: KEGGREST, KEGGgraph, and pathview."
- [other] Load metabolite abundance table from Metabolomics Workbench format (rows=metabolites, columns=samples).: "Load metabolite abundance table from Metabolomics Workbench format (rows=metabolites, columns=samples)."
- [other] Compute enrichment statistics (e.g., Fisher's exact test, hypergeometric test, or rank-based enrichment score) for each pathway.: "Compute enrichment statistics (e.g., Fisher's exact test, hypergeometric test, or rank-based enrichment score) for each pathway."
