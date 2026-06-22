---
name: ionization-mode-specific-preprocessing-handling
description: Use when you have raw MS/MS spectra in supported formats (.mgf, .mzML, or .msp) from mixed ionization modes and need to prepare them for downstream topic modeling (LDA) or motif discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - Python
  - Conda
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
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
---

# ionization-mode-specific-preprocessing-handling

## Summary

This skill applies ion-mode-aware filtering and cleaning to tandem mass spectrometry (MS/MS) spectra before conversion to bag-of-fragments format, treating positive and negative ion mode data with separate processing pipelines to remove low-intensity noise and m/z artifacts while preserving structurally informative fragments and neutral losses.

## When to use

Apply this skill when you have raw MS/MS spectra in supported formats (.mgf, .mzML, or .msp) from mixed ionization modes and need to prepare them for downstream topic modeling (LDA) or motif discovery. The skill is triggered when preprocessing is the first workflow step prior to generating a structured corpus for MS2LDA modeling.

## When NOT to use

- Input spectra are already in bag-of-fragments format or have been preprocessed by another tool; re-preprocessing risks information loss and inconsistent mode handling.
- Spectra lack ionization mode annotation or come from a single, uniform ionization mode where mode-specific filtering would be redundant.
- Input file format is not one of the supported formats (.mgf, .mzML, .msp); the preprocessing module will fail or require format conversion upstream.

## Inputs

- Raw MS/MS spectra files (.mgf, .mzML, or .msp format)
- Metadata specifying ionization mode (positive or negative) for each spectrum or batch
- Precursor mass and fragment ion m/z values with intensity annotations

## Outputs

- Filtered spectra corpus (documents and vocabulary in bag-of-fragments format)
- Mode-partitioned spectral subsets (positive and negative ion mode separately)
- Structured corpus object ready for LDA modeling via MS2LDA.Preprocessing.generate_corpus
- Neutral loss token sets per spectrum

## How to apply

Load the raw spectral data using the MS2LDA.Preprocessing.load_and_clean module, which reads the input file format. Immediately partition spectra by ionization mode (positive vs. negative ion) to apply mode-specific filtering thresholds that account for the different fragmentation and noise characteristics of each mode. For each mode-partitioned subset, remove low-intensity noise peaks and m/z artifacts according to mode-appropriate cutoffs. Simultaneously extract neutral loss values by computing the difference between the precursor mass and each observed fragment ion mass. Convert the filtered spectra into bag-of-fragments format, aggregating fragment ions and neutral losses as discrete tokens alongside their normalized intensities. Finally, pass the processed corpus (documents and vocabulary) to MS2LDA.Preprocessing.generate_corpus to produce the structured corpus object required for LDA inference. The rationale is that positive and negative ion modes produce distinct fragmentation signatures and noise profiles; separating them during preprocessing prevents cross-mode artifact propagation and improves the specificity of learned motifs.

## Related tools

- **MS2LDA** (Provides the preprocessing module (MS2LDA.Preprocessing.load_and_clean and MS2LDA.Preprocessing.generate_corpus) that implements ionization-mode-specific filtering and corpus generation) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Programming language used to invoke the MS2LDA preprocessing functions and manage spectral data manipulation)
- **Conda** (Environment manager for configuring and reproducibly installing MS2LDA and its dependencies)

## Evaluation signals

- Verify that spectra are successfully partitioned by ionization mode with no cross-mode contamination; check that positive and negative ion subsets have distinct m/z and intensity distributions.
- Confirm that the output bag-of-fragments corpus contains fragment ion tokens and neutral loss tokens with normalized intensities; inspect a random sample of documents to ensure tokens are discrete and non-duplicated within a spectrum.
- Validate that low-intensity noise peaks have been removed by comparing the fragment ion count before and after filtering; the post-filter count should be substantially lower and contain only high-confidence peaks.
- Check that neutral loss values are correctly computed: for each fragment, the neutral loss should equal precursor_mass minus fragment_m/z; spot-check 5–10 spectra manually.
- Ensure the final corpus object passes the MS2LDA.Preprocessing.generate_corpus validation step without errors, confirming vocabulary and document indices are consistent and ready for LDA input.

## Limitations

- Mode-specific filtering thresholds are not explicitly parametrized in the provided documentation; users may need empirical tuning or domain expertise to set cutoffs appropriate for their ionization method and instrument.
- Neutral loss extraction assumes well-calibrated precursor mass values; errors in precursor mass annotation will propagate to incorrect neutral loss tokens.
- Only three input file formats are supported (.mgf, .mzML, .msp); users with other formats (e.g., raw vendor formats) must convert upstream.
- The preprocessing skill addresses noise and fragmentation artifacts but does not correct for systematic mass calibration errors or handle mixed-mode spectra acquired simultaneously (e.g., alternating positive/negative scans in a single file).

## Evidence

- [other] Load MS/MS spectra from supported input file formats (.mgf, .mzML, or .msp) using the MS2LDA.Preprocessing.load_and_clean module: "Load MS/MS spectra from supported input file formats (.mgf, .mzML, or .msp) using the MS2LDA.Preprocessing.load_and_clean module"
- [other] Apply ionization-mode-specific filtering to handle positive and negative ion mode data separately, removing low-intensity noise peaks and m/z artifacts: "Apply ionization-mode-specific filtering to handle positive and negative ion mode data separately, removing low-intensity noise peaks and m/z artifacts"
- [other] Extract neutral loss values from each spectrum by computing differences between precursor mass and observed fragment ions: "Extract neutral loss values from each spectrum by computing differences between precursor mass and observed fragment ions"
- [other] Convert filtered spectra into bag-of-fragments format, aggregating fragment ions and neutral losses as discrete tokens with their intensities: "Convert filtered spectra into bag-of-fragments format, aggregating fragment ions and neutral losses as discrete tokens with their intensities"
- [other] Pass the processed corpus (documents and vocabulary) to MS2LDA.Preprocessing.generate_corpus to produce the structured corpus object required for LDA modeling: "Pass the processed corpus (documents and vocabulary) to MS2LDA.Preprocessing.generate_corpus to produce the structured corpus object required for LDA modeling"
- [methods] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
- [methods] MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data: "MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data"
- [readme] These steps assume you have Conda installed: "These steps assume you have Conda installed"
