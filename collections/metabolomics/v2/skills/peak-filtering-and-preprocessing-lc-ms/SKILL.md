---
name: peak-filtering-and-preprocessing-lc-ms
description: Use when you have raw LC-MS/MS spectra from vendor instruments (mzML,
  mzXML, MGF, or MSP format) with variable peak quality and intensity distributions,
  and you plan to perform library matching, molecular networking, or spectral similarity
  comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - matchms
  - gensim
  - Numba
  - Pandas
  - scipy
  - spec2vec
  - Word2Vec
  - Pandas / NumPy / SciPy
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim
  [37]
- making extensive use of Numpy [24] and Numba [25]
- by making extensive use of Numpy [24] and Numba [25], the library
- Spec2Vec was optimised by making extensive use of Numpy [24] and Numba [25], the
  library matching was implemented using Pandas [40]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: spec2vec_grounded
    doi: 10.1371/journal.pcbi.1008724
    title: Spec2Vec
  dedup_kept_from: spec2vec_grounded
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1008724
  all_source_dois:
  - 10.1371/journal.pcbi.1008724
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-filtering-and-preprocessing-LC-MS

## Summary

Standardized preprocessing pipeline for liquid chromatography–tandem mass spectrometry (LC-MS/MS) spectra that removes low-quality peaks, filters spectra by fragment count and mass range, and normalizes peak intensities to enable fair similarity scoring and structural matching. This skill is essential before applying spectral similarity methods like Spec2Vec or cosine-based scoring, as preprocessing directly impacts true-positive rate and reduces false positives in library matching.

## When to use

Apply this skill when you have raw LC-MS/MS spectra from vendor instruments (mzML, mzXML, MGF, or MSP format) with variable peak quality and intensity distributions, and you plan to perform library matching, molecular networking, or spectral similarity comparison. Preprocessing is required before Spec2Vec embedding or cosine similarity scoring, especially when comparing spectra across different ionization conditions or instrument platforms where peak noise and artifact peaks differ.

## When NOT to use

- Input spectra are already intensity-normalized and artifact-removed (e.g., from a published preprocessed library). Reapplying intensity filtering may discard legitimate low-intensity fragments.
- Dataset is GC-MS data without neutral losses; Spec2Vec peak filtering is validated only for LC-MS/MS where neutral losses are reliably measured and informative.
- Analysis requires preservation of all observed peaks for novel fragment discovery or de novo annotation; aggressive intensity filtering (0.01 threshold) may remove rare but structurally informative peaks.

## Inputs

- Raw mass spectrometry spectra in vendor formats (mzML, mzXML, MGF, msp)
- Spectrum metadata: precursor m/z, parent mass, ionization mode
- Optional: InChIKey annotations for quality control and ground-truth validation

## Outputs

- Cleaned spectrum list with peaks filtered by m/z range and intensity threshold
- Peak-filtered spectra ready for Spec2Vec embedding or cosine similarity comparison
- Quality-control report: spectra retained vs. discarded counts, peak statistics

## How to apply

Execute the preprocessing pipeline in order: (1) Remove all peaks with m/z ratios outside the range [0, 1000] to eliminate implausible fragment ions. (2) Discard entire spectra with fewer than 10 fragment peaks, as they lack sufficient fragmentation information for reliable matching. (3) Remove spectra without InChIKey annotation if performing ground-truth validation. (4) For cosine and modified cosine similarity scoring, apply intensity-based peak filtering by ignoring all peaks with relative intensities <0.01 compared to the highest intensity peak in that spectrum. (5) For Spec2Vec, apply parent-mass-scaled peak filtering by retaining at most 0.5 × parent_mass peaks per spectrum (selecting peaks by intensity rank), which balances fragment representation across molecular weight ranges. (6) Validate that the filtered spectrum retains at least the minimum matching peaks threshold (typically 6 for cosine, 10 for modified cosine) to enable downstream scoring. The rationale is that low-intensity and out-of-range peaks are mostly noise or instrument artifacts, mass-based spectrum filtering prevents undersampling of heavier molecules, and the minimum peak count ensures sufficient overlap information for similarity computation.

## Related tools

- **matchms** (Core Python package implementing cosine and modified cosine scoring; provides standardized Spectrum object model and built-in peak filtering and metadata cleaning functions.) — https://github.com/matchms/matchms
- **spec2vec** (Applies parent-mass-scaled peak filtering (max_peaks = 0.5 × parent_mass) before Word2Vec embedding; depends on matchms for spectrum I/O and preprocessing.) — https://github.com/iomega/spec2vec
- **Word2Vec** (Embedding model trained on filtered peak and neutral-loss 'words' to learn spectral relationships; accepts preprocessed spectra as input documents.)
- **gensim** (Python library implementing Word2Vec; used by spec2vec to train and apply spectral embeddings.)
- **Pandas / NumPy / SciPy** (Data manipulation and numerical computation for peak filtering, intensity normalization, and threshold application.)

## Examples

```
from matchms.importing_utils import load_from_mgf
from matchms import Spectrum
spectra = [s for s in load_from_mgf('raw_spectra.mgf') if len(s.peaks) >= 10 and all(mz >= 0 and mz <= 1000 for mz, _ in s.peaks)]
filtered = [Spectrum(mz=s.mz, peaks=[(mz, i) for mz, i in s.peaks if i >= 0.01 * max([x[1] for x in s.peaks])]) for s in spectra]
```

## Evaluation signals

- Verify m/z range: all retained peaks fall within [0, 1000]; any peaks outside this range were removed.
- Verify minimum peak count: all retained spectra contain ≥10 fragment peaks; histogram of peak counts per spectrum should show no values <10.
- Verify intensity threshold: for cosine/modified cosine, no peaks with relative intensity <0.01 remain; spot-check highest-intensity peak for each spectrum and confirm all other peaks meet threshold.
- Verify parent-mass scaling (Spec2Vec only): max retained peaks per spectrum ≈ 0.5 × parent_mass; plot peak count vs. parent mass and confirm linear trend with slope ≈0.5.
- Compare quality metrics before/after: report true-positive and false-positive rates in library matching; preprocessing should reduce false-positive rate compared to unfiltered spectra.

## Limitations

- Parent-mass-scaled peak filtering (0.5 × parent_mass) for Spec2Vec assumes fragment ions scale with molecule size; may undersample small molecules (<100 Da) or oversample very large molecules (>2000 Da) if library is skewed.
- Minimum 10-peak threshold discards low-fragmentation spectra from weakly-ionizing compounds; for such compounds, library coverage will be incomplete.
- Spec2Vec requires retraining of Word2Vec models when applied to experimental data not represented in the training set; model trained on AllPositive dataset (positive ionization) will not generalize well to negative ionization mode without retraining.
- Intensity-based peak filtering depends on signal-to-noise ratio and instrument calibration; spectra from instruments with high baseline noise may lose legitimate low-intensity fragments after 0.01-threshold filtering.
- Pipeline validated only on LC-MS/MS data; GC-MS data cannot be processed with Spec2Vec peak filtering because neutral losses are usually not measured in GC-MS.

## Evidence

- [methods] We removed all peaks with m/z ratios outside the range [0, 1000] and discarded all spectra with less than 10 peaks.: "We removed all peaks with m/z ratios outside the range [0, 1000] and discarded all spectra with less than 10 peaks"
- [methods] For both the cosine and modified cosine score calculations we ignored all peaks with relative intensities <0.01 compared to the highest intensity peak: "For both the cosine and modified cosine score calculations we ignored all peaks with relative intensities <0.01 compared to the highest intensity peak"
- [methods] the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass: "the maximum number of kept peaks per spectrum was set to scale linearly with the estimated parent mass: max(n_peaks) = 0.5 × parentmass"
- [results] removing all spectra with fewer than 10 fragment peaks: "removing all spectra with fewer than 10 fragment peaks"
- [discussion] In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured.: "In the present work, we have only demonstrated performance on LC-MS data and not yet assessed Spec2Vec for GC-MS data. For GC-MS, neutral losses are usually not measured."
- [discussion] one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships; however, since this not necessarily needs to be library spectra and in: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships"
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity."
