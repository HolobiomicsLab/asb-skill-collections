---
name: building-block-annotation-export
description: Use when you have retrieved a user database entry (sequence or building-block structure record) from the MassSpecBlocks backend and need to generate a file in CycloBranch format for mass spectra analysis, interpretation, or sharing with collaborators using the CycloBranch software.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_3520
  tools:
  - PHP
  - Symfony
  - MySQL 8
  - MariaDB 10
  - CycloBranch
  - MySQL 8 / MariaDB 10
  - MassSpecBlocks backend
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
---

# building-block-annotation-export

## Summary

Export user-managed chemical structure and building-block annotations from a relational database into the CycloBranch-compatible file format for downstream mass spectra analysis. This skill transforms stored sequence or structure metadata into a standardized interchange format consumable by external mass spectrometry interpretation tools.

## When to use

Apply this skill when you have retrieved a user database entry (sequence or building-block structure record) from the MassSpecBlocks backend and need to generate a file in CycloBranch format for mass spectra analysis, interpretation, or sharing with collaborators using the CycloBranch software.

## When NOT to use

- The user database entry is not yet persisted (has not been saved to the backend database)
- The target external tool is not CycloBranch; use a different export format skill if the consumer is ChemSpider, PubChem, Norine, ChEBI, COCONUT, or NP Atlas
- The chemical structure contains unresolved or malformed building-block annotations that cannot be serialized into the CycloBranch schema

## Inputs

- user database entry (sequence or building-block structure record)
- chemical structure metadata (building-block annotations, monoisotopic masses, sequence positions)
- relational database connection (MySQL 8 / MariaDB 10)

## Outputs

- CycloBranch export format file
- file path or file stream ready for download

## How to apply

First, retrieve the target user database entry (sequence/structure data) from the MySQL/MariaDB backend via the PHP/Symfony REST API. Next, serialize the chemical structure and building-block annotations according to the CycloBranch export format specification. Then, construct and write the formatted export data to a file (with the file format determined by the CycloBranch specification document). Finally, return the generated file to the user for download or further processing. Validate that all building-block metadata (e.g., monoisotopic mass, structural class, sequence position) has been correctly mapped into the CycloBranch field schema before file write.

## Related tools

- **Symfony** (PHP web framework for the REST API endpoint that retrieves user database entries from the backend) — https://symfony.com
- **MySQL 8 / MariaDB 10** (Relational database storing user-managed chemical structures and building-block annotations) — https://github.com/privrja/thesis
- **CycloBranch** (External mass spectrometry analysis software that consumes the export format produced by this skill) — https://ms.biomed.cas.cz/cyclobranch/docs/html/
- **MassSpecBlocks backend** (Implements the export serialization logic and REST API endpoint) — https://github.com/privrja/thesis

## Evaluation signals

- The generated CycloBranch export file conforms to the CycloBranch format specification (validate against schema or sample file structure)
- All building-block annotations from the source database entry are present in the exported file with no data loss
- The exported file can be successfully imported and parsed by the CycloBranch software without format errors
- Monoisotopic masses, sequence positions, and structural class metadata are correctly serialized and mapped to CycloBranch field names
- File is written to disk or returned as a stream without truncation or encoding errors

## Limitations

- The skill depends on the accuracy and completeness of the CycloBranch export format specification; deviations or version changes in CycloBranch may break compatibility
- Complex or non-standard building-block annotations not covered by the CycloBranch schema may be lost or require manual post-processing
- Export performance scales with database query latency; large structures or deep nested annotations may incur serialization overhead

## Evidence

- [other] MassSpecBlocks provides an export format designed for the open-source CycloBranch program, enabling conversion of stored chemical structures and building blocks into a format consumable by CycloBranch for mass spectra analysis.: "MassSpecBlocks provides an export format designed for the open-source CycloBranch program, enabling conversion of stored chemical structures and building blocks into a format consumable by CycloBranch"
- [other] 1. Retrieve the user database entry (sequence/structure data) from the MySQL/MariaDB backend via the PHP/Symfony API. 2. Serialize the chemical structure and building-block annotations into the CycloBranch export format specification. 3. Write the formatted export data to a file (format determined by CycloBranch specification) and return it to the user for download or further processing.: "Retrieve the user database entry (sequence/structure data) from the MySQL/MariaDB backend via the PHP/Symfony API. Serialize the chemical structure and building-block annotations into the CycloBranch"
- [readme] Application is developed for Mysql 8 /MariaDB 10, but when using Symfony you can create your migrations for another database.: "Application is developed for Mysql 8 /MariaDB 10"
- [readme] The application provides an export format for open source program CycloBranch from Jiří Novák (Laboratory of Molecular Structure Characterization - Academy of Sciences of the Czech Republic).: "The application provides an export format for open source program CycloBranch"
