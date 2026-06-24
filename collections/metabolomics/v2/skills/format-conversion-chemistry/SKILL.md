---
name: format-conversion-chemistry
description: Use when when you have retrieved a user database entry (sequence or structure
  data) from the MassSpecBlocks backend and need to enable mass spectra analysis in
  the open-source CycloBranch program, or when you need to export NRP sequences and
  building-block annotations for consumption by external.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3375
  tools:
  - PHP
  - Symfony
  - MySQL 8
  - MariaDB 10
  - CycloBranch
  - PHP/Symfony
  - MySQL 8 / MariaDB 10
  - React / TypeScript
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s13321-021-00530-2
  title: MassSpecBlocks
evidence_spans:
- Backend is written in PHP with Symfony framework
- Application is developed for Mysql 8 /MariaDB 10
- export format for open source program CycloBranch from Jiří Novák
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massspecblocks_cq
    doi: 10.1186/s13321-021-00530-2
    title: MassSpecBlocks
  dedup_kept_from: coll_massspecblocks_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00530-2
  all_source_dois:
  - 10.1186/s13321-021-00530-2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# format-conversion-chemistry

## Summary

Convert chemical structure and building-block annotations stored in a user database into CycloBranch-compatible export format for mass spectra analysis. This skill enables interoperability between MassSpecBlocks' internal representation and external mass spectrometry software.

## When to use

When you have retrieved a user database entry (sequence or structure data) from the MassSpecBlocks backend and need to enable mass spectra analysis in the open-source CycloBranch program, or when you need to export NRP sequences and building-block annotations for consumption by external mass spectrometry tools.

## When NOT to use

- Input data is already in a format natively supported by CycloBranch or other target software; direct export is unnecessary.
- The chemical structure lacks required building-block annotations; conversion will fail or produce incomplete output.
- The target software is not CycloBranch or a tool with a defined conversion specification in MassSpecBlocks.

## Inputs

- User database entry (chemical structure or NRP sequence) from MySQL/MariaDB backend
- Building-block annotations associated with the structure
- CycloBranch export format specification

## Outputs

- CycloBranch-compatible export file (format specified by CycloBranch)
- Downloadable file containing serialized structure and building-block data

## How to apply

Retrieve the chemical structure and building-block annotations from the MySQL/MariaDB backend via the PHP/Symfony REST API endpoint. Serialize the retrieved structure data according to the CycloBranch export format specification, ensuring all building-block metadata and sequence information are correctly mapped to CycloBranch's expected schema. Write the serialized export data to a file in the format determined by the CycloBranch specification (typically XML or a structured text format). Return the formatted file to the user for download or pass it to CycloBranch for downstream mass spectra analysis. Validate the output by confirming CycloBranch can parse and load the exported file without errors.

## Related tools

- **PHP/Symfony** (Backend framework for retrieving structure data from MySQL/MariaDB and serializing it into export format) — https://github.com/privrja/thesis
- **MySQL 8 / MariaDB 10** (Backend database storing user chemical structures and building-block annotations)
- **CycloBranch** (Target software that consumes the exported format for mass spectra analysis) — https://ms.biomed.cas.cz/cyclobranch/docs/html/
- **React / TypeScript** (Frontend for user interaction to trigger export and download formatted file) — https://github.com/privrja/thesis-frontend-react

## Evaluation signals

- The exported file can be successfully opened and parsed by CycloBranch without validation errors.
- All building-block annotations and sequence metadata from the original database entry are present and correctly mapped in the output file.
- File format and schema conform to the CycloBranch specification; spot-check against specification documentation shows no structural deviations.
- Mass spectra analysis workflow in CycloBranch proceeds without import-related failures after consuming the exported file.
- Round-trip test: re-importing the exported file produces equivalent structure and building-block data to the original.

## Limitations

- Conversion fidelity depends on completeness of building-block annotations in the source database; missing or malformed annotations will produce invalid or incomplete exports.
- CycloBranch specification changes or versioning differences may require recalibration of the serialization logic; no changelog is documented for format updates.
- The skill assumes the target software is CycloBranch; generalization to other mass spectrometry tools would require additional format specifications and converter implementations.

## Evidence

- [other] MassSpecBlocks provides an export format designed for the open-source CycloBranch program, enabling conversion of stored chemical structures and building blocks into a format consumable by CycloBranch for mass spectra analysis.: "MassSpecBlocks provides an export format designed for the open-source CycloBranch program, enabling conversion of stored chemical structures and building blocks into a format consumable by"
- [other] Retrieve the user database entry (sequence/structure data) from the MySQL/MariaDB backend via the PHP/Symfony API. Serialize the chemical structure and building-block annotations into the CycloBranch export format specification. Write the formatted export data to a file (format determined by CycloBranch specification) and return it to the user for download or further processing.: "Retrieve the user database entry (sequence/structure data) from the MySQL/MariaDB backend via the PHP/Symfony API. Serialize the chemical structure and building-block annotations into the CycloBranch"
- [readme] The application provides an export format for open source program CycloBranch from Jiří Novák (Laboratory of Molecular Structure Characterization - Academy of Sciences of the Czech Republic).: "The application provides an export format for open source program CycloBranch from Jiří Novák (Laboratory of Molecular Structure Characterization - Academy of Sciences of the Czech Republic)."
- [readme] open-source web application to manage own user databases of chemical structures like NRPs and to find structures on other chemical projects: "open-source web application to manage own user databases of chemical structures like NRPs and to find structures on other chemical projects"
