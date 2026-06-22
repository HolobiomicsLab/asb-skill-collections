---
name: mass-spectrometry-reference-database-integration
description: Use when you have individual MS/MS spectra or batch .mgf files from untargeted metabolomics experiments and need to search them against domain-specific reference libraries (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3391
  tools:
  - microbeMASST
  - metadataMASST
  - GNPS_MASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - Fast Search API
  - MZmine
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41538-022-00137-3
  title: foodMASST
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
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

# mass-spectrometry-reference-database-integration

## Summary

Integrate standalone mass spectrometry search applications with domain-specific reference databases to enable single-spectrum or batch spectral queries against curated microbe, plant, tissue, microbiome, or food metabolite libraries. This skill configures spectral indexing and deploys web applications that match experimental MS/MS spectra to reference data and generate structured outputs for downstream taxonomic and metabolomic inference.

## When to use

You have individual MS/MS spectra or batch .mgf files from untargeted metabolomics experiments and need to search them against domain-specific reference libraries (e.g., microbial metabolites, plant secondary metabolites) to obtain taxonomic context, spectral matches, and structured aggregation of results across multiple curated datasets. Use this when single-spectrum or batch matching is required and results must be formatted for visualization or Level 2 metabolite annotation.

## When NOT to use

- Input spectra are already Level 3 or Level 4 annotated (i.e., matched library hits are finalized and no re-searching is needed).
- You require targeted MS/MS matching to a custom, non-indexed reference library outside GNPS/MassIVE/Metabolomics Workbench/Metabolights/NORMAN; this skill depends on pre-indexed, curated repositories.
- You need to perform complex post-search statistical filtering or advanced visualization beyond domain-specific trees; metadataMASST aggregation is the endpoint here.

## Inputs

- MS/MS spectra in .mgf format (MZmine export or GNPS molecular networking output)
- Universal Spectrum Identifier (USI) lists in .csv or .tsv format
- Single mass spectrum (for interactive web app queries)
- Domain-specific reference library indexed in GNPS, MassIVE, or partner repositories

## Outputs

- Interactive HTML tree files per domain (_microbe.html, _plant.html, etc.)
- JSON tree structures (_microbe.json, etc.) encoding spectral match hierarchies
- _matches.tsv file listing all matched scans with metadata and similarity scores
- _library.tsv file of GNPS library matches enabling Level 2 metabolite annotation
- _datasets.tsv file with count of unique samples per dataset per query spectrum
- _count_domain.tsv files with per-domain match summaries
- Aggregated and visualized results via metadataMASST

## How to apply

First, clone the GNPS_MASST repository and the domain-specific implementation (e.g., robinschmid/microbe_masst) to obtain standalone web application code and spectral indexing logic. Configure the chosen domainMASST (microbeMASST, plantMASST, etc.) with the appropriate reference library and ensure the indexing pipeline links to current GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN repositories. For batch searches, use jobs.py to define input spectra (as .mgf files, USI lists, or single spectra), set search parameters (cosine similarity threshold, m/z tolerance, minimum matching peaks), and execute the Fast Search API. Re-run the batch job multiple times with skip_existing=True to capture transient API failures. Outputs include domain-specific HTML trees, JSON match hierarchies, TSV files listing matched scans, GNPS library-derived Level 2 annotations, dataset counts, and per-domain match summaries. Validate by confirming that cosine scores and peak matching counts meet your thresholds and that aggregation across domains is complete.

## Related tools

- **GNPS_MASST** (Provides the core standalone web application codebase and Fast Search API for single-spectrum and batch spectral searches) — https://github.com/mwang87/GNPS_MASST
- **microbeMASST** (Domain-specific MASST for microbial metabolite searches; web app instance searches against microbe-curated reference library) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific MASST for plant secondary metabolite searches) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific MASST for tissue-derived metabolite searches) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific MASST for microbiome-associated metabolite searches) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific MASST for food-derived metabolite searches) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (Aggregates and visualizes search outputs across all domainMASSTs into unified interactive results) — https://masst.gnps2.org/metadatamasst/
- **Fast Search API** (Enables batch processing of multiple spectra; accessed via jobs.py for high-throughput spectral matching) — https://fasst.gnps2.org/fastsearch/
- **MZmine** (Recommended tool for generating .mgf export files from raw MS data for input to batch search pipeline) — https://github.com/mzmine/mzmine

## Examples

```
python jobs.py  # after editing jobs.py to add ("spectra.mgf", "output/results") to files list and adjusting cosine_score_min, mz_tolerance, min_matching_peaks parameters
```

## Evaluation signals

- Confirm that all output files are generated (_matches.tsv, _library.tsv, _datasets.tsv, domain-specific HTML and JSON files) and contain non-empty result tables with cosine similarity scores and scan metadata.
- Verify that matched spectra have cosine scores and matching peak counts consistent with your configured thresholds (minimum cosine, m/z tolerance, minimum matching peaks).
- Check that _library.tsv entries are linked to GNPS library entries and comply with Level 2 annotation standards (structure and spectrum match confirmed).
- Ensure that _count_domain.tsv files show expected distribution of matches across domains and that total matches across domain-specific outputs align with _matches.tsv counts.
- Run jobs.py multiple times with skip_existing=True and confirm that no new outputs are generated on the final iteration, indicating convergence and complete API response capture.

## Limitations

- Fast Search API can be unreliable on first execution; the README explicitly recommends running jobs.py multiple times until no new outputs are generated due to transient API failures.
- Reference library coverage depends on current indexing of GNPS, MassIVE, Metabolomics Workbench, Metabolights, and NORMAN; spectra from under-represented organisms or metabolite classes may have low match rates.
- Batch processing requires Python 3.10; version mismatch will cause execution failure.
- Results are constrained to pre-indexed, curated domain-specific taxonomies (e.g., microbeMASST covers 561 genera and 1379 species); queries outside these lineages will not be annotated with domain context.
- Standalone web applications are single-spectrum at a time; batch workflows require jobs.py and the Fast Search API, not the interactive web interface.

## Evidence

- [other] microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database: "microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database"
- [other] Clone the GNPS_MASST repository and the microbeMASST-specific implementation, then deploy the standalone application to accept single-spectrum input queries: "Clone the GNPS_MASST repository from https://github.com/mwang87/GNPS_MASST and the microbeMASST-specific implementation from github.com/robinschmid/microbe_masst"
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data: "Running [jobs.py](https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py) allows users to leverage the [Fast Search API](https://fasst.gnps2.org/fastsearch/) and execute a batch search"
- [readme] A _matches.tsv file will be generated containing all the scans found to match your searched spectrum, and a _library.tsv file enables Level 2 annotation: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed. This includes also samples that are"
- [readme] You can run either a single .mgf file from MZmine or molecular networking, or a list of USIs provided via .csv or .tsv file: "You can run either a single .mgf file generated via [MZmine](https://github.com/mzmine/mzmine), from the molecular networking in GNPS workflow, or a list of"
- [readme] Make sure to run jobs.py a couple of times until no new output is generated due to Fast Search API failures: "Make sure to run [jobs.py](https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py) **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`."
- [readme] Aggregated search outputs can be generated and visualized using metadataMASST: "Aggregated search outputs can be generated and visualized using metadataMASST"
- [readme] microbeMASST covers 8 kingdoms, 20 phyla, 48 classes, 561 genera, 1379 species, and 542 strains: "microbeMASST | 8 | 20 | 48 | 124 | 278 | 561 | 1379 | 542"
