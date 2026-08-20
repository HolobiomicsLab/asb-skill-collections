---
name: ms2-spectral-feature-extraction
description: Use when you have LC-MS/MS metabolomics data in MGF format and need to
  prepare it for Latent Dirichlet Allocation (LDA) topic modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - gensim
  - run_gensim.py
  techniques:
  - LC-MS
  license_tier: open
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

# ms2-spectral-feature-extraction

## Summary

Extracts mass-to-charge ratio (m/z) peaks from LC-MS/MS fragmentation spectra in MGF format and converts them into a bag-of-words corpus representation suitable for unsupervised topic modeling. This step transforms raw tandem mass spectrometry data into feature vectors that encode the compositional structure of each spectrum.

## When to use

You have LC-MS/MS metabolomics data in MGF format and need to prepare it for Latent Dirichlet Allocation (LDA) topic modeling. The input should be a single MGF file containing MS2 fragmentation spectra from your experiment, and your goal is to extract features (peaks) and create a machine-readable corpus that serves as input to the gensim LDA pipeline.

## When NOT to use

- Input is not in MGF format (e.g. mzML, netCDF, or vendor-specific binary formats not explicitly supported by run_gensim.py corpus -f mgf).
- You need to retain full spectrum metadata (retention time, precursor m/z, charge state) — the corpus extraction step discards auxiliary spectrum annotations and outputs only the feature bag-of-words representation.
- The MGF file contains MS1 (precursor) spectra only, without MS2 (fragmentation) data — the corpus generation step requires tandem MS spectra with fragment peaks.

## Inputs

- MGF file containing LC-MS/MS tandem mass spectrometry data (MS2 fragmentation spectra)

## Outputs

- JSON corpus file in gensim bag-of-words format (dictionary of spectrum_id → list of (peak_index, frequency) tuples)

## How to apply

Load the MGF file using the ms2ldaviz `run_gensim.py corpus` command with the `-f mgf` flag, which invokes gensim's corpus generation module to parse MS2 fragmentation spectra. The routine extracts m/z peaks from each spectrum, builds a dictionary mapping unique peaks to feature indices, and serializes the output as a JSON file in gensim's bag-of-words format. Each spectrum is represented as a list of (feature_index, frequency) pairs. Verify that the JSON corpus file is valid JSON, contains entries for each spectrum in the input MGF, and that all feature indices are non-negative integers within the vocabulary size.

## Related tools

- **gensim** (Corpus generation module that parses MGF spectra, extracts m/z peaks as features, builds the vocabulary dictionary, and serializes the bag-of-words representation as JSON.) — https://github.com/RaRe-Technologies/gensim
- **run_gensim.py** (Command-line wrapper script that orchestrates the corpus extraction workflow; invoked with 'corpus -f mgf' subcommand to perform MS2-to-corpus conversion.) — https://github.com/glasgowcompbio/ms2ldaviz
- **Python** (Runtime environment for executing the run_gensim.py script and gensim library.)

## Examples

```
./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json
```

## Evaluation signals

- Output JSON file is parseable as valid JSON and contains at least one entry (one spectrum/document).
- Each spectrum entry in the corpus is a list of (feature_index, count) tuples with non-negative integer indices and positive integer frequencies.
- Feature indices are contiguous integers from 0 to (vocabulary_size - 1); no gaps or negative indices.
- The number of unique features (vocabulary size) is reasonable for MS2 fragmentation data (typically tens to low thousands of distinct m/z peaks across the experiment).
- The corpus JSON can be successfully ingested by the downstream `run_gensim.py gensim` LDA fitting step without parse errors.

## Limitations

- The extraction step discards all spectrum metadata (precursor m/z, retention time, scan number, charge state) and retains only the peak list; if you need to map results back to original spectra, store the mapping separately.
- Low-abundance peaks may be lost if the MGF importer or gensim corpus builder applies intensity thresholds or filtering; no explicit control over peak selection thresholds is documented in the README.
- The bag-of-words representation treats all m/z peaks as unordered features; spectral order and fragmentation tree structure are discarded.

## Evidence

- [other] The corpus generation step accepts an MGF-format MS2 file and outputs a JSON corpus representation via the command: `./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json`: "Load the MGF file using gensim's corpus generation module. Parse MS2 fragmentation spectra and extract mass-to-charge ratio (m/z) peaks as features. Build a dictionary mapping peaks to feature"
- [readme] Topics inferred from Latent Dirichlet Allocation can be used to assist in unsupervised characterisation of fragmented LC-MS-MS metabolomics data: "A web application developed in Django+D3 to visualise how topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS)"
- [readme] Step 1 of the gensim LDA pipeline is corpus/feature generation from MS2 file: "Performs 3 steps: 1. Generate corpus/features from MS2 file"
- [other] The corpus serves as input to the downstream gensim LDA modeling step: "which serves as input to the subsequent gensim LDA modeling step"
