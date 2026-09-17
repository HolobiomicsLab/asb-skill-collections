---
name: metabolomics-data-representation
description: Use when you have a raw MGF file containing fragmented LC-MS-MS metabolomics
  spectra and want to apply Latent Dirichlet Allocation (LDA) to discover hidden topics
  (molecular families, biochemical patterns) across your sample set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3663
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - gensim
  - run_gensim.py
  techniques:
  - LC-MS
  - NMR
  license_tier: open
  provenance_tier: literature
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

# metabolomics-data-representation

## Summary

Transform raw LC-MS-MS metabolomics spectra (MGF files) into a structured corpus representation (JSON) suitable for unsupervised topic modeling. This skill bridges acquisition data and latent semantic analysis by encoding document-term relationships that capture fragmentation patterns.

## When to use

You have a raw MGF file containing fragmented LC-MS-MS metabolomics spectra and want to apply Latent Dirichlet Allocation (LDA) to discover hidden topics (molecular families, biochemical patterns) across your sample set. Use this skill as the mandatory first step in the ms2ldaviz workflow before LDA inference.

## When NOT to use

- Input is already a feature table or pre-computed term-document matrix in a different format (e.g., CSV, h5ad).
- Spectra have already been processed into a corpus representation by a different tool or workflow.
- Raw MS2 data is in a format other than MGF (e.g., mzML, netCDF) without prior conversion.

## Inputs

- MGF file (tandem mass spectrometry spectra in MGF format)
- Experimental metadata (sample identifiers, optional phenotypes)

## Outputs

- corpus JSON file (document-term matrix with feature frequencies and metadata)

## How to apply

Load the MGF file containing MS2 spectra and convert each spectrum (or spectrum group) into a document representation where terms are molecular features (e.g., fragment masses, intensity bins, or chemical shifts). The corpus generation step performs feature extraction and normalization to produce a JSON file where each document records term frequencies and metadata. This intermediate corpus format decouples raw instrumental data from the probabilistic model, allowing independent iteration on corpus design (e.g., mass binning resolution, intensity thresholding) without re-running expensive LDA inference. The resulting corpus.json is a prerequisite input to the gensim LDA inference step.

## Related tools

- **gensim** (Consumes the generated corpus JSON to infer topic distributions via LDA inference; the corpus is the mandatory input format for gensim LDA execution in this workflow.)
- **run_gensim.py** (CLI script that orchestrates corpus generation from MGF input via the 'corpus' subcommand with format flag.) — https://github.com/glasgowcompbio/ms2ldaviz
- **Python** (Language in which the corpus generation logic is implemented.)

## Examples

```
./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json
```

## Evaluation signals

- Output corpus.json file is valid JSON and can be parsed without errors.
- Each document entry in the corpus contains a term frequency vector with non-negative integer or float values.
- Total document count in the corpus matches the number of spectra or spectrum groups in the input MGF file.
- All feature terms are present and mapped consistently across documents (schema validation).
- Corpus JSON can be successfully loaded by gensim without file format or schema exceptions.

## Limitations

- Corpus generation depends on correct MGF format and valid spectral metadata; malformed or truncated MGF files may cause silent data loss or feature extraction errors.
- Feature extraction parameters (e.g., mass binning resolution, intensity normalization) are fixed at generation time and cannot be adjusted post-hoc without re-running this step.
- The ms2ldaviz implementation is designed for LC-MS-MS metabolomics; applicability to other mass spectrometry modalities (e.g., proteomics, MALDI) is not documented.

## Evidence

- [readme] Generate corpus/features from MS2 file: "1. Generate corpus/features from MS2 file"
- [readme] Command to generate corpus from MGF: "./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json"
- [readme] Corpus input to LDA: "2. Run lda using gensim"
- [other] Load the corpus JSON file containing preprocessed document-term representations: "Load the corpus JSON file (myexp.corpus.json) containing preprocessed document-term representations"
- [readme] Topics from LC-MS-MS metabolomics: "visualise how topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data"
