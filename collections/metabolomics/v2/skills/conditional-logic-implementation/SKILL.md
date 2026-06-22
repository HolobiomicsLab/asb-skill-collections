---
name: conditional-logic-implementation
description: Use when you have a user-submitted spectrum with domain-context metadata (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3373
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
  - Fast Search API
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_microbemasst
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41564-023-01575-9
  all_source_dois:
  - 10.1038/s41564-023-01575-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# conditional-logic-implementation

## Summary

Implement conditional routing logic that maps user-selected domain context (microbial, plant, tissue, microbiome, food, or metadata) to the appropriate standalone MASST web application endpoint. This skill ensures spectrum queries are dispatched to the correct domain-specific MASST tool based on metadata and user selection.

## When to use

Apply this skill when you have a user-submitted spectrum with domain-context metadata (e.g., sample origin, organism kingdom, or explicit domain selection) and need to route it to one of six domain-specific MASST applications (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, metadataMASST) for specialized searching.

## When NOT to use

- Input spectrum lacks domain context metadata or organism/sample origin information — use metadata enrichment or user clarification before routing.
- Batch search across multiple domains simultaneously — use the Fast Search API and jobs.py batch processing instead, which searches all domains in parallel.
- Routing logic is already embedded in the calling application or front-end framework — avoid duplicate conditional implementation.

## Inputs

- user-submitted MS/MS spectrum (in .mgf format or USI reference)
- spectrum metadata containing domain context (organism kingdom, sample type, or explicit domain selection)
- GNPS_MASST repository codebase containing six domain-specific application definitions

## Outputs

- routed spectrum query submitted to the correct domain-specific MASST application endpoint
- domain-specific search results (interactive HTML tree, JSON output, matches.tsv, library.tsv, datasets.tsv, count_domain.tsv)

## How to apply

Parse the user-submitted spectrum metadata to extract the domain-context selection (organism kingdom, sample type, or explicit domain choice). Implement conditional branching logic that maps each domain context to the corresponding MASST application endpoint URL (e.g., masst.gnps2.org/microbemasst/ for microbial domain). Validate routing rules against all six defined domain-specific MASST applications in the GNPS_MASST repository to ensure comprehensive coverage. Test the routing module with representative spectrum submissions (e.g., MS/MS spectra in .mgf format from MZmine or GNPS workflows) across each domain context to confirm correct application dispatch. The routing decision should occur before spectrum submission to the backend Fast Search API, ensuring the query reaches the correct indexed data partition for that domain.

## Related tools

- **GNPS_MASST** (contains the underlying codebase and routing logic for all six standalone web applications; used as source of truth for routing rules and application endpoints) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (target application for microbial domain context; receives routed spectrum queries for bacterial, archaeal, and fungal samples) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (target application for plant domain context; receives routed spectrum queries from plant tissues and organisms) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (target application for tissue domain context; receives routed spectrum queries from human and animal tissue samples) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (target application for microbiome domain context; receives routed spectrum queries from complex microbial community samples) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (target application for food domain context; receives routed spectrum queries from food and beverage samples) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (aggregation application for cross-domain metadata visualization; receives routed aggregated search results from multiple domain queries) — https://masst.gnps2.org/metadatamasst/
- **Fast Search API** (backend service invoked after routing; executes the actual spectrum search against domain-specific indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN) — https://fasst.gnps2.org/fastsearch/

## Examples

```
# Conditional routing in jobs.py context: extract domain and dispatch query
if domain_context == 'microbial':
    endpoint = 'https://masst.gnps2.org/microbemasst/'
elif domain_context == 'plant':
    endpoint = 'https://masst.gnps2.org/plantmasst/'
elif domain_context == 'tissue':
    endpoint = 'https://masst.gnps2.org/tissuemasst/'
# ... route spectrum query to endpoint via Fast Search API
```

## Evaluation signals

- Routed spectrum query reaches the expected domain-specific MASST application endpoint URL (e.g., masst.gnps2.org/microbemasst/ for microbial context).
- Search results returned contain domain-appropriate matches (e.g., microbeMASST results show only microbial organism taxa; plantMASST results show only plant lineage data).
- All six domain contexts (microbial, plant, tissue, microbiome, food, metadata aggregation) route to their corresponding applications without error or fallback.
- Spectrum metadata domain-context field is correctly parsed and matches one of the six defined routing rules before submission to backend API.
- No spectrum queries are submitted to incorrect domain applications or bypass the routing logic entirely.

## Limitations

- Routing logic depends on explicit or unambiguous domain-context metadata in user submission; ambiguous or multi-domain samples may require manual curation or fallback to metadataMASST.
- The six domain-specific MASST applications index non-overlapping subsets of public MS/MS libraries; a single spectrum may return incomplete results if domain context is misspecified.
- Fast Search API has documented retry failures requiring multiple runs of jobs.py to capture all possible matches, which may delay routed query results in batch scenarios.
- Routing does not validate whether the spectrum is compatible with the selected domain (e.g., a plant spectrum routed to microbeMASST will search against inappropriate reference libraries).

## Evidence

- [other] extract the domain-context selection (e.g., microbial, plant, tissue, microbiome, food, or metadata aggregation): "Parse user-submitted spectrum metadata and extract the domain-context selection (e.g., microbial, plant, tissue, microbiome, food, or metadata aggregation)."
- [other] implement conditional routing logic that maps domain context to the corresponding standalone web application endpoint: "Implement conditional routing logic that maps domain context to the corresponding standalone web application endpoint or module."
- [other] validate routing rules against all six domain-specific MASST applications: "Validate routing rules against all six domain-specific MASST applications defined in the GNPS_MASST repository."
- [other] test routing module with representative spectrum submissions across each domain: "Test routing module with representative spectrum submissions across each domain to confirm correct application dispatch."
- [readme] standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
- [readme] six domain-specific MASSTs under development in the Dorrestein Lab including microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST: "This repository contains the code and data for the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego"
- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST."
