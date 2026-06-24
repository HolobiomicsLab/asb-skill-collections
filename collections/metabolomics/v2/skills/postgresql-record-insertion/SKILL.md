---
name: postgresql-record-insertion
description: Use when after successful gensim LDA inference has produced a JSON result
  file (e.g., myexp.ldaresult.json) and you need to make those topic assignments and
  model parameters queryable and accessible to a Django web application.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - PostgreSQL
  - Python
  - Docker
  - gensim
  - Django
  license_tier: open
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- docker run --name some-pg -d -p 5432:5432
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# postgresql-record-insertion

## Summary

Load gensim LDA result JSON files into a PostgreSQL database via command-line insertion. This skill bridges topic modeling output and persistent storage, enabling subsequent web-based visualization and querying of LDA topics inferred from metabolomics data.

## When to use

After successful gensim LDA inference has produced a JSON result file (e.g., myexp.ldaresult.json) and you need to make those topic assignments and model parameters queryable and accessible to a Django web application. Use this when you have completed the corpus generation and LDA inference steps in the ms2ldaviz pipeline and are ready to populate the database for visualization.

## When NOT to use

- LDA result JSON file has not yet been generated (run gensim step first)
- PostgreSQL database is not running or credentials are incorrect
- Experiment identifier already exists in the database (will cause collision or duplicate key error)

## Inputs

- LDA result JSON file (myexp.ldaresult.json)
- PostgreSQL username (string, e.g., 'stefanv')
- Experiment identifier (string, e.g., 'myexp')
- Running PostgreSQL database instance (port 5432)

## Outputs

- PostgreSQL database records containing LDA topics, word–topic associations, and experiment metadata
- Database record accessible to Django web application
- Experiment queryable by name in ms2ldaviz interface

## How to apply

Execute the run_gensim.py insert command with three required arguments: the LDA result JSON filename, a PostgreSQL username (e.g., stefanv), and an experiment identifier (e.g., myexp). The command parses the JSON file containing topic distributions, word–topic associations, and metadata, then inserts records into the PostgreSQL schema. Verify success by confirming the absence of error messages and by querying the database to confirm the experiment record and associated topic data are accessible. For faster insertion, an alternative gensim-formatted workflow (insert_gensim) can be used, which excludes LDA info from the JSON and imports a gensim-native dataset format instead.

## Related tools

- **PostgreSQL** (Target relational database for persistent storage of LDA results and experiment metadata)
- **gensim** (Prior LDA inference engine; produces JSON result files consumed by this insertion step)
- **Python** (run_gensim.py script interpreter for executing the insert command)
- **Docker** (Optional container runtime for PostgreSQL database instance)
- **Django** (Web application framework that queries the populated PostgreSQL database for visualization) — https://github.com/glasgowcompbio/ms2ldaviz

## Examples

```
./run_gensim.py insert myexp.ldaresult.json stefanv myexp
```

## Evaluation signals

- Command executes without errors or warnings; stdout/stderr is clean
- Database contains inserted records: query `SELECT * FROM experiments WHERE name='myexp'` returns non-empty result
- Topic and word–topic association records exist in their respective tables (e.g., `topics`, `words`, `topic_word_assignments`)
- Django web application can retrieve and display the experiment in the `/uploads/` interface
- Row counts in database tables match expected structure (e.g., number of topics, number of unique words)

## Limitations

- Requires pre-existing PostgreSQL database with schema initialized (run Django migrations first)
- Username must have INSERT and UPDATE privileges on the target schema
- Experiment identifier must be unique; duplicate names will fail insertion or produce database conflicts
- JSON file must conform to the expected gensim LDA output schema; malformed or incomplete files may cause parsing errors
- Alternative gensim-formatted insertion (insert_gensim) requires tarballing (tar -zcf) and manual tarball upload via web interface for some deployments

## Evidence

- [other] The insert step consumes the LDA result JSON file (myexp.ldaresult.json) and loads it into the database using the command ./run_gensim.py insert with parameters for the result file, a username (stefanv), and an experiment name (myexp).: "The insert step consumes the LDA result JSON file (myexp.ldaresult.json) and loads it into the database using the command ./run_gensim.py insert with parameters for the result file, a username"
- [other] Execute the database insertion command via ./run_gensim.py insert with arguments: LDA result JSON filename, PostgreSQL username, and experiment identifier.: "Execute the database insertion command via ./run_gensim.py insert with arguments: LDA result JSON filename, PostgreSQL username, and experiment identifier."
- [readme] ./run_gensim.py insert myexp.ldaresult.json stefanv myexp: "./run_gensim.py insert myexp.ldaresult.json stefanv myexp"
- [readme] The last command inserts the gensim lda results into the database.: "The last command inserts the gensim lda results into the database."
- [readme] docker run --name some-pg -d -p 5432:5432 -e POSTGRES_PASSWORD=j7z3rL40w9 -e POSTGRES_USER=django postgres: "docker run --name some-pg -d -p 5432:5432 -e POSTGRES_PASSWORD=j7z3rL40w9 -e POSTGRES_USER=django postgres"
