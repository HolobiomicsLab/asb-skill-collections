---
name: ms2-spectral-similarity-scoring
description: Use when after temporal intensity profile correlation and exact mass
  difference refinement have identified candidate ion-species pairs in direct-injection
  plasma ionization MS data (e.g., DBDI-MS, DBDI-FT-ICR-MS).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DBDIpy
  - Python
  - matchms
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btad088/7036334
  title: DBDIpy
evidence_spans:
- DBDIpy is an open-source Python library for the curation and interpretation of dielectric
  barrier discharge ionisation mass spectrometric datasets
- DBDIpy is an open-source Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbdipy_cq
    doi: 10.1093/bioinformatics/btad088/7036334
    title: DBDIpy
  dedup_kept_from: coll_dbdipy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btad088/7036334
  all_source_dois:
  - 10.1093/bioinformatics/btad088/7036334
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2 spectral similarity scoring for ion-pair confirmation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute cosine similarity or related spectral matching scores between MS2 fragment ion profiles to confirm that candidate ion-species pairs originate from the same analyte compound. This is the final refinement step in a three-stage DBDIpy identification pipeline following temporal correlation and exact mass difference analysis.

## When to use

After temporal intensity profile correlation and exact mass difference refinement have identified candidate ion-species pairs in direct-injection plasma ionization MS data (e.g., DBDI-MS, DBDI-FT-ICR-MS). Use this skill when MS2 fragment spectra are available for the candidate pairs and you need to confirm shared analyte origin rather than false positives from mass or temporal coincidence alone.

## When NOT to use

- MS2 fragmentation data are not available or unreliable (e.g., low signal-to-noise ratio, insufficient fragment peaks)
- Candidate pairs come from methods that already enforce orthogonal confirmation (e.g., paired chromatography or isotope labeling)
- Input data are already curated feature tables without raw MS spectra or fragment ion information

## Inputs

- MS2 spectral data (fragment m/z-intensity pairs for each precursor ion)
- Candidate ion-species pair list (output from mass difference refinement step)
- Preprocessed feature table with imputed intensities
- Mass spectrometric parameters (e.g., resolution, fragmentation method)

## Outputs

- Annotated candidate pair table with MS2 spectral similarity scores
- Confirmation status (binary: confirmed/unconfirmed) per pair
- Filtered list of confirmed shared-analyte ion pairs
- Summary metrics of similarity score distribution

## How to apply

Extract and preprocess MS2 fragment spectra for each candidate ion-species pair (normalize intensity, remove noise). Calculate MS2 spectral similarity score using cosine similarity or equivalent spectral matching algorithm between the normalized fragment profiles of the pair. Annotate each pair with its similarity score and apply an acceptance threshold (e.g., cosine similarity > 0.7 or equivalent) to flag pairs as confirmed shared-analyte relationships. Generate an output table mapping candidate pairs to their spectral similarity scores and confirmation status. This third step is critical because direct-injection data lacks chromatographic separation, making temporal and mass information alone insufficient to distinguish true adducts/fragments from unrelated features.

## Related tools

- **DBDIpy** (Core library implementing the three-step identification procedure; wraps MS2 spectral similarity scoring step after temporal correlation and mass difference analysis) — https://github.com/leopold-weidner/DBDIpy
- **matchms** (Ecosystem library integrated into DBDIpy for MS data handling, spectral alignment, and spectral matching algorithms)
- **Python** (Programming language; required runtime for DBDIpy and spectral similarity calculations)

## Evaluation signals

- All candidate pairs from the input list are assigned a numeric similarity score (no missing values)
- Similarity scores fall within the expected range for the algorithm used (0–1 for cosine similarity)
- Output table row count matches input candidate pair count
- Confirmed pairs exhibit visually or statistically coherent fragment patterns when compared side-by-side
- Threshold acceptance rate is within expected range given the precision of prior correlation and mass difference steps (e.g., >50% confirmation typical for high-confidence candidates)

## Limitations

- MS2 spectral similarity scoring depends on quality and completeness of fragment ion data; low signal-to-noise spectra or sparse fragmentation may yield unreliable scores
- Cosine similarity and related metrics assume that similar fragments indicate shared analyte origin, but can fail if two different compounds produce accidentally similar fragmentation patterns
- Threshold selection is user-defined; no universally optimal cutoff is provided; performance is sensitive to choice of acceptance threshold
- Direct-injection data inherently lack chromatographic separation, so multiple analytes can co-ionize and generate spurious fragment overlaps despite temporal correlation steps

## Evidence

- [other] DBDIpy implements a three-step identification procedure in which MS2 spectral similarity scoring is the final step: "DBDIpy implements a three-step identification procedure in which MS2 spectral similarity scoring is the final step, following pointwise correlation analysis of temporal intensity profiles and exact"
- [other] Extract, preprocess, calculate cosine similarity, annotate and flag pairs, generate output table: "For each candidate pair, extract and preprocess the corresponding MS2 fragment spectra (normalize intensity, remove noise). 3. Calculate MS2 spectral similarity score using cosine similarity or"
- [readme] Identifies multiple ion species from one analyte compound in time-resolved plasma ionization datasets: "in-silico approach to putatively identify multiple ion species arising from one analyte compound specially tailored for time-resolved datasets from plasma ionization techniques"
- [readme] Three-step procedure refines two-step search algorithm with MS2 spectral similarity scoring: "modification of the former two-step search algorithm towards refinement by MS2 spectral similarity scoring"
- [readme] Direct-injection MS data lack chromatographic separation, complicating identification of fragments and adducts: "Mass spectrometric data from direct injection analysis is hard to interpret as missing chromatographic separation complicates identification of fragments and adducts"
