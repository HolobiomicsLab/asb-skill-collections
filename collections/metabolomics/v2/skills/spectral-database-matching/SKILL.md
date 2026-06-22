---
name: spectral-database-matching
description: Use when when you have MS2 .mzML format data files from untargeted metabolomics or proteomics experiments and need to perform an initial annotation step by matching experimental spectra against known reference libraries (GNPS, HMDB, MassBank) with a defined precursor mass tolerance (e.g., 15 ppm).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Spectra
  - R
  - GNPS
  - HMDB
  - MassBank
  techniques:
  - CE-MS
  - ion-mobility-MS
  - NMR
derived_from:
- doi: 10.1186/s13321-023-00695-y
  title: MAW
evidence_spans:
- performs spectral database dereplication using R Package
- spectral database dereplication using R Package Spectra
- workflow takes MS2 .mzML format data files as an input in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_maw_cq
    doi: 10.1186/s13321-023-00695-y
    title: MAW
  dedup_kept_from: coll_maw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-023-00695-y
  all_source_dois:
  - 10.1186/s13321-023-00695-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-database-matching

## Summary

Spectral database matching identifies and ranks MS2 spectra from untargeted metabolomics data by comparing them against reference spectral libraries using the Spectra R package. This dereplication step assigns confidence scores to potential metabolite identifications before downstream compound database searching.

## When to use

When you have MS2 .mzML format data files from untargeted metabolomics or proteomics experiments and need to perform an initial annotation step by matching experimental spectra against known reference libraries (GNPS, HMDB, MassBank) with a defined precursor mass tolerance (e.g., 15 ppm).

## When NOT to use

- Input is already a compound identification table or final annotated metabolite list — spectral matching is an early-stage dereplication step and would be redundant.
- MS1-only data without MS2 fragmentation spectra — spectral database matching requires MS2 spectra for similarity scoring.
- Reference spectral libraries are unavailable or incompatible with Spectra package format (.rda).

## Inputs

- MS2 .mzML format mass spectrometry data files
- Reference spectral library databases (GNPS, HMDB, MassBank in .rda format)

## Outputs

- Spectral matches table (CSV format) with columns: precursor m/z, matched library identifier, match score, and spectrum metadata
- Annotated spectral results indexed by precursor mass and library source

## How to apply

Load MS2 .mzML files into R using the Spectra package, then execute spectral database dereplication against reference spectral libraries (GNPS, HMDB, or MassBank) specifying a precursor mass tolerance threshold (the MAW workflow uses 15 ppm). The Spectra package identifies and ranks matching spectra by calculating similarity scores between experimental and reference MS2 fragmentation patterns. Generate and export a table of spectral matches with match scores, metadata, and library identifiers. The resulting spectral matches table serves as input to the next workflow stage (compound database dereplication via SIRIUS or MetFrag) and should contain at minimum the precursor m/z, matched library identifier, cosine similarity or other match score metric, and matched spectrum metadata.

## Related tools

- **Spectra** (Performs spectral database dereplication by comparing experimental MS2 spectra against reference libraries and scoring matches) — https://rformassspectrometry.github.io/Spectra/
- **R** (Runtime environment for loading .mzML files and executing Spectra package functions)
- **GNPS** (Reference spectral library database used as matching source) — https://zenodo.org/record/7519270
- **HMDB** (Reference spectral library database (version 5.0) used as matching source) — https://zenodo.org/record/7519270
- **MassBank** (Reference spectral library database (version 2022.12) used as matching source) — https://zenodo.org/record/7519270

## Examples

```
Rscript --no-save --no-restore --verbose Workflow_R_Script_all_MetFrag.r your_file_name.mzML gnps.rda hmdb.rda mbankNIST.rda 15 TRUE
```

## Evaluation signals

- Output spectral matches table contains non-null entries for all input precursor masses with at least one match above a match score threshold (e.g., cosine similarity ≥ 0.7 if applicable).
- Precursor m/z values in output match the input MS2 data within the specified tolerance window (±15 ppm in MAW workflow).
- All matched spectra are resolvable to a valid library identifier in the reference database (GNPS, HMDB, or MassBank).
- Match scores are ranked in descending order per precursor, with the highest-scoring match listed first for each input spectrum.
- Spectral matches table structure validates against expected schema: contains columns for precursor m/z, library ID, match score, and metadata; no rows have missing values in critical fields.

## Limitations

- Spectral matching sensitivity depends critically on reference library completeness and quality; if target metabolites are absent from the reference libraries, no match will be returned regardless of similarity.
- Precursor mass tolerance (e.g., 15 ppm) must be tuned to instrument accuracy; overly tight tolerances may miss valid matches in lower-resolution instruments, while loose tolerances increase false positives.
- The workflow does not resolve isomeric or isobaric compounds; multiple structurally distinct metabolites can share identical MS2 spectra, and the matching step cannot differentiate them without additional orthogonal data (retention time, ion mobility, NMR).
- Performance scales with file size; the README notes that one precursor mass takes ~2 minutes on a 64 GB Ubuntu system, so files with many precursor masses may require distributed execution or background job submission (disown PID) in Docker environments.

## Evidence

- [other] The workflow takes MS2 .mzML format data files as input in R and performs spectral database dereplication using the Spectra R package.: "The workflow takes MS2 .mzML format data files as an input in R. It performs spectral database dereplication using R Package Spectra"
- [other] Spectral database dereplication against reference libraries generates ranked spectral matches with scores and metadata.: "Execute spectral database dereplication against a reference spectral library using Spectra to identify and rank matching spectra"
- [readme] MAW workflow uses multiple reference databases (GNPS, HMDB, MassBank) for spectral matching.: "Download the databases gnps.rda, hmdb.rda, and mbankNIST.rda from https://zenodo.org/record/7519270. This submission contains GNPS saved at 2023-01-09 15:24:46, HMDB Current Version (5.0), MassBank"
- [readme] Spectral matching precursor tolerance parameter is set to 15 ppm in the MAW workflow.: "Rscript --no-save --no-restore --verbose Workflow_R_Script_all_MetFrag.r your_file_name.mzML gnps.rda hmdb.rda mbankNIST.rda 15 TRUE coconut"
- [other] Spectral matching output feeds directly into compound database dereplication as part of the annotation workflow.: "performs spectral database dereplication using R Package Spectra and compound database dereplication using SIRIUS OR MetFrag. Final candidate selection is done in Python"
