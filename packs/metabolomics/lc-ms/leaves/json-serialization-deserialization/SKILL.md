---
name: json-serialization-deserialization
description: Use when when you have completed a computational step (e.g., corpus feature extraction or gensim LDA inference) and need to persist the result for later retrieval, pass it to a separate process (e.g., Celery task), or load it into a database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - gensim
  - Python json module
  - PostgreSQL
  - Django
  techniques:
  - LC-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- pipenv --python 2.7
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

# json-serialization-deserialization

## Summary

Convert between in-memory structured data objects (corpus representations, LDA results, model metadata) and JSON file format for persistence, inter-process communication, and database ingestion in metabolomics topic modeling workflows. This skill is essential for bridging gensim LDA inference steps with downstream database insertion and web visualization pipelines.

## When to use

When you have completed a computational step (e.g., corpus feature extraction or gensim LDA inference) and need to persist the result for later retrieval, pass it to a separate process (e.g., Celery task), or load it into a database. Specifically: after generating document-term representations from MS2 files, before running gensim LDA; after gensim LDA completes, before inserting results into PostgreSQL; and when importing pre-computed gensim LDA objects into the web application.

## When NOT to use

- If you need real-time streaming of large corpora (>GB scale); JSON serialization is text-based and slower than binary formats like HDF5 or Protocol Buffers.
- If the LDA model must be updated incrementally after initial training; serialized JSON snapshots represent a fixed point and do not encode online-learning state.
- If you are working within a single Python process and do not need inter-process handoff; keep objects in memory instead of serializing to disk.

## Inputs

- Python dictionary or gensim corpus object (document-term matrix with vocabulary)
- gensim LdaModel object or topic–term distribution dictionary
- LDA metadata dictionary (hyperparameters, iteration count, log-likelihood)

## Outputs

- JSON file containing corpus (myexp.corpus.json): document-term pairs and vocabulary
- JSON file containing LDA result (myexp.ldaresult.json): topic distributions and term weights
- gensim-format LDA tarball (myexp.lda.gensim.tar.gz): binary model for fast database import

## How to apply

Use Python's json module (or json serialization built into gensim) to encode structured objects—document-term matrices, topic distributions, term weights, model metadata—into JSON text, then write to file. When deserializing, read the JSON file and parse it back into Python dictionaries or gensim-compatible data structures. The ms2ldaviz pipeline uses this pattern: (1) serialize corpus as JSON after feature extraction, (2) deserialize corpus for gensim LDA input, (3) serialize LDA result (topic–term weights, document–topic distributions) to JSON, and (4) deserialize LDA result for database insertion via insert or insert_gensim commands. Choose standard JSON format for human readability and inter-tool portability, or gensim format (via --ldaformat gensim flag) for faster database insertion if model metadata exclusion is acceptable. Validate JSON schema (e.g., presence of required keys: 'documents', 'vocab', 'doc_topics', 'term_topics') before downstream processing.

## Related tools

- **gensim** (Provides LdaModel serialization methods and corpus format; outputs JSON or binary gensim format for topic–term and document–topic distributions.)
- **Python json module** (Standard library for JSON encoding/decoding of corpus and LDA metadata dictionaries.)
- **PostgreSQL** (Target database for deserializing and inserting LDA results via Django ORM after JSON deserialization.)
- **Django** (Web framework that deserializes LDA JSON during experiment upload and model instantiation for visualization.) — https://github.com/glasgowcompbio/ms2ldaviz

## Examples

```
./run_gensim.py gensim myexp.corpus.json myexp.ldaresult.json
```

## Evaluation signals

- JSON file is valid (parses without error via json.load(); no truncation or corruption).
- Required keys present: corpus JSON must contain 'documents' and 'vocab'; LDA result JSON must contain 'doc_topics' and 'term_topics' (or equivalent gensim-compatible keys).
- Round-trip consistency: deserialize JSON, compare structure and values to original Python object; numeric values match to floating-point precision.
- File size and row count reasonable: corpus JSON size scales linearly with document count; LDA JSON contains one entry per topic and per term in vocabulary.
- Downstream process (gensim LDA or database insert) accepts deserialized object without schema or type errors; no silent data loss (e.g., NaN or missing distributions).

## Limitations

- JSON is human-readable but verbose; large corpora (>10M terms or >100k documents) produce multi-GB files, increasing I/O time and storage cost.
- Floating-point precision in JSON is limited to ~15 significant digits; downstream numerical operations may accumulate rounding error.
- gensim format (--ldaformat gensim) omits some metadata (e.g., LDA hyperparameters, iteration count) compared to standard JSON, reducing reproducibility but enabling faster import.
- No built-in versioning or schema validation in JSON; schema changes (e.g., adding a new metadata field) require manual migration scripts.

## Evidence

- [other] The gensim LDA step accepts a corpus JSON file as input and produces an LDA result JSON file as output via the command './run_gensim.py gensim myexp.corpus.json myexp.ldaresult.json'.: "Load the corpus JSON file (myexp.corpus.json) containing preprocessed document-term representations. 2. Execute the gensim LDA model using ./run_gensim.py with arguments 'gensim', input corpus path,"
- [readme] Multi-step gensim LDA workflow with explicit JSON serialization at corpus and result stages.: "./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json
./run_gensim.py gensim myexp.corpus.json myexp.ldaresult.json
./run_gensim.py insert myexp.ldaresult.json stefanv myexp"
- [readme] Alternative gensim format for faster database insertion with metadata exclusion.: "This will exclude the lda info from the json file and write/import a gensim formatted lda dataset."
- [readme] Tarball serialization for gensim LDA upload via web interface.: "The gensim result must be tarballed with for example `tar -zcf myexp.lda.gensim.tar.gz myexp.lda.gensim*` and then uploaded in the form."
