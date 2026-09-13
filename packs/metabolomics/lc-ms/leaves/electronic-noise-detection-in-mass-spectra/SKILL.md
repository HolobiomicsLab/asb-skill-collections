---
name: electronic-noise-detection-in-mass-spectra
description: Use when you have raw MS/MS peak lists and suspect electronic noise contamination—particularly
  when peaks show repeated, identical intensity values across multiple m/z entries
  within a single spectrum, which are rare in genuine biological spectra but common
  in instrument artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - spectral_denoising
  - numpy
  - ms_entropy
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-025-02646-x
  title: Spectral Denoising
- doi: 10.1038/s41592-023-02012-9
  title: ''
evidence_spans:
- Spectral denoising requires ``Python >= 3.8`` installed on your system
- import spectral_denoising as sd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectral_denoising_cq
    doi: 10.1038/s41592-025-02646-x
    title: Spectral Denoising
  dedup_kept_from: coll_spectral_denoising_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02646-x
  all_source_dois:
  - 10.1038/s41592-025-02646-x
  - 10.1038/s41592-023-02012-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# electronic-noise-detection-in-mass-spectra

## Summary

Identify and flag electronic noise ions in MS/MS peak lists by detecting ions with identical intensities that occur with statistically anomalous frequency. This enables removal of spurious signals before spectral matching or compound identification.

## When to use

Apply this skill when you have raw MS/MS peak lists and suspect electronic noise contamination—particularly when peaks show repeated, identical intensity values across multiple m/z entries within a single spectrum, which are rare in genuine biological spectra but common in instrument artifacts.

## When NOT to use

- Input spectrum is already known to be free of electronic noise or has been pre-screened by instrument vendor software
- Intensity quantization or binning is expected (e.g., integer-only detector output where identical intensities are expected by design)
- Analysis requires retention of all peaks for comparative or archival purposes without modification

## Inputs

- Peak list as 2D numpy array (n, 2) with m/z and intensity columns
- MS/MS spectrum in any format convertible to peak array (e.g., from MSP file)

## Outputs

- Denoised peak list as 2D numpy array with same shape as input
- Boolean or integer flags marking peaks identified as electronic noise (optional)

## How to apply

Load the peak list as a 2D numpy array with shape [n, 2] containing m/z and intensity columns. Count the frequency of each unique intensity value across all peaks in the spectrum. Identify intensity values that occur more than 4 times—an empirically validated threshold derived from analysis of the NIST23 database, where such occurrences are <0.05% in genuine spectra. Flag or remove peaks whose intensity values exceed this frequency threshold. Return the filtered peak list with the same array structure as input. The threshold of 4 is the key decision point: intensities appearing 5+ times signal electronic noise rather than biological variation.

## Related tools

- **spectral_denoising** (Python package exposing electronic_denoising() function to detect and remove electronic noise ions from peak lists) — https://github.com/FanzhouKong/spectral_denoising
- **numpy** (Array creation, frequency counting, and logical indexing operations for intensity histograms and peak filtering)
- **ms_entropy** (Spectral entropy computation for evaluating denoising quality before/after electronic noise removal)

## Examples

```
import spectral_denoising as sd; import numpy as np; peak = np.array([[48.99, 154.0], [63.01, 265.0], [63.99, 663.0], [65.99, 596.0], [79.02, 521.0], [81.02, 659.0]], dtype=np.float32); peak_denoised = sd.electronic_denoising(peak)
```

## Evaluation signals

- Verify that peaks with intensity values occurring ≤4 times are retained; peaks with intensity values occurring >4 times are removed
- Check that output array has same column structure as input [m/z, intensity] and ≤n rows (never increases)
- Confirm that removed peaks cluster in narrow intensity bands (e.g., 596, 663, 659 in the example would suggest noise if all occurred >4 times)
- Calculate spectral entropy before and after: genuine denoising should not drastically reduce entropy; extreme entropy drop suggests over-filtering
- Compare against NIST23 reference spectra: noise-flagged intensity frequencies should remain <0.05% in the reference set

## Limitations

- Threshold of 4 occurrences is empirically derived from NIST23 database and may not generalize to other instruments, MS/MS protocols, or mass analyzers without revalidation
- Method assumes electronic noise manifests as repeated exact intensity values; chemical noise (e.g., rearrangement ions, water loss) with varied intensities will not be detected
- Spectrum must contain sufficient peak diversity (many unique m/z values) for frequency counting to be reliable; very simple spectra with few peaks may yield false positives
- Does not distinguish between benign repeated intensities (rare but possible in genuine spectra) and instrument artifacts; manual review may be needed for borderline cases

## Evidence

- [other] The electronic_denoising function removes obvious electronic noise ions in MS/MS spectra, which are characterized by ions with identical intensities within a single peak list.: "The electronic_denoising function removes obvious electronic noise ions in MS/MS spectra, which are characterized by ions with identical intensities within a single peak list."
- [other] Identify intensity values that occur more than 4 times (a threshold empirically validated on NIST23 database where such occurrences are <0.05% in genuine spectra).: "Identify intensity values that occur more than 4 times (a threshold empirically validated on NIST23 database where such occurrences are <0.05% in genuine spectra)."
- [intro] Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises.: "Noise ions in MS/MS spectra are largely categorized as 1. electronic noises and 2. chemical noises."
- [other] Load a peak list as a 2D numpy array with shape [n, 2] containing m/z and intensity columns. Count the frequency of each unique intensity value across all peaks.: "Load a peak list as a 2D numpy array with shape [n, 2] containing m/z and intensity columns. Count the frequency of each unique intensity value across all peaks."
- [other] Filter the peak list to retain only peaks whose intensity values do not exceed this threshold. Return the denoised spectrum as a numpy array with the same shape as input.: "Filter the peak list to retain only peaks whose intensity values do not exceed this threshold. Return the denoised spectrum as a numpy array with the same shape as input."
