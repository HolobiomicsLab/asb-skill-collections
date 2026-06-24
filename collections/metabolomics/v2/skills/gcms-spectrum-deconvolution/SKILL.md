---
name: gcms-spectrum-deconvolution
description: Use when input GC-MS data (netCDF or mzML format) exhibits overlapping
  chromatographic peaks where multiple analytes co-elute at the same retention time,
  resulting in composite mass spectra that conflate signals from distinct molecular
  species.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - GNPS_GC
  techniques:
  - GC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub_cq
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-020-0700-3
  all_source_dois:
  - 10.1038/s41587-020-0700-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# GC-MS Spectrum Deconvolution

## Summary

Resolves overlapping co-eluting component signals in gas chromatography–mass spectrometry data by applying spectral deconvolution algorithms to separate composite mass spectra into individual, coherent component spectra. Use this skill when raw GC-MS chromatograms contain unresolved peaks that obscure the true number and identity of analytes.

## When to use

Input GC-MS data (netCDF or mzML format) exhibits overlapping chromatographic peaks where multiple analytes co-elute at the same retention time, resulting in composite mass spectra that conflate signals from distinct molecular species. The goal is to recover the individual mass spectra and peak features for each co-eluting component to enable downstream molecular identification and networking.

## When NOT to use

- Input chromatogram is already baseline-resolved with no co-eluting peaks
- Raw data is in a format other than netCDF or mzML (e.g., proprietary vendor formats without conversion)
- Analysis goal is limited to untargeted feature detection from well-resolved chromatography; standard peak picking is sufficient

## Inputs

- Raw GC-MS data in netCDF or mzML format
- Composite mass spectra with co-eluting ion signals

## Outputs

- Deconvolved peak table (tabular format, one row per component)
- Individual mass spectra for each resolved component
- Peak features including retention time, m/z values, and intensity per component

## How to apply

Load raw GC-MS data in netCDF or mzML format containing regions of co-eluting ions. Apply a spectral deconvolution algorithm to the composite signals to separate and resolve individual mass spectra for each co-eluting component. Extract deconvolved peak features—retention time, m/z values, and intensity—for each resolved component. Output results as a peak table with one row per deconvolved component. Validate deconvolution quality by confirming that the peak count increases relative to the input and by verifying that separated component spectra are internally coherent (consistent m/z spacing and intensity relationships). Reject poorly deconvolved regions where spectral coherence is compromised or where peaks cannot be reliably separated.

## Related tools

- **GNPS_GC** (Companion repository implementing auto-deconvolution algorithm for GC-MS data processing within the MSHub pipeline) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Peak count in deconvolved output table is greater than the number of distinct chromatographic regions in the raw data
- Each resolved component mass spectrum exhibits internal spectral coherence: consistent m/z-to-intensity ratios across the retention time window and no spurious low-intensity fragments
- Retention times of deconvolved components fall within the same or adjacent chromatographic regions, confirming co-elution separation rather than artificial fragmentation
- Total ion current (TIC) reconstructed from deconvolved peaks closely matches the input composite TIC, indicating mass balance and absence of information loss
- Manual expert review confirms that deconvolved component spectra are chemically plausible (e.g., match known fragmentation patterns or library spectra)

## Limitations

- Deconvolution quality depends on spectral overlap degree: heavily overlapping signals with similar fragmentation patterns may not resolve completely
- Algorithm assumes that co-eluting components have distinguishable mass spectra; components with nearly identical fragmentation are difficult to separate
- No changelog or versioning information provided in repository documentation; reproducibility across versions uncertain
- Validation relies partly on manual expert review, making automated quality gates difficult to standardize

## Evidence

- [other] Load raw GC-MS data (netCDF or mzML format) containing overlapping chromatographic peaks. Apply spectral deconvolution algorithm to separate co-eluting ions and resolve individual mass spectra from composite signals.: "Load raw GC-MS data (netCDF or mzML format) containing overlapping chromatographic peaks. 2. Apply spectral deconvolution algorithm to separate co-eluting ions and resolve individual mass spectra"
- [other] Extract deconvolved peak features including retention time, m/z values, and intensity for each resolved component. 4. Generate output peak table in tabular format with one row per deconvolved component, including intensity, m/z, and retention time columns.: "Extract deconvolved peak features including retention time, m/z values, and intensity for each resolved component. 4. Generate output peak table in tabular format with one row per deconvolved"
- [other] Validate deconvolution quality by confirming peak count increase and verifying spectral coherence of separated components.: "Validate deconvolution quality by confirming peak count increase and verifying spectral coherence of separated components."
- [intro] Development of methods for auto-deconvolution of gas chromatography–mass spectrometry data: "Development of methods for auto-deconvolution of gas chromatography–mass spectrometry data"
- [readme] Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data. Nature Biotechnology (2020): "Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data. _Nature Biotechnology_ (2020)"
