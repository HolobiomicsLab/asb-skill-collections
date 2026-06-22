---
name: spectral-data-format-conversion
description: Use when you have raw tandem mass spectrometry data in one or more of the vendor formats (MGF, mzML, or msp) and need to apply unsupervised topic modeling (LDA-based motif discovery) or comparative fragmentation analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  - Spectra
  - xcms
  - R
  - knitr
  - kableExtra
  - ProteoWizard MSConvert
  - TARDIS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
- doi: 10.1021/acs.analchem.5c00567
  title: ''
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
  - build: coll_tardis
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_ms2lda_2_cq
schema_version: 0.2.0
---

# spectral-data-format-conversion

## Summary

Convert raw mass spectrometry spectral data from vendor-specific input formats (MGF, mzML, msp) into a unified bag-of-fragments representation with neutral losses retained, preparing spectra for downstream topic modeling in MS2LDA. This standardization is essential because MS/MS data arrives in heterogeneous formats but LDA modeling requires a consistent, normalized feature representation.

## When to use

You have raw tandem mass spectrometry data in one or more of the vendor formats (MGF, mzML, or msp) and need to apply unsupervised topic modeling (LDA-based motif discovery) or comparative fragmentation analysis. Apply this skill before any modeling step that expects spectra in bag-of-fragments format with explicit neutral loss information.

## When NOT to use

- Input is already a pre-processed feature table or bag-of-words vector — skip directly to modeling
- Data is from a single, proprietary vendor tool that has already performed internal standardization and neutral-loss extraction — conversion may introduce redundancy or information loss
- Spectra lack valid precursor mass or charge information, making neutral-loss computation impossible

## Inputs

- MGF-format mass spectrometry spectral files
- mzML-format mass spectrometry spectral files
- msp-format mass spectrometry spectral files
- Precursor m/z and charge state per spectrum
- Fragment m/z values and intensities per spectrum

## Outputs

- Bag-of-fragments representation with neutral losses
- Polarity-filtered spectrum collection
- Noise-cleaned high-quality fragment ion set
- Normalized spectrum vectors ready for LDA modeling

## How to apply

Load raw MS/MS spectra from the input file using MS2LDA.Preprocessing.load_and_clean, which automatically detects and parses .mgf, .mzML, or .msp format. Select ionization polarity mode (positive or negative ion mode) to filter spectra by your experimental design. Apply noise filtering by removing low signal-to-noise ratio peaks, retaining only high-quality fragment ions above the instrument's detection threshold. Compute neutral losses by subtracting each fragment mass from the precursor mass, capturing loss patterns (e.g., water, ammonia) that encode structural information. Convert the filtered spectrum into a bag-of-fragments representation where each fragment and its associated neutral loss are indexed as features. Output the collection in model-ready format—typically a normalized data structure compatible with LDA inference engines.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Core module that loads, parses, and filters raw spectra from MGF/mzML/msp files by polarity and noise threshold) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Parent tool providing the preprocessing pipeline and downstream LDA modeling framework) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Programming language used to configure and execute preprocessing workflows)
- **Conda** (Environment management system for installing MS2LDA and dependencies)

## Examples

```
from ms2lda.Preprocessing import load_and_clean; spectra = load_and_clean('data.mgf', polarity='positive', noise_threshold=0.01); bag_of_fragments = convert_to_bag_of_fragments(spectra, extract_neutral_losses=True)
```

## Evaluation signals

- All spectra in output have valid, non-zero precursor m/z and charge state; no records are dropped except those failing polarity or SNR filters
- Neutral loss values are strictly non-negative and do not exceed the precursor mass (invariant: 0 ≤ neutral_loss ≤ precursor_mass)
- Fragment peaks retained in output exceed user-specified SNR threshold; low-intensity noise peaks are absent
- Bag-of-fragments vectors are sparse, non-negative, and uniform in dimensionality across the spectrum collection
- Output format is serializable and compatible with downstream LDA inference (e.g., pyLDAvis or Mallet input format)

## Limitations

- Neutral loss extraction assumes single-charge or known charge state; multiply-charged precursors may produce ambiguous or duplicate neutral losses if charge is incorrectly inferred
- SNR-based noise filtering is heuristic and may discard low-abundance but genuine fragment ions; threshold tuning is data-dependent and may require manual validation
- MGF, mzML, and msp formats have variable metadata completeness; missing or corrupted precursor mass or charge fields will cause parsing errors or data loss
- Polarity mode filtering is mutually exclusive (positive OR negative); mixed-polarity datasets must be split and processed separately, doubling computation

## Evidence

- [other] 1. Load MS/MS spectra from input file (.mgf, .mzML, or .msp format) using MS2LDA.Preprocessing.load_and_clean module.: "Load MS/MS spectra from input file (.mgf, .mzML, or .msp format) using MS2LDA.Preprocessing.load_and_clean module"
- [other] 2. Filter spectra by ionization polarity (positive or negative ion mode) based on user selection.: "Filter spectra by ionization polarity (positive or negative ion mode) based on user selection"
- [other] 3. Apply noise filtering to remove low signal-to-noise ratio peaks and retain only high-quality fragment ions.: "Apply noise filtering to remove low signal-to-noise ratio peaks and retain only high-quality fragment ions"
- [other] 4. Extract neutral losses from each spectrum by computing the difference between precursor mass and fragment mass.: "Extract neutral losses from each spectrum by computing the difference between precursor mass and fragment mass"
- [other] 5. Convert filtered spectra into a bag-of-fragments representation with neutral losses retained.: "Convert filtered spectra into a bag-of-fragments representation with neutral losses retained"
- [methods] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
- [methods] Convert MS/MS spectra into a bag-of-fragments format: "Convert MS/MS spectra into a bag-of-fragments format"
- [methods] Extract neutral losses: "Extract neutral losses"
- [methods] MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data.: "MS2LDA applies probabilistic topic modeling, originally developed for natural language processing (NLP), to tandem mass spectrometry (MS/MS) data"
