---
name: corpus-bag-of-words-representation
description: Use when when you have raw LC-MS/MS data in MGF format and need to prepare it for unsupervised topic modeling of metabolomics fragmentation patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - gensim
  - run_gensim.py
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

# corpus-bag-of-words-representation

## Summary

Convert LC-MS/MS metabolomics spectra from MGF format into a bag-of-words corpus representation suitable for topic modeling. This serializes each MS2 spectrum as a dictionary of mass-to-charge (m/z) peak features and their abundances, enabling downstream latent Dirichlet allocation (LDA) analysis.

## When to use

When you have raw LC-MS/MS data in MGF format and need to prepare it for unsupervised topic modeling of metabolomics fragmentation patterns. Apply this skill as the mandatory first step before running gensim LDA, to extract spectral features (m/z peaks) as a corpus suitable for probabilistic topic inference.

## When NOT to use

- Input is already a feature table or pre-computed document-term matrix (skip directly to LDA)
- Data is in a non-MS2 format (e.g., quantification tables, gene expression matrices) that does not represent fragmentation spectra
- You require retention of raw spectrum metadata (e.g., retention time, precursor m/z, scan IDs) for downstream analysis—this step produces only bag-of-words tokens

## Inputs

- MGF file (Mascot Generic Format) containing LC-MS/MS spectra with MS2 fragmentation data and m/z peak lists

## Outputs

- JSON corpus file containing bag-of-words representation of spectra (list of (feature_index, abundance) pairs per spectrum)
- Feature dictionary mapping m/z peaks to integer indices

## How to apply

Load the MGF file using gensim's corpus generation module, then parse MS2 fragmentation spectra to extract mass-to-charge ratio (m/z) peaks as feature tokens. Build a dictionary mapping each unique peak to a feature index. Serialize the resulting bag-of-words representation—where each spectrum is encoded as a list of (feature_index, abundance) pairs—into a JSON corpus file. The corpus JSON format must be compatible with gensim's downstream LDA and serialization modules, preserving the spectral feature vocabulary for consistent topic inference.

## Related tools

- **gensim** (Provides corpus generation module and bag-of-words serialization for MS2 feature extraction and LDA-compatible dictionary building) — https://github.com/sdrogers/ms2ldaviz
- **Python** (Runtime environment and primary scripting language for corpus generation via run_gensim.py) — https://github.com/sdrogers/ms2ldaviz
- **run_gensim.py** (Command-line tool that orchestrates MGF parsing, m/z feature extraction, dictionary creation, and JSON corpus serialization) — https://github.com/sdrogers/ms2ldaviz

## Examples

```
./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json
```

## Evaluation signals

- Output JSON file is valid and parseable, containing a list of documents (spectra) each represented as (feature_index, count) pairs
- Feature dictionary size and peak coverage reflect the expected m/z range and complexity of the input spectra (e.g., verify against raw MGF peak counts)
- Downstream gensim LDA step runs without vocabulary mismatch errors, confirming corpus feature indices align with dictionary
- Corpus sparsity and token distribution are reasonable (majority of spectra should have multiple peaks, no single spectrum dominates feature space)
- Re-running corpus generation on the same MGF produces identical JSON output (deterministic feature ordering and indexing)

## Limitations

- Bag-of-words representation discards peak ordering, intensity magnitude scaling, and spectral metadata (retention time, precursor m/z); may lose signal for methods requiring temporal or structural context.
- Peak discretization via m/z binning into integer indices can lose fine-grained mass accuracy; choice of m/z tolerance or binning strategy is not parameterized in the cited command.
- MGF format parsing assumes well-formed input; malformed spectra (missing peaks, invalid m/z values) may cause silent errors or vocabulary inconsistencies.
- Memory scaling with corpus size is not discussed; very large MGF files may exceed gensim's in-memory dictionary building capacity.

## Evidence

- [other] The corpus generation step accepts an MGF-format MS2 file and outputs a JSON corpus representation via the command: `./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json`: "corpus generation step accepts an MGF-format MS2 file and outputs a JSON corpus representation via the command: `./run_gensim.py corpus -f mgf myexp.mgf myexp.corpus.json`"
- [other] Parse MS2 fragmentation spectra and extract mass-to-charge ratio (m/z) peaks as features. Build a dictionary mapping peaks to feature indices. Serialize the corpus as a JSON file containing the bag-of-words representation of each spectrum using the gensim corpus format.: "Parse MS2 fragmentation spectra and extract mass-to-charge ratio (m/z) peaks as features. Build a dictionary mapping peaks to feature indices. Serialize the corpus as a JSON file containing the"
- [readme] Perform 3 steps: 1. Generate corpus/features from MS2 file 2. Run lda using gensim 3. Insert lda result into db: "Performs 3 steps: 1. Generate corpus/features from MS2 file 2. Run lda using gensim 3. Insert lda result into db"
- [intro] visualise how topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data: "visualise how topics inferred from Latent Dirichlet Allocation can be used to assist in the unsupervised characterisation of fragmented (LC-MS-MS) metabolomics data"
