---
name: ionization-polarity-selection-and-filtering
description: Use when loading raw mass spectrometry data (MGF, mzML, or msp format) into MS2LDA and you need to isolate spectra from a single ionization polarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
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
---

# ionization-polarity-selection-and-filtering

## Summary

Filter tandem mass spectrometry spectra by ionization polarity (positive or negative ion mode) to prepare a homogeneous subset of spectra for downstream topic modeling and motif discovery. This preprocessing step ensures that only spectra from the selected polarity are retained, reducing noise from mixed ionization modes and improving the quality of learned fragmentation patterns.

## When to use

Apply this skill when loading raw mass spectrometry data (MGF, mzML, or msp format) into MS2LDA and you need to isolate spectra from a single ionization polarity. Use it before noise filtering and bag-of-fragments conversion, especially when your dataset contains mixed positive and negative ion mode acquisitions and you want to model substructure patterns within a chemically coherent polarity subset.

## When NOT to use

- Input spectra have already been separated by polarity in upstream processing or are from a single-polarity instrument run.
- Your analysis goal is to discover cross-polarity motifs or compare fragmentation behavior between ionization modes; in this case, preserve the full mixed-polarity dataset.
- Metadata tags for ionization polarity are missing or unreliable in the input file; polarity selection will fail or produce incorrect results.

## Inputs

- raw MS/MS spectra file (MGF, mzML, or msp format)
- ionization polarity selection parameter (positive or negative ion mode)

## Outputs

- polarity-filtered spectrum collection
- retained spectrum count and metadata for selected polarity

## How to apply

Within the MS2LDA.Preprocessing.load_and_clean module, specify the desired ionization polarity (positive or negative ion mode) as a user-selectable parameter during spectrum loading. The preprocessing module will scan the metadata of each spectrum in the input file to identify its assigned polarity and retain only spectra matching the selected mode. This filtering occurs before noise filtering and neutral loss extraction, ensuring a clean and uniform spectrum collection. The rationale is that fragmentation patterns differ systematically between positive and negative ionization, so separating them prevents polarity-driven artifacts in the learned motifs and improves interpretability of Mass2Motifs within each chemical ionization regime.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Core module that implements polarity selection and filtering logic during spectrum loading) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Parent tool providing the integrated preprocessing, modeling, and annotation workflow) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Runtime environment for executing MS2LDA preprocessing and filtering operations)
- **Conda** (Environment management for installing and configuring MS2LDA and dependencies)

## Evaluation signals

- Output spectrum collection contains only spectra with the selected polarity metadata tag; inspect a sample of spectrum headers to confirm polarity consistency.
- Polarity-filtered spectrum count is less than or equal to the input count; verify that no spectra were retained incorrectly due to metadata parsing errors.
- Downstream noise filtering and bag-of-fragments conversion run without polarity-related errors or warnings.
- Mass2Motifs learned from the filtered spectra show coherent fragmentation patterns consistent with the selected ionization mode (e.g., positive-mode motifs include common adducts like [M+H]+ or [M+Na]+).
- Comparison of learned motifs from separate positive and negative mode runs shows distinct chemical signatures rather than cross-polarity artifacts.

## Limitations

- Polarity selection depends on accurate metadata in the input MS/MS file; if polarity tags are missing or corrupted, the filter will either fail or retain incorrect spectra. Manual validation of input file format is recommended.
- This filtering step is binary (polarity in or out); mixed-polarity spectra or spectra with ambiguous polarity metadata will be discarded, potentially reducing dataset size.
- The skill assumes that polarity metadata is stored in standard MS/MS file format fields (e.g., scanlist polarity attribute in mzML); non-standard file formats may not be compatible without preprocessing.

## Evidence

- [full_text] Filter spectra by ionization polarity (positive or negative ion mode) based on user selection.: "Filter spectra by ionization polarity (positive or negative ion mode) based on user selection."
- [full_text] Load MS/MS spectra from input file (.mgf, .mzML, or .msp format) using MS2LDA.Preprocessing.load_and_clean module.: "Load MS/MS spectra from input file (.mgf, .mzML, or .msp format) using MS2LDA.Preprocessing.load_and_clean module."
- [methods] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
- [methods] Convert MS/MS spectra into a bag-of-fragments format: "Convert MS/MS spectra into a bag-of-fragments format"
