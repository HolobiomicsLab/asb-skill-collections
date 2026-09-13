---
name: mass-spectrum-tokenization-and-bag-of-fragments-generation
description: Use when after filtering and cleaning MS/MS spectra (positive/negative
  ion mode) but before applying Latent Dirichlet Allocation for Mass2Motif discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2LDA
  - Python
  - Conda
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural
  language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- Invoke the main script `ms2lda_runfull.py` with your arguments
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- These steps assume you have [Conda](http://conda.io/) installed.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_cq
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

# mass-spectrum-tokenization-and-bag-of-fragments-generation

## Summary

Convert filtered MS/MS spectra into a bag-of-fragments representation by extracting fragment ions and neutral losses as discrete tokens with their intensities. This preprocessing step transforms raw spectral data into a document-like format suitable for topic modeling (LDA) in MS2LDA.

## When to use

After filtering and cleaning MS/MS spectra (positive/negative ion mode) but before applying Latent Dirichlet Allocation for Mass2Motif discovery. Use this skill when you need to convert continuous m/z and intensity data into a discrete, aggregated format where fragment ions and neutral losses become the vocabulary tokens for probabilistic topic modeling.

## When NOT to use

- Input spectra have not yet been cleaned or filtered for noise and low-intensity artifacts — apply preprocessing first
- Target is direct spectral comparison (e.g., library matching, cosine similarity) rather than motif discovery — bag-of-fragments aggregation loses m/z resolution
- Precursor mass or charge state information is missing or unreliable — neutral loss calculation requires accurate precursor mass

## Inputs

- Filtered MS/MS spectra (mgf, mzML, or msp format)
- Precursor m/z and mass values per spectrum
- Fragment ion m/z and intensity pairs
- Ionization-mode metadata (positive or negative)

## Outputs

- Bag-of-fragments corpus object (MS2LDA.Preprocessing.generate_corpus output)
- Document-term matrix with fragments and neutral losses as vocabulary
- Structured vocabulary mapping (fragment m/z or neutral loss → token ID)

## How to apply

Extract neutral loss values from each spectrum by computing differences between the precursor mass and each observed fragment ion m/z. Aggregate all fragment ions and neutral losses for each spectrum as discrete tokens, preserving their intensities or normalized abundance values. Pass the resulting corpus (documents and vocabulary) through MS2LDA.Preprocessing.generate_corpus to produce the structured corpus object. The rationale is that MS/MS fragmentation patterns are best modeled as a mixture of recurring substructures (motifs); tokenization converts continuous spectral peaks into countable, comparable units that LDA can discover and interpret as recurrent fragmentation patterns across a dataset.

## Related tools

- **MS2LDA** (Hosts the Preprocessing.load_and_clean and Preprocessing.generate_corpus modules used to load spectra and convert filtered spectra into bag-of-fragments corpus format) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Programming language used to implement the tokenization and corpus generation workflow)

## Examples

```
from MS2LDA.Preprocessing import load_and_clean, generate_corpus; spectra = load_and_clean('data.mgf', ionization_mode='positive'); corpus = generate_corpus(spectra)
```

## Evaluation signals

- Corpus object is non-empty and contains all spectra from the input dataset with no null documents
- Fragment and neutral loss tokens in vocabulary are numeric (m/z values) or labeled consistently; no malformed or duplicate token IDs
- Document-term matrix dimensions match: number of rows = number of spectra, number of columns = size of vocabulary
- Intensity/abundance values in the bag-of-fragments are preserved and non-negative; sum-to-nonzero per document
- Neutral loss values are correctly computed: precursor_mass − fragment_m/z for each fragment; no negative or unrealistic (> precursor mass) losses

## Limitations

- Tokenization discards m/z resolution and temporal order information; spectra with closely spaced fragments (within instrument resolution) may be collapsed into single tokens
- Neutral loss extraction assumes accurate precursor mass and charge state; errors in precursor assignment propagate to incorrect loss values
- Intensity normalization method (raw vs. relative abundance) is not specified in the workflow; choice affects weighting in downstream LDA modeling
- Multi-charge precursor ions require deconvolution or charge-aware neutral loss calculation, which may not be handled automatically

## Evidence

- [other] Extract neutral loss values from each spectrum by computing differences between precursor mass and observed fragment ions.: "Extract neutral loss values from each spectrum by computing differences between precursor mass and observed fragment ions."
- [other] Convert filtered spectra into bag-of-fragments format, aggregating fragment ions and neutral losses as discrete tokens with their intensities.: "Convert filtered spectra into bag-of-fragments format, aggregating fragment ions and neutral losses as discrete tokens with their intensities."
- [other] Pass the processed corpus (documents and vocabulary) to MS2LDA.Preprocessing.generate_corpus to produce the structured corpus object required for LDA modeling.: "Pass the processed corpus (documents and vocabulary) to MS2LDA.Preprocessing.generate_corpus to produce the structured corpus object required for LDA modeling."
- [methods] Convert MS/MS spectra into a bag-of-fragments format: "Convert MS/MS spectra into a bag-of-fragments format"
- [methods] MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data.: "MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data."
