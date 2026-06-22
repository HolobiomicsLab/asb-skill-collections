---
name: mass-fragment-neutral-loss-representation
description: Use when when you have raw or minimally processed MS/MS spectra (in positive or negative ion mode) and aim to infer recurring fragmentation patterns (Mass2Motifs) using topic modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - Python
  - Latent Dirichlet Allocation (LDA)
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- Invoke the main script `ms2lda_runfull.py` with your arguments
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-fragment-neutral-loss-representation

## Summary

Convert tandem mass spectrometry (MS/MS) spectra into a bag-of-fragments representation with extracted neutral losses and noise filtering, producing a structured document-term matrix suitable for probabilistic topic modeling. This preprocessing step transforms raw spectral peaks into interpretable fragmentation vocabularies that enable discovery of recurring substructures.

## When to use

When you have raw or minimally processed MS/MS spectra (in positive or negative ion mode) and aim to infer recurring fragmentation patterns (Mass2Motifs) using topic modeling. Apply this skill before LDA to convert peaks into a standardized bag-of-fragments format with neutral losses explicitly represented and noise removed.

## When NOT to use

- When input spectra are already library-matched compounds with known structures; MS2LDA is designed for unsupervised discovery, not confirmation of known compounds.
- When spectra have very low signal-to-noise ratio or minimal fragmentation (e.g., single dominant peak); bag-of-fragments will be too sparse to infer meaningful motifs.
- When you require quantitative abundance estimation rather than presence/absence or relative intensity patterns; bag-of-fragments treats fragments as discrete vocabulary terms, losing fine-grained intensity dynamics.

## Inputs

- raw MS/MS spectra (mzML, mzXML, or similar format)
- precursor m/z and mass values
- spectrum intensity profiles
- ion mode specification (positive/negative)

## Outputs

- bag-of-fragments document-term matrix
- neutral-loss vocabulary
- noise-filtered spectral corpus
- fragment-loss probability distributions (input to LDA)
- JSON-serialized spectral representation

## How to apply

Load preprocessed spectra and convert each spectrum into a bag-of-fragments representation by extracting individual m/z peaks and computing neutral losses (differences between precursor mass and fragment peaks). Filter out low-intensity noise peaks according to signal-to-noise thresholds and ion-mode-specific cutoffs. Construct a document-term matrix where each spectrum is a document and fragments/losses are terms with their intensities or occurrence counts as weights. This bag-of-fragments corpus is then passed to LDA, which learns which fragments and losses co-occur across spectra to infer motif topics. The representation succeeds when fragments and losses are discretized into a vocabulary, noise is suppressed below a usable threshold, and the resulting matrix is sparse and suitable for convergence under LDA iteration.

## Related tools

- **MS2LDA** (orchestrates the full workflow including preprocessing, LDA modeling, and annotation of bag-of-fragments spectra) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (probabilistic topic model applied to the bag-of-fragments matrix to infer Mass2Motifs)
- **Python** (runtime environment for loading, filtering, and serializing spectral corpus)

## Examples

```
from ms2lda.preprocessing import prepare_spectra; corpus = prepare_spectra('spectra.mzML', ion_mode='positive', noise_threshold=0.01, min_fragment_mz=50); print(f'Corpus size: {len(corpus)} spectra, {len(corpus.vocabulary)} fragments/losses')
```

## Evaluation signals

- Bag-of-fragments matrix is sparse, non-empty, and compatible with LDA input schema (document × term with non-negative weights).
- Neutral loss vocabulary is complete: all losses are >= 1 m/z and <= precursor m/z; no impossible or duplicate loss entries.
- Noise filtering reduces the number of low-intensity peaks by >50% while retaining significant fragment peaks (e.g., base peak and top N peaks per spectrum remain).
- Serialized JSON output contains valid JSON with consistent schema: each spectrum has 'fragments', 'losses', 'precursor_mz', and 'intensity' fields populated.
- LDA convergence monitoring shows decreasing perplexity or increasing likelihood over iterations; if convergence is flat or diverges, the fragment representation may be malformed or the corpus too sparse.

## Limitations

- Bag-of-fragments discards peak order and intensity fine structure; temporal or sequential fragmentation information is lost.
- Neutral loss computation depends on accurate precursor mass; errors in precursor assignment propagate into the loss vocabulary.
- Noise filtering thresholds are dataset- and ion-mode-dependent; aggressive filtering may discard rare but informative low-abundance losses.
- Only a fraction of available mass spectrometry information is traditionally utilized; this representation focuses on fragment and loss patterns but does not encode charge states, isotope patterns, or other spectral features.
- The bag-of-fragments approach assumes fragments and losses are exchangeable within a spectrum; it cannot encode positional or hierarchical fragmentation pathways.

## Evidence

- [methods] Convert MS/MS spectra into a bag-of-fragments format, extract neutral losses, and filter out noise: "Convert MS/MS spectra into a bag-of-fragments format and extract neutral losses, filter out noise"
- [other] Load the preprocessed spectral corpus (bag-of-fragments representation with neutral losses extracted and noise filtered) into memory using Python: "Load the preprocessed spectral corpus (bag-of-fragments representation with neutral losses extracted and noise filtered) into memory using Python"
- [other] MS2LDA applies Latent Dirichlet Allocation to infer which motifs are most likely to explain the observed fragmentation patterns in mass spectrometry data: "MS2LDA applies Latent Dirichlet Allocation to infer which motifs are most likely to explain the observed fragmentation patterns in mass spectrometry data"
- [readme] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
- [readme] MS2LDA identifies recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "MS2LDA identifies recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
