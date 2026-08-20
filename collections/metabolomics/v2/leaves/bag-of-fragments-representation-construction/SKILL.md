---
name: bag-of-fragments-representation-construction
description: Use when after noise filtering and polarity selection of MS/MS spectra
  (from .mgf, .mzML, or .msp files), when you need to prepare spectra for unsupervised
  discovery of recurring fragmentation patterns without prior compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  - Latent Dirichlet Allocation (LDA)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural
  language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- ms2lda_runfull.py
- '::: MS2LDA.Preprocessing.load_and_clean'
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- These steps assume you have [Conda](http://conda.io/) installed.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_2_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_2_cq
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

# bag-of-fragments-representation-construction

## Summary

Convert filtered MS/MS spectra into a bag-of-fragments representation that encodes fragment ions and their neutral losses as discrete features, enabling downstream topic modeling with LDA. This representation flattens the ordered sequence of fragment peaks into an unordered multiset suitable for probabilistic inference of recurring fragmentation motifs.

## When to use

After noise filtering and polarity selection of MS/MS spectra (from .mgf, .mzML, or .msp files), when you need to prepare spectra for unsupervised discovery of recurring fragmentation patterns without prior compound identification. Use this skill when your goal is to apply LDA-based topic modeling to infer Mass2Motifs that explain observed fragmentation behavior across a spectral dataset.

## When NOT to use

- Input spectra are already in feature-vector or continuous intensity form without explicit m/z annotation; bag-of-fragments requires discrete fragment identity and precursor mass.
- Analysis goal is to preserve peak intensity rank-ordering or isotope patterns; this representation discards ordering and treats all fragment occurrences equally.
- Spectra have not been noise-filtered or polarity-selected; raw spectra with low-quality peaks will produce uninformative bags dominated by noise fragments.

## Inputs

- Noise-filtered MS/MS spectra collection (post-polarity-selection)
- Precursor m/z values per spectrum
- Fragment ion m/z and intensity peaks per spectrum

## Outputs

- Bag-of-fragments representation (multiset of fragment ions and neutral losses per spectrum)
- Model-ready spectrum collection with discrete fragment/loss features
- Normalized spectrum collection in LDA-compatible format

## How to apply

Following preprocessing that filters spectra by ionization polarity and removes low signal-to-noise ratio peaks, compute neutral losses for each spectrum by subtracting fragment ion m/z values from the precursor mass. Represent each spectrum as a bag (multiset) where each element is a discrete fragment ion or neutral loss value, preserving occurrence frequency but discarding peak intensity ordering. This bag-of-fragments encoding converts continuous m/z intensities into a categorical feature space amenable to LDA's multinomial likelihood model. Retain neutral loss information explicitly, as these encode important structural clues about fragmentation pathways. The resulting collection of bags is then ready for LDA training to discover which fragment/neutral-loss combinations co-occur frequently across the dataset.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Loads raw MS/MS spectra and applies polarity filtering and noise removal prior to bag-of-fragments construction) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Applies Latent Dirichlet Allocation to the bag-of-fragments representation to infer Mass2Motifs) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Probabilistic topic model that operates on bag-of-fragments data to discover recurring fragmentation patterns)
- **Python** (Programming language in which MS2LDA preprocessing and bag-of-fragments construction are implemented)

## Evaluation signals

- Each spectrum is represented as a multiset with positive integer counts for each discrete fragment/neutral-loss feature; verify no negative or fractional counts.
- Neutral loss values are correctly computed as (precursor_mass − fragment_mass) for each observed fragment; spot-check 5–10 spectra against raw peak lists.
- The bag representation preserves all high-quality fragments after noise filtering; verify fragment count per spectrum is consistent with post-filter peak inventory.
- Downstream LDA inference converges within expected iterations and produces interpretable motifs with recurring fragment/neutral-loss signatures; if LDA fails or motifs are uninformative, bag construction may have lost critical structural information.
- Output format is compatible with LDA input schema (e.g., scipy sparse matrix, dictionary of counts, or equivalent); verify row/column dimensions and sparsity match expected spectrum × feature space.

## Limitations

- Bag-of-fragments representation discards peak intensity information and ordering, which may remove information about relative abundance or fragmentation pathway priority; sensitivity to fragment abundance is not recoverable from the bag.
- Neutral loss computation depends on accurate precursor m/z; errors in precursor mass assignment propagate into incorrect neutral loss features and degrade motif quality.
- Representation assumes all fragments are independent; complex fragmentation cascades or sequential losses may not be correctly captured in a simple bag without explicit higher-order structure.
- Very low abundance fragments that survive noise filtering but occur in only a few spectra may create spurious motif associations; no automatic filtering by frequency or support threshold is mentioned.

## Evidence

- [other] Convert MS/MS spectra into a bag-of-fragments representation with neutral losses retained.: "Convert MS/MS spectra into a bag-of-fragments representation with neutral losses retained."
- [other] Extract neutral losses from each spectrum by computing the difference between precursor mass and fragment mass.: "Extract neutral losses from each spectrum by computing the difference between precursor mass and fragment mass."
- [other] Output the cleaned and normalized spectrum collection in model-ready format for downstream LDA modeling.: "Output the cleaned and normalized spectrum collection in model-ready format for downstream LDA modeling."
- [readme] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns.: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns."
