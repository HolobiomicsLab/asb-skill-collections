---
name: database-similarity-scoring
description: Use when you have one or more MS/MS spectra (query spectra in mzML, mzXML, or MGF format) and need to identify unknown compounds by comparing them against curated spectral databases organized by biological domain (microbe, plant, tissue, microbiome, food).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - GNPS_MASST
  - Fast Search API
  - jobs.py
  - metadataMASST
  techniques:
  - LC-MS
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

# database-similarity-scoring

## Summary

Score and rank mass spectrometry query spectra against domain-specific reference databases using cosine similarity and spectral matching metrics. This skill enables taxonomically informed identification of unknown metabolites by comparing query MS/MS spectra to curated, organism-specific spectral libraries.

## When to use

Apply this skill when you have one or more MS/MS spectra (query spectra in mzML, mzXML, or MGF format) and need to identify unknown compounds by comparing them against curated spectral databases organized by biological domain (microbe, plant, tissue, microbiome, food). Use this when Level 2 metabolomics annotation via spectral matching is the goal, or when you need to understand which organisms or taxa are likely sources of observed metabolites.

## When NOT to use

- Input spectra are already annotated at Level 1 (exact mass match only) and no spectral library matching is needed.
- Query spectra are low-quality (few peaks, weak intensity) or highly fragmented with insufficient peak information for reliable cosine similarity calculation.
- The organism or biological domain of interest is not covered by any available domain-specific MASST tool (e.g., environmental samples from non-standard domains not listed: microbe, plant, tissue, microbiome, food).

## Inputs

- Query mass spectrum (single or multiple) in mzML, mzXML, or MGF format
- Spectrum metadata: precursor m/z, ionization mode, collision energy (optional)
- Search parameters: minimum cosine score threshold, m/z tolerance, minimum matching peaks

## Outputs

- Ranked list of matched spectra with cosine similarity scores
- Library spectrum metadata (compound name, precursor m/z, ionization mode)
- Organism/taxonomy information (NCBI lineage: Kingdom, Phylum, Class, Order, Family, Genus, Species, Strain)
- Domain-specific match counts per MASST (microbe, plant, tissue, microbiome, food)
- Structured output files: _matches.tsv (all matches), _library.tsv (GNPS library matches for Level 2 annotation), _datasets.tsv (dataset-level match summaries), interactive HTML tree visualization

## How to apply

Normalize query spectrum intensities and format metadata (precursor m/z, ionization mode, collision energy if available). Submit the spectrum to the appropriate domain-specific MASST web application or use the Fast Search API via jobs.py for batch processing. Configure search parameters including minimum cosine score (typical threshold ~0.7), m/z tolerance (e.g., 0.1 Da for high-resolution instruments), and minimum matching peaks. The system retrieves ranked matches from the curated domain MASST database, returning match scores alongside library spectrum metadata and organism/taxonomy lineage information. Parse results into structured outputs (TSV/JSON) with similarity scores, specimen metadata, and taxonomic provenance. Re-run batch jobs multiple times with skip_existing=True until no new matches emerge, as the underlying Fast Search API may require retry cycles for complete coverage.

## Related tools

- **microbeMASST** (Domain-specific MASST web application for scoring spectra against curated microbial metabolite library (8 kingdoms, 20 phyla, 48 classes, 1379 species)) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific MASST web application for scoring plant spectra against plant metabolite library (1 kingdom, 11 classes, 3712 species)) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific MASST web application for scoring tissue/organ spectra) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific MASST web application for scoring microbiome spectra) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific MASST web application for scoring food spectra) — https://masst.gnps2.org/foodmasst2/
- **GNPS_MASST** (Standalone web application codebase and API endpoints for single-spectrum similarity scoring against all domain-specific databases) — https://github.com/mwang87/GNPS_MASST
- **Fast Search API** (Backend API for batch scoring of multiple spectra against indexed GNPS/MassIVE, Metabolomics Workbench, MetaboLights, and NORMAN databases) — https://fasst.gnps2.org/fastsearch/
- **jobs.py** (Python 3.10 script for orchestrating batch similarity scoring of multiple spectra (.mgf files or USI lists) across all domain MASSTs via Fast Search API) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py
- **metadataMASST** (Aggregation and visualization tool for consolidated similarity search results across multiple domain MASSTs) — https://masst.gnps2.org/metadatamasst/

## Examples

```
python code/jobs.py  # After populating files list with entries: ('input_spectra.mgf', 'output/batch_001') and setting parameters (min_cosine_score=0.7, mz_tolerance=0.1, min_matching_peaks=6)
```

## Evaluation signals

- Returned match scores are within expected range (0–1 for cosine similarity); all matches meet or exceed the configured minimum cosine score threshold.
- Taxonomy lineage information is complete and consistent with NCBI taxonomy for each matched spectrum (all requested fields: Kingdom through Strain present where applicable).
- Output TSV/JSON files contain all expected columns: match score, library spectrum ID, compound name, precursor m/z, organism lineage, dataset source, and domain MASST origin.
- Batch re-runs with skip_existing=True produce no new matches, indicating convergence and complete coverage by the Fast Search API.
- Domain-specific match counts in _count_domain.tsv files are non-zero for expected domains and zero for irrelevant domains based on query spectrum composition.

## Limitations

- Batch similarity scoring requires Python 3.10; other versions may cause runtime failures.
- Fast Search API returns can be incomplete on first submission; multiple sequential re-runs (with skip_existing=True) are necessary to retrieve all available matches from indexed databases.
- Coverage is limited to indexed datasets in GNPS/MassIVE, Metabolomics Workbench, MetaboLights, and NORMAN; private or offline spectral libraries are not included.
- Domain-specific MASSTs cover only five biological domains (microbe, plant, tissue, microbiome, food); samples outside these categories cannot be scored against curated organism-specific databases.
- Similarity scoring depends on spectrum quality (peak count, intensity distribution); low-quality or highly noisy spectra may produce low cosine scores and fewer reliable matches.

## Evidence

- [other] microbeMASST is a standalone web application accessible at https://masst.gnps2.org/microbemasst/ that enables users to search one spectrum at a time and retrieve matched results.: "microbeMASST is a standalone web application accessible at https://masst.gnps2.org/microbemasst/ that enables users to search one spectrum at a time and retrieve matched results."
- [other] Submit the query spectrum to the microbeMASST web application endpoint and retrieve the ranked list of matching spectra from the microbeMASST database.: "Submit the query spectrum to the microbeMASST web application endpoint and retrieve the ranked list of matching spectra from the microbeMASST database."
- [other] Parse and structure the search results (match scores, library spectrum metadata, organism/taxonomy information) into a machine-readable output table.: "Parse and structure the search results (match scores, library spectrum metadata, organism/taxonomy information) into a machine-readable output table."
- [readme] Running [jobs.py] allows users to leverage the [Fast Search API] and execute a batch search of multiple MS/MS spectra against the current indexed data: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data"
- [readme] Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks: "Check and adjust the different parameters for the search, such as minimum cosine score, mz tolerance, and number of minimum matching peaks"
- [readme] Make sure to run [jobs.py] **_a couple of times_**, until no new output is generated by having the option: `skip_existing=True`. Due to the Fast Search API some of the entries will fail.: "Make sure to run jobs.py a couple of times, until no new output is generated by having the option: skip_existing=True. Due to the Fast Search API some entries will fail."
- [readme] A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed.: "A _matches.tsv file will be generated. This contains all the scans found to match your searched spectrum of interest in the data that have been currently indexed."
- [readme] A _library.tsv file will be generated. This contains a list of spectra from the GNPS libraries found to match your spectrum of interest. This enables a Level 2 annotation according the Metabolomics Standards Initiative.: "A _library.tsv file will be generated enabling a Level 2 annotation according the Metabolomics Standards Initiative."
- [readme] microbeMASST | 8 | 20 | 48 | 124 | 278 | 561 | 1379 | 542: "microbeMASST covers 8 kingdoms, 20 phyla, 48 classes, 124 orders, 278 families, 561 genera, 1379 species, 542 strains"
- [readme] The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
