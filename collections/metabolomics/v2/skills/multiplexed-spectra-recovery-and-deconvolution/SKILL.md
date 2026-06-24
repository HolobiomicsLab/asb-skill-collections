---
name: multiplexed-spectra-recovery-and-deconvolution
description: Use when you have raw IM-MS data in UIMF or Agilent MassHunter .d format
  acquired from a multiplexed (interleaved) ion mobility experiment, and you need
  to recover individual, demultiplexed frames to reconstruct conventional IM-MS spectra
  for downstream omics analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - PNNL PreProcessor
  - Agilent MassHunter
  - .NET Framework
  - Microsoft Visual C++ Runtime x64
  - IM-MS Browser
  - IMFE
  - .NET Framework 4.7.2
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.4c00220
  title: PNNL PreProcessor
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass
  spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass
  spectrometry data files (MS-files) from drift tube (DT) and structure for lossless
  ion manipulations (SLIM) IM-MS
- Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files)
- Agilent MassHunter (.d) and UIMF mass spectrometry data files
- .NET Framework 4.7.2 or later (included with Windows 10 update 1803 and later releases
- Microsoft Visual C++ Runtime x64 (may already be installed, if the program doesn't
  work then you can download vcredist_x64.exe
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pnnl_preprocessor_cq
    doi: 10.1021/jasms.4c00220
    title: PNNL PreProcessor
  dedup_kept_from: coll_pnnl_preprocessor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00220
  all_source_dois:
  - 10.1021/jasms.4c00220
  - 10.1021/acs.jproteome.1c00425
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multiplexed-spectra-recovery-and-deconvolution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Recover conventional IM-MS spectra from multiplexed acquisitions using demultiplexing and artifact removal algorithms with selectable pulse coverage parameters. This skill applies the PNNL PreProcessor's integrated demultiplexing strategy to decompose interleaved ion mobility frames and maximize sensitivity for low-level signals in drift tube and SLIM instruments.

## When to use

Apply this skill when you have raw IM-MS data in UIMF or Agilent MassHunter .d format acquired from a multiplexed (interleaved) ion mobility experiment, and you need to recover individual, demultiplexed frames to reconstruct conventional IM-MS spectra for downstream omics analysis. The skill is appropriate when raw data contains overlapping or convoluted mobility arrivals that require frame-level deconvolution.

## When NOT to use

- Input data is already a conventional (non-multiplexed) IM-MS acquisition; demultiplexing is unnecessary and may introduce artifacts.
- Ions have highly convoluted elution/mobility profiles caused by severe interferences; saturation repair and demultiplexing may produce incorrect results.
- Raw data is in formats other than UIMF or Agilent MassHunter .d; PNNL PreProcessor does not support those formats.

## Inputs

- raw IM-MS data file (UIMF format)
- raw IM-MS data file (Agilent MassHunter .d format)
- multiplexed frame data
- ion mobility dimension values
- mass-to-charge ratios (m/z)
- frame intensity arrays

## Outputs

- demultiplexed IM-MS spectra
- recovered conventional IM-MS frames
- deconvolved abundance profiles
- artifact-removed MS-file (original instrument format)
- spike-corrected ion mobility data
- multidimensionally smoothed spectra

## How to apply

Load the raw multiplexed IM-MS data file (UIMF or Agilent MassHunter .d format) into PNNL PreProcessor. Apply ion mobility dimension interpolation using the HRdm (high-resolution demultiplexing) strategy to improve deconvolution resolution. Execute the integrated PNNL demultiplexing and artifact removal algorithm, which employs a selectable pulse coverage percentage parameter to recover multiplexed frames and maximize sensitivity for low-level signals. Remove spike artifacts using the integrated spike-removal algorithm to reduce noise, then apply multidimensional smoothing to enhance real signals and reduce variations in abundance, elution, and mobility profiles. Export the processed data as a new MS-file in the original instrument data format. The rationale is that multiplexed acquisitions interleave ion pulses to improve duty cycle, but demultiplexing must account for pulse timing and frame boundaries; the selectable pulse coverage parameter allows users to trade recovery completeness against artifact suppression based on data quality.

## Related tools

- **PNNL PreProcessor** (Primary demultiplexing and artifact removal engine; executes HRdm deconvolution strategy, spike removal, multidimensional smoothing, and saturation repair) — https://github.com/PNNL-Comp-Mass-Spec/PNNL-PreProcessor
- **Agilent MassHunter** (Provides proprietary data access component library for reading and writing .d format IM-MS files) — https://www.agilent.com
- **IM-MS Browser** (Provides .m method files for polygon extraction and batch processing of region-of-interest definitions)
- **IMFE** (Converts demultiplexed IM/MS data to data-dependent acquisition (DDA) format with mobility-aligned fragmentation)
- **.NET Framework 4.7.2** (Runtime dependency for PNNL PreProcessor binary execution)
- **Microsoft Visual C++ Runtime x64** (Runtime dependency for PNNL PreProcessor binary execution)

## Evaluation signals

- Demultiplexed frames match the input pulse pattern and frame count; no artificial frame duplication or loss.
- Recovered IM-MS spectra exhibit smooth, resolved peaks in low-abundance ions without jagged artifacts; multidimensional smoothing has enhanced signal fidelity.
- Spike removal has reduced high-frequency noise spikes while preserving underlying abundance and mobility profiles.
- Export file is valid in the original instrument format (UIMF or .d) with correct metadata and frame structure; file can be re-imported into instrument software or other IM-MS tools without corruption.
- Pulse coverage percentage parameter adjustment correlates with trade-off between signal recovery (higher %) and artifact suppression (lower %); users can tune the parameter based on sample quality and downstream analysis goal.

## Limitations

- Saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences, leading to false intensity recovery.
- Multidimensional smoothing removes artifacts in jagged peaks common in low-abundance ions but may over-smooth weak signals and reduce peak resolution if not tuned appropriately.
- PNNL PreProcessor is closed-source and restricted to proprietary Agilent MassHunter data formats; vendor-specific dependencies limit portability and reproducibility.
- No changelog available in repository; version tracking and reproducibility information are absent, complicating audit and replication.

## Evidence

- [intro] demultiplexing and artifact removal algorithm definition: "The PNNL PreProcessor includes a demultiplexing and artifact removal algorithm with a selectable pulse coverage percentage parameter to recover conventional IM-MS spectra from multiplexed data."
- [methods] HRdm strategy and interpolation rationale: "Data interpolation of the ion mobility dimension to improve the results of the HRdm demultiplexing and peak deconvolution strategy"
- [methods] supported input formats and tools: "we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files"
- [methods] multidimensional smoothing effect on signal: "Smoothing removes artifacts in jagged peaks, which are common in low-abundance ions. Real signals are enhanced"
- [methods] saturation repair limitation with complex profiles: "the saturation repair software may produce incorrect results for ions with highly convoluted elution/mobility profiles caused by interferences"
- [readme] comprehensive skill scope in README: "data compression and interpolation, ion mobility demultiplexing, multidimensional smoothing, noise filtering by low intensity threshold and spike removal, saturation repair and metadata export"
