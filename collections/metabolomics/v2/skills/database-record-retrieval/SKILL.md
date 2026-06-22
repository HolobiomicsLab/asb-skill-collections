---
name: database-record-retrieval
description: Use when you need to access a stored chemical structure, NRP sequence, or building-block annotation from the MassSpecBlocks database in order to export it to an external format (e.g., CycloBranch), transform it for mass spectra analysis, or integrate it with another chemical database query.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3431
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3336
  - http://edamontology.org/topic_0602
  tools:
  - PHP
  - Symfony
  - MySQL 8
  - MariaDB 10
  - CycloBranch
  - PHP/Symfony Framework
  - Doctrine ORM
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

# database-record-retrieval

## Summary

Retrieve user database entries (chemical structures, sequences, or building-block annotations) from a MySQL/MariaDB backend via a PHP/Symfony REST API, preparing them for downstream serialization or export. This skill is essential when exporting structures to external formats like CycloBranch or performing analysis on stored metabolite data.

## When to use

Apply this skill when you need to access a stored chemical structure, NRP sequence, or building-block annotation from the MassSpecBlocks database in order to export it to an external format (e.g., CycloBranch), transform it for mass spectra analysis, or integrate it with another chemical database query. Typical trigger: user requests a structure export, or a workflow requires fetching a previously stored compound record by ID or sequence identifier.

## When NOT to use

- Input structure is already in memory or loaded from a file (no database round-trip needed).
- You need to search across external databases (PubChem, ChemSpider, Norine, ChEBI, COCONUT, NP Atlas) — use those databases' native APIs instead.
- The record does not exist in the user's MassSpecBlocks database and requires creation or import first.

## Inputs

- Unique database record identifier (integer or UUID)
- Optional: sequence or SMILES string for lookup
- Optional: filter parameters (e.g., building-block type, mass range)

## Outputs

- Deserialized chemical structure object (with SMILES, metadata)
- Building-block annotation record(s)
- Associated mass spectra or analysis metadata

## How to apply

Query the MySQL 8 / MariaDB 10 backend via the PHP/Symfony REST API using the record's unique identifier or sequence data. The API retrieves the serialized chemical structure and any associated building-block annotations from the user database. Verify that the retrieved record contains all required fields: structure SMILES representation, building-block metadata, and any associated mass spectra annotations. Check that the returned data is well-formed JSON or appropriate serialized object. Once retrieved, the record is ready for downstream processes such as format conversion (e.g., to CycloBranch export format) or rendering via SmilesDrawer.

## Related tools

- **MySQL 8** (Primary relational database engine storing user chemical structures and building-block records)
- **MariaDB 10** (Alternative relational database backend compatible with MassSpecBlocks for structure storage)
- **PHP/Symfony Framework** (REST API server that exposes database query methods and serialization logic) — https://github.com/privrja/thesis
- **Doctrine ORM** (Object-relational mapper used by Symfony to abstract and query database records programmatically) — https://github.com/privrja/thesis

## Evaluation signals

- Returned record contains non-null SMILES string and valid building-block metadata matching the requested identifier.
- JSON response from REST API is valid and conforms to the documented MassSpecBlocks schema (verifiable at /rest/doc).
- Query execution time is within acceptable latency (typically < 500 ms for single-record retrieval on a well-indexed database).
- Retrieved structure can be successfully rendered or serialized downstream (e.g., parsed by SmilesDrawer or converted to CycloBranch format without parse errors).
- Database connection and authentication to MySQL/MariaDB backend succeeds without timeouts or permission errors.

## Limitations

- Retrieval performance depends on database indexing and backend server load; large bulk retrievals may timeout.
- The skill assumes valid database credentials and network connectivity to the MySQL/MariaDB and PHP/Symfony backend — network failures or authentication errors will block retrieval.
- Building-block annotations and metadata are only as complete as the original user input; missing or malformed annotations in the database will be retrieved as-is.
- No changelog is provided in the public documentation, so API breaking changes or schema updates may not be communicated in advance.

## Evidence

- [other] Retrieve the user database entry (sequence/structure data) from the MySQL/MariaDB backend via the PHP/Symfony API.: "Retrieve the user database entry (sequence/structure data) from the MySQL/MariaDB backend via the PHP/Symfony API."
- [readme] Application is developed for Mysql 8 /MariaDB 10, but when using Symfony you can create your migrations for another database.: "Application is developed for Mysql 8 /MariaDB 10, but when using Symfony you can create your migrations for another database."
- [readme] open-source web application to manage own user databases of chemical structures like NRPs and to find structures on other chemical projects: "open-source web application to manage own user databases of chemical structures like NRPs and to find structures on other chemical projects"
- [readme] Documentation of API is [localhost:8000/rest/doc] Rest API is on [localhost:8000/rest]: "Documentation of API is [localhost:8000/rest/doc] Rest API is on [localhost:8000/rest]"
