---
name: chemical-structure-serialization
description: Use when you need to export a stored chemical structure (sequence or
  building-block entry) from the MassSpecBlocks database to enable mass spectra analysis
  in CycloBranch or when preparing structures for import into other cheminformatics
  workflows that require a standardized structure interchange.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3375
  tools:
  - PHP
  - Symfony
  - MySQL 8
  - MariaDB 10
  - CycloBranch
  - MySQL 8 / MariaDB 10
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# chemical-structure-serialization

## Summary

Serialize chemical structures and building-block annotations from a user database into a format consumable by external analysis programs like CycloBranch. This skill enables interchange of structure data between MassSpecBlocks and mass spectra analysis tools by transforming internal database representations into standardized export formats.

## When to use

Apply this skill when you need to export a stored chemical structure (sequence or building-block entry) from the MassSpecBlocks database to enable mass spectra analysis in CycloBranch or when preparing structures for import into other cheminformatics workflows that require a standardized structure interchange format.

## When NOT to use

- When the user database entry is incomplete or lacks required building-block annotations needed by the target program
- When the target analysis program uses a format incompatible with the available serialization specification
- When working with structures from external databases (PubChem, ChemSpider, ChEBI, COCONUT, NP Atlas, Norine) that have not yet been imported into the MassSpecBlocks user database

## Inputs

- User database entry (MySQL/MariaDB record containing sequence or structure data)
- Chemical structure representation with building-block annotations
- Target export format specification (e.g., CycloBranch format)

## Outputs

- CycloBranch-compatible file (serialized structure format)
- Formatted export data ready for download or downstream analysis

## How to apply

First, retrieve the user database entry (sequence or structure data) from the MySQL/MariaDB backend via the PHP/Symfony REST API. Next, parse the internal chemical structure representation and associated building-block annotations. Then serialize this data into the target export format specification (determined by the consuming program—for CycloBranch, this follows CycloBranch's documented specification). Finally, write the formatted export data to a file and return it to the user for download or further processing. The process preserves chemical topology, atom connectivity, and building-block metadata throughout serialization.

## Related tools

- **Symfony** (REST API framework for retrieving and serializing structure data from the backend) — https://symfony.com
- **PHP** (Server-side language for implementing serialization logic and API endpoints)
- **MySQL 8 / MariaDB 10** (Database system storing the chemical structure and building-block entries to be serialized)
- **CycloBranch** (Target analysis program consuming the serialized structure export format) — https://ms.biomed.cas.cz/cyclobranch/docs/html/

## Evaluation signals

- Exported file validates against the CycloBranch format specification (correct file extension, schema compliance, required fields present)
- Round-trip consistency: reimporting the exported file into MassSpecBlocks or CycloBranch preserves chemical structure topology and building-block annotations without loss
- Completeness check: all building-block metadata from the source database entry appears in the serialized output
- File download succeeds and file size is non-zero and consistent with the complexity of the input structure
- CycloBranch successfully loads and processes the exported file for mass spectra analysis without parse errors

## Limitations

- The export format specification is tailored to CycloBranch; structures may need format conversion to work with other mass spectrometry analysis tools
- Complex or unusual building-block annotations in the user database may not have direct equivalents in the CycloBranch format, potentially causing data loss during serialization
- No changelog is available in the MassSpecBlocks repository to track changes to the export format specification across versions, which may affect compatibility between MassSpecBlocks releases and specific CycloBranch versions

## Evidence

- [other] MassSpecBlocks provides an export format designed for the open-source CycloBranch program: "MassSpecBlocks provides an export format designed for the open-source CycloBranch program, enabling conversion of stored chemical structures and building blocks into a format consumable by"
- [other] Retrieve, serialize, write workflow for export: "Retrieve the user database entry (sequence/structure data) from the MySQL/MariaDB backend via the PHP/Symfony API. 2. Serialize the chemical structure and building-block annotations into the"
- [readme] CycloBranch interoperability purpose: "The application provides an export format for open source program CycloBranch from Jiří Novák (Laboratory of Molecular Structure Characterization - Academy of Sciences of the Czech Republic)."
- [readme] Symfony API backend architecture: "Backend is written in PHP with Symfony framework"
- [readme] Database technology stack: "Application is developed for Mysql 8 /MariaDB 10"
