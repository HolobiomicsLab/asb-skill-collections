---
name: json-file-parsing-and-loading
description: Use when after generating a structured JSON result file from a prior computational step (e.g., gensim LDA model output in myexp.ldaresult.json format) and needing to store it in PostgreSQL for web application access, visualization, or further analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Docker
  - PostgreSQL
  - gensim
  - run_gensim.py
  - Django
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- pipenv --python 2.7
- docker run --name some-redis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_substructure_discovery_mass2motif_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_substructure_discovery_mass2motif_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# JSON file parsing and loading

## Summary

Parse a JSON file containing structured experimental results and load it into a relational database (PostgreSQL) for persistent storage and downstream querying. This skill bridges intermediate computational results and database persistence in multi-step analytical workflows.

## When to use

After generating a structured JSON result file from a prior computational step (e.g., gensim LDA model output in myexp.ldaresult.json format) and needing to store it in PostgreSQL for web application access, visualization, or further analysis. Use this skill when the JSON contains hierarchical or complex result structures that must be made queryable and accessible to other components (e.g., Django web interface, Celery tasks).

## When NOT to use

- JSON file is malformed or does not conform to the expected LDA result schema (e.g., missing required fields for topics, documents, or term–topic mappings).
- PostgreSQL database server is not running or network connectivity to the database is unavailable.
- The experiment identifier already exists in the database and primary key uniqueness constraints would cause insertion to fail without explicit override/merge logic.

## Inputs

- JSON file containing LDA result data (e.g., myexp.ldaresult.json)
- PostgreSQL username (string)
- Experiment identifier (string)

## Outputs

- PostgreSQL database records containing parsed LDA results
- Experiment metadata record in database
- Database schema entries for topics, documents, and term–topic associations

## How to apply

Execute the database insertion command with three required arguments: (1) the path to the JSON result file (e.g., myexp.ldaresult.json), (2) the PostgreSQL username (e.g., stefanv), and (3) a unique experiment identifier (e.g., myexp). The run_gensim.py insert command parses the JSON, validates its structure against the expected schema, and writes records to the PostgreSQL database. Verify successful insertion by confirming no error messages in the command output and by querying the database to confirm the experiment record and associated results are accessible. If insertion fails, check that the JSON file is well-formed, the database server is running and accessible, and credentials match the PostgreSQL environment configuration.

## Related tools

- **PostgreSQL** (Relational database backend that stores parsed LDA results, experiment metadata, and topic–term associations for persistent retrieval and querying)
- **gensim** (Upstream tool that generates the LDA result JSON file consumed by this skill) — https://github.com/sdrogers/ms2ldaviz
- **Python** (Language in which run_gensim.py insert command and JSON parsing logic are implemented) — https://github.com/sdrogers/ms2ldaviz
- **run_gensim.py** (Command-line driver script that orchestrates JSON file parsing and database insertion via the 'insert' subcommand) — https://github.com/sdrogers/ms2ldaviz
- **Django** (Web application framework that queries the PostgreSQL database after insertion to display and visualize LDA results) — https://github.com/sdrogers/ms2ldaviz

## Examples

```
./run_gensim.py insert myexp.ldaresult.json stefanv myexp
```

## Evaluation signals

- Command exits with return code 0 and produces no error messages to stderr.
- Database query (e.g., `SELECT * FROM experiments WHERE name = 'myexp'`) returns a record matching the provided experiment identifier and contains non-null topic, document, and term–topic data.
- Row count in relevant database tables (e.g., topics, documents, terms) increases by the expected amounts corresponding to the JSON result structure.
- Subsequent web interface queries (e.g., via Django ORM or SQL) can retrieve and display the inserted LDA topics and document–topic associations without timeout or data corruption errors.
- If a gensim LDA model file was uploaded separately, verify that both the JSON-inserted data and gensim model data reference the same experiment identifier and are consistent in topic count and vocabulary size.

## Limitations

- The JSON schema must match the expected LDA result format (topics, documents, term–topic associations); malformed or non-conformant JSON will cause insertion to fail or produce incomplete/incorrect database records.
- PostgreSQL credentials and network connectivity must be correctly configured; insertion cannot proceed if the database server is unreachable or credentials are invalid.
- Large JSON files may consume significant memory during parsing; for very large LDA models, consider batch insertion or streaming approaches not covered in the baseline workflow.
- The skill assumes the JSON file is generated from a trusted source (e.g., gensim LDA); if the JSON is untrusted or corrupted, insertion may introduce invalid data into the database without validation.

## Evidence

- [other] The insert step consumes the LDA result JSON file (myexp.ldaresult.json) and loads it into the database using the command ./run_gensim.py insert with parameters for the result file, a username (stefanv), and an experiment name (myexp).: "The insert step consumes the LDA result JSON file (myexp.ldaresult.json) and loads it into the database using the command ./run_gensim.py insert with parameters for the result file, a username"
- [readme] Perform 3 steps: 1. Generate corpus/features from MS2 file; 2. Run lda using gensim; 3. Insert lda result into db: "Performs 3 steps:
1. Generate corpus/features from MS2 file
2. Run lda using gensim
3. Insert lda result into db"
- [readme] ./run_gensim.py insert myexp.ldaresult.json stefanv myexp: "./run_gensim.py insert myexp.ldaresult.json stefanv myexp"
- [readme] The last command inserts the gensim lda results into the database.: "The last command inserts the gensim lda results into the database."
