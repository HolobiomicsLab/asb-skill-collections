---
name: spectral-noise-filtering-and-artifact-removal
description: Use when you have raw MS/MS spectra in supported formats (.mgf, .mzML,
  or .msp) containing both chemical signal and experimental noise, prior to structural
  motif discovery via topic modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
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

# spectral-noise-filtering-and-artifact-removal

## Summary

Remove low-intensity noise peaks and m/z artifacts from tandem mass spectrometry spectra while preserving biologically relevant fragment ions, applied separately for positive and negative ionization modes before conversion to bag-of-fragments format for downstream LDA modeling.

## When to use

Apply this skill when you have raw MS/MS spectra in supported formats (.mgf, .mzML, or .msp) containing both chemical signal and experimental noise, prior to structural motif discovery via topic modeling. This is the mandatory first step before bag-of-fragments conversion and LDA inference in the MS2LDA workflow.

## When NOT to use

- Input spectra have already been preprocessed and converted to bag-of-fragments format (filtering would be redundant).
- Analysis goal is solely peak detection or mass calibration, not motif discovery (noise filtering for LDA is distinct from quality control for other purposes).
- Spectral data lacks precursor mass information or ionization mode metadata (neutral loss extraction requires both).

## Inputs

- Raw MS/MS spectra in .mgf, .mzML, or .msp file format
- Ionization mode metadata (positive or negative ion mode)
- Precursor mass and fragment ion m/z values with intensities

## Outputs

- Cleaned spectra corpus with noise and artifacts removed
- Bag-of-fragments representation with fragment ions and neutral losses as discrete tokens
- Processed vocabulary and document structure ready for LDA modeling

## How to apply

Load raw spectra using MS2LDA.Preprocessing.load_and_clean, then apply ionization-mode-specific filtering to handle positive and negative ion mode data separately. Remove low-intensity noise peaks and m/z artifacts while retaining fragment ions above a signal threshold; the filtering preserves sufficient intensity variation to extract neutral losses (computed as differences between precursor mass and observed fragment ions) without corrupting the fragmentation signature. Pass the cleaned spectra to MS2LDA.Preprocessing.generate_corpus to produce the structured corpus object required for LDA modeling. Correctness is verified by confirming that neutral loss extraction succeeds and the resulting bag-of-fragments vocabulary contains expected mass differences and fragment tokens with non-zero intensity.

## Related tools

- **MS2LDA** (Provides the Preprocessing.load_and_clean and Preprocessing.generate_corpus modules that implement ionization-mode-aware spectral filtering and bag-of-fragments conversion) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Runtime environment for executing MS2LDA preprocessing functions)
- **Conda** (Environment management for installing MS2LDA dependencies and configuring the preprocessing workflow)

## Examples

```
from MS2LDA.Preprocessing import load_and_clean, generate_corpus; spectra = load_and_clean('raw_spectra.mgf', ion_mode='positive'); corpus = generate_corpus(spectra)
```

## Evaluation signals

- Neutral loss values are successfully computed for all spectra (no NaN or zero-intensity losses).
- Bag-of-fragments vocabulary contains expected fragment ions and neutral losses with non-zero intensities.
- Low-intensity noise peaks are absent from the filtered spectra (verify by comparing intensity distributions before and after filtering).
- Downstream LDA inference converges without errors, indicating corpus structure is valid and noise removal did not corrupt fragment token frequencies.
- Ion-mode specific filtering is confirmed: positive and negative mode spectra are processed with separate thresholds and artifact-removal rules.

## Limitations

- Ionization mode must be correctly specified in metadata; incorrect mode assignment will apply wrong filtering thresholds and degrade motif discovery.
- Neutral loss extraction depends on accurate precursor mass annotation; missing or incorrect precursor values will produce spurious or invalid neutral loss tokens.
- Filtering threshold selection is not explicitly described in the workflow; over-aggressive noise removal may eliminate low-abundance but structurally meaningful fragments.
- Supported input formats are limited to .mgf, .mzML, and .msp; other mass spectrometry data formats require prior conversion.

## Evidence

- [other] MS2LDA preprocessing filters and cleans spectra while handling both positive and negative ion modes as part of the initial workflow step prior to downstream modeling.: "MS2LDA preprocessing filters and cleans spectra while handling both positive and negative ion modes as part of the initial workflow step prior to downstream modeling."
- [other] Apply ionization-mode-specific filtering to handle positive and negative ion mode data separately, removing low-intensity noise peaks and m/z artifacts.: "Apply ionization-mode-specific filtering to handle positive and negative ion mode data separately, removing low-intensity noise peaks and m/z artifacts."
- [other] Load MS/MS spectra from supported input file formats (.mgf, .mzML, or .msp) using the MS2LDA.Preprocessing.load_and_clean module.: "Load MS/MS spectra from supported input file formats (.mgf, .mzML, or .msp) using the MS2LDA.Preprocessing.load_and_clean module."
- [other] Extract neutral loss values from each spectrum by computing differences between precursor mass and observed fragment ions.: "Extract neutral loss values from each spectrum by computing differences between precursor mass and observed fragment ions."
- [other] Convert filtered spectra into bag-of-fragments format, aggregating fragment ions and neutral losses as discrete tokens with their intensities.: "Convert filtered spectra into bag-of-fragments format, aggregating fragment ions and neutral losses as discrete tokens with their intensities."
- [methods] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
