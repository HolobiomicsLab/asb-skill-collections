---
name: multi-domain-search-result-aggregation
description: Use when you have executed batch searches of MS/MS spectra against multiple domain-specific MASST tools and need to synthesize results across domains (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - GNPS_MASST
  - Fast Search API
  - jobs.py
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41538-022-00137-3
  title: foodMASST
evidence_spans:
- Aggregated search outputs can be generated and visualized using metadataMASST
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_foodmasst_2_cq
    doi: 10.1038/s41538-022-00137-3
    title: foodMASST
  dedup_kept_from: coll_foodmasst_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41538-022-00137-3
  all_source_dois:
  - 10.1038/s41538-022-00137-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-domain-search-result-aggregation

## Summary

Combine and normalize heterogeneous mass spectrometry search outputs from multiple domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) into a unified data structure, then visualize the aggregated results interactively using metadataMASST. This skill enables cross-domain metabolite discovery by merging spectrum matches across taxonomic, plant, tissue, microbiome, and food sample repositories.

## When to use

Apply this skill when you have executed batch searches of MS/MS spectra against multiple domain-specific MASST tools and need to synthesize results across domains (e.g., a single unknown spectrum matched compounds in both microbeMASST and plantMASST, and you want one unified view of all matches ranked by cosine score and coverage across domains). Also use when reporting comparative findings across biological domains or when end-user dashboards must surface matches from all indexed domain repositories simultaneously.

## When NOT to use

- Searches have not yet been executed against the domain-specific MASST tools — run individual batch searches first via jobs.py before aggregating.
- You need single-domain results only (e.g., only microbeMASST matches for a pure microbial metabolomics study) — aggregation adds unnecessary complexity.
- Input spectra are not in MGF format or as validated USIs — metadataMASST aggregation expects output from Fast Search API, which requires standardized input.

## Inputs

- Domain-specific MASST JSON trees (_microbe.json, _plant.json, _tissue.json, _microbiome.json, _food.json)
- Domain-specific MASST HTML tree outputs (_microbe.html, _plant.html, etc.)
- _matches.tsv file containing all spectrum-to-spectrum matches across indexed datasets
- _datasets.tsv file containing match counts per dataset
- Domain-specific _count_domain.tsv files with per-domain match metadata
- Batch input file (MGF, USI list as CSV/TSV)

## Outputs

- Aggregated normalized data structure (unified JSON or relational table of all domain matches)
- Interactive HTML visualization from metadataMASST showing cross-domain match results
- Aggregated TSV table with columns for spectrum ID, matched compound, cosine score, domains represented, and dataset sources
- Domain overlap report (which matches appear in multiple domain-specific MASSTs)

## How to apply

First, execute batch searches via jobs.py against each domain-specific MASST using the Fast Search API with consistent parameters (cosine score threshold, m/z tolerance, minimum matching peaks). Collect the domain-specific output files (_microbe.json, _plant.json, etc.) along with the _matches.tsv and _datasets.tsv files. Normalize each domain's JSON tree structure and TSV match records into a common schema (e.g., unifying field names, standardizing identifier formats, ensuring consistent cosine score ranges). Route all domain outputs into metadataMASST's aggregation layer, which combines heterogeneous records into a single normalized data structure keyed by spectrum match. Finally, invoke metadataMASST's visualization module to render interactive HTML trees and plots showing match density, domain overlap, and ranked hits across all domains. Verify correctness by spot-checking that the total number of unique matches in the aggregated output equals or exceeds the sum of individual domain matches (accounting for overlap).

## Related tools

- **metadataMASST** (Aggregates and visualizes search outputs from all domain-specific MASSTs; implements the aggregation layer and rendering of interactive HTML visualizations) — https://github.com/mwang87/GNPS_MASST
- **GNPS_MASST** (Base framework containing the metadataMASST module and aggregation logic; hosts the aggregation API endpoints and visualization rendering templates) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (Domain-specific MASST tool; produces _microbe.json and _microbe.html outputs integrated into aggregation pipeline)
- **plantMASST** (Domain-specific MASST tool; produces _plant.json and _plant.html outputs integrated into aggregation pipeline)
- **tissueMASST** (Domain-specific MASST tool; produces _tissue.json and _tissue.html outputs integrated into aggregation pipeline)
- **microbiomeMASST** (Domain-specific MASST tool; produces _microbiome.json and _microbiome.html outputs integrated into aggregation pipeline)
- **foodMASST** (Domain-specific MASST tool; produces _food.json and _food.html outputs integrated into aggregation pipeline)
- **Fast Search API** (REST API that executes batch searches of spectra across indexed repositories (GNPS/MassIVE, Metabolomics Workbench, Metabolights, NORMAN); required to generate domain-specific outputs for aggregation) — https://fasst.gnps2.org/fastsearch/
- **jobs.py** (Python 3.10 batch runner that submits spectra to Fast Search API and orchestrates generation of all domain-specific and aggregation outputs) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py

## Examples

```
python jobs.py  # (after populating files list with input MGF and output directory; runs batch search across all domain-specific MASSTs and metadataMASST aggregation with skip_existing=True until convergence)
```

## Evaluation signals

- Verify that the aggregated output contains all unique spectrum–match pairs from individual domain files with no loss of records due to collision or overwrite.
- Cross-check that the sum of matches in domain-specific _count_domain.tsv files, after deduplication by match ID, matches the total count in the aggregated table.
- Confirm that normalized fields (cosine score, m/z tolerance, peak matching thresholds) are consistent across all domain records in the aggregated structure.
- Inspect the interactive HTML visualization from metadataMASST to ensure all domain-specific trees are rendered, clickable, and linked to underlying match data without rendering errors.
- Validate that spectrum IDs and matched compound identifiers are traceable back to their original domain-specific JSON files, confirming no data loss or field mapping errors during aggregation.

## Limitations

- Aggregation requires re-running jobs.py multiple times (until no new outputs are generated) due to transient Fast Search API failures; this can introduce operational latency.
- Domain overlap (spectra matching in multiple domains) is reported but not automatically deduplicated; users must manually inspect overlap regions to avoid duplicate conclusions.
- Visualization scaling may degrade if input contains >10,000 spectrum matches across domains; metadataMASST's interactive rendering is optimized for hundreds to low thousands of matches.
- Only works with spectral data indexed in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN; private or non-deposited spectra cannot be aggregated.

## Evidence

- [other] metadataMASST enables generation and visualization of aggregated search outputs across domain-specific MASST searches: "metadataMASST enables generation and visualization of aggregated search outputs across domain-specific MASST searches, distinguishing it from standalone tools that search one spectrum at a time."
- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [other] Implement aggregation logic to combine heterogeneous search outputs from all domain sources into a single normalized data structure: "Implement aggregation logic to combine heterogeneous search outputs from all domain sources into a single normalized data structure."
- [other] Develop visualization components (plots, tables, interactive elements) to display aggregated results across all domains: "Develop visualization components (plots, tables, interactive elements) to display aggregated results across all domains."
- [readme] A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html: "A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html (e.g., _microbe.html)"
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data: "Running [jobs.py](https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py) allows users to leverage the [Fast Search API](https://fasst.gnps2.org/fastsearch/) and execute a batch search"
- [readme] You can run either a single .mgf file generated via MZmine, from the molecular networking in GNPS workflow, or a list of USIs: "You can run either a single .mgf file generated via [MZmine](https://github.com/mzmine/mzmine), from the molecular networking in GNPS workflow, or a list of"
- [readme] Make sure to run jobs.py a couple of times, until no new output is generated by having the option: skip_existing=True: "Make sure to run [jobs.py](https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py) **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`."
