---
name: mass-spectrometry-peak-filtering-and-noise-reduction
description: Use when you have raw MS/MS spectra in MGF, mzML, or msp format and need to prepare them for mass2motif discovery or topic modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3068
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-peak-filtering-and-noise-reduction

## Summary

Filters and cleans tandem mass spectrometry (MS/MS) spectra from raw input formats (MGF, mzML, msp) by selecting ionization polarity mode and removing low signal-to-noise ratio peaks to prepare spectra for downstream topic modeling. This preprocessing step is essential for converting raw spectral data into a model-ready bag-of-fragments representation suitable for unsupervised substructure discovery via LDA.

## When to use

Apply this skill when you have raw MS/MS spectra in MGF, mzML, or msp format and need to prepare them for mass2motif discovery or topic modeling. Use it at the beginning of any MS2LDA workflow to ensure only high-quality fragment ions with adequate signal-to-noise are retained, particularly when working with datasets from different ionization sources or when noise levels vary across experiments.

## When NOT to use

- Input spectra are already in a processed bag-of-fragments or feature table format — skip directly to LDA modeling
- Your analysis requires retention of low-abundance peaks or isotopologue information for isotope pattern analysis — this filter removes such fine structure
- Mixed-polarity datasets where you need to preserve both positive and negative ion mode spectra in a single analysis — apply this skill separately to each polarity subset

## Inputs

- Raw MS/MS spectra in MGF format
- Raw MS/MS spectra in mzML format
- Raw MS/MS spectra in msp format
- User-specified ionization polarity (positive or negative ion mode)
- Signal-to-noise ratio threshold (implicit quality parameter)

## Outputs

- Polarity-filtered spectrum collection
- Noise-reduced spectrum collection with high-quality fragment ions
- Bag-of-fragments representation with neutral losses
- Model-ready spectrum collection prepared for LDA
- Neutral loss feature matrix

## How to apply

Load raw spectra using MS2LDA.Preprocessing.load_and_clean module, then filter by ionization polarity mode (positive or negative ion mode) based on your experimental design. Apply noise filtering to remove peaks with low signal-to-noise ratio, retaining only high-quality fragment ions. Extract neutral losses by computing the difference between precursor mass and fragment mass for each spectrum. Convert the filtered spectra into a bag-of-fragments representation with neutral losses retained. Verify output by checking that all spectra belong to a single polarity mode, noise-filtered peaks exceed your SNR threshold, and neutral loss columns are populated correctly before passing to LDA modeling.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Core module that loads and executes polarity filtering and noise reduction on raw spectra from MGF, mzML, or msp files) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Parent framework that orchestrates preprocessing, LDA modeling, and annotation; preprocessing is the required first stage of the MS2LDA workflow) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Execution environment for the MS2LDA preprocessing module)
- **Conda** (Environment and dependency manager for installing MS2LDA and its prerequisites)

## Examples

```
from ms2lda.preprocessing import load_and_clean; spectra = load_and_clean('input.mgf', polarity='positive', snr_threshold=default)
```

## Evaluation signals

- All retained spectra belong to a single ionization polarity mode (positive or negative) with no mixed-polarity contamination
- Neutral loss column is populated for all spectra; neutral loss values are non-negative and ≤ precursor m/z
- Fragment ion peak count per spectrum decreases after noise filtering, indicating successful removal of low-SNR peaks
- Output spectra conform to bag-of-fragments schema with fragment masses and neutral losses as distinct feature columns
- No spectra are lost during filtering; row count matches input (or documents filtering rationale if spectra are removed)

## Limitations

- The skill does not perform compound identification or structural assignment — it only removes noise and normalizes representation; substructure meaning is assigned downstream in the Annotation stage
- Signal-to-noise ratio threshold is not explicitly parameterized in the provided documentation; practitioners must verify that the default SNR cutoff is appropriate for their instrument and sample type
- Neutral loss extraction assumes accurate precursor mass assignment; errors in precursor mass will propagate into incorrect neutral loss values
- The skill is designed for tandem MS/MS data (fragment spectra) and is not applicable to intact mass spectrometry or MS1-only datasets

## Evidence

- [other] Load MS/MS spectra from input file (.mgf, .mzML, or .msp format) using MS2LDA.Preprocessing.load_and_clean module: "Load MS/MS spectra from input file (.mgf, .mzML, or .msp format) using MS2LDA.Preprocessing.load_and_clean module."
- [other] Filter spectra by ionization polarity (positive or negative ion mode) based on user selection: "Filter spectra by ionization polarity (positive or negative ion mode) based on user selection."
- [other] Apply noise filtering to remove low signal-to-noise ratio peaks and retain only high-quality fragment ions: "Apply noise filtering to remove low signal-to-noise ratio peaks and retain only high-quality fragment ions."
- [other] Extract neutral losses from each spectrum by computing the difference between precursor mass and fragment mass: "Extract neutral losses from each spectrum by computing the difference between precursor mass and fragment mass."
- [other] Convert filtered spectra into a bag-of-fragments representation with neutral losses retained: "Convert filtered spectra into a bag-of-fragments representation with neutral losses retained."
- [other] Output the cleaned and normalized spectrum collection in model-ready format for downstream LDA modeling: "Output the cleaned and normalized spectrum collection in model-ready format for downstream LDA modeling."
- [readme] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
- [readme] MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data.: "MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data."
