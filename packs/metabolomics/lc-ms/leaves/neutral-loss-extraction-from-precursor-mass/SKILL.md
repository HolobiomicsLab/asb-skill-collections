---
name: neutral-loss-extraction-from-precursor-mass
description: Use when after loading and noise-filtering raw MS/MS spectra (in .mgf,
  .mzML, or .msp format) and before applying LDA for Mass2Motif inference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
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

# neutral-loss-extraction-from-precursor-mass

## Summary

Extract neutral losses from tandem mass spectrometry spectra by computing the difference between precursor mass and each fragment ion mass. This step converts raw fragmentation data into a bag-of-fragments representation that encodes structural information for downstream topic modeling and motif discovery.

## When to use

Apply this skill after loading and noise-filtering raw MS/MS spectra (in .mgf, .mzML, or .msp format) and before applying LDA for Mass2Motif inference. Neutral loss extraction is required when you need to represent fragmentation patterns as features for unsupervised motif discovery, particularly when the goal is to identify recurring substructures across a spectral dataset without prior compound identification.

## When NOT to use

- Input spectra have not been filtered for noise or polarity — apply preprocessing first to avoid including low-quality fragments in neutral loss calculations.
- Precursor mass values are missing or unreliable — neutral loss computation depends on accurate precursor m/z; verify mass calibration before proceeding.
- Goal is to perform library matching or spectral similarity search — neutral loss extraction is specific to unsupervised motif discovery and is not the standard feature for spectral networking or MS/MS library searches.

## Inputs

- Noise-filtered MS/MS spectra collection (positive or negative ion mode)
- Precursor m/z values per spectrum
- Fragment ion m/z values per spectrum

## Outputs

- Bag-of-fragments representation with neutral losses retained
- Neutral loss feature vectors (precursor_mass − fragment_mass for each fragment)
- Model-ready spectrum collection with neutral losses encoded

## How to apply

For each spectrum in the preprocessed collection, compute the neutral loss value as (precursor_mass − fragment_mass) for every detected fragment ion. Retain the computed neutral losses alongside their corresponding fragment masses in the bag-of-fragments representation. The rationale is that neutral losses encode diagnostic structural information: loss of water (18 Da), ammonia (17 Da), carbon dioxide (44 Da), and other characteristic moieties reveal functional groups present in the original compound. By including neutral losses as explicit features in the topic model, LDA can identify motifs that represent recurring loss patterns, improving both discovery and interpretability of substructures.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Loads raw MS/MS spectra from input files and performs initial noise filtering and polarity selection before neutral loss extraction) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Consumes the bag-of-fragments with neutral losses and applies LDA to learn Mass2Motifs that describe recurring fragmentation and neutral loss patterns) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Programming language used to implement neutral loss computation within the MS2LDA workflow)

## Evaluation signals

- All spectra in the output collection have neutral loss values computed; no missing or NaN neutral loss entries for valid fragment ions.
- Neutral loss values are all positive and fall within expected range (typically 0–500 Da for small-molecule fragmentation); extreme or negative values indicate precursor mass errors.
- Bag-of-fragments representation is sparse and interpretable: each spectrum contains only fragment masses and their corresponding neutral losses, with no duplicates or redundant entries.
- Model-ready format is compatible with downstream LDA inference: the structure matches the expected input schema for MS2LDA's modeling module (e.g., dictionary of fragment IDs and neutral loss counts per spectrum).
- Neutral loss distribution across the dataset shows expected patterns (e.g., peaks at 18, 44, 17 Da for common losses like H₂O, CO₂, NH₃), indicating that extracted losses encode real structural information rather than noise.

## Limitations

- Accuracy depends critically on precursor mass calibration and quality of noise filtering in the preprocessing step; miscalibrated precursor m/z values propagate directly into all neutral loss calculations.
- Neutral loss extraction alone does not disambiguate isobaric losses (e.g., loss of N₂ vs. CO from different precursors can yield the same m/z difference); additional context or complementary fragmentation rules are needed for chemical interpretation.
- Large fragmentation trees with hundreds of fragments per spectrum can produce dense, uninformative neutral loss distributions that may hinder LDA convergence; manual filtering or parameter tuning may be required for high-complexity spectra.
- The method assumes that fragment ions result from single neutral loss events; multiply-charged or multiply-fragmented ions may produce spurious neutral loss values that degrade motif quality.

## Evidence

- [other] Extract neutral losses from each spectrum by computing the difference between precursor mass and fragment mass.: "Extract neutral losses from each spectrum by computing the difference between precursor mass and fragment mass."
- [other] Convert MS/MS spectra into a bag-of-fragments representation with neutral losses retained.: "Convert filtered spectra into a bag-of-fragments representation with neutral losses retained."
- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns.: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns."
- [readme] Mass spectrometry fragmentation patterns hold abundant structural information vital for analytical chemistry, natural product research, and food safety assessments.: "Mass spectrometry fragmentation patterns hold abundant structural information vital for analytical chemistry, natural product research, and food safety assessments."
