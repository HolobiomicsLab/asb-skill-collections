---
name: mass-spectral-component-extraction
description: Use when raw GC-MS data (netCDF or mzML format) contains overlapping chromatographic peaks with co-eluting ions that cannot be resolved by retention time alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - GNPS_GC
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectral-component-extraction

## Summary

Automated separation of co-eluting ion signals in GC-MS data using spectral deconvolution to resolve individual mass spectra from composite chromatographic peaks. This skill extracts resolved component features (retention time, m/z, intensity) into a tabular peak table for downstream analysis.

## When to use

Apply this skill when raw GC-MS data (netCDF or mzML format) contains overlapping chromatographic peaks with co-eluting ions that cannot be resolved by retention time alone. Use it as a preprocessing step before molecular networking, compound identification, or quantification when peak purity is critical and manual peak picking is impractical at scale.

## When NOT to use

- Input is already a quality-controlled feature table with resolved peaks
- GC-MS data contains no co-eluting peaks (manual peak picking is more interpretable)
- Retention time separation is sufficient and peak purity is not a downstream requirement

## Inputs

- raw GC-MS data in netCDF format
- raw GC-MS data in mzML format
- overlapping chromatographic peak regions

## Outputs

- deconvolved peak table (tabular format, one row per component)
- individual mass spectra for each resolved component
- feature matrix with retention time, m/z, and intensity columns

## How to apply

Load raw GC-MS data in netCDF or mzML format and apply a spectral deconvolution algorithm to separate mass spectra of co-eluting components. The algorithm resolves individual ion signals from composite peaks by identifying spectral coherence patterns across the elution window. Extract deconvolved features including retention time, m/z values, and intensity for each separated component. Generate an output peak table with one row per deconvolved component, ensuring columns include intensity, m/z, and retention time. Validate deconvolution quality by confirming the peak count increases relative to the input and verifying that separated components exhibit coherent mass spectra characteristic of distinct molecules rather than noise or artifacts.

## Related tools

- **GNPS_GC** (spectral deconvolution and component extraction pipeline for GC-MS data) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Peak count in deconvolved output exceeds peak count in raw data, indicating successful separation of co-eluting components
- Deconvolved mass spectra exhibit spectral coherence (consistent m/z patterns) when plotted across the elution window
- Output peak table schema validation: all rows contain valid retention time (numeric), m/z (numeric > 0), and intensity (numeric ≥ 0) values
- Manual expert review confirms that separated components correspond to distinct molecular species rather than noise or redundant fragments
- No NaN or missing values in intensity, m/z, or retention time columns for resolved peaks

## Limitations

- Deconvolution quality depends on spectral coherence and may fail or produce artifacts when co-eluting components have highly similar mass spectra or fragmentation patterns
- Performance on severely overlapping peaks with marginal signal-to-noise ratio is not characterized in the manuscript
- No changelog or version history available for the GNPS_GC implementation, limiting reproducibility across releases

## Evidence

- [other] Load raw GC-MS data in netCDF or mzML format containing overlapping chromatographic peaks: "Load raw GC-MS data (netCDF or mzML format) containing overlapping chromatographic peaks."
- [other] Apply spectral deconvolution algorithm to separate co-eluting ions and resolve individual mass spectra: "Apply spectral deconvolution algorithm to separate co-eluting ions and resolve individual mass spectra from composite signals."
- [other] Extract deconvolved peak features including retention time, m/z, and intensity for each resolved component: "Extract deconvolved peak features including retention time, m/z values, and intensity for each resolved component."
- [other] Generate output peak table with one row per deconvolved component in tabular format: "Generate output peak table in tabular format with one row per deconvolved component, including intensity, m/z, and retention time columns."
- [other] Validate deconvolution by confirming peak count increase and verifying spectral coherence: "Validate deconvolution quality by confirming peak count increase and verifying spectral coherence of separated components."
- [intro] Auto-deconvolution as a processing method for gas chromatography–mass spectrometry data: "Development of methods for auto-deconvolution of gas chromatography–mass spectrometry data"
- [readme] GNPS_GC is the companion repository implementing auto-deconvolution: "This is a companion repository to the following manuscript: Aksenov, A.A., Laponogov, I., Zhang, Z. _et al_. Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data."
