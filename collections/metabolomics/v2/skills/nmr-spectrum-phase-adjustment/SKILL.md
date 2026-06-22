---
name: nmr-spectrum-phase-adjustment
description: Use when you have acquired raw 1D NMR spectra (FID or processed spectra in NMRPipe format) that exhibit phase distortion—where peaks are not in pure absorption mode—and you need to prepare the spectrum for automatic deconvolution into peak tables.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - SAND
  - NMRPipe
  - NMRBox
derived_from:
- doi: 10.1021/acs.analchem.3c03078
  title: SAND
evidence_spans:
- Any user is welcome to make new modificaitons on the SAND code, particularly its version for NMRBox
- interface to NMRPipe (pipe_scripts/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_sand_cq
    doi: 10.1021/acs.analchem.3c03078
    title: SAND
  dedup_kept_from: coll_sand_cq
schema_version: 0.2.0
---

# nmr-spectrum-phase-adjustment

## Summary

Phase correction is a critical preprocessing step in 1D NMR spectral processing that aligns peak phases to absorption-mode lineshapes, enabling accurate downstream deconvolution. SAND integrates NMRPipe utilities to automatically apply phase correction as part of its spectral processing pipeline before peak decomposition.

## When to use

Apply this skill when you have acquired raw 1D NMR spectra (FID or processed spectra in NMRPipe format) that exhibit phase distortion—where peaks are not in pure absorption mode—and you need to prepare the spectrum for automatic deconvolution into peak tables. Phase adjustment is necessary before deconvolution because distorted phases prevent accurate peak parameter extraction (chemical shift, intensity, linewidth).

## When NOT to use

- Spectrum has already been phase-corrected by the spectrometer or prior processing step
- Input is already a deconvoluted peak table (phase adjustment applies only to raw spectra)
- Analysis requires retention of phase distortion for specialized phase-sensitive experiments (e.g., certain edited sequences)

## Inputs

- 1D NMR spectrum file (FID or processed spectrum format compatible with NMRPipe)
- NMRBox SAND_V7 processing environment configuration

## Outputs

- Phase-corrected 1D NMR spectrum (ready for deconvolution)
- Processed spectrum with corrected absorption-mode peak phases

## How to apply

Within the SAND pipeline accessed via NMRBox (SAND_V7), phase correction is applied automatically following baseline correction as part of the spectral processing stage. The NMRPipe utilities integrated via pipe_scripts/ handle the phase adjustment; the user loads the raw 1D NMR spectrum file (FID or processed spectrum) into the SAND processing pipeline through the NMRBox interface, and the automatic spectral processing module applies both baseline and phase correction in sequence. The corrected spectrum is then passed to the SAND deconvolution algorithm. Success is verified by inspecting the output peak table for absorption-mode peak shapes and validating peak parameters (chemical shift, intensity, linewidth) against expected values for known reference standards.

## Related tools

- **NMRPipe** (Provides phase correction utilities integrated into SAND via pipe_scripts/ for automatic phase adjustment of 1D NMR spectra)
- **SAND** (Orchestrates the complete spectral processing workflow including phase correction before deconvolution) — https://github.com/edisonomics/SAND
- **NMRBox** (Provides the SAND_V7 interface and execution environment for phase correction and downstream processing) — https://nmrbox.org

## Evaluation signals

- Output peak table row count matches expected number of peaks in the spectrum
- Extracted peak intensity values are positive and consistent with reference standards
- Chemical shift values fall within expected ranges (0–10 ppm for typical 1D ¹H NMR)
- Linewidth parameters are uniform and reasonable for the spectrometer field strength and pulse sequence used
- Visual inspection of the corrected spectrum shows peaks in absorption mode (not dispersive or mixed phase)

## Limitations

- SAND has been tested primarily on urine and worm datasets; applicability to other biological matrices or NMR data types is under development
- No changelog is available to track phase correction algorithm updates or parameter changes across SAND versions
- Automatic phase correction may fail on highly overlapping or complex multiplet regions; manual phase adjustment may be required in such cases

## Evidence

- [other] Apply automatic spectral processing including baseline correction and phase correction using NMRPipe utilities integrated via pipe_scripts/: "Apply automatic spectral processing including baseline correction and phase correction using NMRPipe utilities integrated via pipe_scripts/"
- [readme] SAND automatic process and deconvolute 1D NMR spectra into peak tables: "SAND automatic process and deconvolute 1D NMR spectra into peak tables."
- [methods] latest interface to NMRBox (SAND_V7), and interface to NMRPipe: "latest interface to NMRBox (SAND_V7), and interface to NMRPipe"
- [other] Load the 1D NMR spectrum file (FID or processed spectrum format) into the SAND processing pipeline via NMRBox interface (SAND_V7): "Load the 1D NMR spectrum file (FID or processed spectrum format) into the SAND processing pipeline via NMRBox interface (SAND_V7)."
