---
name: spectral-database-output-normalization
description: Use when you have executed batch spectral searches against two or more domain-specific MASST tools and received heterogeneous output formats (domain-specific HTML trees, JSON objects, TSV match tables) that need to be reconciled into a single normalized schema for downstream aggregation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - jobs.py
  - Fast Search API
  - GNPS_MASST
  techniques:
  - tandem-MS
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

# spectral-database-output-normalization

## Summary

Normalize and aggregate heterogeneous mass spectrometry search outputs from multiple domain-specific spectral databases (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) into a unified data structure for cross-domain comparison and visualization. This skill is essential when combining search results across independent MASST tools to enable metaanalysis of spectral matches across biological domains.

## When to use

Apply this skill when you have executed batch spectral searches against two or more domain-specific MASST tools and received heterogeneous output formats (domain-specific HTML trees, JSON objects, TSV match tables) that need to be reconciled into a single normalized schema for downstream aggregation, visualization, or statistical comparison across domains.

## When NOT to use

- Input is a single domain-specific MASST output that does not require cross-domain aggregation or comparison.
- Spectral searches have not yet been executed; normalization requires pre-computed batch outputs from jobs.py runs.
- Output data structure already exists in a unified format (e.g., from a prior metadataMASST run); re-normalization is redundant.

## Inputs

- Domain-specific MASST batch output files (_matches.tsv, _library.tsv, _datasets.tsv, _count_domain.tsv)
- JSON tree files from each MASST domain (_microbe.json, _plant.json, _tissue.json, _microbiome.json, _food.json)
- HTML tree files from batch run for reference (_microbe.html, _plant.html, etc.)
- Input .mgf file or USI list used to generate the batch search

## Outputs

- Unified normalized TSV table with canonical schema across all domains
- Domain-tagged JSON object with all matches cross-indexed by spectrum USI
- Aggregated metadata table with domain counts and match distribution
- Validation report (record counts, score range checks, coverage statistics)
- Input ready for metadataMASST visualization pipeline

## How to apply

Ingest the output files (_matches.tsv, _library.tsv, _datasets.tsv, and _count_domain.tsv files) generated from batch searches via jobs.py executed against each domain-specific MASST. Parse each domain's TSV output to extract common fields: spectrum identifier, matched library entry, cosine similarity score, m/z tolerance applied, and number of matching peaks. Map domain-specific field names and score scales to a canonical schema that preserves all metadata while making scores and identifiers comparable across domains. Implement validation checks to ensure no records are lost during normalization and that all cosine scores fall within the expected [0, 1] range. Apply the same minimum cosine score threshold (typically ≥0.7 per the Fast Search API default) uniformly across all normalized outputs to ensure consistency. Finally, merge normalized records by spectrum USI or scan identifier to create a deduplicated, domain-tagged result set suitable for metadataMASST aggregation and visualization.

## Related tools

- **jobs.py** (Batch execution engine that runs multiple spectra against all domain-specific MASSTs and generates the heterogeneous output files (TSV, JSON, HTML) that are inputs to normalization) — https://github.com/robinschmid/microbe_masst
- **Fast Search API** (Underlying search backend invoked by jobs.py that returns raw spectral matches across indexed databases (GNPS/MassIVE, Metabolomics Workbench, Metabolights, NORMAN); search parameters (cosine, m/z tolerance, min peaks) determine match quality before normalization) — https://fasst.gnps2.org/fastsearch/
- **metadataMASST** (Downstream visualization and aggregation tool that consumes normalized cross-domain outputs to generate interactive plots, tables, and summaries; output of this skill feeds directly into metadataMASST) — https://masst.gnps2.org/metadatamasst/
- **GNPS_MASST** (Parent codebase containing the base MASST framework and metadataMASST component code; normalization logic integrates with the aggregation layer defined in this repository) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (Domain-specific MASST tool for microbial metabolomics; one source of heterogeneous outputs to be normalized) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific MASST tool for plant metabolomics; one source of heterogeneous outputs to be normalized) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific MASST tool for tissue metabolomics; one source of heterogeneous outputs to be normalized) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific MASST tool for microbiome metabolomics; one source of heterogeneous outputs to be normalized) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific MASST tool for food metabolomics; one source of heterogeneous outputs to be normalized) — https://masst.gnps2.org/foodmasst2/

## Evaluation signals

- All input records from each domain-specific MASST output are present in the normalized table; record count audit confirms no loss during transformation.
- Cosine similarity scores across all domains fall within the valid range [0, 1] and distribution statistics (mean, median, percentiles) are consistent with Fast Search API defaults (typically ≥0.7 for matches).
- Domain tags are correctly assigned and preserved; querying the normalized table by domain returns the exact subset count reported in the original _count_domain.tsv files.
- Spectrum USI or scan identifiers are unique and consistent across all normalized records; no spurious duplicates introduced during merge.
- Schema validation passes: all mandatory fields (spectrum_id, library_id, cosine_score, domain, m/z_tolerance, matching_peaks) are populated; no NULL or malformed entries remain.

## Limitations

- Heterogeneity in taxonomic or chemical annotation metadata between domains may result in information loss if canonical schema does not preserve all domain-specific fields; mapping must be conservative to avoid dropping domain metadata.
- The Fast Search API may fail on some entries during batch execution; jobs.py must be run multiple times (with skip_existing=True) to catch all possible matches, and normalization should account for partial result sets.
- Python 3.10 is required for jobs.py execution; version mismatches may cause import or runtime failures before outputs are generated, preventing normalization.
- Minimum cosine score threshold and m/z tolerance applied during search are fixed at batch time; normalization cannot retroactively adjust thresholds, so re-running jobs.py with different parameters is necessary if downstream analysis requires stricter or looser criteria.

## Evidence

- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [other] Implement aggregation logic to combine heterogeneous search outputs from all domain sources into a single normalized data structure: "Implement aggregation logic to combine heterogeneous search outputs from all domain sources into a single normalized data structure"
- [readme] A series of _count_domain.tsv files will be generated, containing information on matches found for each specific domain MASST: "A series of _count_domain.tsv files will be generated, containing information on matches found for each specific domain MASST"
- [readme] A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest"
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra"
