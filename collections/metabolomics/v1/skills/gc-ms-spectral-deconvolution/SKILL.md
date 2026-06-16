---
name: gc-ms-spectral-deconvolution
description: Use when you have raw GC-MS data (in netCDF or vendor format) containing overlapping chromatographic peaks from complex mixtures where individual compound spectra cannot be resolved by simple peak picking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MSHub
  - GNPS
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans:
- MSHub auto-deconvolution
- Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data
- GNPS molecular networking
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub
schema_version: 0.2.0
---

# GC-MS Spectral Deconvolution

## Summary

Automated separation and extraction of individual component mass spectra from overlapping gas chromatography–mass spectrometry peaks using the MSHub auto-deconvolution algorithm. This skill resolves mixed spectra in complex chemical mixtures to enable accurate compound identification and downstream molecular networking analysis.

## When to use

Apply this skill when you have raw GC-MS data (in netCDF or vendor format) containing overlapping chromatographic peaks from complex mixtures where individual compound spectra cannot be resolved by simple peak picking. Use it when your analysis goal requires extracting pure, deconvolved spectra suitable for molecular networking, spectral library matching, or detailed chemical identification.

## When NOT to use

- Input data is already high-resolution liquid chromatography–mass spectrometry (LC-MS) with baseline-resolved peaks; deconvolution is unnecessary.
- Your workflow requires chromatographic retention indices or quantitative peak area values; deconvolution outputs focus on spectral composition, not chromatographic features.
- Analysis goal is purely quantitative (e.g., measuring total metabolite concentration); spectral deconvolution adds computational overhead without benefit for abundance-only questions.

## Inputs

- raw GC-MS data files (netCDF format)
- raw GC-MS data files (vendor-specific format)
- gas chromatography–mass spectrometry dataset with overlapping peaks

## Outputs

- deconvolved mass spectra (MGF format)
- deconvolved mass spectra (mzML format)
- individual component spectra extracted from overlapping chromatographic peaks

## How to apply

Load raw GC-MS files in netCDF or vendor format into MSHub. Apply the MSHub auto-deconvolution algorithm, which processes overlapping peaks to extract and resolve individual component spectra. The algorithm decomposes mixed mass spectra across retention time windows to separate co-eluting compounds. Export the resulting deconvolved spectra to a standardized format (MGF or mzML) compatible with downstream analysis. Validate deconvolution quality by confirming that output spectra have been properly separated and that fragment ion patterns match expected chemical structures for identified compounds.

## Related tools

- **MSHub** (Performs automated deconvolution of overlapping GC-MS peaks to extract individual component spectra from complex mixtures)
- **GNPS** (Accepts deconvolved spectra (in MGF or mzTab format) for downstream molecular networking and spectral clustering by cosine similarity) — https://github.com/bittremieux/GNPS_GC

## Evaluation signals

- Output spectra file validates against MGF or mzML schema with required metadata fields (precursor m/z, retention time, spectrum intensity array).
- Deconvolved spectra show distinct, non-overlapping fragment ion patterns compared to the input raw data; each output spectrum represents a single, coherent chemical component.
- Number of extracted spectra exceeds number of raw chromatographic peaks, indicating successful separation of co-eluting compounds.
- Deconvolved spectra successfully upload to GNPS and produce a molecular network with expected topology; nodes cluster by chemical similarity as judged by cosine similarity scoring (typically > 0.7 for related compounds).
- Mass accuracy of extracted fragment ions is consistent with expected elemental compositions; no spurious peaks from incomplete deconvolution remain.

## Limitations

- Deconvolution quality depends on the complexity and degree of peak overlap; highly co-eluting compounds or those with very similar fragmentation patterns may not be fully resolved.
- Algorithm assumes mass spectra of individual components follow predictable ionization and fragmentation patterns; unusual or unexpected spectra may be poorly deconvolved.
- Output spectra are suitable for spectral networking and compound identification but do not retain chromatographic quantitative information (e.g., peak area, integration boundaries).
- Computational cost scales with data volume and peak complexity; very large or highly congested GC-MS datasets may require parameter optimization or extended processing time.

## Evidence

- [other] How does the auto-deconvolution method process raw gas chromatography–mass spectrometry data to separate and identify individual chemical components from complex mixtures?: "auto-deconvolution method process raw gas chromatography–mass spectrometry data to separate and identify individual chemical components from complex mixtures"
- [other] The manuscript describes auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis, with implementation available in the companion repository (bittremieux/GNPS_GC).: "auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis"
- [other] Load raw GC-MS files (netCDF or vendor format) from the companion repository or deposited dataset. Apply MSHub auto-deconvolution algorithm to resolve overlapping peaks and extract individual component spectra. Export deconvolved spectra to a standardized output format (MGF or mzML) suitable for downstream molecular networking analysis.: "Load raw GC-MS files (netCDF or vendor format) ... Apply MSHub auto-deconvolution algorithm to resolve overlapping peaks and extract individual component spectra. Export deconvolved spectra to a"
- [other] Obtain the GC-MS raw data from the deposited companion dataset (GNPS or MassIVE repository). Apply MSHub auto-deconvolution algorithm to extract individual compound spectra from overlapping chromatographic peaks.: "Apply MSHub auto-deconvolution algorithm to extract individual compound spectra from overlapping chromatographic peaks"
- [intro] Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data: "Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data"
