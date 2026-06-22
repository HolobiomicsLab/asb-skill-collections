---
name: spectral-match-interpretation
description: Use when you have obtained search results from one or more domain-specific MASST web applications (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) for a query mass spectrum and need to consolidate, rank, and visualize those matches to infer the identity and biological source of.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - microbeMASST
  - metadataMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - GNPS_MASST
  - jobs.py
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
  - build: coll_microbemasst_cq
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst_cq
schema_version: 0.2.0
---

# spectral-match-interpretation

## Summary

Interprets ranked spectral matches returned from domain-specific MASST tools by aggregating results across microbe, plant, tissue, microbiome, and food domains, then visualizing and consolidating hits with associated metadata to enable cross-domain metabolite identification.

## When to use

You have obtained search results from one or more domain-specific MASST web applications (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) for a query mass spectrum and need to consolidate, rank, and visualize those matches to infer the identity and biological source of the metabolite.

## When NOT to use

- Input is a single query spectrum without prior MASST search results — run domain-MASST search first
- Goal is to retrieve new spectral matches rather than interpret existing results — use domain-MASST web applications or Fast Search API directly
- You need Level 1 (confirmed structure) or Level 3 (bioactive compound) annotation that metadataMASST cannot provide; metadataMASST generates Level 2 (probable structure) consensus

## Inputs

- ranked spectral match lists with cosine similarity scores from microbeMASST
- ranked spectral match lists with cosine similarity scores from plantMASST
- ranked spectral match lists with cosine similarity scores from tissueMASST
- ranked spectral match lists with cosine similarity scores from microbiomeMASST
- ranked spectral match lists with cosine similarity scores from foodMASST
- library spectrum metadata (organism, taxonomy, collision energy, ionization mode)
- query spectrum metadata (precursor m/z, ionization mode, collision energy)

## Outputs

- consolidated match table (CSV or TSV with merged hits, similarity scores, metadata)
- interactive HTML tree visualizations per domain (_microbe.html, _plant.html, etc.)
- JSON tree files for programmatic downstream analysis
- _matches.tsv file containing all matching spectra with scores
- _library.tsv file containing GNPS library matches (Level 2 annotation)
- _datasets.tsv file with count of unique samples per dataset
- domain-specific count tables (_count_domain.tsv)
- aggregated visualization showing cross-domain hit distribution and score rankings

## How to apply

Load aggregated search outputs (ranked match lists with cosine similarity scores and library metadata) from domain-specific MASSTs into metadataMASST. Process and consolidate the results by merging hits, similarity scores, and taxonomy/organism metadata across domains. Generate interactive visualizations (e.g., hit distribution plots, score rankings, domain overlap) to identify high-confidence matches and cross-domain consensus. Export the consolidated results with embedded visualizations in structured format (HTML trees, JSON, or TSV tables). Use cosine similarity thresholds and minimum peak-matching criteria (configurable during batch search, typically adjusted via parameters in jobs.py) to filter low-confidence matches, then compare the ranked scores and metadata consistency across domains to judge annotation confidence.

## Related tools

- **metadataMASST** (web application that processes and consolidates aggregated domain-MASST search outputs and generates cross-domain visualizations) — https://masst.gnps2.org/metadatamasst/
- **microbeMASST** (domain-specific MASST for microbial metabolomics that returns ranked spectral matches against microbial reference database) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (domain-specific MASST for plant metabolomics that returns ranked spectral matches against plant reference database) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (domain-specific MASST for tissue metabolomics that returns ranked spectral matches against tissue reference database) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (domain-specific MASST for microbiome metabolomics that returns ranked spectral matches against microbiome reference database) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (domain-specific MASST for food metabolomics that returns ranked spectral matches against food reference database) — https://masst.gnps2.org/foodmasst2/
- **GNPS_MASST** (code repository containing implementation of all domain-specific standalone web applications and batch search infrastructure) — https://github.com/mwang87/GNPS_MASST
- **jobs.py** (batch execution script for searching multiple spectra against all domainMASSTs via Fast Search API and generating multi-domain outputs) — https://github.com/robinschmid/microbe_masst
- **Fast Search API** (backend API enabling batch search of multiple MS/MS spectra against indexed data in GNPS/MassIVE, Metabolomics Workbench, MetaboLights, and NORMAN) — https://fasst.gnps2.org/fastsearch/

## Examples

```
python jobs.py  # After configuring input_file, output_prefix, and parameters (min_cosine_score, mz_tolerance, min_matching_peaks) in jobs.py, execute batch search against all domainMASSTs; re-run until skip_existing=True produces no new files
```

## Evaluation signals

- Consolidated match table contains all input domain results merged with no duplicate rows; verify by counting rows and checking for duplicate (spectrum_id, match_score) pairs
- Cosine similarity scores in output fall within expected range (0–1) and are consistent with input domain-MASST scores; spot-check top 10 matches
- HTML tree visualizations render without errors and display hierarchical hit distribution with domain labels and scores visible
- GNPS library matches achieve Level 2 annotation status (probable structure) with recorded cosine similarity ≥ minimum threshold set in batch parameters
- Cross-domain consensus: metabolites appearing in ≥2 domains with consistent top-ranked match should indicate high-confidence annotation; check for agreement in library ID and organism taxonomy

## Limitations

- metadataMASST requires pre-computed aggregated outputs from individual domain MASSTs; it does not perform the initial spectral search itself
- Batch search via jobs.py may require multiple re-runs to catch all Fast Search API failures; the README notes 'sequent re-runs should catch all the possible matches'
- Python 3.10 is required; compatibility with other Python versions is not documented
- Visualization quality and cross-domain consensus depend on the completeness and curation of underlying domain-specific reference databases; some domains (e.g., microbiomeMASST) have fewer indexed species than others (microbeMASST: 1379 species; plantMASST: 3712 species)
- Results exclude matches outside currently indexed datasets (GNPS, MassIVE, Metabolomics Workbench, MetaboLights, NORMAN); newer or proprietary datasets are not covered

## Evidence

- [intro] metadataMASST takes aggregated search outputs from domain-specific MASSTs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST) and generates visualized aggregated results: "metadataMASST takes aggregated search outputs from domain-specific MASSTs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST) and generates visualized aggregated results as its"
- [other] workflow for metadataMASST result interpretation: "Load aggregated domain-MASST search outputs (from one or more domain-specific MASST tools: microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) as input. 2. Process and consolidate"
- [readme] batch search output types: "A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html (e.g., _microbe.html); A series of JSON files for the different trees will be"
- [readme] library annotation level and metadata: "A _library.tsv file will be generated. This contains a list of spectra from the GNPS libraries found to match your spectrum of interest. This enables a Level 2 annotation according the Metabolomics"
- [readme] requirement for multiple batch search runs: "Make sure to run jobs.py **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`. Due to the Fast Search API some of the entries will fail."
- [readme] Python version requirement: "Please make user to use **_Python 3.10_**"
