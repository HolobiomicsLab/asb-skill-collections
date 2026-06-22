---
name: coeluting-compound-resolution
description: Use when analyzing complex GC-MS mixtures where two or more chemical compounds elute at similar or identical retention times, producing overlapping or merged peaks in the raw chromatogram.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MSHub
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans:
- MSHub auto-deconvolution
- Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub
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

# coeluting-compound-resolution

## Summary

Automated separation and identification of overlapping chemical components in gas chromatography–mass spectrometry (GC-MS) data using deconvolution algorithms. This skill resolves co-eluting compounds that appear as merged peaks in raw chromatograms, extracting individual component mass spectra for downstream analysis.

## When to use

Apply this skill when analyzing complex GC-MS mixtures where two or more chemical compounds elute at similar or identical retention times, producing overlapping or merged peaks in the raw chromatogram. Indicators include: (1) abnormal peak shapes (shoulders, asymmetry, or broadening) that suggest multiple components; (2) mass spectra containing unexpected m/z fragments inconsistent with a single known compound; (3) requirement to identify individual analytes from untargeted or metabolomics samples where peak overlap is expected.

## When NOT to use

- Input data is already processed into individual, well-resolved peaks with no evidence of co-elution.
- Analysis focuses on targeted quantitation of a single known compound; deconvolution adds computational overhead without benefit.
- GC-MS instrument produces baseline-resolved chromatography where peak overlap is negligible or absent.

## Inputs

- Raw GC-MS data files (netCDF format, vendor formats)
- Complex chromatographic peaks with co-eluting components

## Outputs

- Deconvolved individual component mass spectra
- Standardized spectral output (MGF or mzML format)
- Peak intensity and retention time profiles per component

## How to apply

Load raw GC-MS data files in vendor-native or netCDF format. Apply the MSHub auto-deconvolution algorithm, which uses spectral pattern recognition to decompose overlapping peaks into constituent spectra by resolving individual component mass-to-charge ratios and retention time profiles. The algorithm extracts deconvolved spectra that correspond to single chemical entities. Export the resolved spectra to standardized formats (MGF or mzML) that preserve MS fragmentation patterns for subsequent compound identification via molecular networking or spectral library matching. Success is indicated when each deconvolved spectrum shows coherent fragmentation patterns consistent with a single molecular structure, and the sum of deconvolved intensities approximates the original peak intensity.

## Related tools

- **MSHub** (Implements auto-deconvolution algorithm to resolve overlapping peaks and extract individual component spectra from raw GC-MS data) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Each deconvolved spectrum exhibits a single coherent fragmentation pattern with a dominant molecular ion or characteristic base peak, not multiple competing fragmentation signatures.
- Summed intensities of all deconvolved spectra at a given retention time approximate the total intensity of the original co-eluting peak (mass balance check).
- Deconvolved spectra can be matched to known or putative chemical structures via molecular networking or spectral library comparison with cosine similarity scores above expected thresholds.
- Retention time separation between deconvolved components is consistent with the chemical properties and instrument resolution of the GC-MS method.
- Output files conform to MGF or mzML schema with correctly populated m/z, intensity, and metadata fields for each deconvolved spectrum.

## Limitations

- Deconvolution accuracy depends on the degree of peak overlap and the spectral distinctiveness of co-eluting compounds; highly similar or identical fragmentation patterns may not resolve cleanly.
- Algorithm performance is contingent on proper instrument tuning and data quality; noisy or poorly calibrated mass spectra reduce deconvolution fidelity.
- The method is designed for GC-MS and may not be applicable to other chromatography-MS platforms (LC-MS, SFC-MS) without algorithmic adaptation.

## Evidence

- [other] How does the auto-deconvolution method process raw gas chromatography–mass spectrometry data to separate and identify individual chemical components from complex mixtures?: "How does the auto-deconvolution method process raw gas chromatography–mass spectrometry data to separate and identify individual chemical components from complex mixtures?"
- [other] Apply MSHub auto-deconvolution algorithm to resolve overlapping peaks and extract individual component spectra.: "Apply MSHub auto-deconvolution algorithm to resolve overlapping peaks and extract individual component spectra."
- [intro] Auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis: "Auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis"
- [other] Export deconvolved spectra to a standardized output format (MGF or mzML) suitable for downstream molecular networking analysis.: "Export deconvolved spectra to a standardized output format (MGF or mzML) suitable for downstream molecular networking analysis."
