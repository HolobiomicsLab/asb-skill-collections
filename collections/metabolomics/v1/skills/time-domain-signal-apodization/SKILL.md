---
name: time-domain-signal-apodization
description: Use when working with raw FT-ICR transient data (e.g., ESI_NEG_SRFA.d format) prior to noise thresholding and mass-domain calibration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
schema_version: 0.2.0
---

# time-domain-signal-apodization

## Summary

Apply Hanning windowing to time-domain FT-ICR transients with zero-filling to reduce spectral artifacts and improve peak definition before Fourier transformation and mass calibration. This preprocessing step is essential for reducing spectral leakage and enhancing the signal-to-noise ratio of subsequent mass-domain analysis.

## When to use

Apply this skill when working with raw FT-ICR transient data (e.g., ESI_NEG_SRFA.d format) prior to noise thresholding and mass-domain calibration. Use it specifically when the raw time-domain spectrum exhibits edge discontinuities that would introduce spectral ringing artifacts during Fourier transformation, or when peak resolution and mass accuracy are critical for downstream molecular formula assignment.

## When NOT to use

- Input data is already in the frequency/m/z domain (magnitude or centroid spectrum); apodization applies only to raw time-domain transients before FFT.
- Data has already been processed through FFT and peak picking; apodization cannot be retroactively applied to centroided or extracted mass lists.
- Low-resolution or binned time-domain data where edge discontinuities are already minimal and further smoothing would reduce signal fidelity.

## Inputs

- FT-ICR raw transient time-domain spectrum (e.g., ESI_NEG_SRFA.d)
- Time-domain intensity array (complex or real-valued)
- Transient duration / number of data points

## Outputs

- Apodized time-domain spectrum (zero-filled)
- Zero-filled time-domain array ready for Fourier transformation

## How to apply

Load the FT-ICR raw time-domain transient using CoreMS's data factory interface. Apply Hanning apodization (a cosine-squared windowing function) to the entire time-domain spectrum, then apply one zero-fill (doubling the spectral resolution by padding the signal with zeros before FFT). The Hanning window smoothly tapers the signal to zero at the boundaries, eliminating discontinuities that would otherwise cause spectral leakage. Zero-filling increases the density of frequency-domain samples without adding information, improving the fidelity of subsequent peak picking and calibration. Execute the apodization step before any other signal processing (noise thresholding, peak picking, or mass calibration) to ensure clean input for downstream steps.

## Related tools

- **CoreMS** (Provides data factory and apodization implementation for loading and windowing FT-ICR transients; handles Hanning apodization and zero-filling prior to FFT) — https://github.com/EMSL-Computing/CoreMS
- **numpy** (Underlying numerical array operations for apodization window generation and signal multiplication)

## Evaluation signals

- Verify that the apodized spectrum exhibits smooth taper to near-zero at both time-domain boundaries (inspect first and last ~5% of samples).
- Confirm that zero-filling doubled the total number of time-domain data points (original length N → 2N after one zero-fill).
- Check that the Fourier-transformed magnitude spectrum shows reduced spectral leakage (fewer ghosts or sidebands around major peaks) compared to an unapodized FFT of the same transient.
- Validate that downstream mass calibration (MzDomainCalibration against reference data) achieves expected mass error metrics (e.g., sub-ppm accuracy for SRFA reference peaks).
- Confirm that molecular formula assignment success rate and mass error distribution improve or remain consistent after apodization versus raw processing.

## Limitations

- Hanning apodization reduces amplitude of peaks near the edges of the time-domain window; very weak ions present only at the extremes of the transient may be suppressed.
- Zero-filling improves frequency resolution but does not add information; it cannot recover weak peaks buried below the noise floor in the raw transient.
- The skill is specific to FT-ICR transient processing; it does not apply to data already in centroid or profile mode from other MS types (e.g., TOF, Orbitrap).
- No changelog found for CoreMS version history, limiting traceability of apodization parameter changes or bug fixes across releases.

## Evidence

- [other] Apply Hanning apodization with one zero-fill to the time-domain spectrum.: "Apply Hanning apodization with one zero-fill to the time-domain spectrum."
- [readme] Apodization, Zerofilling, and Magnitude mode FT: "Apodization, Zerofilling, and Magnitude mode FT"
- [other] Load ESI_NEG_SRFA.d FT-ICR raw data and SRFA.ref calibration reference using CoreMS data factory.: "Load ESI_NEG_SRFA.d FT-ICR raw data and SRFA.ref calibration reference using CoreMS data factory."
- [other] The pipeline executes complete molecular formula assignment by applying Hanning apodization with zero-fill, noise thresholding, MzDomainCalibration against SRFA.ref reference data, and SearchMolecularFormulas: "The pipeline executes complete molecular formula assignment by applying Hanning apodization with zero-fill, noise thresholding, MzDomainCalibration"
