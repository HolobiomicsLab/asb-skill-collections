---
name: similarity-scoring-for-spectra
description: Use when you have LC-MS/MS query spectra in mgf format that you need to match against a custom database (e.g., prepared with CFM-id) to identify compounds. Apply this skill when you want to rank candidate compounds by spectral similarity and return scored match results for downstream interpretation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MS2Compound
  - CFM-id
  - MS2Compound v1.0.2
  techniques:
  - LC-MS
derived_from:
- doi: 10.1089/omi.2021.0051
  title: MS2Compound
evidence_spans:
- MS2Compound (v1.0.2) is a user friendly Graphical User Interface (GUI) for the identification of the compounds from LC-MS and MS/MS metabolomics data
- compatible with the customized database prepared using CFM-id, the fragment prediction tool
- The current version of MS2Compound is compatible with the customized database prepared using CFM-id, the fragment prediction tool.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2compound_cq
    doi: 10.1089/omi.2021.0051
    title: MS2Compound
  dedup_kept_from: coll_ms2compound_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1089/omi.2021.0051
  all_source_dois:
  - 10.1089/omi.2021.0051
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# similarity-scoring-for-spectra

## Summary

Compute spectral similarity scores between query MS/MS spectra (in Mascot Generic Format) and a reference database to identify compounds. This skill quantifies the degree of spectral match to enable compound assignment in metabolomics workflows.

## When to use

You have LC-MS/MS query spectra in mgf format that you need to match against a custom database (e.g., prepared with CFM-id) to identify compounds. Apply this skill when you want to rank candidate compounds by spectral similarity and return scored match results for downstream interpretation.

## When NOT to use

- Input spectra are not in Mascot Generic Format (mgf) — convert to mgf first.
- Reference database was not prepared using CFM-id; MS2Compound v1.0.2 is optimized for CFM-id–derived databases.
- You need to identify novel compounds with no reference database; this skill requires a pre-built custom database.

## Inputs

- Mascot Generic Format (mgf) query file containing LC-MS/MS spectra
- Custom compound database prepared with CFM-id (fragment prediction tool)
- MS2Compound v1.0.2 GUI configuration

## Outputs

- Compound identification results file with match scores
- Ranked list of candidate compounds per query spectrum
- Metadata and similarity metrics for matched compounds

## How to apply

Load the custom compound database (prepared using CFM-id fragment predictions) into MS2Compound v1.0.2. Import the mgf query file containing LC-MS/MS spectra. Execute the matching algorithm, which compares each query spectrum against database entries and computes similarity scores for all candidate compounds. Export the identified compounds with their match scores and associated metadata. The algorithm's output ranks compounds by similarity strength, allowing prioritization of high-confidence identifications.

## Related tools

- **MS2Compound v1.0.2** (Graphical user interface that implements the spectral matching algorithm and similarity score computation) — https://sourceforge.net/projects/ms2compound/
- **CFM-id** (Fragment prediction tool used to prepare the custom reference database that MS2Compound searches against)

## Evaluation signals

- Match scores are computed for all query spectra against all database entries (no missing values in results file).
- Compound rankings are consistent across repeated runs on identical inputs (deterministic algorithm).
- Results file contains structured metadata including spectrum identifiers, candidate compound names, and similarity scores for each match.
- High-confidence matches (top-ranked compounds with highest similarity scores) correspond to visually similar precursor m/z and fragment patterns in the input mgf.
- Score distribution shows variation across candidates, confirming discrimination between similar and dissimilar compounds.

## Limitations

- MS2Compound is compatible only with custom databases prepared using CFM-id; incompatible with databases from other fragment prediction tools.
- Tool requires Windows operating system (Windows 7, 8, or 10); Linux/macOS deployments are not documented in the README.
- No changelog provided in README; algorithm updates and improvements are not explicitly documented.
- Minimum system configuration (2 GB RAM, Intel i3 64-bit CPU) may limit performance on large databases or high-throughput batches.

## Evidence

- [readme] MS2Compound (v1.0.2) is a user friendly Graphical User Interface (GUI) for the identification of the compounds from LC-MS and MS/MS metabolomics data.: "MS2Compound (v1.0.2) is a user friendly Graphical User Interface (GUI) for the identification of the compounds from LC-MS and MS/MS metabolomics data."
- [readme] The current version of MS2Compound is compatible with the customized database prepared using CFM-id, the fragment prediction tool. Mascot Generic Format (mgf) files can be used as query input file.: "The current version of MS2Compound is compatible with the customized database prepared using CFM-id, the fragment prediction tool. Mascot Generic Format (mgf) files can be used as query input file"
- [other] Execute the matching algorithm to compare query spectra against database entries and compute similarity scores.: "Execute the matching algorithm to compare query spectra against database entries and compute similarity scores."
- [other] Export identified compounds with their match scores and metadata to a results file.: "Export identified compounds with their match scores and metadata to a results file."
