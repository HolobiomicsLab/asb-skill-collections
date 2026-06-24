---
name: taxonomy-metadata-extraction
description: Use when you have executed a spectrum search against one or more domain-specific
  MASSTs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, or foodMASST) and
  need to systematically extract taxonomic lineages (kingdom, phylum, class, order,
  family, genus, species, strain) and sample metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0637
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - GNPS_MASST
  - Fast Search API
  - jobs.py
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41564-023-01575-9
  all_source_dois:
  - 10.1038/s41564-023-01575-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# taxonomy-metadata-extraction

## Summary

Extract and structure taxonomic lineage information and associated metadata from domain-specific MASST search results to enable organism-level interpretation and filtering of mass spectrometry matches. This skill transforms ranked spectral matches into organism-annotated datasets suitable for downstream ecological or metabolomic analysis.

## When to use

Apply this skill when you have executed a spectrum search against one or more domain-specific MASSTs (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, or foodMASST) and need to systematically extract taxonomic lineages (kingdom, phylum, class, order, family, genus, species, strain) and sample metadata from the returned matches to answer organism-level research questions or filter results by taxonomy.

## When NOT to use

- Input spectra have not yet been searched against a domain-specific MASST; use spectral search first.
- Taxonomy information is not available or not required for your analysis; this skill is specific to organism-level interpretation.
- Your data comes from untargeted metabolomics without reference libraries or public GNPS/MassIVE datasets; domain-specific MASSTs index only curated public repositories.

## Inputs

- ranked spectral match results from microbeMASST or domain-specific MASST web application (JSON or structured API response)
- library spectrum metadata including organism/taxonomy fields and NCBI taxonomy IDs
- domain-specific lineage reference tables (CSV or TSV; e.g., from the lineages folder)

## Outputs

- enriched match table with columns for match score, similarity metrics, organism name, and full taxonomic lineage (kingdom, phylum, class, order, family, genus, species, strain)
- CSV or JSON file containing all matches annotated with standardized NCBI taxonomy IDs and lineage strings
- optionally, filtered or grouped subsets of results by taxonomic rank (e.g., genus-level or phylum-level summaries)

## How to apply

Parse the structured search results returned by the microbeMASST or other domain-specific MASST standalone web application to extract library spectrum metadata and associated organism/taxonomy information. Use the lineage information available within each domain-specific MASST (e.g., microbeMASST currently covers 8 kingdoms, 20 phyla, 48 classes, etc.) to enrich each match record with full taxonomic classification from kingdom to strain level. Structure the extracted taxonomic and metadata fields into a machine-readable table (CSV or JSON), preserving match scores and similarity metrics alongside the taxonomy. Apply domain-specific lineage lookup tables (available in the lineages folder of the repository) to standardize NCBI taxonomy IDs and resolve any incomplete or ambiguous taxonomy strings. Filter or group results by specific taxonomic ranks or organism names according to your research question before saving the enriched output.

## Related tools

- **microbeMASST** (domain-specific MASST web application that returns ranked spectral matches with organism/taxonomy metadata for microbial metabolomics data) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (domain-specific MASST web application returning spectral matches with plant taxonomy information) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (domain-specific MASST web application for tissue metabolomics with associated organism lineage data) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (domain-specific MASST web application for microbiome samples with taxonomic annotation) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (domain-specific MASST web application for food metabolomics with organism-level metadata) — https://masst.gnps2.org/foodmasst2/
- **GNPS_MASST** (source code repository providing the standalone web application framework that accepts a single query spectrum and returns structured search results with library metadata) — https://github.com/mwang87/GNPS_MASST
- **Fast Search API** (backend API used by jobs.py to execute batch searches against indexed GNPS/MassIVE, Metabolomics Workbench, Metabolights, and NORMAN data with taxonomic metadata) — https://fasst.gnps2.org/fastsearch/
- **jobs.py** (batch processing script that leverages the Fast Search API and generates domain-specific MASST outputs including _count_domain.tsv files with taxonomy-specific match counts) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py

## Examples

```
python code/jobs.py  # Configure jobs.py with input .mgf file and output prefix, then extract taxonomy by reading generated _count_domain.tsv and _matches.tsv files; lineage tables are in the lineages/ folder for NCBI ID lookup.
```

## Evaluation signals

- All returned spectra are annotated with a complete taxonomic lineage (kingdom, phylum, class, order, family, genus, species where available) and at least one NCBI taxonomy ID that can be validated against NCBI Taxonomy database.
- Output table schema matches the expected structure: columns include original match score/cosine similarity alongside all taxonomic ranks and organism metadata without data loss or truncation.
- Taxonomy strings are standardized and internally consistent; if the same organism appears in multiple rows, its full lineage is identical across all occurrences.
- Domain-specific count files (_count_domain.tsv for microbeMASST, plantMASST, etc.) show non-zero match counts only for organisms present in the curated lineage reference for that domain.
- Extracted metadata can be successfully grouped or filtered by any taxonomic rank without errors, and subset results are reproducible across multiple invocations with identical input.

## Limitations

- Taxonomy coverage is limited to organisms already indexed in the domain-specific MASST; microbeMASST covers 1,379 microbial species and plantMASST covers 3,712 plant species, but rare or newly described organisms may not be present.
- Strain-level taxonomy is available only where indexed in the source libraries; microbeMASST provides 542 strain entries but plantMASST has no strain-level data (marked NA in README).
- Lineage information depends on NCBI Taxonomy IDs provided by library submitters; erroneous or outdated taxonomy IDs in the original library entry will propagate into extracted metadata.
- Batch searches using jobs.py may require multiple re-runs (until no new output is generated) due to transient failures in the Fast Search API; this introduces uncertainty in completeness of taxonomy extraction on first invocation.
- Output files are generated only for spectra that exceed the minimum cosine score and peak-matching thresholds configured by the user; taxonomy extraction will not occur for low-confidence matches.

## Evidence

- [other] parse and structure the search results (match scores, library spectrum metadata, organism/taxonomy information) into a machine-readable output table: "Parse and structure the search results (match scores, library spectrum metadata, organism/taxonomy information) into a machine-readable output table."
- [readme] lineage information of each NCBI taxonomy IDs used in microbeMASST and plantMASST: "Within the folder lineages you can find the complete lineage information of each NCBI taxonomy IDs used in microbeMASST and plantMASST."
- [readme] microbeMASST currently covers taxonomy at kingdom through strain levels: "| microbeMASST | 8 | 20 | 48 | 124 | 278 | 561 | 1379 | 542 |"
- [readme] batch search generates domain-specific outputs with match counts per taxonomy: "A series of _count_domain.tsv files will be generated, containing information on matches found for each specific domain MASST."
- [readme] search results include library spectrum metadata with organism information: "A _library.tsv file will be generated. This contains a list of spectra from the GNPS libraries found to match your spectrum of interest."
