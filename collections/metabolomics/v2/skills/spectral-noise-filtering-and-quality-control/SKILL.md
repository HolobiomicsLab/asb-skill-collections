---
name: spectral-noise-filtering-and-quality-control
description: Use when you have raw MS/MS spectra in multiple formats (.mgf, .msp, .mzML) that contain background noise, instrument artifacts, or low-abundance fragments that would degrade downstream LDA motif discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  - MS2LDA.Preprocessing.generate_corpus
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- from MS2LDA.Preprocessing import load_and_clean
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
- These steps assume you have Conda installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda
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

# spectral-noise-filtering-and-quality-control

## Summary

Filter mass spectrometry spectra by removing low-intensity fragments and neutral losses below statistical significance thresholds, and apply ion mode selection to prepare cleaned data for downstream LDA modeling. This step eliminates noise while preserving structurally informative fragmentation patterns.

## When to use

Apply this skill when you have raw MS/MS spectra in multiple formats (.mgf, .msp, .mzML) that contain background noise, instrument artifacts, or low-abundance fragments that would degrade downstream LDA motif discovery. Use it after spectral loading but before bag-of-fragments corpus generation, especially when working with complex natural product or environmental samples where signal-to-noise ratios vary.

## When NOT to use

- Spectra are already processed or in a pre-filtered bag-of-fragments format; re-filtering would lose information.
- Input data is from a single, well-controlled instrument run with negligible background noise and high signal-to-noise ratio; aggressive filtering may discard low-abundance but genuine signal.
- The analysis goal is spectral similarity search or cosine scoring, where absolute peak intensities and all fragment information must be preserved; noise filtering alters intensity profiles.

## Inputs

- Raw MS/MS spectra in .mgf, .msp, or .mzML format
- Ion mode specification (positive or negative)
- Minimum intensity threshold parameter or statistical significance cutoff

## Outputs

- Cleaned and filtered MS/MS spectra with noise removed
- Peak intensity-normalized spectra per ion mode
- Filtered neutral loss values for fragment pairs

## How to apply

Load MS/MS spectra using MS2LDA.Preprocessing.load_and_clean, which filters spectra by ion mode (positive or negative). Extract fragment ion masses and normalize peak intensities within each spectrum. Calculate neutral loss values for all observed fragment pairs. Apply a minimum intensity threshold or statistical significance cutoff to remove fragments and losses below the cutoff—this eliminates spurious low-abundance peaks that would introduce noise into the bag-of-fragments representation. The thresholds should be calibrated to your instrument's sensitivity and the dataset's dynamic range; typical filtering removes fragments below ~5–10% relative intensity or those not meeting a signal-to-noise criterion. Document the cutoff values used so that results remain reproducible and comparable across batches.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Primary preprocessing module that loads spectra and applies ion mode filtering and initial noise removal) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA.Preprocessing.generate_corpus** (Converts filtered spectra into bag-of-fragments corpus representation with discrete mass binning) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Orchestrates the entire preprocessing and LDA workflow, including noise filtering and corpus generation) — https://github.com/vdhooftcompmet/MS2LDA

## Examples

```
from MS2LDA.Preprocessing import load_and_clean
spectra = load_and_clean(input_file='samples.mgf', ion_mode='positive', min_intensity_threshold=0.05)
```

## Evaluation signals

- Verify that fragments and neutral losses below the minimum intensity threshold are absent from the output corpus.
- Confirm that the number of peaks per spectrum is reduced after filtering, with low-abundance noise eliminated while high-abundance structural fragments are retained.
- Check that ion mode filtering correctly segregates positive and negative ionization mode spectra without cross-contamination.
- Validate that the filtered corpus generates stable, interpretable Mass2Motifs when passed to LDA (compare motif coherence and discovery rate pre- and post-filtering).
- Ensure that the filtered dataset does not exhibit an artificially low peak count per spectrum (e.g., <5 fragments after filtering), which indicates over-aggressive thresholding.

## Limitations

- Over-aggressive filtering (very high intensity thresholds) risks removing low-abundance but genuine fragmentation signals, particularly from minor substructures or weakly fragmented compounds; the optimal threshold is data and instrument-dependent.
- Ion mode filtering assumes clean metadata in input files; mixed ion mode spectra or incorrect ion mode annotation in the source file may not be detected and could bias results.
- Neutral loss calculation depends on accurate precursor mass and fragment mass calibration; poor mass accuracy can produce spurious or missing neutral losses even after intensity filtering.
- Filtering does not account for isobaric or near-isobaric fragments that may collapse when binned into discrete mass tokens; some structurally distinct fragments may be conflated in the final corpus.

## Evidence

- [other] Load MS/MS spectra from input file (.mgf, .msp, or .mzML) using the MS2LDA.Preprocessing.load_and_clean module: "Load MS/MS spectra from input file (.mgf, .msp, or .mzML) using the MS2LDA.Preprocessing.load_and_clean module"
- [other] Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff: "Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff"
- [methods] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
- [other] Extract fragment ion masses and normalize peak intensities within each spectrum: "Extract fragment ion masses and normalize peak intensities within each spectrum"
- [other] The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling: "The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling"
