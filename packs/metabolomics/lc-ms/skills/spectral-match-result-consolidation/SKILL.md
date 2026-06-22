---
name: spectral-match-result-consolidation
description: Use when you have executed batch searches of MS/MS spectra against multiple domain-specific MASST indices and need to integrate the resulting match outputs into a single coherent view.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - Fast Search API
  - jobs.py
  - GNPS_MASST
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- Aggregated search outputs can be generated and visualized using metadataMASST
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
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

# spectral-match-result-consolidation

## Summary

Consolidate and normalize spectral search results from multiple domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) into unified, structured artifacts for visualization and comparative analysis. This skill bridges batch spectral searching across heterogeneous biological domains into a single queryable summary.

## When to use

Apply this skill when you have executed batch searches of MS/MS spectra against multiple domain-specific MASST indices and need to integrate the resulting match outputs into a single coherent view. Use it when you require cross-domain comparison of spectral matches, need to generate interactive visualizations via metadataMASST, or must produce unified reporting tables spanning microbes, plants, tissues, microbiomes, and/or food samples from the same set of input spectra.

## When NOT to use

- Input is a single domain-specific MASST output (e.g., only microbeMASST results) — use direct visualization instead.
- You have not yet executed batch searches and possess only input spectra files (.mgf or USI lists) — first run jobs.py against the Fast Search API to generate domain outputs.
- Results must be searched or re-ranked dynamically — this skill consolidates static output artifacts, not interactive query execution.

## Inputs

- Domain-specific MASST HTML tree files (_microbe.html, _plant.html, _tissue.html, _microbiome.html, _food.html)
- JSON tree outputs from each domain MASST
- TSV match tables (_matches.tsv containing all spectrum matches with scores)
- TSV library tables (_library.tsv with GNPS library annotations)
- TSV dataset count files (_datasets.tsv and _count_domain.tsv)
- Spectrum identifiers (from input .mgf or USI list)

## Outputs

- Unified aggregated match table (TSV) combining all domain results
- Merged JSON structure compatible with metadataMASST web interface
- Interactive HTML summary artifact(s) for visualization
- Validation report confirming completeness and consistency across domains
- Deduplicated spectrum match records with domain source attribution

## How to apply

After executing batch searches via jobs.py against the Fast Search API, collect the domain-specific HTML tree files (_microbe.html, _plant.html, etc.), JSON outputs, and TSV match tables (_matches.tsv, _library.tsv, _datasets.tsv, _count_domain.tsv) generated for each MASST run. Parse and normalize spectrum identifiers, cosine match scores, and metadata fields across all domain outputs using consistent schema. Aggregate records by merging match tables from multiple MASST domains into a unified TSV or JSON structure, deduplicating entries where the same spectrum appears across domains. Validate completeness by cross-checking the total number of unique spectra and ensuring all required metadata columns (sample ID, spectrum match score, domain, dataset source) are populated. Finally, load the aggregated structure into metadataMASST for interactive visualization and summary report generation.

## Related tools

- **metadataMASST** (Ingests aggregated search outputs and generates interactive visualizations and summary artifacts) — https://masst.gnps2.org/metadatamasst/
- **microbeMASST** (Domain-specific spectral search tool; produces domain-tagged match outputs to be consolidated) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific spectral search tool; produces domain-tagged match outputs to be consolidated) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific spectral search tool; produces domain-tagged match outputs to be consolidated) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific spectral search tool; produces domain-tagged match outputs to be consolidated) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific spectral search tool; produces domain-tagged match outputs to be consolidated) — https://masst.gnps2.org/foodmasst2/
- **Fast Search API** (Backend API used by jobs.py to execute batch searches; outputs are inputs to consolidation) — https://fasst.gnps2.org/fastsearch/
- **jobs.py** (Batch search orchestration script that generates domain-specific MASST outputs for downstream consolidation) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py
- **GNPS_MASST** (Parent repository containing standalone web application code for all domain MASSTs) — https://github.com/mwang87/GNPS_MASST

## Examples

```
After executing jobs.py batch searches, consolidate outputs: `python consolidate_masst.py --input_dir ./masst_outputs --output_prefix ./consolidated/summary --validate_schema`
```

## Evaluation signals

- All input domain-specific output files (_microbe.html, _plant.html, etc.) are present and parseable.
- Aggregated match table contains all unique spectra from each input domain with no row duplicates (same spectrum ID, same source dataset).
- Metadata schema is consistent across domain sources: required columns (spectrum_id, cosine_score, domain, dataset) are fully populated and non-null.
- Cross-domain validation: sum of spectrum counts in unified table equals or exceeds the largest individual domain output (accounting for spectra present in multiple domains).
- Aggregated artifact loads successfully into metadataMASST web interface and renders interactive visualization without schema or format errors.

## Limitations

- Consolidation depends on prior successful batch search execution; if jobs.py encounters API timeouts or transient failures, re-runs are needed until no new output is generated (the README recommends running jobs.py multiple times with skip_existing=True).
- Spectrum matching relies on cosine similarity scores from the Fast Search API; consolidation does not re-rank or filter matches—thresholds (minimum cosine, mz tolerance, minimum matching peaks) must be set prior to batch search in jobs.py configuration.
- Consolidation aggregates currently indexed data from GNPS/MassIVE, Metabolomics Workbench, MetaLights, and NORMAN; domain coverage varies by tool (e.g., microbeMASST covers 1379 microbial species vs. plantMASST covers 3712 plant species); coverage limits apply to consolidated results.
- Python 3.10 is required for jobs.py execution; version mismatches may cause script failures upstream of consolidation.

## Evidence

- [other] metadataMASST accepts aggregated search outputs from one or more domain-specific MASST runs and produces visualizable summary artifacts: "metadataMASST accepts aggregated search outputs from one or more domain-specific MASST runs and produces visualizable summary artifacts"
- [other] Parse and normalize search results, extracting spectrum identifiers, match scores, and metadata fields across domain sources; aggregate results by merging records from multiple MASST outputs: "Parse and normalize search results, extracting spectrum identifiers, match scores, and metadata fields across domain sources. 3. Aggregate results by merging records from multiple MASST outputs into"
- [readme] Multiple domain-specific MASST tools are under development in the Dorrestein Lab at UC San Diego for microbes, plants, tissues, microbiomes, and food; aggregated search outputs can be generated and visualized using metadataMASST: "This repository contains the code and data for the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego. This includes microbeMASST, plantMASST,"
- [readme] A _matches.tsv file will be generated containing all the scans found to match your searched spectrum with matches across all indexed data; _library.tsv contains GNPS library matches; _datasets.tsv contains unique sample counts per dataset; _count_domain.tsv files contain domain-specific match information: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed. This includes also samples that are"
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute batch search of multiple MS/MS spectra against indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN to generate outputs for all listed domainMASSTs simultaneously: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
