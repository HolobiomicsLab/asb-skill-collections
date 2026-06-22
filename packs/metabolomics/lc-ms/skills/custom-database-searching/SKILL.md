---
name: custom-database-searching
description: Use when when you have LC-MS/MS data in Mascot Generic Format (mgf) files and need to identify compounds against a curated custom database (e.g., prepared using CFM-id for a specific metabolite class or organism) rather than relying on in-built commercial spectral libraries alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MS2Compound
  - CFM-id
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# custom-database-searching

## Summary

Search LC-MS/MS metabolomics spectra against custom compound databases prepared with CFM-id fragment predictions to identify compounds by spectral matching. This skill enables targeted compound identification when standard databases are insufficient or when organism-specific or metabolite-class-specific databases are needed.

## When to use

When you have LC-MS/MS data in Mascot Generic Format (mgf) files and need to identify compounds against a curated custom database (e.g., prepared using CFM-id for a specific metabolite class or organism) rather than relying on in-built commercial spectral libraries alone.

## When NOT to use

- Input query file is not in Mascot Generic Format (mgf)
- Custom database was not prepared using CFM-id or is in an incompatible format
- Only generic/in-built spectral databases are available and custom databases cannot be constructed

## Inputs

- Custom compound database (prepared using CFM-id)
- Mascot Generic Format (mgf) query file containing LC-MS/MS spectra

## Outputs

- Identified compounds with match scores and metadata
- Results file with ranked compound identifications

## How to apply

Load a custom compound database prepared using CFM-id (a fragment prediction tool) into MS2Compound v1.0.2, import the mgf query file containing LC-MS/MS spectra, execute the matching algorithm to compare query spectra against database entries, and compute similarity scores for each match. The tool generates a results file with identified compounds ranked by match score and annotated with metadata. Success requires that the custom database was properly constructed using CFM-id in a compatible format and that the mgf file contains valid MS/MS spectra with appropriate precursor and fragment m/z values.

## Related tools

- **MS2Compound** (Graphical user interface for spectral matching and compound identification against custom databases) — https://sourceforge.net/projects/ms2compound/
- **CFM-id** (Fragment prediction tool used to prepare and generate custom compound databases compatible with MS2Compound)

## Evaluation signals

- Match scores are computed and returned for each spectrum-to-database comparison
- All query spectra from the mgf file are processed and assigned at least one match result
- Identified compounds are ranked by match score (highest confidence first)
- Results file contains structured metadata (e.g., compound name, database ID, similarity metric) for each match
- No errors or warnings related to database format compatibility or mgf parsing are reported during execution

## Limitations

- MS2Compound v1.0.2 is Windows-only (Windows 7, 8, and 10) with no cross-platform support
- Requires minimum 2 GB RAM and Intel i3 64-bit CPU; performance with very large custom databases or mgf files on minimal hardware is not characterized
- Dependency on CFM-id-generated databases means accuracy is limited by the quality and completeness of fragment predictions from CFM-id
- No changelog or version history available; updates and bug fixes are not documented
- Installation directory path must not contain spaces, which may complicate deployment in certain environments

## Evidence

- [readme] MS2Compound (v1.0.2) is a user friendly Graphical User Interface (GUI) for the identification of the compounds from LC-MS and MS/MS metabolomics data.: "MS2Compound (v1.0.2) is a user friendly Graphical User Interface (GUI) for the identification of the compounds from LC-MS and MS/MS metabolomics data."
- [readme] The current version of MS2Compound is compatible with the customized database prepared using CFM-id, the fragment prediction tool. Mascot Generic Format (mgf) files can be used as query input file: "The current version of MS2Compound is compatible with the customized database prepared using CFM-id, the fragment prediction tool. Mascot Generic Format (mgf) files can be used as query input file"
- [other] Execute the matching algorithm to compare query spectra against database entries and compute similarity scores.: "Execute the matching algorithm to compare query spectra against database entries and compute similarity scores."
- [readme] The tool is independent from all the pre-requisite dependencies.: "The tool is independent from all the pre-requisite dependencies."
- [readme] Windows 7, 8, and 10: "Windows 7, 8, and 10"
