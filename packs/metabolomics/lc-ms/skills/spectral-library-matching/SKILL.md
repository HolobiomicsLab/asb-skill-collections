---
name: spectral-library-matching
description: 'Use when you have one or more MS/MS spectra in .mgf format (or USI identifiers) and need to: (1) identify unknowns by searching against domain-curated reference data; (2) assign Level 2 metabolomics annotations via GNPS library matches; (3) aggregate matches across organism lineages (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - microbeMASST
  - metadataMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - GNPS_MASST
  - GNPS libraries
  - Fast Search API
  - MZmine
  - MASSBANK
  - DrugBANK
  - meRgeION2
  - MergeION2
  - GNPS
  - RChemMass
  - MS2Compound
  - CFM-id
  - mssearchr
  - R
  - NIST API
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41538-022-00137-3
  title: foodMASST
- doi: 10.1021/acs.analchem.2c04343
  title: ''
- doi: 10.1089/omi.2021.0051
  title: ''
- doi: 10.1021/jasms.5c00322
  title: ''
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
- search and annotate an unknown spectrum in their local database or public databases (i.e. drug structures in GNPS, MASSBANK and DrugBANK)
- github.com__daniellyz__meRgeION2
- MS2Compound (v1.0.2) is a user friendly Graphical User Interface (GUI) for the identification of the compounds from LC-MS and MS/MS metabolomics data
- compatible with the customized database prepared using CFM-id, the fragment prediction tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_flash_entropy_search_cq
    doi: 10.1038/s41592-023-02012-9
    title: Flash entropy search
  - build: coll_foodmasst_2_cq
    doi: 10.1038/s41538-022-00137-3
    title: foodMASST
  - build: coll_mergeion_cq
    doi: 10.1021/acs.analchem.2c04343
    title: MeRgeION
  - build: coll_ms2compound_cq
    doi: 10.1089/omi.2021.0051
    title: MS2Compound
  - build: coll_mspepsearchr_cq
    doi: 10.1021/jasms.5c00322
    title: mspepsearchr
  dedup_kept_from: coll_foodmasst_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41538-022-00137-3
  all_source_dois:
  - 10.1038/s41538-022-00137-3
  - 10.1021/acs.analchem.2c04343
  - 10.1089/omi.2021.0051
  - 10.1021/jasms.5c00322
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-matching

## Summary

Match mass spectrometry spectra against domain-specific reference libraries using cosine similarity scoring to identify compounds and assign taxonomic or sample-origin metadata. This skill enables single-spectrum or batch searches across curated domain MASSTs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) and federated public repositories (GNPS libraries, MassIVE, Metabolomics Workbench, MetaboLights, NORMAN).

## When to use

Apply this skill when you have one or more MS/MS spectra in .mgf format (or USI identifiers) and need to: (1) identify unknowns by searching against domain-curated reference data; (2) assign Level 2 metabolomics annotations via GNPS library matches; (3) aggregate matches across organism lineages (e.g., microbe strain/species/genus) or plant taxa; or (4) quantify the distribution of spectral matches across indexed datasets. Particularly appropriate when your input spectra are from a domain of known biology—microbes, plants, tissues, microbiomes, or food samples—and you want to leverage taxonomic metadata enrichment.

## When NOT to use

- Your spectra are not MS/MS data or are in a format not convertible to .mgf (e.g., raw vendor instrument files without prior conversion).
- You seek unknown compound identification without any domain context—batch MASST searches assume the biology is known (e.g., sample is from microbes, plants, or food); general-purpose spectral libraries may be more appropriate.
- Your reference library is not indexed in GNPS, MassIVE, Metabolomics Workbench, MetaboLights, or NORMAN, or you require real-time updates to a private spectrum collection—domainMASSTs query only the current indexed datasets.

## Inputs

- .mgf file (MS/MS spectra in mascot generic format)
- USI list (.csv or .tsv with Universal Spectrum Identifiers)
- Cosine similarity threshold (default 0.7)
- m/z tolerance in Da (default ±0.1)
- Minimum matching peaks (default 6)

## Outputs

- Interactive HTML tree files per domain (_domain.html, e.g., _microbe.html)
- JSON tree files per domain (_domain.json)
- _matches.tsv (all scans matching the queried spectrum)
- _library.tsv (GNPS library matches for Level 2 annotation)
- _datasets.tsv (unique samples per indexed dataset)
- _count_domain.tsv files (domain-specific match counts)

## How to apply

Prepare MS/MS spectra in .mgf format (e.g., exported from MZmine or GNPS molecular networking) or as a .csv/.tsv list of Universal Spectrum Identifiers (USIs). Configure search parameters: set a minimum cosine similarity threshold (typically 0.7 for high stringency), m/z tolerance (commonly ±0.1 Da), and a minimum number of matching peaks (e.g., ≥6). Submit the query to the domain-specific MASST web application (e.g., microbeMASST for bacterial/archaeal spectra) or execute batch searches via the Fast Search API (jobs.py script). The search algorithm computes cosine similarity scores between your spectra and all indexed reference spectra in the domain library and federated repositories. Iterate batch runs (re-run jobs.py until no new outputs are generated) to capture all matches despite occasional API failures. Outputs include interactive HTML trees per domain, JSON trees, a _matches.tsv file (all matched scans), a _library.tsv file (GNPS library hits for Level 2 annotation), a _datasets.tsv file (match counts per dataset), and _count_domain.tsv files summarizing domain-specific hits.

## Related tools

- **microbeMASST** (Domain-specific spectral library for microbial metabolomics; indexes 1379 microbial species and 542 strains across 8 kingdoms, 20 phyla, 48 classes, 124 orders, 278 families, 561 genera.) — https://github.com/robinschmid/microbe_masst
- **plantMASST** (Domain-specific spectral library for plant metabolomics; indexes 3712 plant species across 1 kingdom, 1 phylum, 11 classes, 81 orders, 319 families, 1796 genera.) — https://github.com/robinschmid/microbe_masst
- **tissueMASST** (Domain-specific spectral library for tissue-derived metabolomics data.) — https://github.com/robinschmid/microbe_masst
- **microbiomeMASST** (Domain-specific spectral library for microbiome sample metabolomics.) — https://github.com/robinschmid/microbe_masst
- **foodMASST** (Domain-specific spectral library for food metabolomics.) — https://github.com/robinschmid/microbe_masst
- **metadataMASST** (Visualization and aggregation of search outputs from multiple domainMASSTs.) — https://github.com/robinschmid/microbe_masst
- **GNPS_MASST** (Core web application framework providing standalone search interfaces and the Fast Search API for batch querying across domain MASSTs.) — https://github.com/mwang87/GNPS_MASST
- **GNPS libraries** (Reference spectral library indexed by domainMASSTs; used to generate Level 2 metabolomics annotations.)
- **Fast Search API** (Backend API for batch search of multiple spectra against all indexed domainMASSTs and federated repositories.) — https://fasst.gnps2.org/fastsearch/
- **MZmine** (Preprocessing tool to generate .mgf files suitable for import into domainMASST batch search.) — https://github.com/mzmine/mzmine

## Examples

```
python jobs.py  # After configuring input files and parameters (minimum cosine score, m/z tolerance, minimum matching peaks) in jobs.py, then re-run until skip_existing=True yields no new outputs
```

## Evaluation signals

- Cosine similarity scores for all returned matches fall within the specified threshold (≥ minimum cosine score parameter).
- All matched spectra in _matches.tsv show m/z differences ≤ the specified tolerance; number of matching peaks ≥ minimum threshold.
- Level 2 annotations in _library.tsv correspond to GNPS library entries; presence of _library.tsv confirms successful library matching.
- _datasets.tsv and _count_domain.tsv files contain non-zero match counts for at least one domain, confirming indexing and search execution.
- Re-running jobs.py with `skip_existing=True` produces no new output files, indicating convergence and complete API query coverage.

## Limitations

- Due to the Fast Search API, some entries may fail on first execution; re-running jobs.py is necessary to achieve complete match recovery. Python 3.10 is required.
- domainMASSTs query only currently indexed datasets (GNPS/MassIVE, Metabolomics Workbench, MetaboLights, NORMAN); private or recently-added reference spectra are not discoverable until indexed in one of these federated repositories.
- Batch search outputs include matches from all indexed data, not only the curated domain-specific subset; filtering by _count_domain.tsv is necessary if domain-specific matches alone are desired.
- Single-spectrum searches via the standalone web applications (microbeMASST, plantMASST, etc.) return matches but do not generate the full suite of tabular outputs; batch scripts (jobs.py) are required for comprehensive .tsv export.
- Cosine similarity scoring assumes comparable ionization and mass analyzer settings between query and library spectra; significant instrumental differences may reduce match quality.

## Evidence

- [readme] The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
- [readme] Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [readme] A _library.tsv file will be generated. This contains a list of spectra from the GNPS libraries found to match your spectrum of interest. This enables a Level 2 annotation according the Metabolomics Standards Initiative.: "A _library.tsv file will be generated. This contains a list of spectra from the GNPS libraries found to match your spectrum of interest. This enables a Level 2 annotation according the Metabolomics"
- [readme] Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks based on your research question.: "Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks based on your research question."
- [readme] You can run either a single .mgf file generated via MZmine, from the molecular networking in GNPS workflow, or a list of USIs provided either via a .csv or .tsv file.: "You can run either a single .mgf file generated via MZmine, from the molecular networking in GNPS workflow, or a list of USIs provided either via a .csv or .tsv file."
- [readme] Make sure to run jobs.py a couple of times, until no new output is generated by having the option: skip_existing=True. Due to the Fast Search API some of the entries will fail.: "Make sure to run jobs.py a couple of times, until no new output is generated by having the option: skip_existing=True. Due to the Fast Search API some of the entries will fail."
- [other] microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database: "microbeMASST is implemented as a standalone web application that accepts individual mass spectra as input and performs searches against a microbe-specific reference database"
- [readme] Within the folder lineages you can find the complete lineage information of each NCBI taxonomy IDs used in microbeMASST and plantMASST. These tools currently cover microbeMASST: 1379 species, plantMASST: 3712 species: "Within the folder lineages you can find the complete lineage information of each NCBI taxonomy IDs used in microbeMASST and plantMASST. These tools currently cover microbeMASST: 1379 species,"
