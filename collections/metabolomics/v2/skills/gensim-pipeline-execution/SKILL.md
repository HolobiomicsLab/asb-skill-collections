---
name: gensim-pipeline-execution
description: Use when you have an MS2 spectral file (MGF format) from LC-MS/MS metabolomics analysis and need to discover latent topics across fragmentation patterns for unsupervised characterization. Use it as the prerequisite step before topic visualization in the ms2lda web interface.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - gensim
  - Python
  - Docker
  - PostgreSQL
  - Django
  techniques:
  - LC-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- Run gensim lda
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

# gensim-pipeline-execution

## Summary

Execute a three-stage gensim LDA pipeline to infer topics from LC-MS/MS metabolomics data: generating a corpus from MS2 spectra, running latent Dirichlet allocation, and loading results into PostgreSQL. This skill orchestrates the complete workflow from raw mass spectrometry input to database-backed topic visualization.

## When to use

Apply this skill when you have an MS2 spectral file (MGF format) from LC-MS/MS metabolomics analysis and need to discover latent topics across fragmentation patterns for unsupervised characterization. Use it as the prerequisite step before topic visualization in the ms2lda web interface.

## When NOT to use

- Input is already a pre-computed LDA model or topic table — use the insert endpoint directly instead.
- MS2 file is in a format other than MGF — first convert to MGF or use appropriate preprocessing.
- PostgreSQL or Django server is not running — set up Docker containers or local services first.

## Inputs

- MS2 spectral file (MGF format)
- PostgreSQL server connection (running and accessible)
- Django server (up and running, as noted in README)

## Outputs

- Corpus JSON file (intermediate: feature representation from MS2 data)
- LDA result JSON file (gensim model: topic distributions and model parameters)
- PostgreSQL database records (experiment metadata, topic assignments, LDA artifacts)

## How to apply

Execute three sequential commands via run_gensim.py: (1) corpus generation from an MGF file with `./run_gensim.py corpus -f mgf <input.mgf> <output.corpus.json>`, which extracts features/corpus representation; (2) gensim LDA inference with `./run_gensim.py gensim <corpus.json> <ldaresult.json>`, which infers topic distributions; (3) database insertion with `./run_gensim.py insert <ldaresult.json> <username> <experiment_name>`, which loads the JSON result into PostgreSQL for web access. Verify success by confirming no errors in each stage and that the experiment is accessible in the database.

## Related tools

- **gensim** (Performs Latent Dirichlet Allocation topic inference on the corpus representation of MS2 spectra)
- **PostgreSQL** (Stores LDA results, experiment metadata, and topic assignments for persistent access and web visualization)
- **Django** (Web application framework hosting the ms2lda server that provides access to inserted LDA experiments) — https://github.com/glasgowcompbio/ms2ldaviz
- **Python** (Language in which run_gensim.py and the pipeline orchestration are implemented)
- **Docker** (Containerization for PostgreSQL and other services required by the ms2lda application)

## Examples

```
./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json && ./run_gensim.py gensim myexp.corpus.json myexp.ldaresult.json && ./run_gensim.py insert myexp.ldaresult.json stefanv myexp
```

## Evaluation signals

- No error messages or exceptions from any of the three run_gensim.py commands (corpus, gensim, insert).
- Corpus JSON file is valid JSON and contains topic term distributions matching the input MGF feature count.
- LDA result JSON file is parseable and includes model parameters (alpha, beta, topic distributions).
- PostgreSQL query confirms that the experiment record exists with the provided username and experiment name.
- Web interface (http://localhost:8000) returns the experiment when queried or browsed post-insertion.

## Limitations

- Requires a running Django server and PostgreSQL database — offline or disconnected workflows will fail at the insert stage.
- The pipeline is synchronous and blocking; large MGF files may require significant computation time for LDA inference.
- Input must be MGF format; other MS2 formats (e.g., mzML) require external conversion before corpus generation.

## Evidence

- [intro] topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data: "topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data"
- [readme] Performs 3 steps: 1. Generate corpus/features from MS2 file 2. Run lda using gensim 3. Insert lda result into db: "Performs 3 steps: 1. Generate corpus/features from MS2 file 2. Run lda using gensim 3. Insert lda result into db"
- [readme] ./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json ./run_gensim.py gensim myexp.corpus.json myexp.ldaresult.json ./run_gensim.py insert myexp.ldaresult.json stefanv myexp: "./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json ./run_gensim.py gensim myexp.corpus.json myexp.ldaresult.json ./run_gensim.py insert myexp.ldaresult.json stefanv myexp"
- [readme] Requires server to be up and running.: "Requires server to be up and running."
- [other] The insert step consumes the LDA result JSON file (myexp.ldaresult.json) and loads it into the database using the command ./run_gensim.py insert with parameters for the result file, a username (stefanv), and an experiment name (myexp).: "The insert step consumes the LDA result JSON file (myexp.ldaresult.json) and loads it into the database using the command ./run_gensim.py insert with parameters for the result file, a username"
