---
name: coeluting-ion-separation
description: Use when raw GC-MS data (netCDF or mzML format) exhibits overlapping chromatographic peaks—i.e., when multiple analytes elute at similar retention times and produce composite mass spectra with ambiguous m/z signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0673
  - http://edamontology.org/topic_3520
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

# coeluting-ion-separation

## Summary

Spectral deconvolution method that separates co-eluting ions in gas chromatography–mass spectrometry (GC-MS) data to resolve individual mass spectra from overlapping chromatographic peaks. This skill transforms composite signals into distinct component-level features suitable for molecular identification and networking.

## When to use

Apply this skill when raw GC-MS data (netCDF or mzML format) exhibits overlapping chromatographic peaks—i.e., when multiple analytes elute at similar retention times and produce composite mass spectra with ambiguous m/z signals. Use it as a preprocessing step before molecular networking, feature extraction, or metabolite annotation to increase peak count and spectral coherence.

## When NOT to use

- Input is already a feature table or pre-deconvolved peak list
- GC-MS data contains no overlapping peaks (baseline-resolved chromatography)
- Instrument produces high-resolution separations where co-elution is not a concern

## Inputs

- Raw GC-MS data in netCDF format
- Raw GC-MS data in mzML format
- Mass spectrometry data with overlapping chromatographic peaks

## Outputs

- Deconvolved peak table (tabular format, one row per component)
- Peak features (retention time, m/z values, intensity per component)
- Individual resolved mass spectra for each co-eluting component

## How to apply

Load raw GC-MS data in netCDF or mzML format containing overlapping peaks. Apply a spectral deconvolution algorithm that separates co-eluting ions by resolving individual mass spectra from composite signals. Extract deconvolved peak features (retention time, m/z values, intensity) for each resolved component and generate a peak table with one row per deconvolved component. Validate deconvolution quality by confirming an increase in peak count and verifying spectral coherence of separated components—components should have internally consistent m/z patterns consistent with single analytes.

## Related tools

- **GNPS_GC** (Implements auto-deconvolution algorithm and spectral separation workflow for GC-MS data) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Peak count increases after deconvolution compared to raw input (indicates successful component separation)
- Deconvolved peak table schema includes retention time, m/z, and intensity columns with valid numeric values
- Separated mass spectra exhibit internal coherence (m/z ratios consistent with single chemical compounds)
- Retention time ranges of separated components do not exceed instrument resolution limits
- Visual inspection confirms that previously overlapping signals are now resolved into distinct spectral patterns

## Limitations

- Deconvolution quality depends on peak overlap severity; heavily overlapped signals may not fully resolve
- Method assumes input data is in valid netCDF or mzML format; malformed files will fail
- No documented changelog or versioning in the repository limits reproducibility tracking across releases
- Spectral coherence validation requires manual expert review for complex or noisy data

## Evidence

- [other] Load raw GC-MS data (netCDF or mzML format) containing overlapping chromatographic peaks.: "Load raw GC-MS data (netCDF or mzML format) containing overlapping chromatographic peaks."
- [other] Apply spectral deconvolution algorithm to separate co-eluting ions and resolve individual mass spectra from composite signals.: "Apply spectral deconvolution algorithm to separate co-eluting ions and resolve individual mass spectra from composite signals."
- [other] Extract deconvolved peak features including retention time, m/z values, and intensity for each resolved component.: "Extract deconvolved peak features including retention time, m/z values, and intensity for each resolved component."
- [other] Generate output peak table in tabular format with one row per deconvolved component, including intensity, m/z, and retention time columns.: "Generate output peak table in tabular format with one row per deconvolved component, including intensity, m/z, and retention time columns."
- [other] Validate deconvolution quality by confirming peak count increase and verifying spectral coherence of separated components.: "Validate deconvolution quality by confirming peak count increase and verifying spectral coherence of separated components."
- [other] Auto-deconvolution as a processing method for gas chromatography–mass spectrometry data, implemented in the GNPS_GC companion repository.: "auto-deconvolution as a processing method for gas chromatography–mass spectrometry data, implemented in the GNPS_GC companion repository."
