---
name: lipid-identifier-normalization
description: Use when when you have a list of lipids identified by different database
  identifiers (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_3375
  tools:
  - R
  - readr
  - dplyr
  - KEGGREST
  - LION lipid ontology database
  - enrichmet
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
- doi: 10.5281/zenodo.17819145
  title: ''
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed
  through a single R function call
- library(readr)
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
  - 10.5281/zenodo.17819145
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-identifier-normalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Normalize and map lipid identifiers across multiple ontology systems (KEGG, LION, HMDB, PubChem, CHEBI, STITCH) to enable consistent enrichment analysis and cross-database querying. This skill transforms heterogeneous lipid nomenclature into a unified reference frame compatible with pathway and ontology databases.

## When to use

When you have a list of lipids identified by different database identifiers (e.g., KEGG IDs, HMDB IDs, common names) and need to map them to a standardized lipid ontology (such as LION) or cross-reference them across multiple databases for enrichment testing, network analysis, or metabolite-protein interaction lookup.

## When NOT to use

- Input lipids are already formatted in a PathwayVsMetabolites matrix (ontology × lipid) — skip directly to enrichment.
- No reference mapping file or ontology is available for your lipid set — use generic KEGG mappings via KEGGREST instead.
- Your analysis focuses only on lipid abundance or correlation, not on ontology-based enrichment or pathway membership.

## Inputs

- lipid_list (character vector or data.frame with lipid identifiers)
- lipid_ontology_mapping_file (CSV, e.g. LION_Lipid_Ontology.csv, with ontology categories × lipids)
- mapping_df (data.frame with columns: KEGG_ID, HMDB_ID, PubChem_CID, CHEBI_ID, STITCH_ID, Compound_Name)

## Outputs

- normalized_lipid_mapping (data.frame with input lipids linked to ontology categories and cross-database IDs)
- unmapped_lipids (character vector of lipids that could not be resolved)
- coverage_report (numeric: % of input lipids successfully mapped)
- PathwayVsMetabolites_ontology (data.frame in enrichmet-compatible format: ontology categories × normalized lipid IDs for downstream enrichment)

## How to apply

Load your input lipid list and the reference ontology mapping file (e.g., LION_Lipid_Ontology.csv from Zenodo 10.5281/zenodo.17819145) into R as data.frames. Extract and normalize KEGG IDs from complex identifiers (splitting multi-ID fields by '|' delimiter if present). Join the input lipids against the mapping_df using KEGG_ID or alternative identifier columns (HMDB_ID, PubChem_CID, CHEBI_ID, STITCH_ID) to resolve each lipid to its canonical ontology category and metadata. Filter out unmapped lipids and report the match count and coverage. Apply the resulting normalized mapping to downstream analyses (enrichment, centrality, STITCH interaction lookup) using the standardized ontology categories as the reference pathway-to-metabolite structure.

## Related tools

- **readr** (Load lipid list and ontology mapping CSV files into R data.frames)
- **dplyr** (Join, filter, and normalize lipid identifiers across mapping tables)
- **KEGGREST** (Query KEGG for alternative lipid identifiers and pathway-to-metabolite mappings)
- **LION lipid ontology database** (Reference ontology for mapping input lipids to standardized lipid categories) — https://zenodo.org/api/records/17819145/files/LION_Lipid_Ontology.csv/content
- **enrichmet** (Consume normalized lipid mapping as input for Fisher's exact test enrichment against ontology categories) — https://github.com/biodatalab/enrichmet

## Examples

```
library(readr); library(dplyr); lipid_list <- c('C00001', 'C00002', 'C00003'); lion_map <- read_csv('LION_Lipid_Ontology.csv'); mapping_df <- read_csv('mapping_df.csv'); normalized <- lipid_list %>% enframe(name=NULL, value='KEGG_ID') %>% left_join(mapping_df, by='KEGG_ID') %>% left_join(lion_map, by='KEGG_ID'); write_csv(normalized, 'lipid_normalized_mapping.csv')
```

## Evaluation signals

- Coverage metric: ≥80% of input lipids successfully matched to LION or reference ontology categories (report unmapped lipids by name).
- Schema validation: output mapping data.frame contains exactly one row per unique input lipid and columns for all required identifiers (KEGG_ID, ontology_category, HMDB_ID, PubChem_CID, CHEBI_ID, STITCH_ID).
- Consistency check: no duplicate lipid→ontology mappings; each lipid assigned to exactly one primary ontology category.
- Downstream compatibility: the normalized mapping successfully converts to PathwayVsMetabolites format (ontology categories as rows, normalized lipid IDs as comma-separated columns) and runs without error through enrichmet::enrichmet() Fisher's exact test.
- Cross-database alignment: a random sample of 5–10 mapped lipids can be manually verified in KEGG, HMDB, or PubChem to confirm identifier correctness.

## Limitations

- Mapping relies on external reference files (LION, KEGG, STITCH); lipids not in these databases cannot be mapped and must be handled separately.
- Complex KEGG IDs with multiple identifiers (split by '|') are resolved by selecting the first valid ID; context-specific disambiguation may be needed for ambiguous cases.
- STITCH interaction data (chemical_chemical.tsv) may have incomplete coverage for rare or newly discovered lipids; interactions not in STITCH will be absent from network analyses.
- Lipid nomenclature ambiguity (e.g., isomers with identical KEGG IDs) cannot be resolved at this step; m/z and retention time-based validation is recommended post-normalization.
- Ontology mappings are static (based on Zenodo release 10.5281/zenodo.17819145); updates to LION or KEGG may render mappings outdated.

## Evidence

- [other] Load the user-provided lipid list and the LION lipid ontology mapping file (LION_Lipid_Ontology.csv from Zenodo) into R.: "Load the user-provided lipid list and the LION lipid ontology mapping file (LION_Lipid_Ontology.csv from Zenodo) into R"
- [other] Format the lipid list and ontology mapping into a PathwayVsMetabolites-compatible structure with lipid ontology categories as rows and lipids as columns.: "Format the lipid list and ontology mapping into a PathwayVsMetabolites-compatible structure with lipid ontology categories as rows and lipids as columns"
- [readme] Processing complex KEGG IDs (splitting by |)... Split 20 complex IDs into 20 unique KEGG IDs: "Processing complex KEGG IDs (splitting by |)... Split 20 complex IDs into 20 unique KEGG IDs"
- [readme] mapping_df (data.frame with columns: KEGG_ID, HMDB_ID, PubChem_CID, CHEBI_ID, STITCH_ID, Compound_Name): "mapping_df <- data.frame( KEGG_ID = inputMetabolites, HMDB_ID = paste0("HMDB", stringr::str_pad(...)), PubChem_CID = as.character(...), CHEBI_ID = paste0("CHEBI:", ...), STITCH_ID = paste0("CIDs","
- [readme] Successfully extracted KEGG IDs for 23 metabolites... Sample extracted KEGG IDs: C00001, C00002, C00003, C00004, C00005, C00006: "Successfully extracted KEGG IDs for 23 metabolites... Sample extracted KEGG IDs: C00001, C00002, C00003, C00004, C00005, C00006"
- [other] The enrichment workflow successfully adapted to lipidomics by applying Fisher's exact test enrichment analysis against a lipid ontology mapping file generated in the same PathwayVsMetabolites format: "The enrichment workflow successfully adapted to lipidomics by applying Fisher's exact test enrichment analysis against a lipid ontology mapping file generated in the same PathwayVsMetabolites format"
